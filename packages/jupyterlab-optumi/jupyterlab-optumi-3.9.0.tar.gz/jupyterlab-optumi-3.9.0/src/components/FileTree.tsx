import * as React from 'react'
import { Global } from '../Global';
import { TreeView, TreeItem } from '@material-ui/lab'
import { ChevronRight, ExpandMore } from '@material-ui/icons';
import { withStyles } from '@material-ui/core';
import FileExtensionIcon from './FileExtensionIcon';

type TreeNode<FileMetadata> = DirectoryNode<FileMetadata> | FileNode<FileMetadata>

interface MinimumFileMetadata {
    path: string
}

interface DirectoryNode<FileMetadata> {
    path: string
    file: string
    children: TreeNode<FileMetadata>[]
    metadata: undefined
}

interface FileNode<FileMetadata> {
    path: string
    file: string
    metadata: FileMetadata
    children: undefined
}

interface HidableIcon {
    icon: JSX.Element
    width: number
    height: number
}

interface IProps<FileMetadata> {
    files: FileMetadata[]
    fileHidableIcon?: (file: FileMetadata) => HidableIcon
    directoryHidableIcon?: (path: string) => HidableIcon
    fileTitle?: (file: FileMetadata) => string
    directoryTitle?: (path: string) => string
}

interface IState {
    expanded: string[]
}

export class FileTree<FileMetadata extends MinimumFileMetadata> extends React.Component<IProps<FileMetadata>, IState> {

    constructor(props: IProps<FileMetadata>) {
        super(props);
        
        this.state = {
            expanded: [],
        }
    }

    private renderTreeItems = (files: FileMetadata[]): JSX.Element[] | undefined => {

        const generateTreeStructure = (): TreeNode<FileMetadata> => {

            const generatePathStructure = (metadata: FileMetadata, path: string, file: string): TreeNode<FileMetadata> => {
                let parts = file.split(/(?<=^\/?[^\/]+)(?=\/)/)
                if (parts.length > 1) {
                    return {
                        path: path,
                        file: parts[0],
                        children: [generatePathStructure(metadata, path + parts[0], parts[1])]
                    } as DirectoryNode<FileMetadata>
                } else {
                    return {path, file, metadata} as FileNode<FileMetadata>
                }
            }

            const mergePathStructure = (treeStructure: TreeNode<FileMetadata>, pathStructure: TreeNode<FileMetadata>): TreeNode<FileMetadata> => {
                if (treeStructure.children === undefined) {
                    treeStructure.children = [pathStructure]
                    return treeStructure
                } else if (pathStructure.children === undefined) {
                    treeStructure.children.push(pathStructure)
                    return treeStructure
                } else {
                    for (let i = 0; i < treeStructure.children.length; i++) {
                        let child = treeStructure.children[i]
                        if (child.file === pathStructure.file) {
                            treeStructure.children[i] = mergePathStructure(child, pathStructure.children[0])
                            return treeStructure
                        }
                    }
                    treeStructure.children.push(pathStructure)
                    return treeStructure
                }
            }

            let treeStructure: TreeNode<FileMetadata> = {path: '', file: '', children: []} as DirectoryNode<FileMetadata>
            for (let file of files) {
                let pathStructure = generatePathStructure(file, '', file.path)
                treeStructure = mergePathStructure(treeStructure, pathStructure)
            }
            return treeStructure
        }

        const collapseTreeStructure = (structure: TreeNode<FileMetadata>): TreeNode<FileMetadata> => {
            if (structure.children === undefined) {
                return structure                
            } else if (structure.children.length === 1) {
                let child = structure.children[0]
                structure.file += child.file
                structure.metadata = child.metadata
                structure.children = child.children
                return collapseTreeStructure(structure)
            } else {
                for (let i = 0; i < structure.children.length; i++) {
                    structure.children[i] = collapseTreeStructure(structure.children[i])
                }
                return structure
            }
        }

        const renderTreeStructure = (structure: TreeNode<FileMetadata>, includeSlash: boolean): JSX.Element => {
            let hasChildren = Array.isArray(structure.children)
            let cappedMessage
            const maxChildren = 50
            if (hasChildren && structure.children.length > maxChildren) {
                cappedMessage = (
                    <TreeItem
                        endIcon={<></>}
                        key={structure.path + structure.file + 'toomany'}
                        nodeId={structure.path + structure.file + 'toomany'}
                        label={(
                            <div style={{
                                flexGrow: 1,
                                fontSize: 'var(--jp-ui-font-size1)',
                                fontFamily: 'var(--jp-ui-font-family)',
                                overflowX: 'hidden',
                                whiteSpace: 'nowrap',
                                textOverflow: 'ellipsis',
                            }}>
                                Too many files, hiding remaining {structure.children.length - maxChildren}
                            </div>
                        )}
                    />
                )
            }
            return (
                <FileTreeItem
                    structure={structure}
                    includeSlash={includeSlash}
                    title={hasChildren ? (
                        this.props.directoryTitle && this.props.directoryTitle(structure.path + structure.file)
                    ) : (
                        this.props.fileTitle && this.props.fileTitle(structure.metadata)
                    )}
                    hidableIcon={hasChildren ? (
                        this.props.directoryHidableIcon ? this.props.directoryHidableIcon(structure.path + structure.file) : undefined
                    ) : (
                        this.props.fileHidableIcon ? this.props.fileHidableIcon(structure.metadata) : undefined
                    )}
                >
                    {hasChildren ? (
                        <>
                            {structure.children.splice(0, maxChildren).map((child: TreeNode<FileMetadata>) => renderTreeStructure(child, false))}
                            {cappedMessage}
                        </>
                    ) : undefined}
                </FileTreeItem>
            )
        }

        let structure: TreeNode<FileMetadata> = generateTreeStructure()
        return Array.isArray(structure.children) ? (
            structure.children.map((child: TreeNode<FileMetadata>) => renderTreeStructure(collapseTreeStructure(child), true))
        ) : undefined
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <TreeView
                disableSelection
                defaultCollapseIcon={<ExpandMore />}
                defaultExpandIcon={<ChevronRight />}
                expanded={this.state.expanded}
                onNodeToggle={(event: React.ChangeEvent<{}>, nodeIds: string[]) => {
                    this.setState({ expanded: nodeIds })
                }}
            >
                {this.renderTreeItems(this.props.files)}
            </TreeView>
        )
    }

    public shouldComponentUpdate = (nextProps: IProps<FileMetadata>, nextState: IState): boolean => {
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

interface ItemProps<FileMetadata> {
    structure: TreeNode<FileMetadata>
    includeSlash: boolean
    title?: string
    hidableIcon?: HidableIcon
    children?: undefined | JSX.Element | JSX.Element[]
}

interface ItemState {
    hovered: boolean
}

export class FileTreeItem<FileMetadata extends MinimumFileMetadata> extends React.Component<ItemProps<FileMetadata>, ItemState> {
    private _isMounted = false
    private StyledTreeItem: any

    constructor(props: ItemProps<FileMetadata>) {
        super(props)

        this.StyledTreeItem = withStyles({
            '@global': {
                '.hovered > .MuiTreeItem-root > .MuiTreeItem-content': {
                    width: 'calc(100% - ' + (props.hidableIcon ? props.hidableIcon.width : 0) + 'px)',
                    transitionDuration: '300ms',
                }
            },
            root: {
                width: '100%',
                transitionDuration: '300ms',
            },
            label: {
                display: 'flex',
                width: 'calc(100% - 19px)',
                alignItems: 'center',
            }
        })(TreeItem)

        this.state = {
            hovered: false,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const structure = this.props.structure
        const hidableIcon = this.props.hidableIcon
        return (
            <div
                key={structure.path + structure.file}
                className={this.state.hovered ? 'hovered' : undefined}
                style={{display: 'flex', width: '100%', position: 'relative'}}
            >
                {hidableIcon && (
                    <div
                        style={{position: 'absolute', right: '0px'}}
                        onMouseOver={() => this.safeSetState({hovered: true})}
                        onMouseOut={() => this.safeSetState({hovered: false})}
                    >
                        <div style={{display: 'inline-flex', position: 'absolute', right: '0px'}}>
                            {hidableIcon.icon}
                        </div>
                        <div style={{
                            position: 'absolute',
                            right: this.state.hovered ? hidableIcon.width + 'px' : '0px',
                            width: this.state.hovered ? '0px' : hidableIcon.width + 'px',
                            height: hidableIcon.height,
                            backgroundColor: 'var(--jp-layout-color1)',
                            transitionDuration: '300ms',
                        }} />
                    </div>
                )}
                <this.StyledTreeItem
                    nodeId={structure.path + structure.file}
                    endIcon={<FileExtensionIcon path={structure.file}/>}
                    label={(
                        <div
                            onMouseOver={() => this.safeSetState({hovered: true})}
                            onMouseOut={() => this.safeSetState({hovered: false})}
                            title={this.props.title}
                            style={{
                                flexGrow: 1,
                                fontSize: 'var(--jp-ui-font-size1)',
                                fontFamily: 'var(--jp-ui-font-family)',
                                overflowX: 'hidden',
                                whiteSpace: 'nowrap',
                                textOverflow: 'ellipsis',
                                height: hidableIcon && hidableIcon.height + 'px',
                                lineHeight: hidableIcon && hidableIcon.height + 'px',
                            }}
                        >
                            {structure.file.replace(this.props.includeSlash ? '' : /^\//, '') /*+ (hasChildren ? '/' : '')*/}
                        </div>
                    )}
                >
                    {this.props.children}
                </this.StyledTreeItem>
            </div>
        )
    }
    
    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
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

    public shouldComponentUpdate = (nextProps: ItemProps<FileMetadata>, nextState: ItemState): boolean => {
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
