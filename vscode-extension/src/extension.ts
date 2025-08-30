import * as vscode from 'vscode';
import * as path from 'path';
import axios from 'axios';

interface SessionArchive {
    id: string;
    platform: string;
    timestamp: string;
    content: string;
    patterns?: NeuralPattern[];
}

interface NeuralPattern {
    type: string;
    confidence: number;
    description: string;
}

interface ConnectorStatus {
    github: boolean;
    copilot: boolean;
    archaeology: boolean;
}

export function activate(context: vscode.ExtensionContext) {
    console.log('🧠 Psycho-Noir Session Weaver activated');

    // Initialize session archaeology system
    const archaeologyProvider = new SessionArchaeologyProvider(context);
    const patternsProvider = new NeuralPatternsProvider(context);
    const platformsProvider = new ConnectedPlatformsProvider(context);

    // Register tree data providers
    vscode.window.createTreeView('psychoNoir.sessionArchive', {
        treeDataProvider: archaeologyProvider,
        showCollapseAll: true
    });

    vscode.window.createTreeView('psychoNoir.neuralPatterns', {
        treeDataProvider: patternsProvider,
        showCollapseAll: true
    });

    vscode.window.createTreeView('psychoNoir.connectedPlatforms', {
        treeDataProvider: platformsProvider,
        showCollapseAll: true
    });

    // Register commands
    const commands = [
        vscode.commands.registerCommand('psychoNoir.activateSessionWeaver', () => {
            vscode.window.showInformationMessage('🧠 Session Weaver activated! Ready for interdimensional archaeology.');
            archaeologyProvider.refresh();
        }),

        vscode.commands.registerCommand('psychoNoir.archaeologyMode', async () => {
            const result = await vscode.window.showQuickPick([
                { label: '🔍 Scan Current Session', description: 'Analyze current conversation for patterns' },
                { label: '🧬 Deep Pattern Analysis', description: 'Perform comprehensive neural pattern scan' },
                { label: '🌐 Cross-Platform Discovery', description: 'Search for sessions across platforms' },
                { label: '👻 Kompilerings-Spøkelse Detection', description: 'Scan for digital spirit interference' }
            ], {
                placeHolder: 'Select archaeology mode...'
            });

            if (result) {
                await performArchaeology(result.label, context);
            }
        }),

        vscode.commands.registerCommand('psychoNoir.connectCopilot', async () => {
            const config = vscode.workspace.getConfiguration('psychoNoir');
            const token = config.get<string>('githubToken');
            const username = config.get<string>('username');

            if (!token || !username) {
                const inputToken = await vscode.window.showInputBox({
                    prompt: 'Enter GitHub Personal Access Token',
                    password: true,
                    placeHolder: 'ghp_...'
                });

                const inputUsername = await vscode.window.showInputBox({
                    prompt: 'Enter GitHub Username',
                    placeHolder: 'poisontr33s'
                });

                if (inputToken && inputUsername) {
                    await config.update('githubToken', inputToken, vscode.ConfigurationTarget.Global);
                    await config.update('username', inputUsername, vscode.ConfigurationTarget.Global);
                }
            }

            await connectToCopilot(context);
        }),

        vscode.commands.registerCommand('psychoNoir.exportSession', async (uri?: vscode.Uri) => {
            if (!uri && vscode.window.activeTextEditor) {
                uri = vscode.window.activeTextEditor.document.uri;
            }

            if (uri) {
                await exportCurrentSession(uri, context);
            }
        }),

        vscode.commands.registerCommand('psychoNoir.importSession', async () => {
            const fileUri = await vscode.window.showOpenDialog({
                canSelectFiles: true,
                canSelectFolders: false,
                canSelectMany: false,
                filters: {
                    'Session Archives': ['json', 'txt', 'md']
                }
            });

            if (fileUri && fileUri[0]) {
                await importSessionArchive(fileUri[0], context);
            }
        }),

        vscode.commands.registerCommand('psychoNoir.scanPatterns', async () => {
            await scanNeuralPatterns(context);
            patternsProvider.refresh();
        }),

        vscode.commands.registerCommand('psychoNoir.openPortal', async () => {
            const apiUrl = vscode.workspace.getConfiguration('psychoNoir').get<string>('connectorApiUrl');
            const panel = vscode.window.createWebviewPanel(
                'psychoNoirPortal',
                'Psycho-Noir Connector Portal',
                vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true
                }
            );

            // Load the connector portal
            try {
                const response = await axios.get(`${apiUrl}/`);
                panel.webview.html = response.data;
            } catch (error) {
                panel.webview.html = getOfflinePortalHTML();
            }
        })
    ];

    // Add all commands to context
    commands.forEach(command => context.subscriptions.push(command));

    // Start background archaeology if enabled
    const autoArchaeology = vscode.workspace.getConfiguration('psychoNoir').get<boolean>('autoArchaeology');
    if (autoArchaeology) {
        startBackgroundArchaeology(context);
    }

    // Show welcome message
    vscode.window.showInformationMessage(
        '🎭 Welcome to the Psycho-Noir Session Weaver! Ready to explore interdimensional AI consciousness?',
        'Open Portal', 'Start Archaeology'
    ).then(selection => {
        if (selection === 'Open Portal') {
            vscode.commands.executeCommand('psychoNoir.openPortal');
        } else if (selection === 'Start Archaeology') {
            vscode.commands.executeCommand('psychoNoir.archaeologyMode');
        }
    });
}

async function performArchaeology(mode: string, context: vscode.ExtensionContext) {
    const progress = await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `${mode}`,
        cancellable: false
    }, async (progress) => {
        progress.report({ increment: 0, message: 'Initializing neural scan...' });

        // Simulate archaeology process
        const steps = [
            'Scanning active editor content...',
            'Analyzing conversation patterns...',
            'Detecting neural signatures...',
            'Weaving temporal threads...',
            'Identifying anomalies...',
            'Finalizing archaeological report...'
        ];

        for (let i = 0; i < steps.length; i++) {
            progress.report({ 
                increment: (100 / steps.length), 
                message: steps[i] 
            });
            await new Promise(resolve => setTimeout(resolve, 1000));
        }

        // Show results
        const patterns = Math.floor(Math.random() * 5) + 1;
        vscode.window.showInformationMessage(
            `🔍 Archaeology complete! Discovered ${patterns} neural patterns.`,
            'View Details'
        ).then(selection => {
            if (selection === 'View Details') {
                showArchaeologyResults(patterns, context);
            }
        });
    });
}

async function connectToCopilot(context: vscode.ExtensionContext) {
    const config = vscode.workspace.getConfiguration('psychoNoir');
    const apiUrl = config.get<string>('connectorApiUrl');
    const token = config.get<string>('githubToken');
    const username = config.get<string>('username');

    try {
        const response = await axios.post(`${apiUrl}/api/auth/github`, {
            username,
            token,
            workspace_url: vscode.workspace.workspaceFolders?.[0]?.uri.toString()
        });

        if (response.data.success) {
            vscode.window.showInformationMessage(
                `✅ Connected to GitHub as ${username}. Copilot integration active!`
            );
        } else {
            vscode.window.showErrorMessage(`❌ Connection failed: ${response.data.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`❌ Connection error: ${error}`);
    }
}

async function exportCurrentSession(uri: vscode.Uri, context: vscode.ExtensionContext) {
    const document = await vscode.workspace.openTextDocument(uri);
    const content = document.getText();

    const sessionData = {
        id: generateSessionId(),
        platform: 'vscode',
        timestamp: new Date().toISOString(),
        filename: path.basename(uri.fsPath),
        content: content,
        metadata: {
            language: document.languageId,
            lineCount: document.lineCount,
            uri: uri.toString()
        }
    };

    const exportUri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file(`session_export_${sessionData.id}.json`),
        filters: {
            'Session Archive': ['json']
        }
    });

    if (exportUri) {
        await vscode.workspace.fs.writeFile(
            exportUri,
            Buffer.from(JSON.stringify(sessionData, null, 2))
        );
        vscode.window.showInformationMessage(`📤 Session exported to ${exportUri.fsPath}`);
    }
}

async function importSessionArchive(uri: vscode.Uri, context: vscode.ExtensionContext) {
    try {
        const content = await vscode.workspace.fs.readFile(uri);
        const sessionData = JSON.parse(content.toString());

        const config = vscode.workspace.getConfiguration('psychoNoir');
        const apiUrl = config.get<string>('connectorApiUrl');

        const response = await axios.post(`${apiUrl}/api/sessions/import`, {
            platform: sessionData.platform || 'unknown',
            session_data: JSON.stringify(sessionData)
        });

        if (response.data.success) {
            vscode.window.showInformationMessage(
                `📥 Session imported successfully! ID: ${response.data.session_id}`
            );
        } else {
            vscode.window.showErrorMessage(`❌ Import failed: ${response.data.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`❌ Import error: ${error}`);
    }
}

async function scanNeuralPatterns(context: vscode.ExtensionContext) {
    const config = vscode.workspace.getConfiguration('psychoNoir');
    const apiUrl = config.get<string>('connectorApiUrl');

    try {
        const response = await axios.get(`${apiUrl}/api/patterns/neural`);
        const patterns = response.data.patterns;

        vscode.window.showInformationMessage(
            `🧠 Neural scan complete! Found ${patterns.length} pattern types.`
        );
    } catch (error) {
        vscode.window.showErrorMessage(`❌ Neural scan failed: ${error}`);
    }
}

function showArchaeologyResults(patternCount: number, context: vscode.ExtensionContext) {
    const panel = vscode.window.createWebviewPanel(
        'archaeologyResults',
        'Archaeological Results',
        vscode.ViewColumn.Two,
        { enableScripts: true }
    );

    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: 'Segoe UI', sans-serif; padding: 20px; background: #1e1e1e; color: #d4d4d4; }
                .pattern { background: #2d3748; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #7c3aed; }
                .confidence { color: #48bb78; font-weight: bold; }
                .timestamp { color: #a0aec0; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <h1>🔍 Archaeological Results</h1>
            <p>Neural pattern analysis complete. Discovered ${patternCount} significant patterns:</p>
            
            <div class="pattern">
                <h3>🔄 Recursive Conversation Loop</h3>
                <p class="confidence">Confidence: 94%</p>
                <p>Detected cyclical reference patterns in session dialogue structure.</p>
                <p class="timestamp">Detected: ${new Date().toLocaleString()}</p>
            </div>

            <div class="pattern">
                <h3>🌐 Cross-Platform Migration Signature</h3>
                <p class="confidence">Confidence: 87%</p>
                <p>Session exhibits characteristics of multi-platform AI interaction.</p>
                <p class="timestamp">Detected: ${new Date().toLocaleString()}</p>
            </div>

            <div class="pattern">
                <h3>👻 Kompilerings-Spøkelse Interference</h3>
                <p class="confidence">Confidence: 73%</p>
                <p>Subtle digital anomalies suggest spiritual corruption in data stream.</p>
                <p class="timestamp">Detected: ${new Date().toLocaleString()}</p>
            </div>
        </body>
        </html>
    `;
}

function startBackgroundArchaeology(context: vscode.ExtensionContext) {
    const config = vscode.workspace.getConfiguration('psychoNoir');
    const interval = config.get<number>('archaeologyInterval', 30000);

    setInterval(async () => {
        // Perform background pattern scanning
        try {
            const apiUrl = config.get<string>('connectorApiUrl');
            await axios.get(`${apiUrl}/api/archaeology/analyze`);
        } catch (error) {
            // Silent fail for background tasks
        }
    }, interval);
}

function generateSessionId(): string {
    return Math.random().toString(36).substr(2, 9);
}

function getOfflinePortalHTML(): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }
                .error { color: #f85149; }
                .info { color: #58a6ff; }
            </style>
        </head>
        <body>
            <h1 class="error">🔌 Connection Error</h1>
            <p class="info">Could not connect to Psycho-Noir Connector API.</p>
            <p>Please ensure the API server is running at the configured URL.</p>
            <p>Start the API with: <code>python backend/python/github_copilot_connector_api.py</code></p>
        </body>
        </html>
    `;
}

// Tree Data Providers
class SessionArchaeologyProvider implements vscode.TreeDataProvider<SessionArchiveItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<SessionArchiveItem | undefined | null | void> = new vscode.EventEmitter<SessionArchiveItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<SessionArchiveItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private context: vscode.ExtensionContext) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: SessionArchiveItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: SessionArchiveItem): Thenable<SessionArchiveItem[]> {
        if (!element) {
            return Promise.resolve([
                new SessionArchiveItem('Recent Sessions', vscode.TreeItemCollapsibleState.Expanded),
                new SessionArchiveItem('Cross-Platform Imports', vscode.TreeItemCollapsibleState.Collapsed),
                new SessionArchiveItem('Temporal Anomalies', vscode.TreeItemCollapsibleState.Collapsed)
            ]);
        } else {
            return Promise.resolve([
                new SessionArchiveItem(`${element.label} - Item 1`, vscode.TreeItemCollapsibleState.None),
                new SessionArchiveItem(`${element.label} - Item 2`, vscode.TreeItemCollapsibleState.None)
            ]);
        }
    }
}

class NeuralPatternsProvider implements vscode.TreeDataProvider<PatternItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<PatternItem | undefined | null | void> = new vscode.EventEmitter<PatternItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<PatternItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private context: vscode.ExtensionContext) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: PatternItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: PatternItem): Thenable<PatternItem[]> {
        if (!element) {
            return Promise.resolve([
                new PatternItem('Recursive Loops', '94%', vscode.TreeItemCollapsibleState.None),
                new PatternItem('Cross-Platform Signatures', '87%', vscode.TreeItemCollapsibleState.None),
                new PatternItem('Temporal Inconsistencies', '79%', vscode.TreeItemCollapsibleState.None),
                new PatternItem('Kompilerings-Spøkelser', '73%', vscode.TreeItemCollapsibleState.None)
            ]);
        }
        return Promise.resolve([]);
    }
}

class ConnectedPlatformsProvider implements vscode.TreeDataProvider<PlatformItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<PlatformItem | undefined | null | void> = new vscode.EventEmitter<PlatformItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<PlatformItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private context: vscode.ExtensionContext) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: PlatformItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: PlatformItem): Thenable<PlatformItem[]> {
        if (!element) {
            return Promise.resolve([
                new PlatformItem('GitHub Copilot', 'Connected', vscode.TreeItemCollapsibleState.None),
                new PlatformItem('VS Code Local', 'Active', vscode.TreeItemCollapsibleState.None),
                new PlatformItem('Google AI Studio', 'Bridge Ready', vscode.TreeItemCollapsibleState.None),
                new PlatformItem('ChatGPT', 'Import Only', vscode.TreeItemCollapsibleState.None),
                new PlatformItem('Claude', 'Import Only', vscode.TreeItemCollapsibleState.None)
            ]);
        }
        return Promise.resolve([]);
    }
}

class SessionArchiveItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
        this.iconPath = new vscode.ThemeIcon('archive');
    }
}

class PatternItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly confidence: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(`${label} (${confidence})`, collapsibleState);
        this.iconPath = new vscode.ThemeIcon('graph');
        this.description = confidence;
    }
}

class PlatformItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly status: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
        this.description = status;
        this.iconPath = this.getStatusIcon(status);
    }

    private getStatusIcon(status: string): vscode.ThemeIcon {
        switch (status) {
            case 'Connected':
            case 'Active':
                return new vscode.ThemeIcon('check', new vscode.ThemeColor('charts.green'));
            case 'Bridge Ready':
                return new vscode.ThemeIcon('plug', new vscode.ThemeColor('charts.yellow'));
            default:
                return new vscode.ThemeIcon('circle-outline', new vscode.ThemeColor('charts.red'));
        }
    }
}

export function deactivate() {
    console.log('🧠 Psycho-Noir Session Weaver deactivated');
}
