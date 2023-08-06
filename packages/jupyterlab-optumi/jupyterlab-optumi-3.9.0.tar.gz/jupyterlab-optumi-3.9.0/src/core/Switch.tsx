/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { withStyles, Switch as OtherSwitch } from '@material-ui/core';
import ExtraInfo from '../utils/ExtraInfo';

interface IProps {
    style?: React.CSSProperties
    tooltip?: string
    getValue: () => boolean
    saveValue: (value: boolean) => void
    label?: string
    labelWidth?: string
    labelBefore?: boolean;
    flip?: boolean
    ref?: any
    disabled?: boolean
    color?: string
    onMouseOver?: (...args: any[]) => any
    onMouseOut?: (...args: any[]) => any
}

interface IState {
    value: boolean,
}

export const getStyledSwitch = (color: string = '#10A0F9') => {
    return withStyles({
        root: {
            width: '42px',
            height: '24px',
            padding: '0px',
        },
        thumb: {
            width: '20px',
            height: '20px',
            padding: '0px',
            margin: '2px',
        },
        switchBase: {
            padding: '0px',
            '&$checked': {
                color: color,
            },
            '&$checked + $track': {
                backgroundColor: color,
            },
        },
        checked: {
            color: color,
        },
        track: {
            height: '12px',
            width: '34px',
            borderRadius: '6px',
            padding: '0px',
            margin: '6px',
        },
    }) (OtherSwitch);
}

export class Switch extends React.Component<IProps, IState> {
    private _isMounted = false

    StyledSwitch: any;

    public constructor(props: IProps) {
        super (props);
        this.StyledSwitch = getStyledSwitch(props.color);
        this.state = { value: this.props.getValue() }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div
                style={Object.assign({
                    display: 'inline-flex',
                    width: this.props.label ? '100%' : undefined,
                    padding: '6px 0px',
                }, this.props.style)}
                ref={this.props.ref}
                onMouseOver={this.props.onMouseOver}
                onMouseOut={this.props.onMouseOut}
            >
                {this.props.label && this.props.labelBefore && (
                    <div style={{width: '100%', textAlign: 'left', margin: 'auto 12px'}}>
                        {this.props.label}
                    </div>
                )}
                <ExtraInfo reminder={this.props.tooltip || ''}>
                    <div 
                        style={{
                        minWidth: this.props.labelWidth || 'unset',
                        lineHeight: '24px',
                        textAlign: 'center',
                        direction: this.props.flip ? 'rtl' : 'ltr'
                    }}>
                        <this.StyledSwitch
                            inputProps={{style: {height: '24px'}}}
                            checked={this.state.value}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                this.safeSetState({value: event.currentTarget.checked})
                                this.props.saveValue(event.currentTarget.checked)
                            }}
                            disabled={this.props.disabled}
                        />
                    </div>
                </ExtraInfo>
                {this.props.label && (this.props.labelBefore == undefined || this.props.labelBefore == false) && (
                    <div style={{width: '100%', textAlign: 'left', margin: 'auto 6px'}}>
                        {this.props.label}                    
                    </div>
                )}
            </div>
        )
    }

    private handleMetadataChange = () => { this.safeSetState({value: this.props.getValue()}) }
    private handleThemeChange = () => {
        this.StyledSwitch = getStyledSwitch(this.props.color)
        this.forceUpdate();
    }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
