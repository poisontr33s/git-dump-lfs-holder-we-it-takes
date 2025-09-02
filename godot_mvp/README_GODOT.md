# Godot 4 in Codespaces / Devcontainer

Context: The GDScript language server error appears because Godot editor (or language server) isn’t running. Inside a headless container you need a Godot binary.

Install (manual):
- Download Godot 4.x Linux x86_64 (standard) and put the binary on PATH as `godot4`.
- Example (host): place it under `~/.local/bin/godot4` and forward into the container, or copy into the devcontainer and chmod +x.

Start editor or language server:
- Editor: `godot4 --path /workspaces/PsychoNoir-Kontrapunkt/godot_mvp/godot --editor`
- Headless LS: `godot4 --headless --editor --path /workspaces/PsychoNoir-Kontrapunkt/godot_mvp/godot`

VS Code Godot Tools looks for a running editor. If remote download is blocked, install locally and connect via Remote - SSH / Codespaces port forwarding.
