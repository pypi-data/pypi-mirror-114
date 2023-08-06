/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { ChangePasswordPopup } from './ChangePasswordPopup';
import { CheckoutForm } from './CheckoutForm';
import { Header, Switch, TextBox, TextBoxDropdown } from '../../core';
import FormatUtils from '../../utils/FormatUtils';
import { Button, Divider, IconButton } from '@material-ui/core';
import GetAppIcon from '@material-ui/icons/GetApp';
import DataConnectorBrowser, { DataConnectorMetadata } from '../deploy/dataConnectorBrowser/DataConnectorBrowser';
import { AmazonS3ConnectorPopup } from '../deploy/AmazonS3ConnectorPopup';
import { GoogleCloudStorageConnectorPopup } from '../deploy/GoogleCloudStorageConnectorPopup';
import { GoogleDriveConnectorPopup } from '../deploy/GoogleDriveConnectorPopup';
import { KaggleConnectorPopup } from '../deploy/KaggleConnectorPopup';
import { WasabiConnectorPopup } from '../deploy/WasabiConnectorPopup';
import { PhoneTextBox } from '../../core/PhoneTextBox';
import { AzureBlobStorageConnectorPopup } from '../deploy/AzureBlobStorageConnector';
import DeleteIcon from '@material-ui/icons/Delete';
import { FileMetadata } from '../deploy/fileBrowser/FileBrowser';
import { FileTree } from '../FileTree';
import moment from 'moment';

// Properties from parent
interface IProps {
    phoneValidOnBlur?: (valid: boolean) => void
	style?: CSSProperties
}

// Properties for this component
interface IState {}

const emUpSub = 'Upgrade subscription to unlock'

const LABEL_WIDTH = '80px'

interface IAccountGeneralSubMenuState {
    switchKey: number
}

export class AccountGeneralSubMenu extends React.Component<IProps, IAccountGeneralSubMenuState> {

    constructor(props: IProps) {
        super(props);
        this.state = {
            // We need to increment this when the user changes his number so the switch will be enabled/disabled properly
            switchKey: 0
        }
    }

    private getPasswordValue(): string { return '******' }
    private savePasswordValue(password: string) {
        Global.user.changePassword("", "", password);
    }
    
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <div style={Object.assign({padding: '6px'}, this.props.style)}>
                    {/* <ResourceTextBox<string>
                        getValue={this.getNameValue}
                        label='Name'
                        editPressRequired
                    /> */}
                    <div style={{display: 'inline-flex', width: '100%'}}>
                        <TextBox<string>
                            style={{flexGrow: 1}}
                            getValue={this.getPasswordValue}
                            saveValue={this.savePasswordValue}
                            label='Password'
                            labelWidth={LABEL_WIDTH}
                        />
                        <ChangePasswordPopup style={{margin: '8px 0px', height: '20px', fontSize: '12px', lineHeight: '12px'}}/>
                    </div>
                    <PhoneTextBox
                        getValue={() => Global.user.phoneNumber}
                        saveValue={(phoneNumber: string) => {
                            if (phoneNumber == '') Global.user.notificationsEnabled = false;
                            Global.user.phoneNumber = phoneNumber;
                            // We need to update so the switch below will be updated properly
                            this.setState({ switchKey: this.state.switchKey+1 });
                        }}
                        validOnBlur={this.props.phoneValidOnBlur}
                        label='Phone'
                        labelWidth={LABEL_WIDTH}
                    />
                    <Switch
                        key={this.state.switchKey}
                        getValue={() => Global.user.notificationsEnabled }
                        saveValue={(notificationsEnabled: boolean) => { Global.user.notificationsEnabled = notificationsEnabled }}
                        label='Enable SMS notifications to the listed phone number'
                        disabled={Global.user.phoneNumber == ''}
                        labelBefore
                        flip
                    />
                    <Switch
                        getValue={() => Global.user.compressFilesEnabled}
                        saveValue={(compressFilesEnabled: boolean) => { Global.user.compressFilesEnabled = compressFilesEnabled }}
                        label='Compress my files before uploading'
                        labelBefore
                        flip
                    />
                    <Switch
                        getValue={() => Global.user.snapToInventoryEnabled}
                        saveValue={(snapToInventoryEnabled: boolean) => { Global.user.snapToInventoryEnabled = snapToInventoryEnabled }}
                        label='Snap resource selection sliders to existing inventory'
                        labelBefore
                        flip
                    />
                    {Global.user.showMonitoringEnabled && (
                        <Button 
                            variant="outlined"
                            color="primary"
                            startIcon={<GetAppIcon />}
                            style={{width: '100%'}}
                            onClick={async () => {
                                const data = [];
                                for (let app of Global.user.appTracker.finishedJobsOrSessions) {
                                    const machine = app.machine;
                                    data.push(
                                        [
                                            this.stringToCSVCell(app.name),
                                            this.stringToCSVCell(app.annotationOrRunNum),
                                            app.timestamp,
                                            app.getTimeElapsed(),
                                            app.getCost(),
                                            app.getAppMessage(),
                                            machine.name,
                                            machine.computeCores,
                                            FormatUtils.styleCapacityUnitValue()(machine.memorySize),
                                            FormatUtils.styleCapacityUnitValue()(machine.storageSize),
                                            machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + ' ' + machine.graphicsCardType) : 'None',
                                            app.uuid,
                                        ]
                                    );
                                    
                                    var link = document.createElement("a");
                                    var blob = new Blob([JSON.stringify(app.machine)], {
                                        type: "text/plain;charset=utf-8"
                                    });
                                    link.setAttribute("href", window.URL.createObjectURL(blob));
                                    link.setAttribute("download", app.uuid + ".txt");
                                    document.body.appendChild(link); // Required for FF
                                    link.click();

                                    await new Promise(resolve => setTimeout(resolve, 100));

                                    // const ipynbContent = 'data:text/plain;charset=utf-8,'
                                    //     + JSON.stringify(app.notebook);
                                    var link = document.createElement("a");
                                    var blob = new Blob([JSON.stringify(app.notebook)], {
                                        type: "text/plain;charset=utf-8"
                                    });
                                    link.setAttribute("href", window.URL.createObjectURL(blob));
                                    link.setAttribute("download", app.uuid + ".ipynb");
                                    document.body.appendChild(link); // Required for FF
                                    link.click();

                                    await new Promise(resolve => setTimeout(resolve, 100));
                                }
            
                                const headers = [
                                    ["Name", "Annotation", "Start Time", "Duration", "Cost", "Status", "Machine", "Cores", "RAM", "Disk", "GPUs", "UUID"]
                                ];
            
                                var link = document.createElement("a");
                                var blob = new Blob([headers.map(e => e.join(",")).join("\n") + '\n' + data.map(e => e.join(",")).join("\n") + '\n'], {
                                    type: "data:text/csv;charset=utf-8,"
                                });
                                link.setAttribute("href", window.URL.createObjectURL(blob));
                                link.setAttribute("download", "run_history.csv");
                                document.body.appendChild(link); // Required for FF
                                link.click();
                            }
                        }>
                            Download all runs
                        </Button>
                    )}
                </div>
            </>
        )
    }

    public stringToCSVCell(str: string): string {
        var s = "\"";
        for(let nextChar of str) {
            s += nextChar;
            if (nextChar == '"')
                s += "\"";
        }
        s += "\"";
        return s;
    }

    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

interface IAccountLimitsSubMenuState {
    holdoverFocused: boolean;
    budgetFocused: boolean;
    recsFocused: boolean;
}

export class AccountLimitsSubMenu extends React.Component<IProps, IAccountLimitsSubMenuState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        this.state = {
            holdoverFocused: false,
            budgetFocused: false,
            recsFocused: false,
        }
    }
    private getUserBudgetValue(): number { return Global.user.userBudget }
    private saveUserBudgetValue(userBudget: number) { Global.user.userBudget = userBudget }

    private getMaxJobsValue(): number { return Global.user.maxJobs }
    private saveMaxJobsValue(value: number) { Global.user.maxJobs = value }

    private getMaxMachinesValue(): number { return Global.user.maxMachines }
    private saveMaxMachinesValue(value: number) { Global.user.maxMachines = value }

    private getUserHoldoverTimeValue(): number { return Global.user.userHoldoverTime }
    private saveUserHoldoverTimeValue(userHoldoverTime: number) { Global.user.userHoldoverTime = userHoldoverTime }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <div style={Object.assign({padding: '6px'}, this.props.style)}>
                    {Global.user.userExpertise > 0 ? (<TextBox<number>
                        getValue={this.getUserBudgetValue}
                        saveValue={this.saveUserBudgetValue}
                        styledUnitValue={(value: number) => '$' + value.toFixed(2)}
                        unstyleUnitValue={(value: string) => { return value.replace('$', '').replace('.', '').replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value.replace('$', '')) }}
                        label='Budget'
                        labelWidth={LABEL_WIDTH}
                        onFocus={() => this.safeSetState({budgetFocused: true})}
                        onBlur={() => this.safeSetState({budgetFocused: false})}
                        helperText={this.state.budgetFocused ? `Must be between $1 and $${Global.user.maxBudget}` : 'Max monthly spend'}
                        minValue={1}
                        maxValue={Global.user.maxBudget}
                        // disabledMessage={Global.user.userExpertise < 2 ? emUpSub : ''}
                    />) : (<></>)}
                    <TextBox<number>
                        getValue={this.getMaxJobsValue}
                        saveValue={this.saveMaxJobsValue}
                        unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value) }}
                        label='Jobs/Sessions'
                        labelWidth={LABEL_WIDTH}
                        helperText={'Max combined number of concurrent jobs and sessions'}
                        disabledMessage={emUpSub}
                    />
                    <TextBox<number>
                        getValue={this.getMaxMachinesValue}
                        saveValue={this.saveMaxMachinesValue}
                        unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value) }}
                        label='Machines'
                        labelWidth={LABEL_WIDTH}
                        helperText='Max number of concurrent machines'
                        disabledMessage={emUpSub}
                    />
                    <TextBoxDropdown
                        getValue={this.getUserHoldoverTimeValue}
                        saveValue={this.saveUserHoldoverTimeValue}
                        unitValues={[
                            {unit: 'seconds', value: 1},
                            {unit: 'minutes', value: 60},
                            {unit: 'hours', value: 3600},
                        ]}
                        label='Auto-release'
                        labelWidth={LABEL_WIDTH}
                        onFocus={() => this.safeSetState({holdoverFocused: true})}
                        onBlur={() => this.safeSetState({holdoverFocused: false})}
                        helperText={this.state.holdoverFocused ? `Must be between 0 seconds and ${Global.user.maxHoldoverTime / 3600} hours` : 'Time before releasing idle machines'}
                        minValue={0}
                        maxValue={Global.user.maxHoldoverTime}
                    />
                </div>
            </>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

interface IAccountPaymentSubMenuState {
    balance: number;
    billing: any[];
}

export class AccountPaymentSubMenu extends React.Component<IProps, IAccountPaymentSubMenuState> {
    private _isMounted = false;
    private polling = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            balance: 0,
            billing: [],
        }
    }

    private getDuration = (record: any): string => {
        var endTime = new Date(record.endTime as string);
        var startTime = new Date(record.startTime as string);
        var diff = endTime.getTime() - startTime.getTime();
        const stillRunning = diff < 0;
        if (stillRunning) {
            diff = new Date().getTime() - startTime.getTime();
        }
        var time = FormatUtils.msToTime(diff).split(':');
        var formatted;
        if (time.length == 3) {
            formatted = time[0] + 'h ' + time[1] + 'm ' + time[2] + 's';
        } else {
            formatted = time[0] + 'm ' + time[1] + 's';
        }
        return stillRunning ? formatted + ' (still running)' : formatted;
    }

    private getCost = (record: any): string => {
        var endTime = new Date(record.endTime as string);
        var startTime = new Date(record.startTime as string);
        var diff = endTime.getTime() - startTime.getTime();
        const stillRunning = diff < 0;
        if (stillRunning) {
            diff = new Date().getTime() - startTime.getTime();
        }
        var formatted = '$' + ((diff / 3600000) * record.machine.rate).toFixed(2);
        return stillRunning ? formatted + ' (still running)' : formatted;
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <div style={Object.assign({padding: '6px'}, this.props.style)}>
                    <div style={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                        <div 
                            style={{
                            lineHeight: '24px',
                            margin: '0px 12px',
                            flexGrow: 1,
                        }}
                        >
                            {'Remaining balance:'}
                        </div>
                        <div style={{padding: '0px 6px 0px 6px'}}>
                            {'$' + (-this.state.balance).toFixed(2)}
                        </div>
                    </div>
                    <CheckoutForm />
                    <div style={{padding: '6px', width: '100%'}}>
                        <Button
                            variant="outlined"
                            color="primary"
                            startIcon={<GetAppIcon />}
                            style={{width: '100%'}}
                            onClick={() => this.getDetailedBilling(true)}
                        >
                            Billing records
                        </Button>
                    </div>
                </div>
            </>
        )
    }

    private async receiveUpdate() {
		const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-total-billing";
        const now = new Date();
        const epoch = new Date(0);
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: epoch.toISOString(),
				endTime: now.toISOString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (this.polling) {
				// If we are polling, send a new request in 2 seconds
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.receiveUpdate(), 2000);
			}
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body) {
                this.safeSetState({ balance: body.balance });
			}
        });
    }
    
    private getDetailedBilling = (save: boolean) => {
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-detailed-billing";
        const now = new Date();
        const epoch = new Date(0);
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: epoch.toISOString(),
				endTime: now.toISOString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body) {
                this.safeSetState({ billing: body.records });
                if (save) {
                    const data: string[][] = [];
                    var sorted: any[] = body.records.sort((n1: any, n2: any) => {
                        if (n1.startTime > n2.startTime) {
                            return -1;
                        }
                        if (n1.startTime < n2.startTime) {
                            return 1;
                        }
                        return 0;
                    });
                    for (let record of sorted) {
                        const machine = record.machine;
                        data.push(
                            [
                                new Date(record.startTime).toLocaleString().replace(/,/g, ''),
                                new Date(0).toISOString() == new Date(record.endTime).toISOString() ? 'Still running' : new Date(record.endTime).toLocaleString().replace(/,/g, ''),
                                this.getDuration(record),
                                '$' + machine.rate.toFixed(2),
                                this.getCost(record),
                                machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + 'x' + machine.graphicsCardType) : 'No GPU',
                                machine.computeCores + ' cores',
                                FormatUtils.styleCapacityUnitValue()(machine.memorySize),
                                FormatUtils.styleCapacityUnitValue()(machine.storageSize)
                            ]
                        );
                    }

                    const headers = [
                        ["Start Time", "End Time", "Duration", "Rate ($/hr)", "Cost", "GPU", "CPU", "RAM", "Disk"]
                    ];
                    
                    var link = document.createElement("a");
                    var blob = new Blob([headers.map(e => e.join(",")).join("\n") + '\n' + data.map(e => e.join(",")).join("\n") + '\n'], {
                        type: "data:text/csv;charset=utf-8,"
                    });
                    link.setAttribute("href", window.URL.createObjectURL(blob));
                    link.setAttribute("download", "billing_records.csv");
                    document.body.appendChild(link); // Required for FF
                    link.click();
                }
			}
        });
    }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
        this.getDetailedBilling(false);
        this.polling = true;
        this.receiveUpdate();
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        this._isMounted = false;
        this.polling = false;
    }
    
    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

interface IAccountConnectorsSubMenuState {
    dataConnectors: DataConnectorMetadata[],
    browserKey: number,
}

export class AccountConnectorsSubMenu extends React.Component<IProps, IAccountConnectorsSubMenuState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        this.state = {
            dataConnectors: [],
            browserKey: 0,
        }
    }

    // Use a key to force the data connector browser to refresh
    private forceNewBrowser = () => {
        this.safeSetState({ browserKey: this.state.browserKey + 1 })
    }

    public request = async () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'optumi/get-data-connectors'
		return ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json()
		})
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <div style={Object.assign({}, this.props.style)}>
                    <div style={{display: 'inline-flex', margin: '6px'}}>
                        <Header title='Existing Connectors' style={{ lineHeight: '24px', margin: '6px 6px 6px 11px' }} />
                    </div>
                    <Divider />
                    <DataConnectorBrowser
                        key={this.state.browserKey}
                        style={{
                            maxHeight: 'calc(100% - 60px - 2px)',
                        }}
                        handleDelete={(dataConnectorMetadata: DataConnectorMetadata) => {
                            const settings = ServerConnection.makeSettings();
                            const url = settings.baseUrl + "optumi/remove-data-connector";
                            const init: RequestInit = {
                                method: 'POST',
                                body: JSON.stringify({
                                    name: dataConnectorMetadata.name,
                                }),
                            };
                            ServerConnection.makeRequest(
                                url,
                                init, 
                                settings
                            ).then((response: Response) => {
                                Global.handleResponse(response);
                            }).then(() => {
                                var newDataConnectors = [...this.state.dataConnectors]
                                newDataConnectors = newDataConnectors.filter(dataConnector => dataConnector.name !== dataConnectorMetadata.name)
                                this.safeSetState({dataConnectors: newDataConnectors})
                                this.forceNewBrowser()
                            }).then(() => Global.dataConnectorChange.emit(void 0));                   
                        }}
                    />
                    <Divider style={{marginTop: '33px'}}/>
                    <div style={{display: 'inline-flex', margin: '6px'}}>
                        <Header title='New Connectors' style={{ lineHeight: '24px', margin: '6px 6px 6px 11px'  }} />
                    </div>
                    <Divider />
                    <div style={{marginBottom: '6px'}} />
                    <AmazonS3ConnectorPopup onClose={this.forceNewBrowser} />
                    <AzureBlobStorageConnectorPopup onClose={this.forceNewBrowser} />
                    <GoogleCloudStorageConnectorPopup onClose={this.forceNewBrowser} />
                    <GoogleDriveConnectorPopup onClose={this.forceNewBrowser} />
                    <KaggleConnectorPopup onClose={this.forceNewBrowser} />
                    <WasabiConnectorPopup onClose={this.forceNewBrowser} />
                </div>
            </>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
        this.request().then(json => this.safeSetState({dataConnectors: json.connectors}))
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: IProps, nextState: IAccountConnectorsSubMenuState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

interface IAccountFilesSubMenuState {}

export class AccountFilesSubMenu extends React.Component<IProps, IAccountFilesSubMenuState> {
    constructor(props: IProps) {
        super(props);
        this.state = {
            files: [],
            appsToFiles: new Map(),
            filesToApps: new Map(),
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const files = Global.user.fileTracker.files;
        return (
            <>
                <div style={Object.assign({padding: '20px 6px 6px 20px'}, this.props.style)}>
                    <div>
                        Listed files are securely stored in the Optumi platform. If you want to delete a file hit its associated trash can icon.
                        {this.getTotalUsedStorage() > 0 && <>
                            <br />
                            <br />
                            Total used storage: {this.formatSize(this.getTotalUsedStorage())}
                        </>}
                    </div>
                    <FileTree<FileMetadata>
                        files={files}
                        fileTitle={file => (
`Name: ${file.name}
${file.size === null ? '' : `Size: ${this.formatSize(file.size)}
`}${file.path === '' ? '' : `Path: ${file.path.replace(file.name, '').replace(/\/$/, '')}
`}Modified: ${moment(file.last_modified).format('YYYY-MM-DD hh:mm:ss')}`
                        )}
                        fileHidableIcon={file => ({
                            width: 72,
                            height: 36,
                            icon: (
                                <>
                                    <IconButton
                                        onClick={() => this.downloadFile(file)}
                                        style={{ width: '36px', height: '36px', padding: '3px' }}
                                    >
                                        <GetAppIcon style={{ width: '30px', height: '30px', padding: '3px' }} />
                                    </IconButton>
                                    <IconButton
                                        onClick={() => this.deleteFile(file)}
                                        style={{ width: '36px', height: '36px', padding: '3px' }}
                                    >
                                        <DeleteIcon style={{ width: '30px', height: '30px', padding: '3px' }} />
                                    </IconButton>
                                </>
                            ),
                        })}
                        directoryHidableIcon={path => ({
                            width: 72,
                            height: 36,
                            icon: (
                                <>
                                    <IconButton
                                        onClick={() => this.downloadDirectory(path)}
                                        style={{ width: '36px', height: '36px', padding: '3px' }}
                                    >
                                        <GetAppIcon style={{ width: '30px', height: '30px', padding: '3px' }} />
                                    </IconButton>
                                    <IconButton
                                        onClick={() => this.deleteDirectory(path)}
                                        style={{ width: '36px', height: '36px', padding: '3px' }}
                                    >
                                        <DeleteIcon style={{ width: '30px', height: '30px', padding: '3px' }} />
                                    </IconButton>
                                </>
                            ),
                        })}
                    />
                </div>
            </>
        )
    }

    private formatSize = (value: number) => {
		if (value == 0) return "";
		if (value < Math.pow(1024, 1)) {
            return value.toFixed() + ' B';
        } else if (value < Math.pow(1024, 2)) {
            return (value / Math.pow(1024, 1)).toFixed(1) + ' KiB';
        } else if (value < Math.pow(1024, 3)) {
            return (value / Math.pow(1024, 2)).toFixed(1) + ' MiB';
        } else if (value < Math.pow(1024, 4)) {
            return (value / Math.pow(1024, 3)).toFixed(1) + ' GiB';
        } else if (value < Math.pow(1024, 5)) {
            return (value / Math.pow(1024, 4)).toFixed(1) + ' TiB';
        } else {
            return (value / Math.pow(1024, 5)).toFixed(1) + ' PiB';
        }
	}

    private getTotalUsedStorage = (): number => {
        let totalUsedStorage: number = 0
        for (let file of Global.user.fileTracker.files) {
            totalUsedStorage += file.size
        }
        return totalUsedStorage
    }

    private async deleteFile(file: FileMetadata) {
        Global.user.fileTracker.deleteFiles([file]);
    }

    private async downloadFile(file: FileMetadata) {
		Global.user.fileTracker.downloadFiles(file.path, [file], false);
    }

    private async deleteDirectory(path: string) {
        let filesToDelete: FileMetadata[] = []
        for (let file of Global.user.fileTracker.files) {
            if (file.path.startsWith(path)) {
                filesToDelete.push(file)
            }
        }
        Global.user.fileTracker.deleteFiles(filesToDelete);
    }

    private async downloadDirectory(path: string) {
        let filesToDownload: FileMetadata[] = []
        for (let file of Global.user.fileTracker.files) {
            if (file.path.startsWith(path)) {
                filesToDownload.push(file)
            }
        }
        Global.user.fileTracker.downloadFiles(path, filesToDownload, false);
    }

    private handleFilesChange = () => this.forceUpdate();

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        Global.user.fileTracker.getFilesChanged().connect(this.handleFilesChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.user.fileTracker.getFilesChanged().disconnect(this.handleFilesChange);
    }

    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}
export class TeamSubMenu extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <Header title='Members' />
        )
    }
}
