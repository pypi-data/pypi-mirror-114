/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import {
	ListItem,
	IconButton,
	CircularProgress,
} from '@material-ui/core';

import GetAppIcon from '@material-ui/icons/GetApp';
import DoneIcon from '@material-ui/icons/Done';
import { FileMetadata } from './fileBrowser/FileBrowser';

// Properties from parent
interface IProps {
	workloadUUID: string;
    moduleUUID: string;
    name: string;
	files: FileMetadata[];
    disabled: boolean;
    overwrite: boolean;
}

// Properties for this component
interface IState {
	downloading: boolean
	downloaded: boolean
}

export class FileEntry extends React.Component<IProps, IState> {
	// We need to know if the component is mounted to change state
	_isMounted = false;
	
	constructor(props: IProps) {
		super(props);
		this.state = {
			downloading: false,
			downloaded: false,
		};
	}

	private formatSize = (value: number) => {
		if (value == 0) return "";
		if (value < Math.pow(1024, 1)) {
            return value.toFixed() + ' B';
        } else if (value < Math.pow(1024, 2)) {
            return (value / Math.pow(1024, 1)).toFixed(1) + ' KiB';
        } else if (value < Math.pow(1024, 3)) {
            return (value / Math.pow(1024, 2)).toFixed(1) + ' MiB';
        } else if (value < Math.pow(1024, 4)) {
            return (value / Math.pow(1024, 3)).toFixed(1) + ' GiB';
        } else if (value < Math.pow(1024, 5)) {
            return (value / Math.pow(1024, 4)).toFixed(1) + ' TiB';
        } else {
            return (value / Math.pow(1024, 5)).toFixed(1) + ' PiB';
        }
	}

	private formatExtraInfo = () => {
		if (this.props.files.length == 0) return "";
		var lastModified = this.props.files.length > 1 || this.props.files[0].last_modified == undefined ? "" : new Date(this.props.files[0].last_modified).toLocaleTimeString();
		var size = this.formatSize(this.props.files.reduce((a, b) => { return { size: a.size + b.size } }, {size: 0}).size);
		if (lastModified == "" && size == "") return "";
		if (lastModified == "") return " (" + size + ")";
		if (size == "") return " (" + lastModified + ")";
		return " (" + size + ", " + lastModified + ")";
	}

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		const progress = Global.user.fileTracker.get(this.props.name);
        const download = progress.filter(x => x.type == 'download');
		return (
            <ListItem style={{paddingTop: "2px", paddingBottom: "2px"}}>
				{ this.state.downloaded ? (
					<IconButton
						edge="end"
						disabled
					>
						<DoneIcon />
					</IconButton>
				) : (
					<div>
						{download.length > 0 ? (
							<div style={{position: 'relative', height: '48px', width: '48px'}}>
							<CircularProgress />
							<span style={{position: 'absolute', top: '12.5px', left: '9px', fontSize: '0.75rem'}}>
								{((download[0].progress/download[0].total) * 100).toFixed(0) + "%"}
							</span>
						</div>
						) : (
							<IconButton
								edge="end"
								disabled={this.props.disabled}
								onClick={ () => {
										const withHashes = [];
										const withoutHashes = [];
										for (let file of this.props.files) {
											if (file.hash) {
												withHashes.push(file);
											} else {
												withoutHashes.push(file);
											}
										}
										if (withHashes.length > 0) Global.user.fileTracker.downloadFiles(this.props.name, withHashes, this.props.overwrite);
										if (withoutHashes.length > 0) Global.user.fileTracker.getNotebookOutputFiles(this.props.name, withoutHashes, this.props.workloadUUID, this.props.moduleUUID, this.props.overwrite);
										this.safeSetState({ downloading: true });
									}
								}
							>
								<GetAppIcon />
							</IconButton>
						)}
					</div>
				)}
                <div
					style={{
						overflow: 'auto',
						marginLeft: download.length > 0 ? '24px' : '12px',
						marginTop: '4px',
						marginBottom: '4px',
						opacity: this.props.disabled ? '0.5' : '1',
					}}>
					{ this.props.name + this.formatExtraInfo() }
				</div>
                    
            </ListItem>
		);
	}

	private update = () => {
		if (this._isMounted) {
			const progress = Global.user.fileTracker.get(this.props.name);
        	const download = progress.filter(x => x.type == 'download');
			if (this.state.downloading && download.length == 0) {
				this.safeSetState({ downloading: false, downloaded: true });
				setTimeout(() => this.safeSetState({ downloaded: false }) , 5000);
			}
			this.forceUpdate();
		}
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
		Global.user.fileTracker.getFilesChanged().connect(this.update)
		this.update();
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.user.fileTracker.getFilesChanged().disconnect(this.update)
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
