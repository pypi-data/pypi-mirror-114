/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import { MenuItem, Select, withStyles } from '@material-ui/core';
import { GraphicsConfig } from '../../../models/GraphicsConfig';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {
    selectedCard: string
}

const StyledSelect = withStyles({
    root: {
        fontSize: "var(--jp-ui-font-size1)",
        width: '68px',
    },
    iconOutlined: {
        right: '0px'
    }
}) (Select)

const StyledMenuItem = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)',
        padding: '3px 3px 3px 6px',
        justifyContent: 'center',
    }
}) (MenuItem)

export class GraphicsEquipment extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        var card = this.getCardValue();
        card = Global.user.machines.graphicsCards.includes(card) ? card : 'U';
        this.state = {
            selectedCard: card,
        }
        this.saveCardValue(this.state.selectedCard);
    }
    
    private getCardValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        return graphics.boardType;
	}

	private async saveCardValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.boardType = value;
        tracker.setMetadata(optumi);
    }
    


    private handleCardChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        const value: string = event.target.value as string;
        this.safeSetState({ selectedCard: value });
        this.saveCardValue(value);
    }

    private getCardItems = (): JSX.Element[] => {
        var cardItems: JSX.Element[] = new Array();
        cardItems.push(<StyledMenuItem key={'U'} value={'U'}>Any</StyledMenuItem>)
        const availableCards = Global.user.machines.graphicsCards;
        for (var i = 0; i < availableCards.length; i++) {
            var value = availableCards[i]
            cardItems.push(<StyledMenuItem key={value} value={value}>{value}</StyledMenuItem>)
        }
        return cardItems;
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div style={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                {/* <div 
                    style={{
                    minWidth: '68px',
                    lineHeight: '24px',
                    textAlign: 'center',
                    margin: '0px 6px',
                }}/> */}
                <div style={{display: 'inline-flex', width: '100%', justifyContent: 'center'}}>
                    <div style={{padding: '0px 6px 0px 6px'}}>
                        <StyledSelect
                            value={this.state.selectedCard}
                            variant='outlined'
                            onChange={this.handleCardChange}
                            SelectDisplayProps={{style: {padding: '3px 20px 3px 6px'}}}
                            MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '6px'}}}}
                        >
                            {this.getCardItems()}
                        </StyledSelect>
                    </div>
                </div>               
                <div 
                    // title={this.props.tooltip || ''}
                    style={{
                    minWidth: '68px',
                    lineHeight: '24px',
                    textAlign: 'center',
                    margin: '0px 6px',
                }}>
                    {'Cards'}
                </div>
            </div>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
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
