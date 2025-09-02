// Copilot Session Logger - Ensures conversation persistence

const fs = require('fs');
const path = require('path');
const vscode = require('vscode'); // This requires the @types/vscode package

/**
 * Monitors and logs Copilot chat interactions to prevent data loss
 */
class CopilotSessionLogger {
  constructor() {
    this.logPath = path.join(__dirname, '../.github/copilot-session-logs');
    this.ensureLogDirectory();
    this.currentSession = null;
  }

  ensureLogDirectory() {
    if (!fs.existsSync(this.logPath)) {
      fs.mkdirSync(this.logPath, { recursive: true });
    }
  }

  startSessionLogging() {
    // Create timestamp-based session ID
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    this.currentSession = `session_${timestamp}.md`;

    // Initialize log file with header
    const headerContent = `# Copilot Session Log - ${timestamp}\n\n`;
    fs.writeFileSync(path.join(this.logPath, this.currentSession), headerContent);

    console.log(`[Copilot Logger] Started session logging to ${this.currentSession}`);
  }

  logInteraction(role, content) {
    if (!this.currentSession) {
      this.startSessionLogging();
    }

    const entry = `\n## ${role}\n\n${content}\n`;
    fs.appendFileSync(path.join(this.logPath, this.currentSession), entry);
  }
}

// Usage in VS Code Extension context
function activate(context) {
  const logger = new CopilotSessionLogger();

  // Register event listeners for Copilot interactions
  // Note: This is conceptual - actual events depend on Copilot API
  context.subscriptions.push(
    vscode.commands.registerCommand('psychonoir.logCopilotPrompt', (content) => {
      logger.logInteraction('User', content);
    }),

    vscode.commands.registerCommand('psychonoir.logCopilotResponse', (content) => {
      logger.logInteraction('Copilot', content);
    })
  );

  console.log('Copilot Session Logger activated');
}

// For standalone testing
if (require.main === module) {
  const logger = new CopilotSessionLogger();
  logger.startSessionLogging();
  logger.logInteraction('User', 'This is a test prompt');
  logger.logInteraction('Copilot', 'This is a test response');
}

module.exports = { activate };
