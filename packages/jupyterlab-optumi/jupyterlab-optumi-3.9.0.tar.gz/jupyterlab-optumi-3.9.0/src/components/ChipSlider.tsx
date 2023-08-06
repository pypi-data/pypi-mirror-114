import * as React from 'react'
import { Global } from '../Global';

import { Slider, Theme, withStyles, withTheme } from '@material-ui/core';
import { CSSProperties } from '@material-ui/styles';

interface IProps {
    style?: CSSProperties
    theme: Theme
    label: string
    min?: number
    step?: number
    marks?: { value: number, label?: string }[] 
    max?: number
    color: string
    getValue: () => number[]
    saveValue: (value: number[]) => any
    styleValue: (value: number) => string,
    styleUnit: (value: number) => string,
    disabled?: boolean,
}

interface IState {
    value: number[]
}

var retrievingPreview: boolean = false;
var updatePreviewAgain: boolean = false;
var latestValue: number[];

class ChipSlider extends React.Component<IProps, IState> {
    _isMounted = false;
    close: () => void = () => {}
    stopPropagation: () => void = () => {}

    private StyledSlider: any;

    private min: number
    private max: number

    public constructor(props: IProps) {
        super(props)
        this.state = {
            value: this.props.getValue(),
        }
        this.StyledSlider = withStyles({
            root: {
                color: props.color,
                padding: '6px 0px',
                height: '6px',
            },
            track: {
                height: '6px',
            },
            rail: {
                height: '6px',
                borderRadius: '0px',
                marginLeft: '1px',
            },
            thumb: {
                height: '18px',
                width: '18px',
                marginTop: '-6px',
                marginLeft: '-9px',
                '&:focus, &:hover, &$active': {
                    boxShadow: '0px 0px 0px 7px ' + props.color + '29',
                },
                '&.Mui-disabled': {
                    width: '12px',
                    height: '12px',
                    marginTop: '-3px',
                    marginLeft: '-6px',
                }
            },
            mark: {
                marginTop: '1px',
                width: '2px',
                height: '4px',
                borderRadius: '0px',
            }
        })(Slider)
        this.min = this.props.marks ? this.props.marks[0].value : this.props.min;
        this.max = this.props.marks ? this.props.marks[this.props.marks.length-1].value : this.props.max;
    }

    private delay = (ms: number) => { return new Promise(resolve => setTimeout(resolve, ms)) }
    private slowDownSaveValue = (newValue: number[], bypassLimiter?: boolean) => {
        if (newValue != null) latestValue = newValue;
        if (bypassLimiter || !retrievingPreview) {
            retrievingPreview = true;
            this.delay(100).then(() => {
                this.props.saveValue(latestValue);
                if (updatePreviewAgain) {
                    updatePreviewAgain = false;
                    this.slowDownSaveValue(null, true);
                } else {
                    retrievingPreview = false;
                }
            }, () => {
                retrievingPreview = false;
            });
        } else {
            updatePreviewAgain = true;
        }
	}

    private handleChange = async (event: React.ChangeEvent<{}>, newValue: number | number[]) => {
		if (newValue instanceof Array) {
            const value = [...newValue];
            if (value[0] == this.min) value[0] = -1;
            if (value[1] == this.max) value[1] = -1;
			this.safeSetState({ value: value });
            this.slowDownSaveValue(value);
		}
    }

    private handleChangeCommitted = async (event: React.ChangeEvent<{}>, newValue: number | number[]) => {
        if (newValue instanceof Array) {
            const value = [...newValue];
            if (value[0] == this.min) value[0] = -1;
            if (value[1] == this.max) value[1] = -1;
            this.safeSetState({ value: value });
            this.props.saveValue(value);
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const theme: Theme = this.props.theme
        const value = [...this.state.value];
        if (value[0] == -1) value[0] = this.min;
        if (value[1] == -1) value[1] = this.max;
        return (
            <div style={Object.assign({marginTop: '12px'}, this.props.style)}>
                <div style={{margin: theme.spacing(0, 0.5), height: '18px'}}>
                    <this.StyledSlider
                        value={value}
                        min={this.min}
                        max={this.max}
                        step={this.props.step}
                        marks={this.props.marks}
                        onChange={this.handleChange}
                        onChangeCommitted={this.handleChangeCommitted}
                        disabled={this.props.disabled}
                    />
                </div>
                <div style={{display: 'inline-flex', width: '100%', marginTop: '12px'}}>
                    <div style={{flexGrow: 1, textAlign: 'left', fontSize: '13px', color: theme.palette.text.disabled}}>
                        {`${this.props.styleValue(this.min)} ${this.props.styleUnit(this.min)}`}
                    </div>
                    <div style={{flexGrow: 1, textAlign: 'center'}}>
                        {`${this.props.label}`}
                    </div>
                    <div style={{flexGrow: 1, textAlign: 'right', fontSize: '13px', color: theme.palette.text.disabled}}>
                        {`${this.props.styleValue(this.max)} ${this.props.styleUnit(this.max)}`}
                    </div>
                </div>
            </div>
        )
	}

    private handleMetadataChanged = () => {
        this.safeSetState ({ value: this.props.getValue() });
    }

    public componentDidMount = () => {
		this._isMounted = true;
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChanged);
	}

	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChanged);
		this._isMounted = false;
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
const ThemedChipSlider = withTheme(ChipSlider)
export {ThemedChipSlider as ChipSlider}
