/**
 * 🎭 UNIVERSAL SESSION DETECTOR
 * Pure JavaScript - fungerer i VS Code terminal på ALLE platformer
 * Windows 11, Mac, Linux - ingen dependencies!
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

class UniversalSessionDetector {
    constructor() {
        this.workspaceRoot = process.cwd();
        this.sessionIdentityFile = path.join(this.workspaceRoot, '.session-identity.json');
        this.copilotBridgeDir = path.join(this.workspaceRoot, '.copilot-bridge');
    }

    detectEnvironment() {
        return {
            platform: os.platform(),
            arch: os.arch(),
            hostname: os.hostname(),
            username: os.userInfo().username,
            isCodespaces: process.env.CODESPACES === 'true',
            isRemote: !!process.env.VSCODE_REMOTE_USER,
            nodeVersion: process.version,
            workspaceRoot: this.workspaceRoot
        };
    }

    findExistingSessions() {
        if (!fs.existsSync(this.copilotBridgeDir)) {
            return [];
        }

        const sessions = [];
        
        try {
            const files = fs.readdirSync(this.copilotBridgeDir);
            
            for (const file of files) {
                if (file.startsWith('session_export_') && file.endsWith('.json')) {
                    const filePath = path.join(this.copilotBridgeDir, file);
                    
                    try {
                        const sessionData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
                        const conversationCount = sessionData.conversations?.length || 0;
                        
                        if (conversationCount > 5) {
                            sessions.push({
                                file: file,
                                filePath: filePath,
                                conversations: conversationCount,
                                environment: sessionData.environment || 'unknown',
                                exportTime: sessionData.export_time || 'unknown',
                                size: Math.round(fs.statSync(filePath).size / 1024) + 'KB'
                            });
                        }
                    } catch (error) {
                        // Skip invalid files
                    }
                }
            }
        } catch (error) {
            console.log('🎭 Could not scan bridge directory');
        }

        // Sort by modification time (newest first)
        sessions.sort((a, b) => {
            try {
                const aTime = fs.statSync(a.filePath).mtime;
                const bTime = fs.statSync(b.filePath).mtime;
                return bTime - aTime;
            } catch {
                return 0;
            }
        });

        return sessions;
    }

    showSessionOptions() {
        const env = this.detectEnvironment();
        const sessions = this.findExistingSessions();

        console.log('\n🎭 PSYCHO-NOIR UNIVERSAL SESSION DETECTOR');
        console.log('='.repeat(50));
        console.log(`📍 Platform: ${env.platform} (${env.arch})`);
        console.log(`🖥️  Host: ${env.hostname}`);
        console.log(`👤 User: ${env.username}`);
        console.log(`🌐 Environment: ${env.isCodespaces ? 'Codespaces' : env.isRemote ? 'Remote' : 'Local'}`);
        console.log(`📁 Workspace: ${this.workspaceRoot}`);

        if (sessions.length === 0) {
            console.log('\n✨ No existing sessions found. Starting fresh!');
            this.createSessionIdentity(env, null);
            return;
        }

        console.log(`\n🔍 FOUND ${sessions.length} EXISTING SESSION(S):`);
        console.log('-'.repeat(60));

        sessions.forEach((session, index) => {
            console.log(`${index + 1}. 💬 ${session.conversations} conversations (${session.size})`);
            console.log(`   📅 Exported: ${session.exportTime}`);
            console.log(`   🌐 From: ${session.environment}`);
            console.log(`   📄 File: ${session.file}`);
            console.log('');
        });

        // Show available actions
        console.log('🎯 AVAILABLE ACTIONS:');
        console.log('   • Use VS Code Command Palette (Ctrl+Shift+P)');
        console.log('   • Run: "🎭 Check Session Continuity"');
        console.log('   • Or run: "🎭 Import Session"');
        console.log('');
        console.log('💡 TO CONTINUE AN EXISTING SESSION:');
        console.log('   1. Open GitHub Copilot Chat (Ctrl+Shift+I)');
        console.log('   2. Say: "Continue our previous work on [topic]"');
        console.log('   3. Reference specific features you were working on');
        console.log('');
        console.log('🎭 Den Usynlige Hånd: SESSION_DETECTION_COMPLETE!');
    }

    createSessionIdentity(env, importedSession) {
        const identity = {
            machineId: `${env.hostname}-${env.username}`,
            environmentType: env.isCodespaces ? 'codespaces' : env.isRemote ? 'remote' : 'local',
            platform: env.platform,
            sessionStartTime: new Date().toISOString(),
            workspacePath: this.workspaceRoot,
            detectorVersion: '1.0.0',
            importedFrom: importedSession
        };

        fs.writeFileSync(this.sessionIdentityFile, JSON.stringify(identity, null, 2));
        console.log('✅ Session identity created!');
    }

    // Quick Windows batch file generator
    generateWindowsShortcut() {
        if (os.platform() === 'win32') {
            const batchContent = `@echo off
echo 🎭 PSYCHO-NOIR SESSION DETECTOR
echo Running universal session check...
node "${__filename}"
pause`;

            fs.writeFileSync(path.join(this.workspaceRoot, 'check-sessions.bat'), batchContent);
            console.log('📁 Created check-sessions.bat for Windows!');
        }
    }
}

// Auto-run if called directly
if (require.main === module) {
    const detector = new UniversalSessionDetector();
    detector.showSessionOptions();
    detector.generateWindowsShortcut();
}

module.exports = UniversalSessionDetector;
