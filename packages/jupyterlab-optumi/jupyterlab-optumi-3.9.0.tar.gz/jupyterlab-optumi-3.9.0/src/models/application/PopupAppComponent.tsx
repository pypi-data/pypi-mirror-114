/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, Dialog, DialogContent, IconButton, Tab, Tabs, withStyles } from '@material-ui/core';
import * as React from 'react';
import { Global } from '../../Global';
import PopupIcon from '@material-ui/icons/MoreVert';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import CloseIcon from '@material-ui/icons/Close';
import { App } from './App';
import { ScrollableDiv } from '../../components/monitor/ScrollableDiv';
import { OutputFileList } from '../../components/deploy/OutputFileList';
import { Status } from '../Module';
import { MachineCapability } from '../machine/MachineCapabilities';
import { ShadowedDivider } from '../../core';

import OpenInNewIcon from '@material-ui/icons/OpenInNew';
import Notebook from '../../core/notebook/Notebook';
import FileServerUtils from '../../utils/FileServerUtils';
import { NotificationContent } from '../../core/NotificationContent';
import { OptumiConfig } from '../OptumiConfig';
import ExtraInfo from '../../utils/ExtraInfo';
import { ResourceGraph } from '../../core/ResourceGraph';

const StyledDialog = withStyles({
    paper: {
        width: '80%',
        height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

const enum Page {
    SUMMARY = 0,
    NOTIFICATIONS = 1,
    NOTEBOOK = 2,
    FILES = 3,
    MACHINE = 4,
    LOG = 5,
    GRAPH = 6,
}

interface IProps {
    style?: CSSProperties
    app: App
    onOpen?: () => void
	onClose?: () => void
    onMouseOver?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
}

interface IState {
    open: boolean,
	selectedPanel: number,
	inputLine: string
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class PopupAppComponent extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
			selectedPanel: Page.SUMMARY,
			inputLine: ''
		};
    }
    
    private handleClickOpen = () => {
        if (this.props.onOpen) this.props.onOpen()
		this.safeSetState({ open: true });
	}

	private handleClose = () => {
        this.safeSetState({ open: false });
        if (this.props.onClose) this.props.onClose()
	}
    
    private handleMouseOver = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    private openSession = () => {
        window.open('http://' + window.location.hostname + ':' + this.props.app.sessionPort + '?token=' + this.props.app.sessionToken, '_blank');
    }

    private openAsNewNotebook = async () => {
        const app = this.props.app;
        var path = app.path.replace('.ipynb', '-' + (app.annotationOrRunNum.replace(/\W/g, '')) + '.ipynb');
        
        var inc = 0;
        var newPath = path;
        while ((await FileServerUtils.checkIfPathExists(newPath))[0]) {
            inc++;
            newPath = inc == 0 ? path : path.replace('.', '(' + inc + ').');
        }

        if (app.interactive) {
            const module = app.modules[0];
            for (let file of module.files) {
                if (file.path === '~/' + app.path) {
                    Global.user.fileTracker.downloadFiles(app.path, [file], false, [newPath]).then(() => { Global.docManager.open(newPath) });
                }
            }
        } else {
            var notebook: any = app.notebook;
            FileServerUtils.saveNotebook(newPath, notebook).then((success: boolean) => { Global.docManager.open(newPath) });
        }
        
        // Close the dialog
        this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var i = 0;
        const app = this.props.app;
        return (
            <>
                <IconButton
                    onClick={this.handleClickOpen}
                    style={{
                        display: 'inline-block',
                        width: '36px',
                        height: '36px',
                        padding: '3px',
                    }}
                    onMouseOver={this.handleMouseOver}
                    onMouseOut={this.handleMouseOut}
                >
                    <PopupIcon
                        style={{
                            width: '30px',
                            height: '30px',
                            padding: '3px',
                        }}
                    />
                </IconButton>
                <StyledDialog
					open={this.state.open}
					onClose={this.handleClose}
                    scroll='paper'
				>
					<MuiDialogTitle
					    disableTypography
                        style={{
                            display: 'inline-flex',
                            backgroundColor: 'var(--jp-layout-color2)',
                            height: '60px',
                            padding: '6px',
                            borderRadius: '4px',
                        }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            minWidth: '150px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the MuiDialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <div style={{margin: 'auto', paddingLeft: '12px'}}>
            					{app.interactive ? "Session" : "Job"}
                            </div>
                        </div>
						<div style={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
	                        <div style={{flexGrow: 1, margin: 'auto 0px'}}>
                                {app.path}
                            </div>
                            {app.interactive && (
                                <Button
                                    style={{margin: '6px'}}
                                    disableElevation
                                    variant='contained'
                                    color='primary'
                                    onClick={this.openSession}
                                    disabled={app.getAppStatus() == Status.COMPLETED || !(app.modules.length > 0 && app.modules[0].sessionReady)}
                                    endIcon={<OpenInNewIcon />}
                                >
                                    Open session
                                </Button>
                            )}
                            <ExtraInfo reminder='Create as a new notebook' >
                                <Button
                                    style={{margin: '6px'}}
                                    disableElevation
                                    variant='contained'
                                    color='primary'
                                    onClick={this.openAsNewNotebook}
                                    disabled={app.getAppStatus() != Status.COMPLETED}
                                    endIcon={<OpenInNewIcon />}
                                >
                                    Save + Open
                                </Button>
                            </ExtraInfo>
						</div>
                        <IconButton
                            onClick={this.handleClose}
                            style={{
                                display: 'inline-block',
                                width: '36px',
                                height: '36px',
                                padding: '3px',
                                margin: '6px',
                            }}
                        >
                            <CloseIcon
                                style={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
					</MuiDialogTitle>
                    <ShadowedDivider />
                    <div style={{display: 'flex', height: 'calc(100% - 60px - 2px'}}>
                        <div style={{width: '150px'}}>
                            <DialogContent style={{padding: '0px'}}>
                                <div style={{padding: '12px 6px'}}>
                                    <Tabs
                                        value={this.state.selectedPanel}
                                        onChange={(event, newValue) => this.safeSetState({selectedPanel: newValue})}
                                        orientation='vertical'
                                        variant='fullWidth'
                                        indicatorColor='primary'
                                        textColor='primary'
                                        style={{minHeight: '24px'}}
                                    >
                                        <Tab
                                            label='SUMMARY'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.SUMMARY}
                                        />
                                        {!app.interactive && <Tab
                                            label='NOTIFICATIONS'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.NOTIFICATIONS}
                                        />}
                                        {!app.interactive && <Tab
                                            label='NOTEBOOK'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.NOTEBOOK}
                                        />}
                                        <Tab
                                            label='FILES'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.FILES}
                                        />
                                        {/* <Tab
                                            label='NEW_FILES'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.NEW_FILES}
                                        /> */}
                                        <Tab
                                            label='MACHINE'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.MACHINE}
                                        />
                                        {app.modules.length > 0 && /*app.interactive &&*/ <Tab
                                            label='LOG'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.LOG}
                                        />}
                                        {Global.user.showMonitoringEnabled && <Tab
                                            label='GRAPH'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.GRAPH}
                                        />}
                                    </Tabs>
                                </div>
                            </DialogContent>
                        </div>
                        <ShadowedDivider orientation='vertical' />
                        <div style={{display: 'flex', flexFlow: 'column', overflow: 'hidden', width: 'calc(100% - 150px)', height: '100%'}}>
                            <DialogContent style={{
                                flexGrow: 1, 
                                overflowY: 'auto',
                                width: '100%',
                                height: '100%',
                                padding: '0px',
                                marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
                                // lineHeight: 'var(--jp-code-line-height)',
                                fontSize: 'var(--jp-ui-font-size1)',
                                // fontFamily: 'var(--jp-code-font-family)',
                            }}>
                                {this.state.selectedPanel == Page.SUMMARY ? (
                                    <div style={{padding: '20px'}}>
                                        {app.interactive ? 'Session' : 'Job'} launched at {app.timestamp.toLocaleTimeString('en-US', { 
                                            hour: 'numeric', minute: 'numeric',
                                        })} on {app.timestamp.toLocaleDateString('en-US', { 
                                            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
                                        })}
                                        <br/>
                                        {app.runNum ? (
                                            <>
                                                Run #{app.runNum + (app.config.annotation != '' ? ': ' + app.config.annotation : '')}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        {app.getTimeElapsed() ? (
                                            <>
                                                Duration: {app.getTimeElapsed()}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        {app.getCost() ? (
                                            <>
                                                Estimated cost: {app.getCost()}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        <br/>
                                        {/* The must have unique key error apparently applies to fragments as well, despite not being able to hold keys */}
                                        {(app.initializing.messages + app.preparing.messages + app.running.messages).split('\n').map((value: string) => (<span style={{whiteSpace: 'pre'}} key={value + i++}>{app.adjustMessage(value)}<br /></span>))}
                                    </div>
                                ) : this.state.selectedPanel == Page.NOTIFICATIONS ? (
                                    <div style={{padding: '20px'}}>
                                        <NotificationContent 
                                            getValue={() => app.config}
                                            saveValue={(config: OptumiConfig) => app.config = config}
                                            disabled={app.getAppStatus() == Status.COMPLETED}
                                            openUserDialogTo={this.props.openUserDialogTo}
                                            handleClose={this.handleClose}
                                        />
                                    </div>
                                ) : this.state.selectedPanel == Page.NOTEBOOK ? (
                                    <div style={{overflow: 'auto', width: '100%', height: '100%'}}>
                                        <Notebook notebook={app.notebook} />
                                    </div>
                                ) : this.state.selectedPanel == Page.FILES ? (
                                    <div style={{padding: '8px'}}>
                                        {app.interactive && app.getAppStatus() != Status.COMPLETED ? (
                                            <div style={{padding: '12px'}}>
                                                Files will appear here after your session has completed. Until then, you can upload/download files directly from the session tab.
                                            </div>
                                        ) : (
                                            <OutputFileList app={app} />
                                        )}
                                    </div>
                                ) : this.state.selectedPanel == Page.MACHINE ? (
                                    <div style={{padding: '14px 8px'}}>
                                         {app.machine ? (
									        <MachineCapability machine={app.machine} />
                                        ) : (
                                            <div style={{padding: '6px 12px'}}>
                                                Machine information will appear when the {app.interactive ? ' session ' : ' job '} starts.
                                            </div>
                                        )}
                                    </div>
                                    
								) : this.state.selectedPanel == Page.LOG ? (
                                    <div style={{overflow: 'hidden', width: '100%', height: '100%'}}>
                                        <ScrollableDiv
                                            key='output'
                                            source={Object.assign([], app.modules[0].output.filter(x => !x.line.startsWith('  warnings.warn(')))}
                                            autoScroll={true}
                                        />
                                    </div>
								) : this.state.selectedPanel == Page.GRAPH && (
                                    <div style={{overflow: 'hidden', width: '100%', height: '100%'}}>
                                        {app.modules.map(module => <ResourceGraph key={module.uuid} app={app} />)}
                                    </div>
								)}
                            </DialogContent>
                        </div>
                    </div>
				</StyledDialog>
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
}
