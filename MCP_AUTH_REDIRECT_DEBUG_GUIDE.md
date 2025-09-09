# 🔐 MCP / GitHub Auth Redirect Failure Forensics Ritual

You are facing a recurring **404 redirect / partial auth** issue when launching the GitHub MCP server (or other MCP-backed extensions) inside a remote / devcontainer VS Code context. This guide captures *exactly where to look*, *how to raise log verbosity*, and *what artifacts to collect* so we can surgically neutralize the failure.

---
## 1. Core Symptom Profile
| Symptom | Interpretation |
|---------|---------------|
| External browser (or internal handler) opens → 404 | Callback target unreachable (remote container boundary) OR stale OAuth state. |
| Red error badge next to MCP server in Extensions → Servers | Handshake registered but capability init partially failed (often auth mismatch). |
| MCP tools partly work (read ops) but UI shows error | Cached token used; refresh or scope revalidation failed. |
| Repeats every session | Persisted broken token / duplicate server registration / stale global storage. |

---
## 2. High-Yield Log Sources (In-IDE)
Open these in sequence *immediately after reproducing the redirect failure*.

1. Output Panel (View → Output) → Select channels:
   - `Model Context Protocol`
   - `GitHub` (sometimes `GitHub Authentication` depending on extension version)
   - `Log (Extension Host)`
   - `Log (Window)`
2. Developer Console:
   - Command Palette: `Developer: Toggle Developer Tools` → Console tab
   - Filter terms: `oauth`, `mcp`, `401`, `403`, `404`, `redirect`, `device`, `authorize`
3. Authentication Sessions:
   - Command Palette: `Developer: Show Authentication Sessions`
   - Look for multiple GitHub entries or expired scopes.

---
## 3. On-Disk Log Directories
VS Code keeps rotating timestamped logs.

**Linux (Codespaces / Devcontainer base):**
```
~/.config/Code/logs/<YYYYMMDDTHHMMSS>/
```
Key subfolders:
- `renderer1/` → window logs
- `sharedprocess/` → auth + IPC intermediation
- `exthost1/` → extension host logs

Fast triage command examples (run in container shell):
```
find ~/.config/Code/logs -maxdepth 2 -type f -name '*.log' -newerct '1 hour ago'
 tail -n 120 ~/.config/Code/logs/*/exthost*/output_logging_*.log | grep -i github
 tail -n 80 ~/.config/Code/logs/*/sharedprocess.log | grep -Ei 'oauth|device|redirect'
```

Or open the folder via VS Code command:
- Command Palette: `Developer: Open Logs Folder`

---
## 4. Elevate Verbosity
Add (or temporarily inject) into **User Settings (JSON)**:
```jsonc
{
  // Increase MCP handshake logging (if supported by extension)
  "mcp.trace.server": "verbose",
  // Extension host / general logs already pick up auth, but enabling telemetry debug can help
  "github.logging.level": "debug" // (Some versions honor this key)
}
```
Then: `Developer: Reload Window`.

---
## 5. Reproduction Ritual (Deterministic)
1. Ensure **only one** MCP GitHub server definition exists (avoid duplicate names):
   - Search settings JSON for `"mcp.servers"`.
2. Sign out completely:
   - Accounts menu (lower-left) → Sign Out of GitHub
   - Command Palette: `Developer: Show Authentication Sessions` → Remove any GitHub sessions.
3. Reload window.
4. Start GitHub MCP server (Extensions pane → MCP Servers → Start).
5. Let the redirect fail (observe 404).
6. Immediately capture logs (Section 2 & 3).
7. Run presence probe inside repo (already available):
   ```bash
   bun run unified_mcp_consciousness_orchestrator.ts --call env_secret_presence_probe '{}'
   ```
8. (Optional) Run our internal GitHub meta call to prove external path still works:
   ```bash
   bun run unified_mcp_consciousness_orchestrator.ts --call github_repo_meta '{"owner":"oven-sh","repo":"bun"}'
   ```

---
## 6. Common Failure Archetypes & Signatures
| Log Snippet | Likely Root Cause | Fix Path |
|-------------|------------------|----------|
| `redirect_uri_mismatch` | Extension expects local callback not exposed in container | Use device code flow or PAT; remove broken oauth client config |
| `401 unauthorized` + immediate retry loop | Expired token in keytar/global storage | Clear auth sessions + global storage; re-init device flow |
| `EADDRINUSE` or duplicate server name in MCP logs | Two servers same `name` field | Remove older server entry / rename |
| `net::ERR_CONNECTION_REFUSED` hitting callback URL | Local callback port blocked / not forwarded | Force device code auth |
| Silent (only red badge) | Internal promise rejection suppressed | Increase trace level, restart with `--verbose` (if CLI variant exists) |

---
## 7. Headless Workaround (Bypass Redirect Entirely)
Use already-integrated device code or PAT workflow:

**Device Code Initiate:**
```bash
bun run unified_mcp_consciousness_orchestrator.ts --call github_device_code_initiate '{"client_id":"<your_client_id>","scope":"repo read:user"}'
```
**Poll (after entering user code):**
```bash
bun run unified_mcp_consciousness_orchestrator.ts --call github_device_code_poll '{"client_id":"<your_client_id>","device_code":"<device_code>","create":true}'
```
This persists `GITHUB_TOKEN` into `.env` → bypasses extension-driven interactive login.

---
## 8. Deep Reset (Nuclear) – Use Only If Repeats After Cleanup
1. Backup then remove suspicious global storage folders:
   - `~/.config/Code/User/globalStorage/github.*`
   - `~/.config/Code/User/globalStorage/*mcp*`
2. Remove/rename `state.vscdb*` (will reset window layout & some ephemeral state). **Backup first.**
3. Re-open workspace, re-add minimal `mcp.servers` entry.
4. Apply device code flow before starting server.

---
## 9. Optional Enhancements To Add (We Can Implement Next)
- `github_rate_limit_status` tool (API quota + auth mode check)
- `mcp_server_health_probe` (simulated aggregator of env + token presence + test call)
- Automatic periodic env secret + token expiry sentinel (background file drop)
- Log harvesting tool (tail & compress targeted VS Code log sets)

Tell me which of these you want and I’ll carve it into the orchestrator.

---
## 10. What To Collect For Further Analysis
Bundle these into a gist (redact tokens):
- Last 200 lines total from: `Model Context Protocol`, `GitHub`, `Log (Extension Host)`
- Developer Console filtered entries (copy as text)
- `mcp.servers` JSON excerpt
- Output of: `env | grep -i github` (remove secrets)
- Output of: presence probe + one working internal GitHub meta call

---
**Return Path:** Once you gather the artifacts, drop them in the chat and we’ll triage root cause definitively.

Stay noir; no more temporal bleed due to auth redirects.
