import * as React from 'react'
import { Global } from '../Global';

import { Dialog, IconButton, Theme, withStyles, withTheme } from '@material-ui/core';
import { Close, InfoOutlined } from '@material-ui/icons';
import { ShadowedDivider } from '.';
import MuiDialogTitle from '@material-ui/core/DialogTitle';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        // width: '100%',
        // height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

interface IProps {
    theme: Theme
    title: string
    popup: JSX.Element
}

interface IState {
    hovered: boolean
    open: boolean
}

class InfoPopup extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super(props)
        this.state = {
            hovered: false,
            open: false,
        }
    }
    
    private handleClickOpen = () => {
		this.safeSetState({ open: true });
	}

	private handleClose = () => {
        this.safeSetState({ open: false });
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const theme = this.props.theme;
		return (
            <>
                <IconButton
                    onClick={this.handleClickOpen}
                    style={{padding: '0px', marginRight: '-3px', margin: 'auto 0px'}}
                    onMouseOver={() => this.safeSetState({hovered: true})}
                    onMouseOut={() => this.safeSetState({hovered: false})}
                >
                    <InfoOutlined style={{width: '14px', height: '14px', color: this.state.hovered || this.state.open ? theme.palette.primary.light : theme.palette.text.disabled}}/>
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
                            minWidth: '225px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the MuiDialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <div style={{margin: 'auto 6px', paddingLeft: '12px'}}>
                                {this.props.title}
                            </div>
                        </div>
                        <div style={{flexGrow: 1}} />
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
                            <Close
                                style={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
                    </MuiDialogTitle>
                    <ShadowedDivider />
                    <div style={{
                        padding: '12px',
                        fontSize: 'var(--jp-ui-font-size1)',
                    }}>
                        {this.props.popup}
                    </div>
                </StyledDialog>
            </>
		);
	}

    public componentDidMount = () => {
		this._isMounted = true;
	}

	public componentWillUnmount = () => {
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
const ThemedInfoPopup = withTheme(InfoPopup)
export {ThemedInfoPopup as InfoPopup}
