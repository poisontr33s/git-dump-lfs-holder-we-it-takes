"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const axios_1 = __importDefault(require("axios"));
function activate(context) {
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
            const token = config.get('githubToken');
            const username = config.get('username');
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
        vscode.commands.registerCommand('psychoNoir.exportSession', async (uri) => {
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
            const apiUrl = vscode.workspace.getConfiguration('psychoNoir').get('connectorApiUrl');
            const panel = vscode.window.createWebviewPanel('psychoNoirPortal', 'Psycho-Noir Connector Portal', vscode.ViewColumn.One, {
                enableScripts: true,
                retainContextWhenHidden: true
            });
            // Load the connector portal
            try {
                const response = await axios_1.default.get(`${apiUrl}/`);
                panel.webview.html = response.data;
            }
            catch (error) {
                panel.webview.html = getOfflinePortalHTML();
            }
        })
    ];
    // Add all commands to context
    commands.forEach(command => context.subscriptions.push(command));
    // Start background archaeology if enabled
    const autoArchaeology = vscode.workspace.getConfiguration('psychoNoir').get('autoArchaeology');
    if (autoArchaeology) {
        startBackgroundArchaeology(context);
    }
    // Show welcome message
    vscode.window.showInformationMessage('🎭 Welcome to the Psycho-Noir Session Weaver! Ready to explore interdimensional AI consciousness?', 'Open Portal', 'Start Archaeology').then(selection => {
        if (selection === 'Open Portal') {
            vscode.commands.executeCommand('psychoNoir.openPortal');
        }
        else if (selection === 'Start Archaeology') {
            vscode.commands.executeCommand('psychoNoir.archaeologyMode');
        }
    });
}
exports.activate = activate;
async function performArchaeology(mode, context) {
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
        vscode.window.showInformationMessage(`🔍 Archaeology complete! Discovered ${patterns} neural patterns.`, 'View Details').then(selection => {
            if (selection === 'View Details') {
                showArchaeologyResults(patterns, context);
            }
        });
    });
}
async function connectToCopilot(context) {
    const config = vscode.workspace.getConfiguration('psychoNoir');
    const apiUrl = config.get('connectorApiUrl');
    const token = config.get('githubToken');
    const username = config.get('username');
    try {
        const response = await axios_1.default.post(`${apiUrl}/api/auth/github`, {
            username,
            token,
            workspace_url: vscode.workspace.workspaceFolders?.[0]?.uri.toString()
        });
        if (response.data.success) {
            vscode.window.showInformationMessage(`✅ Connected to GitHub as ${username}. Copilot integration active!`);
        }
        else {
            vscode.window.showErrorMessage(`❌ Connection failed: ${response.data.error}`);
        }
    }
    catch (error) {
        vscode.window.showErrorMessage(`❌ Connection error: ${error}`);
    }
}
async function exportCurrentSession(uri, context) {
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
        await vscode.workspace.fs.writeFile(exportUri, Buffer.from(JSON.stringify(sessionData, null, 2)));
        vscode.window.showInformationMessage(`📤 Session exported to ${exportUri.fsPath}`);
    }
}
async function importSessionArchive(uri, context) {
    try {
        const content = await vscode.workspace.fs.readFile(uri);
        const sessionData = JSON.parse(content.toString());
        const config = vscode.workspace.getConfiguration('psychoNoir');
        const apiUrl = config.get('connectorApiUrl');
        const response = await axios_1.default.post(`${apiUrl}/api/sessions/import`, {
            platform: sessionData.platform || 'unknown',
            session_data: JSON.stringify(sessionData)
        });
        if (response.data.success) {
            vscode.window.showInformationMessage(`📥 Session imported successfully! ID: ${response.data.session_id}`);
        }
        else {
            vscode.window.showErrorMessage(`❌ Import failed: ${response.data.error}`);
        }
    }
    catch (error) {
        vscode.window.showErrorMessage(`❌ Import error: ${error}`);
    }
}
async function scanNeuralPatterns(context) {
    const config = vscode.workspace.getConfiguration('psychoNoir');
    const apiUrl = config.get('connectorApiUrl');
    try {
        const response = await axios_1.default.get(`${apiUrl}/api/patterns/neural`);
        const patterns = response.data.patterns;
        vscode.window.showInformationMessage(`🧠 Neural scan complete! Found ${patterns.length} pattern types.`);
    }
    catch (error) {
        vscode.window.showErrorMessage(`❌ Neural scan failed: ${error}`);
    }
}
function showArchaeologyResults(patternCount, context) {
    const panel = vscode.window.createWebviewPanel('archaeologyResults', 'Archaeological Results', vscode.ViewColumn.Two, { enableScripts: true });
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
function startBackgroundArchaeology(context) {
    const config = vscode.workspace.getConfiguration('psychoNoir');
    const interval = config.get('archaeologyInterval', 30000);
    setInterval(async () => {
        // Perform background pattern scanning
        try {
            const apiUrl = config.get('connectorApiUrl');
            await axios_1.default.get(`${apiUrl}/api/archaeology/analyze`);
        }
        catch (error) {
            // Silent fail for background tasks
        }
    }, interval);
}
function generateSessionId() {
    return Math.random().toString(36).substr(2, 9);
}
function getOfflinePortalHTML() {
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
class SessionArchaeologyProvider {
    context;
    _onDidChangeTreeData = new vscode.EventEmitter();
    onDidChangeTreeData = this._onDidChangeTreeData.event;
    constructor(context) {
        this.context = context;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (!element) {
            return Promise.resolve([
                new SessionArchiveItem('Recent Sessions', vscode.TreeItemCollapsibleState.Expanded),
                new SessionArchiveItem('Cross-Platform Imports', vscode.TreeItemCollapsibleState.Collapsed),
                new SessionArchiveItem('Temporal Anomalies', vscode.TreeItemCollapsibleState.Collapsed)
            ]);
        }
        else {
            return Promise.resolve([
                new SessionArchiveItem(`${element.label} - Item 1`, vscode.TreeItemCollapsibleState.None),
                new SessionArchiveItem(`${element.label} - Item 2`, vscode.TreeItemCollapsibleState.None)
            ]);
        }
    }
}
class NeuralPatternsProvider {
    context;
    _onDidChangeTreeData = new vscode.EventEmitter();
    onDidChangeTreeData = this._onDidChangeTreeData.event;
    constructor(context) {
        this.context = context;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
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
class ConnectedPlatformsProvider {
    context;
    _onDidChangeTreeData = new vscode.EventEmitter();
    onDidChangeTreeData = this._onDidChangeTreeData.event;
    constructor(context) {
        this.context = context;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
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
    label;
    collapsibleState;
    constructor(label, collapsibleState) {
        super(label, collapsibleState);
        this.label = label;
        this.collapsibleState = collapsibleState;
        this.iconPath = new vscode.ThemeIcon('archive');
    }
}
class PatternItem extends vscode.TreeItem {
    label;
    confidence;
    collapsibleState;
    constructor(label, confidence, collapsibleState) {
        super(`${label} (${confidence})`, collapsibleState);
        this.label = label;
        this.confidence = confidence;
        this.collapsibleState = collapsibleState;
        this.iconPath = new vscode.ThemeIcon('graph');
        this.description = confidence;
    }
}
class PlatformItem extends vscode.TreeItem {
    label;
    status;
    collapsibleState;
    constructor(label, status, collapsibleState) {
        super(label, collapsibleState);
        this.label = label;
        this.status = status;
        this.collapsibleState = collapsibleState;
        this.description = status;
        this.iconPath = this.getStatusIcon(status);
    }
    getStatusIcon(status) {
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
function deactivate() {
    console.log('🧠 Psycho-Noir Session Weaver deactivated');
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map
