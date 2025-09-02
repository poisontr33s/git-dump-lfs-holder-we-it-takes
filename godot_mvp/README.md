# Godot + FastAPI MVP (Psycho‑Noir Kontrapunkt)

This MVP uses Godot 4 (Vulkan) for the client and Python FastAPI for AI/dialogue.
Run both from VS Code.

## Structure
```
godot_mvp/
  godot/
    project.godot
    scenes/
      Main.tscn
    scripts/
      Main.gd
  backend/
    app/
      main.py
      routers/
        dialogue.py
        save.py
    requirements.txt
```

## Run
- Backend (FastAPI): see VS Code tasks (FastAPI: Run)
- Client (Godot): open `godot_mvp/godot` in Godot 4 editor or use task (Godot: Run)
