/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { darken, Slider, withStyles } from '@material-ui/core';
import * as React from 'react';
import { Global } from '../../Global';
import ExtraInfo from '../../utils/ExtraInfo';
import FormatUtils from '../../utils/FormatUtils';
import { Machine, NoMachine } from './Machine';

const GraphicsBar = withStyles(forBar('Graphics', false)) (Slider);
const ComputeBar = withStyles(forBar('Compute', false)) (Slider);
const MemoryBar = withStyles(forBar('Memory', false)) (Slider);
const DiskBar = withStyles(forBar('Disk', false)) (Slider);

const EmptyGraphicsBar = withStyles(forBar('Graphics', true)) (Slider);
const EmptyComputeBar = withStyles(forBar('Compute', true)) (Slider);
const EmptyMemoryBar = withStyles(forBar('Memory', true)) (Slider);
const EmptyDiskBar = withStyles(forBar('Disk', true)) (Slider);

function forBar(type: string, empty: boolean): any {
    var color: string, trackRadius: string, railRadius: string
    if (type == 'Graphics') {
        color = '#ffba7d';
        trackRadius = '4px 4px 4px 0px';
        railRadius = '4px 4px 0px 0px';
    } else if (type == 'Compute') {
        color = '#f48f8d';
        trackRadius = '0px 4px 4px 0px';
        railRadius = '0px';
    } else if (type == 'Memory') {
        color = '#ba9fd1';
        trackRadius = '0px 4px 4px 0px';
        railRadius = '0px';
    } else if (type == 'Disk') {
        color = '#7cdf8e';
        trackRadius = '0px 4px 4px 4px';
        railRadius = '0px 0px 4px 4px';
    }
    return {
        root: {
            marginRight: '6px',
            height: type == 'Disk' ? '14px' : '13px',
            width: '100%',
            padding: '0px',
            lineHeight: 1,
            fontSize: '14px',
        },
        thumb: { // hidden
            height: '14px',
            top: '6px',
            backgroundColor: 'transparent',
            padding: '0px',
            '&:focus, &:hover, &:active': {
                boxShadow: 'none',
            },
            '&::after': {
                left: -6,
                top: -6,
                right: -6,
                bottom: -6,
            },
        },
        track: { // left side
            height: '14px',
            color: color,
            boxSizing: 'border-box',
            border: "1px solid " + darken(color, 0.25),
            borderRadius: trackRadius,
            opacity: empty ? 0 : 1,
        },
        rail: { // right side
            // display: 'none',
            height: '14px',
            color: color,
            borderRadius: railRadius,
        },
    };
}

interface IProps {
    machine: Machine
}

interface IState {}

const FONT_SIZE = '12px'
const COLUMN_WIDTH_1 = '30px'
const COLUMN_WIDTH_2 = '60px'
const COLUMN_MARGIN = '1px 0px 0px 0px'

export class IdentityMachineComponent extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const machine = this.props.machine
        const title = machine instanceof NoMachine ? 'No matching machines' : '';
        return (
            <ExtraInfo reminder={title}>
                <div style={{width: '100%', lineHeight: '9px'}}>
                    <div style={{width: '100%', display: 'inline-flex'}}>
                        {machine.graphicsRating > 0 ? (
                            <GraphicsBar
                                value={machine.graphicsRating}
                                max={1}
                                step={0.01}
                                disabled
                            />
                        ) : (
                            <EmptyGraphicsBar disabled />
                        )}
                        <div style={{minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            GPU
                        </div>
                        <div style={{minWidth: COLUMN_WIDTH_2, textAlign: 'right', margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            {(machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + ' ' + machine.graphicsCardType) : 'None')}
                        </div>
                    </div>
                    <div style={{width: '100%', display: 'inline-flex'}}>
                        {machine.computeRating > 0 ? (
                            <ComputeBar
                                value={machine.computeRating}
                                max={1}
                                step={0.01}
                                disabled
                            />
                        ) : (
                            <EmptyComputeBar disabled />
                        )}
                        <div style={{minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            CPU
                        </div>
                        <div style={{minWidth: COLUMN_WIDTH_2, textAlign: 'right', margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            {machine.computeCores == 1 ? machine.computeCores + ' core' : machine.computeCores + ' cores'}
                        </div>
                    </div>
                    <div style={{width: '100%', display: 'inline-flex'}}>                
                        {machine.memoryRating > 0 ? (
                            <MemoryBar
                                value={machine.memoryRating}
                                max={1}
                                step={0.01}
                                disabled
                            />
                        ) : (
                            <EmptyMemoryBar disabled />
                        )}
                        <div style={{minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            RAM
                        </div>
                        <div style={{minWidth: COLUMN_WIDTH_2, textAlign: 'right', margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            {FormatUtils.styleCapacityUnitValue()(machine.memorySize)}
                        </div>
                    </div>
                    <div style={{width: '100%', display: 'inline-flex'}}>                
                        {machine.storageRating > 0 ? (
                            <DiskBar
                                value={machine.storageRating}
                                max={1}
                                step={0.01}
                                disabled
                            />
                        ) : (
                            <EmptyDiskBar disabled />
                        )}
                        <div style={{minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            DISK
                        </div>
                        <div style={{minWidth: COLUMN_WIDTH_2, textAlign: 'right', margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                            {machine.storageSize != 0 ? FormatUtils.styleCapacityUnitValue()(machine.storageSize) : 'None'}
                        </div>
                    </div>
                </div>
            </ExtraInfo>
        )
    }
}