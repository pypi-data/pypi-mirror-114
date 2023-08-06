/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { App } from '../../models/application/App';

import {
	IconButton,
} from '@material-ui/core';
import { FileMetadata } from './fileBrowser/FileBrowser';
import { FileTree } from '../FileTree';
import GetAppIcon from '@material-ui/icons/GetApp';
import moment from 'moment';

interface IProps {
	app: App;
}

// Properties for this component
interface IState {
	overwrite: boolean
}

export class OutputFileList extends React.Component<IProps, IState> {
	_isMounted = false;

	constructor(props: IProps) {
		super(props);
		this.state = {
			overwrite: false
		};
	}

	private sortFiles = (n1: FileMetadata,n2: FileMetadata) => {
		if (n1.path > n2.path) {
			return 1;
		}
		if (n1.path < n2.path) {
			return -1;
		}
		return 0;
	}

	private getFileHidableIcon = (file: FileMetadata) => {
		return {
			width: 36,
			height: 36,
			icon: (
				<IconButton
					onClick={() => this.downloadFile(file)}
					style={{ width: '36px', height: '36px', padding: '3px' }}
				>
					<GetAppIcon style={{ width: '30px', height: '30px', padding: '3px' }} />
				</IconButton>
			),
		}
	}

	private getFiles() {
		const inputFiles: FileMetadata[] = [];
		const outputFiles: FileMetadata[] = [];
		for (let module of this.props.app.modules) {
            if (module.files) {
                for (let file of module.files) {
                    outputFiles.push(file);
                }
            }
		}
		for (let file of this.props.app.files) {
			inputFiles.push(file);
		}
		var sortedInput: FileMetadata[] = inputFiles.sort(this.sortFiles);
		var sortedOutput: FileMetadata[] = outputFiles.sort(this.sortFiles);
		const log = { name: this.props.app.path.replace('.ipynb', '.log').replace(/^.*\/([^/]*)$/, '$1'), path: '~/' + this.props.app.path.replace('.ipynb', '.log'), size: 0 } as FileMetadata;
		return (
			<div>
				<div>
					<div style={{padding: '8px', fontWeight: 'bold'}}>
						Input files
					</div>
					{sortedInput.length == 0 ? (
						<div>
							No input files
						</div>
					) : (
						<FileTree<FileMetadata>
							files={sortedInput.slice(0, 50)}
							fileTitle={file => (
`Name: ${file.name}
${file.size === null ? '' : `Size: ${this.formatSize(file.size)}
`}${file.path === '' ? '' : `Path: ${file.path.replace(file.name, '').replace(/\/$/, '')}
`}Modified: ${moment(file.last_modified).format('YYYY-MM-DD hh:mm:ss')}`
							)}
							fileHidableIcon={this.getFileHidableIcon}
							directoryHidableIcon={path => ({
								width: 36,
								height: 36,
								icon: (
									<IconButton
										onClick={() => this.downloadDirectory(path, sortedInput)}
										style={{ width: '36px', height: '36px', padding: '3px' }}
									>
										<GetAppIcon style={{ width: '30px', height: '30px', padding: '3px' }} />
									</IconButton>
								),
							})}
						/>
					)}
					{sortedInput.length > 50 && (
						<div style={{paddingLeft: '64px'}}>
							... Not showing {sortedInput.length - 50} files ...
						</div>
					)}
				</div>
				<div>
					<div style={{padding: '8px', fontWeight: 'bold'}}>
						Output files
					</div>
					{sortedOutput.length == 0 ? (
						<div>
							No output files
						</div>
					) : (
						<FileTree<FileMetadata>
							files={[log].concat(sortedOutput).slice(0, 50)}
							fileTitle={file => (
`Name: ${file.name}
${file.size === null ? '' : `Size: ${this.formatSize(file.size)}
`}${file.path === '' ? '' : `Path: ${file.path.replace(file.name, '').replace(/\/$/, '')}
`}Modified: ${moment(file.last_modified).format('YYYY-MM-DD hh:mm:ss')}`
							)}
							fileHidableIcon={this.getFileHidableIcon}
							directoryHidableIcon={path => ({
								width: 36,
								height: 36,
								icon: (
									<IconButton
										onClick={() => this.downloadDirectory(path, [log].concat(sortedOutput))}
										style={{ width: '36px', height: '36px', padding: '3px' }}
									>
										<GetAppIcon style={{ width: '30px', height: '30px', padding: '3px' }} />
									</IconButton>
								),
							})}
						/>
					)}
					{sortedOutput.length > 50 && (
						<div style={{paddingLeft: '64px'}}>
							... Not showing {sortedOutput.length - 50} files ...
						</div>
					)}
				</div>
			</div>
		)
	}

	private downloadFile = (file: FileMetadata) => {
		if (file.hash) {
			Global.user.fileTracker.downloadFiles(file.path, [file], false);
		} else {
			Global.user.fileTracker.getNotebookOutputFiles(file.path, [file], this.props.app.uuid, this.props.app.modules[0].uuid, false);
		}
	}

	private downloadDirectory = (path: string, files: FileMetadata[]) => {
		const withHashes = [];
		const withoutHashes = [];
        for (let file of files) {
            if (file.path.startsWith(path)) {
                if (file.hash) {
					withHashes.push(file);
				} else {
					withoutHashes.push(file);
				}
            }
        }
		if (withHashes.length > 0) Global.user.fileTracker.downloadFiles(path, withHashes, false);
		if (withoutHashes.length > 0) Global.user.fileTracker.getNotebookOutputFiles(path, withoutHashes, this.props.app.uuid, this.props.app.modules[0].uuid, false);
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

	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
			<div style={{padding: '12px', width: "100%"}}>
				{this.getFiles()}
			</div>
		);
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		this._isMounted = false;
	}

	// private safeSetState = (map: any) => {
	// 	if (this._isMounted) {
	// 		let update = false
	// 		try {
	// 			for (const key of Object.keys(map)) {
	// 				if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
	// 					update = true
	// 					break
	// 				}
	// 			}
	// 		} catch (error) {
	// 			update = true
	// 		}
	// 		if (update) {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
	// 			this.setState(map)
	// 		} else {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
	// 		}
	// 	}
	// }

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
