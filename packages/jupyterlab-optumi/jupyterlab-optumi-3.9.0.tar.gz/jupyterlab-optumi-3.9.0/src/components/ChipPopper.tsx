import * as React from 'react'
import { Global } from '../Global';

import { Chip, darken, IconButton, lighten, Theme, withStyles, withTheme } from '@material-ui/core';
import { Popper } from '../core/Popper';
import { Close, KeyboardArrowDown, KeyboardArrowUp } from '@material-ui/icons';
import { CSSProperties } from '@material-ui/styles';

const StyledChip = withStyles(theme => ({
    root: {
        height: '20px',
        fontSize: '12px',
        // borderWidth: '2px',
        // borderStyle: 'solid',
        transition: 'all 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
        transitionProperty: 'background-color',
    },
    icon: {
        position: 'absolute',
        right: theme.spacing(0.75),
    },
    label: {
        position: 'absolute',
        left: theme.spacing(0.5),
        padding: theme.spacing(0),
    },
}))(Chip)

interface IProps {
    style: CSSProperties
    theme: Theme
    title: string
    color: string
    clearValue: () => any
    getChipDescription?: () => string
    getHeaderDescription: () => string
    popperContent: JSX.Element
}

interface IState {
    open: boolean
}

class ChipPopper extends React.Component<IProps, IState> {
    _isMounted = false;
    close: () => void = () => {}
    stopPropagation: () => void = () => {}

    public constructor(props: IProps) {
        super(props)
        this.state = {
            open: false,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const theme: Theme = this.props.theme
        const description = this.props.getHeaderDescription();
        const modified: boolean = description != 'Any';
		return (
            <Popper
                color={this.props.color}
                onOpen={() => this.safeSetState({open: true})}
                onClose={() => this.safeSetState({open: false})}
                close={(close: () => void) => this.close = close}
                stopPropagation={(stopPropagation: () => void) => this.stopPropagation = stopPropagation}
                button={
                    <StyledChip
                        key={this.props.title + 'chip'}
                        clickable
                        style={Object.assign({
                            fontWeight: modified ? 'bold' : undefined,
                            color: modified ? this.props.color : undefined,
                            border: modified ? ('0px solid ' + this.props.color) : undefined,
                            backgroundColor: modified ? Global.themeManager.isLight(Global.themeManager.theme) ? lighten(this.props.color, 0.8): darken(this.props.color, 0.65) : 'var(--jp-layout-color1)'
                        }, this.props.style)}
                        variant='outlined'
                        label={this.props.getChipDescription ? this.props.getChipDescription() : this.props.title + ': ' + this.props.getHeaderDescription()}
                        icon={(
                            modified ? (
                                <IconButton
                                    style={{
                                        padding: theme.spacing(0.25),
                                        margin: theme.spacing(-0.25, -0.75, -0.25, -0.25),
                                        zIndex: 1,
                                    }}
                                    onClick={() => {
                                        this.props.clearValue()
                                        this.stopPropagation()
                                    }}
                                >
                                    <Close style={{height: '14px',width: '14px', color: this.props.color}}/>
                                </IconButton>
                            ) : this.state.open ? (
                                <KeyboardArrowUp style={{height: '14px',width: '14px'}}/>
                            ) : (
                                <KeyboardArrowDown style={{height: '14px',width: '14px'}}/>
                            )
                        )}
                    />
                }
                popup={
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        margin: theme.spacing(1),
                        fontSize: '15px',
                        lineHeight: '15px',
                    }}>
                        <div style={{display: 'flex'}}>
                            <span style={{fontWeight: 'bold'}}>
                                {this.props.title}:
                            </span>
                            <span style={{whiteSpace: 'pre'}}>
                                {` ${description}`}
                            </span>
                            <div style={{width: '100%'}} />
                            <IconButton
                                style={{padding: theme.spacing(0.5), margin: theme.spacing(-0.5)}}
                                onClick={this.close}
                            >
                                <Close style={{width: '15px', height: '15px'}}/>
                            </IconButton>
                        </div>
                        <div style={{fontSize: '14px'}}>
                            {this.props.popperContent}
                        </div>
                    </div>
                }
            />
		);
	}

    private handleThemeChange = () => this.forceUpdate()
    private handleMetadataChange = () => this.forceUpdate()

    public componentDidMount = () => {
		this._isMounted = true;
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
const ThemedChipPopper = withTheme(ChipPopper)
export {ThemedChipPopper as ChipPopper}
