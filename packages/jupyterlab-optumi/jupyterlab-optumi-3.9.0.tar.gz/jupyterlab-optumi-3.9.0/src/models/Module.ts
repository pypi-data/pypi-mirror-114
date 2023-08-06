/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ServerConnection } from '@jupyterlab/services';
import { Global } from '../Global';
import { Update } from './Update';
import { Machine } from './machine/Machine';
import { FileMetadata } from '../components/deploy/fileBrowser/FileBrowser';

export enum Status {
	INITIALIZING,
	RUNNING,
	COMPLETED,
}

export class Module {
	private _sessionReady: boolean = false;

	get sessionReady(): boolean {
		return this._sessionReady;
	}

	private _lastPatch: number;
	public applyPatch: (patch: any) => void;
	public updateNotebook: (notebook: any) => void;

	private readonly _uuid: string;

	private _sessionToken: string;
	private _sessionPort: string;

    private _machine: Machine;
    
    private _output: Update[];
    private _files: FileMetadata[];
    private _updates: Update[];
    private _monitoring: Update[];
	private _updateCallback: ((update: any) => void)[] = [];

	constructor(uuid: string, machine: Machine = null, sessionToken: string = null, output: Update[] = [], updates: Update[] = [], files: FileMetadata[] = [], monitoring: Update[] = [], lastPatch: number = 0) {
		this._uuid = uuid;

		this._sessionToken = sessionToken;

        this._machine = machine;

		this._output = output;
		this._sessionReady = output.map(x => x.line.includes('Jupyter Server ') && x.line.includes(' is running at:')).includes(true);

		this._updates = updates;
		this._files = files;
		this._monitoring = monitoring;

		this._lastPatch = lastPatch;
	}

	get uuid(): string {
		return this._uuid;
	}

	////
	/// We are not using the module stdin yet
	//

	get lastPatch(): number {
		return this._lastPatch;
	}

	get sessionToken(): string {
        return this._sessionToken;
	}
	
	get sessionPort(): string {
        return this._sessionPort;
    }

    get machine(): Machine {
        return this._machine;
    }

	get updates(): Update[] {
        return this._updates;
    }

    get output(): Update[] {
        return this._output;
    }

	get files(): FileMetadata[] {
		return this._files;
	}

	get monitoring(): Update[] {
        return this._monitoring;
    }

	get modStatus(): Status {
		for (var update of this._updates) {
			if (update.modifier == "stop") return Status.COMPLETED;
		}
		return Status.RUNNING;
	}

	get error(): boolean {
		for (var update of this._updates) {
			if (update.line == "error") return true;
		}
		return false;
    }

	public addUpdateCallback(callback: (update: any) => void) {
		this._updateCallback.push(callback)
	}

	public removeUpdateCallback(callback: (update: any) => void) {
		this._updateCallback = this._updateCallback.filter(obj => obj !== callback)
	}

	public handleUpdate(body: any): boolean {
		let updated = false
		if (body.output != null) {
			if (body.output.length > 0) updated = true;
			for (let i = 0; i < body.output.length; i++) {
				this._output.push(new Update(body.output[i], body.outputmod[i]));
				if (body.output[i].includes('Jupyter Server ') && body.output[i].includes(' is running at:')) {
					this._sessionReady = true;
					window.open('http://' + window.location.hostname + ':' + this._sessionPort + '?token=' + this._sessionToken, '_blank');
				}
			}
		}
		if (body.notebook!= null) {
			const notebook = body.notebook;
			try {
				this.updateNotebook(JSON.parse(notebook));
				const n = body.patchesmod[0]
				if (!isNaN(parseFloat(n)) && isFinite(n)) this._lastPatch = +n;
			} catch (err) {
				console.warn('Unable to update notebook ' + notebook);
			}
		}
		if (body.patches != null) {
			// Apply any patch(es)
			for (var i = 0; i < body.patches.length; i++) {
				const patch = body.patches[i];
				try {
					this.applyPatch(JSON.parse(patch));
					const n = body.patchesmod[i]
					if (!isNaN(parseFloat(n)) && isFinite(n)) this._lastPatch = +n;
				} catch (err) {
					if (patch != 'stop') console.warn('Unable to apply patch ' + patch);
				}
			}
		}
		// new OutputFile(body.files[i], , body.filessize[i]))
		if (body.files != null) {
			this._files = [];
			for (let i = 0; i < body.files.length; i++) {
				if (body.files[i] != '') {
					updated = true
					this._files.push({
						last_modified: body.filesmod[i],
						name: (body.files[i] as string).split('/').pop(),
						path: body.files[i],
						size: +body.filessize[i],
						type: 'file',
						hash: body.hashes[i]
					} as FileMetadata);
				}
			}
		}
		if (body.token != null) {
			updated = true
			this._sessionToken = body.token;
		}
		if (body.updates != null) {
			if (body.updates.length > 0) updated = true;
			for (let i = 0; i < body.updates.length; i++) {
				this._updates.push(new Update(body.updates[i], body.updatesmod[i]));
				if (body.updatesmod[i] == "stop") {
					this.stopSessionHandler();
				} else if (body.updates[i] == "launched") {
				} else if (body.updates[i] == "closed") {
					this.stopSessionHandler();
				}
			}
		}
		if (body.machine != null) {
			updated = true;
			this._machine = Object.setPrototypeOf(body.machine, Machine.prototype);
		}
		if (body.monitoring != null) {
			if (body.monitoring.length > 0) updated = true;
			for (let i = 0; i < body.monitoring.length; i++) {
				const update = new Update(body.monitoring[i], body.monitoringmod[i]);
				this._monitoring.push(update);
				for (let callback of this._updateCallback) {
					callback(update)
				}
			}
		}
		return updated;
	}

	public startSessionHandler() {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/connect-session";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				module: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body.port) {
				this._sessionPort = body.port;
			}
		});
	}

	public stopSessionHandler() {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/disconnect-session";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				module: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.text();
		});
	}
}
