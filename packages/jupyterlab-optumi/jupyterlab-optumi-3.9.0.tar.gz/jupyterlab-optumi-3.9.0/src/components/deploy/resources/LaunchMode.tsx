/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { SubHeader } from '../../../core';
// import { EmbeddedYoutube } from '../../../core/EmbeddedYoutube';
import { InfoPopup } from '../../../core/InfoPoppup';
import { Global } from '../../../Global';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import ExtraInfo from '../../../utils/ExtraInfo';

import { OutlinedResourceRadio } from '../OutlinedResourceRadio';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class LaunchMode extends React.Component<IProps, IState> {

    private getValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        return optumi.config.interactive ? "Session" : "Job";
	}

	private saveValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.config.interactive = value == "Session" ? true : false;
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const value = this.getValue();
        return (
            <>
                <div style={{display: 'flex'}}>
                    <SubHeader title='Launch Mode'/>
                    <InfoPopup
                        title='Launch Mode'
                        popup={
                            <div style={{margin: '12px'}}>
                                <p style={{whiteSpace: 'pre-line'}}>
                                    {`The selected launch mode determines how your notebook will be run in the cloud.`}
                                </p>
                                <p style={{whiteSpace: 'pre-line', textDecoration: 'underline', marginBottom: '0'}}>
                                    {`Session`}
                                </p>
                                <p style={{whiteSpace: 'pre-line'}}>
                                    {`If selected, Optumi will start a JupyterLab server in the cloud that you will connect to via browser. A new browser tab will open automatically when the session begins running. You will be able to work interactively, the same way you do in local JupyterLab, however notebook execution will take place on the remote server.

                                    This is often useful when developing or debugging your code.`}
                                </p>
                                <p style={{whiteSpace: 'pre-line', textDecoration: 'underline', marginBottom: '0'}}>
                                    {`Job`}
                                </p>
                                <p style={{whiteSpace: 'pre-line'}}>
                                    {`If selected, Optumi will take a snapshot of your notebook and execute it in the cloud, from start to finish. You will be able to see the notebook output as your job progresses, however you won’t be able to interact with the notebook.

                                    This is often useful when training or hyperparameter tuning. You can think of it as a “fire and forget” mode where you are free to shut your laptop without impacting notebook execution.
                                    `}
                                </p>
                                {/* <EmbeddedYoutube
                                    name='Demo'
                                    url={'https://www.youtube.com/watch?v=MXzv-XL6LLs'}
                                    width={700}
                                    height={480}
                                /> */}
                            </div>
                        }
                    />
                </div>
                <div
                    style={{
                        alignItems: 'center',
                        display: 'inline-flex',
                        width: '100%',
                    }}
                >
                    <ExtraInfo reminder='Run an interactive session'>
                        <OutlinedResourceRadio beta label={'Session'} color={'#afaab0'} selected={value == "Session"} handleClick={() => this.saveValue("Session")}/>
                    </ExtraInfo>
                    <ExtraInfo reminder='Run a batch job'>
                        <OutlinedResourceRadio label={"Job"} color={'#afaab0'} selected={value == "Job"} handleClick={() => this.saveValue("Job")}/>
                    </ExtraInfo>
                </div>
            </>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
