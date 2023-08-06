/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { Machine } from '../models/machine/Machine';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Costs } from './machines/Costs';

interface IProps {
    style?: CSSProperties
    rate: number
    cost: number
    balance: number
    machines: Machine[],
}

interface IState {}

export class MachinesPage extends React.Component<IProps, IState> {

	// The contents of the component
	public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var machines: JSX.Element[] = new Array();
        for (var i = 0; i < this.props.machines.length; i++) {
            var machine: Machine = this.props.machines[i]
            if (Global.user.userExpertise >= 2 || machine.getStateMessage() != 'Releasing') {
                machines.push(
                    <div key={machine.uuid} style={{display: 'inline-flex', width: '100%', padding: '6px 0px'}}>
                        {machine.getComponent()}
                    </div>
                );
            }
        } 
		return (
			<div style={Object.assign({display: 'flex', flexFlow: 'column', overflow: 'hidden'}, this.props.style)}>
                <div style={{margin: '0px 20px'}}>
                    <Costs rate={this.props.rate} cost={this.props.cost} balance={this.props.balance}/>
                </div>
                <div style={{flexGrow: 1, overflowY: 'auto', padding: '6px'}}>
                    {machines.length == 0 ? (
                        <div style={{ textAlign: 'center', margin: '12px'}}>
                            Running machines will appear here.
                        </div>
                    ) : (
                        machines
                    )}
                </div>
			</div>
		);
    }
}
