const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

// Session storage location
const SESSION_STORAGE_DIR = path.join(__dirname, '../../.github/copilot-sessions');
let lastSessionContent = null;

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  // Ensure session storage directory exists
  if (!fs.existsSync(SESSION_STORAGE_DIR)) {
    fs.mkdirSync(SESSION_STORAGE_DIR, { recursive: true });
  }

  // Save current Copilot session
  const saveCurrentSession = vscode.commands.registerCommand(
    'copilot-persistence.saveCurrentSession',
    async () => {
      try {
        // This is conceptual - actual API would depend on GitHub Copilot's extension API
        const copilotPanel = await vscode.commands.executeCommand('github.copilot.chat.getChatContent');

        if (copilotPanel && copilotPanel.content) {
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
          const sessionFile = path.join(SESSION_STORAGE_DIR, `copilot-session-${timestamp}.md`);

          fs.writeFileSync(sessionFile, copilotPanel.content);
          lastSessionContent = copilotPanel.content;

          vscode.window.showInformationMessage(`Copilot session saved to ${sessionFile}`);
        } else {
          vscode.window.showWarningMessage('No active Copilot session content found');
        }
      } catch (err) {
        vscode.window.showErrorMessage(`Failed to save Copilot session: ${err.message}`);
      }
    }
  );

  // Reopen last saved session
  const reopenLastSession = vscode.commands.registerCommand(
    'copilot-persistence.reopenLastSession',
    async () => {
      try {
        if (lastSessionContent) {
          // Re-open session with last saved content
          await vscode.commands.executeCommand('github.copilot.chat.restart', lastSessionContent);
          vscode.window.showInformationMessage('Last Copilot session restored');
        } else {
          // Find most recent session file
          const files = fs.readdirSync(SESSION_STORAGE_DIR)
            .filter(file => file.startsWith('copilot-session-'))
            .sort()
            .reverse();

          if (files.length > 0) {
            const mostRecentFile = path.join(SESSION_STORAGE_DIR, files[0]);
            lastSessionContent = fs.readFileSync(mostRecentFile, 'utf8');
            await vscode.commands.executeCommand('github.copilot.chat.restart', lastSessionContent);
            vscode.window.showInformationMessage('Most recent Copilot session restored');
          } else {
            vscode.window.showWarningMessage('No saved Copilot sessions found');
          }
        }
      } catch (err) {
        vscode.window.showErrorMessage(`Failed to restore Copilot session: ${err.message}`);
      }
    }
  );

  // Register session capture on editor changes to ensure nothing is lost
  const changeDocumentSubscription = vscode.workspace.onDidChangeTextDocument(event => {
    // Check if the document is a Copilot chat
    if (event.document.uri.scheme === 'github-copilot-chat') {
      // Store content to ensure persistence
      lastSessionContent = event.document.getText();
    }
  });

  context.subscriptions.push(
    saveCurrentSession,
    reopenLastSession,
    changeDocumentSubscription
  );
}

function deactivate() { }

module.exports = {
  activate,
  deactivate
};
