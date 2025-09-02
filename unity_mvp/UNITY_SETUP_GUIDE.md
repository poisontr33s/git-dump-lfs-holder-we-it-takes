# 🎭 Steamworks of Magick and Obscura - Unity MVP Setup Guide

## Hardware Requirements & Optimization

### Target Hardware
- **GPU**: Nvidia RTX 4090 Laptop
- **CPU**: Intel Core i9-13900 Series
- **RAM**: 32GB+ recommended
- **Storage**: NVMe SSD with 50GB+ free space

### Unity Configuration for High-End Hardware

#### 1. Unity Installation

```bash
# Download Unity Hub and install Unity 2022.3 LTS or newer
# Required packages:
# - Universal Render Pipeline (URP)
# - Vulkan Graphics API Support
# - NVIDIA Ray Tracing (if available)
```

#### 2. Project Settings Configuration

**Graphics Settings:**
- Graphics API: Vulkan (first priority), DX12 (fallback)
- Color Space: Linear
- Rendering Path: Universal Render Pipeline
- HDR: Enabled
- MSAA: 4x (adjust based on performance)

**Quality Settings:**
- V-Sync: Disabled (for 120+ FPS)
- Target Frame Rate: 120
- Texture Quality: Full Res
- Anisotropic Filtering: Per Texture
- Anti-Aliasing: FXAA or TAA

**XR Settings (if VR support desired):**
- Initialize XR on Startup: Disabled (for now)

#### 3. Vulkan Optimization Settings

**Player Settings > Other Settings:**
- Graphics APIs: Remove OpenGL, prioritize Vulkan
- Multithreaded Rendering: Enabled
- GPU Skinning: Enabled
- Graphics Jobs: Enabled

**URP Asset Configuration:**
- Rendering Path: Forward
- Depth Texture: Enabled
- Opaque Texture: Enabled
- HDR: Enabled
- MSAA: 4x
- Render Scale: 1.0 (or higher for super-sampling)

#### 4. RTX 4090 Specific Optimizations

**Memory Management:**
- Streaming Mipmaps: Enabled
- Mipmap Streaming Memory Budget: 2048 MB
- Async Upload Time Slice: 4ms
- Async Upload Buffer Size: 64 MB

**Ray Tracing (if using HDRP):**
- Enable Ray Tracing
- Ray Tracing Tier: Tier 2
- DLSS: Enabled (if package available)

## File Integration Guide

### 1. Script Integration
Copy all C# scripts from `/unity_mvp/` to your Unity project's `Assets/Scripts/` folder:

```
Assets/
├── Scripts/
│   ├── Core/
│   │   ├── PlayerController.cs
│   │   ├── PerformanceManager.cs
│   │   └── SaveGameManager.cs
│   ├── AI/
│   │   ├── AstridAI.cs
│   │   └── DialogueManager.cs
│   ├── Effects/
│   │   └── GlitchEngine.cs
│   └── Managers/
```

### 2. Scene Setup

#### Basic Scene Structure:
1. **Main Camera**
   - Position: (0, 10, -10)
   - Rotation: (45, 0, 0) for isometric view
   - Attach: `GlitchEngine.cs`, `PerformanceManager.cs`

2. **Player GameObject**
   - Position: (0, 0, 0)
   - Attach: `PlayerController.cs`
   - Add: Rigidbody, Collider, Sprite Renderer

3. **NPCs (Astrid)**
   - Position: (5, 0, 0)
   - Attach: `AstridAI.cs`
   - Add: Collider (Trigger), Sprite Renderer

4. **Game Manager (Empty GameObject)**
   - Attach: `SaveGameManager.cs`, `DialogueManager.cs`

5. **UI Canvas**
   - Dialogue UI elements
   - Debug performance display

### 3. Required Assets

#### Sprites & Textures
- Player character sprite (pixel art, 64x64px)
- Astrid NPC sprite (pixel art, 64x64px)
- Isometric tile set for environment
- UI elements (dialogue boxes, buttons)

#### Materials for Glitch Effects
- Data Mosh Material (Shader: Custom/DataMosh)
- Pixel Sort Material (Shader: Custom/PixelSort)
- Chromatic Aberration Material (Shader: Custom/ChromaticAberration)
- Digital Noise Material (Shader: Custom/DigitalNoise)

#### Audio
- Chiptune background music
- Glitch sound effects
- Voice clips (optional)

### 4. Testing & Performance Validation

#### Performance Benchmarks
- Target: 120 FPS at 4K resolution
- Memory usage: <8GB system RAM, <6GB VRAM
- Frame time: <8.33ms consistently

#### Testing Checklist
- [ ] Player movement responds correctly
- [ ] Dialogue system triggers and displays properly
- [ ] Glitch effects activate without major performance drops
- [ ] Save/load system preserves game state
- [ ] Astrid AI responds contextually to player actions
- [ ] Performance metrics display in real-time

### 5. Build Configuration

#### Build Settings
- Target Platform: Windows
- Architecture: x86_64
- Scripting Backend: IL2CPP
- Api Compatibility Level: .NET Standard 2.1

#### Player Settings for Distribution
- Company Name: [Your Studio Name]
- Product Name: Steamworks of Magick and Obscura
- Default Icon: 1024x1024 game icon
- Splash Screen: Custom Psycho-Noir themed

### 6. Advanced Features Implementation

#### Post-Processing Stack

```csharp
// Add to scene with Volume component
// Effects: Bloom, Chromatic Aberration, Vignette, Color Grading
// Custom profiles for different game states (normal, glitched, dialogue)
```

#### Shader Integration
- Custom shaders for glitch effects
- Post-processing shaders for Psycho-Noir atmosphere
- Particle shaders for "compilation ghosts"

### 7. Debugging & Profiling

#### Performance Monitoring
- Use Unity Profiler for CPU/GPU analysis
- Monitor frame times in real-time
- Track memory allocation patterns
- Vulkan debugging tools (if available)

#### Glitch System Debugging
- Console output for glitch events
- Visual indicators for active glitches
- Performance impact measurement per glitch type

### 8. Deployment Preparation

#### Steam Integration (Future)
- Steamworks SDK integration
- Achievement system
- Cloud saves
- Workshop support for mods

#### Distribution Platforms
- Steam (primary)
- itch.io (NSFW+ version)
- Direct distribution

## Next Development Phases

### Phase 1: Core MVP (Current)
- Basic movement and interaction
- Simple dialogue system
- Glitch effect prototype

### Phase 2: Content Expansion
- Multiple NPCs and areas
- Complex dialogue trees
- Enhanced glitch systems
- Save game persistence

### Phase 3: Polish & Features
- Full art assets
- Audio implementation
- Performance optimization
- Platform-specific features

### Phase 4: Release Preparation
- Extensive testing
- Marketing materials
- Distribution setup
- Community feedback integration

## Troubleshooting Common Issues

### Performance Issues:
- Check Vulkan driver compatibility
- Verify RTX feature availability
- Monitor thermal throttling
- Adjust quality settings dynamically

### Glitch Effect Problems:
- Ensure shader compilation success
- Verify material assignments
- Check Vulkan command buffer setup
- Monitor GPU memory usage

### Save System Issues:
- Verify write permissions
- Check JSON serialization
- Monitor file corruption detection
- Test memory degradation mechanics

---

**Ready to begin development!** Start with the basic scene setup and player movement, then gradually integrate the AI systems and glitch effects. The modular design allows for iterative development and testing.
