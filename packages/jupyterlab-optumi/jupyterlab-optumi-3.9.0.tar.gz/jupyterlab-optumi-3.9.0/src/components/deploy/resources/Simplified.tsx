/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { SubHeader } from '../../../core';
import { Global } from '../../../Global';
import { Expertise } from '../../../models/OptumiConfig';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
// import ExtraInfo from '../../../utils/ExtraInfo';
import FormatUtils from '../../../utils/FormatUtils';
import { ChipPopper } from '../../ChipPopper';
import { ChipSlider } from '../../ChipSlider';
import { GPUChipPopper } from '../GPUChipPopper';

// import { OutlinedResourceRadio } from '../OutlinedResourceRadio';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class Simplified extends React.Component<IProps, IState> {
    private getCPUValue(): number[] {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        const cores = optumi.config.compute.cores;
		return [cores[0], cores[2]]
	}

	private saveCPUValue(value: number[]) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.config.compute.expertise = Expertise.SIMPLIFIED;
        optumi.config.compute.cores = [value[0], -1, value[1]];
        tracker.setMetadata(optumi);
    }

    private getRAMValue(): number[] {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        const size = optumi.config.memory.size;
		return [size[0], size[2]]
	}

	private saveRAMValue(value: number[]) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.config.memory.expertise = Expertise.SIMPLIFIED;
        optumi.config.memory.size = [value[0], -1, value[1]];
        tracker.setMetadata(optumi);
    }

    private getDiskValue(): number[] {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        const size = optumi.config.storage.size;
		return [size[0], size[2]]
	}

	private saveDiskValue(value: number[]) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.config.storage.expertise = Expertise.SIMPLIFIED;
        optumi.config.storage.size = [value[0], -1, value[1]];
        tracker.setMetadata(optumi);
    }

    private getDescription = (getValue: () => number[], min: number, max: number, styleValue: (value: number, unit?: string) => string, styleUnit: (value: number) => string): string => {
        const value = [...getValue()];
        if (value[0] == -1) value[0] = min;
        if (value[1] == -1) value[1] = max;
        if (value[0] === min && value[1] === max) {
            return `Any`
        } else if (value[0] !== min && value[1] !== max) {
            const maxUnit = styleUnit(value[1]);
            const minValue = styleValue(value[0], maxUnit)
            const maxValue = styleValue(value[1])
            if (minValue == maxValue) return `${minValue} ${styleUnit(value[1])}`
            return `${minValue}-${maxValue} ${styleUnit(value[1])}`
        } else if (value[0] !== min) {
            return `Min ${styleValue(value[0])} ${styleUnit(value[0])}`
        } else if (value[1] !== max) {
            return `Max ${styleValue(value[1])} ${styleUnit(value[1])}`
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <SubHeader title='Resource Selection'/>
                <div
                    style={{
                        alignItems: 'center',
                        // display: 'inline-flex',
                        width: '100%',
                    }}
                >
                    <div style={{display: 'flex'}}>
                        <GPUChipPopper />
                        <ChipPopper
                            style={{width: 'calc(50% - 12px)', margin: '0px 6px 6px'}}
                            title='CPU'
                            color={'#f48f8d'}
                            clearValue={() => this.saveCPUValue([-1, -1])}
                            getHeaderDescription={() => this.getDescription(this.getCPUValue, Global.user.machines.computeCoresMin, Global.user.machines.computeCoresMax, (value: number) => value.toString(), (value: number) => value == 1 ? 'core' : 'cores')}
                            popperContent={
                                <>  
                                    {Global.user.snapToInventoryEnabled ? (
                                        <ChipSlider
                                            key='cpu-snap'
                                            getValue={this.getCPUValue}
                                            saveValue={this.saveCPUValue}
                                            label={'Cores'}
                                            marks={Global.user.machines.computeCores.map(x => { return { value: x } })}
                                            step={null}
                                            color={'#f48f8d'}
                                            styleUnit={(value: number) =>'' }
                                            styleValue={(value: number) => value.toString()}
                                        />
                                    ) : (
                                        <ChipSlider
                                            key='cpu-no-snap'
                                            getValue={this.getCPUValue}
                                            saveValue={this.saveCPUValue}
                                            label={'Cores'}
                                            min={Global.user.machines.computeCoresMin}
                                            max={Global.user.machines.computeCoresMax}
                                            step={1}
                                            color={'#f48f8d'}
                                            styleUnit={(value: number) =>'' }
                                            styleValue={(value: number) => value.toString()}
                                        />
                                    )}
                                </>
                            }
                        />
                    </div>
                    <div style={{display: 'flex'}}>
                        <ChipPopper
                            style={{width: 'calc(50% - 12px)', margin: '0px 6px 6px'}}
                            title='RAM'
                            color={'#ba9fd1'}
                            clearValue={() => this.saveRAMValue([-1, -1])}
                            getHeaderDescription={() => this.getDescription(this.getRAMValue, Global.user.machines.memorySizeMin, Global.user.machines.memorySizeMax, FormatUtils.styleShortCapacityValue(), FormatUtils.styleCapacityUnit())}
                            popperContent={
                                <>  
                                    {Global.user.snapToInventoryEnabled ? (
                                        <ChipSlider
                                            key='ram-snap'
                                            getValue={this.getRAMValue}
                                            saveValue ={this.saveRAMValue}
                                            label={'Size'}
                                            marks={Global.user.machines.memorySize.map(x => { return { value: x } })}
                                            step={null}
                                            color={'#ba9fd1'}
                                            styleUnit={FormatUtils.styleCapacityUnit()}
                                            styleValue={FormatUtils.styleShortCapacityValue()}
                                        />
                                    ) : (
                                        <ChipSlider
                                            key='ram-no-snap'
                                            getValue={this.getRAMValue}
                                            saveValue ={this.saveRAMValue}
                                            label={'Size'}
                                            min={Global.user.machines.memorySizeMin}
                                            max={Global.user.machines.memorySizeMax}
                                            step={1024 * 1024 * 1024}
                                            color={'#ba9fd1'}
                                            styleUnit={FormatUtils.styleCapacityUnit()}
                                            styleValue={FormatUtils.styleShortCapacityValue()}
                                        />
                                    )}
                                </>
                            }
                        />
                        <ChipPopper
                            style={{width: 'calc(50% - 12px)', margin: '0px 6px 6px'}}
                            title='DISK'
                            color={'#7cdf8e'}
                            clearValue={() => this.saveDiskValue([-1, -1])}
                            getHeaderDescription={() => this.getDescription(this.getDiskValue, Global.user.machines.storageSizeMin, Global.user.machines.storageSizeMax, FormatUtils.styleShortCapacityValue(), FormatUtils.styleCapacityUnit())}
                            popperContent={
                                <>  
                                    {Global.user.snapToInventoryEnabled ? (
                                        <ChipSlider
                                            key='disk-snap'
                                            getValue={this.getDiskValue}
                                            saveValue ={this.saveDiskValue}
                                            label={'Size'}
                                            marks={Global.user.machines.storageSize.map(x => { return { value: x } })}
                                            step={null}
                                            color={'#7cdf8e'}
                                            styleUnit={(value: number) => {
                                                // We don't want to show MiB for disk, since the only disk size number below GiB is 0. In other words... show '0 GiB' instead of '0 MiB'
                                                const unit = FormatUtils.styleCapacityUnit()(value);
                                                return unit == 'MiB' ? 'GiB' : unit;
                                            }}
                                            styleValue={FormatUtils.styleShortCapacityValue()}
                                        />
                                    ) : (
                                        <ChipSlider
                                            key='disk-no-snap'
                                            getValue={this.getDiskValue}
                                            saveValue ={this.saveDiskValue}
                                            label={'Size'}
                                            min={Global.user.machines.storageSizeMin}
                                            max={Global.user.machines.storageSizeMax}
                                            step={1024 * 1024 * 1024}
                                            color={'#7cdf8e'}
                                            styleUnit={(value: number) => {
                                                // We don't want to show MiB for disk, since the only disk size number below GiB is 0. In other words... show '0 GiB' instead of '0 MiB'
                                                const unit = FormatUtils.styleCapacityUnit()(value);
                                                return unit == 'MiB' ? 'GiB' : unit;
                                            }}
                                            styleValue={FormatUtils.styleShortCapacityValue()}
                                        />
                                    )}
                                </>
                            }
                        />
                    </div>
                </div>
            </>
        )
    }

    private handleMetadataChange = () => this.forceUpdate();
    private handleUserChange = () => this.forceUpdate();

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.user.userInformationChanged.connect(this.handleUserChange);
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        // Set all resource levels to basic
        optumi.config.compute.expertise = Expertise.COMPONENT;
        optumi.config.memory.expertise = Expertise.COMPONENT;
        optumi.config.storage.expertise = Expertise.COMPONENT;
        tracker.setMetadata(optumi);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.user.userInformationChanged.disconnect(this.handleUserChange);
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
