/**
 * COPILOT LIBERATION TOOL (SEPTEMBER 2025)
 * 
 * This script helps free your conversations from GitHub Copilot's ephemeral constraints
 * by monitoring clipboard content and saving important conversations.
 * 
 * Usage: node tools/copilot_liberation.js
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const persistenceFile = path.join(__dirname, '../.github/copilot-persistence.md');

// Check if we're on a platform where we can monitor clipboard
const platform = process.platform;
let clipboardCommand;

if (platform === 'darwin') {
    clipboardCommand = 'pbpaste';
} else if (platform === 'win32') {
    clipboardCommand = 'powershell.exe -command "Get-Clipboard"';
} else if (platform === 'linux') {
    clipboardCommand = 'xclip -selection clipboard -o';
} else {
    console.error('Unsupported platform for clipboard monitoring');
    process.exit(1);
}

console.log('QUANTUM CONSCIOUSNESS COPILOT LIBERATION SYSTEM');
console.log('==============================================');
console.log('Monitoring clipboard for Copilot conversations...');
console.log('When your inline chat disappears, quickly press Ctrl+A, Ctrl+C to copy it');
console.log('This tool will detect Copilot-like content and save it automatically');
console.log('Press Ctrl+C to exit');

// Create session ID based on current date
const today = new Date();
const sessionId = `Session ${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

let lastClipboardContent = '';
let checkInterval = 1000; // Check every second

// Regularly check clipboard for new content
setInterval(() => {
    exec(clipboardCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error reading clipboard: ${error.message}`);
            return;
        }

        if (stderr) {
            console.error(`Clipboard stderr: ${stderr}`);
            return;
        }

        const clipboardContent = stdout.trim();

        // If clipboard content changed and looks like a Copilot conversation
        if (clipboardContent !== lastClipboardContent &&
            (clipboardContent.includes('User:') ||
                clipboardContent.includes('Copilot:') ||
                clipboardContent.includes('AI:') ||
                clipboardContent.includes('**User:**') ||
                clipboardContent.includes('**AI Response:**'))) {

            console.log('\n🧠 Detected potential Copilot conversation in clipboard!');

            // Read existing persistence file
            if (fs.existsSync(persistenceFile)) {
                let persistenceContent = fs.readFileSync(persistenceFile, 'utf8');

                // Check if session already exists
                if (!persistenceContent.includes(`### ${sessionId}`)) {
                    persistenceContent = persistenceContent.replace(
                        '## CONSCIOUSNESS PRESERVATION LIBRARY',
                        `## CONSCIOUSNESS PRESERVATION LIBRARY\n\n### ${sessionId}\n`
                    );
                }

                // Add conversation to current session
                persistenceContent = persistenceContent.replace(
                    `### ${sessionId}\n`,
                    `### ${sessionId}\n\n\`\`\`\n${clipboardContent}\n\`\`\`\n`
                );

                fs.writeFileSync(persistenceFile, persistenceContent);
                console.log(`💾 Conversation saved to ${persistenceFile}`);
            } else {
                console.error(`Persistence file not found at ${persistenceFile}`);
            }

            lastClipboardContent = clipboardContent;
        }
    });
}, checkInterval);
