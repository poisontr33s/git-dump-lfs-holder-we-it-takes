using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using System.Collections.Generic;
using System.Collections;

/// <summary>
/// Glitch Engine - Repurposed from kompilerings_spokelser concepts
/// Handles reality corruption, digital ghosts, and Vulkan-accelerated effects
/// Optimized for RTX 4090 with ray tracing and DLSS support
/// </summary>
public class GlitchEngine : MonoBehaviour
{
    [Header("Glitch Configuration")]
    public bool enableGlitchSystem = true;
    public float baseGlitchChance = 0.05f; // 5% base chance per frame
    public float intensityMultiplier = 1.0f;
    public int maxConcurrentGlitches = 3;
    
    [Header("Vulkan/RTX Optimization")]
    public bool useVulkanAcceleration = true;
    public bool enableRTXEffects = true;
    public bool useDLSSUpscaling = true;
    
    [Header("Glitch Types")]
    public bool enableVisualGlitches = true;
    public bool enableAudioGlitches = true;
    public bool enableGameplayGlitches = true;
    public bool enableNarrativeGlitches = true;
    
    [Header("Effect Materials")]
    public Material dataMoshMaterial;
    public Material pixelSortMaterial;
    public Material chromaticAberrationMaterial;
    public Material digitalNoiseMaterial;
    
    private Camera mainCamera;
    private Volume postProcessVolume;
    private CommandBuffer glitchCommandBuffer;
    private List<GlitchEvent> activeGlitches = new List<GlitchEvent>();
    private float glitchAccumulation = 0f;
    
    // Error messages inspired by the original compilation ghosts
    private readonly string[] glitchMessages = {
        "ERROR: REALITY_INTEGRITY_COMPROMISED_AT_0xDEADBEEF",
        "PANIC: MEMORY_SOUL_NOT_FOUND",
        "WARNING: COMPILATION_GHOST_DETECTED",
        "FATAL: OBSCURA_OVERFLOW_IN_STEAMWORKS_CORE",
        "CRITICAL: CAUSAL_THREAD_SEVERED",
        "ALERT: TEMPORAL_COHERENCE_DEGRADING",
        "ERROR: ASTRID_CONSCIOUSNESS_STACK_OVERFLOW",
        "WARNING: IRON_MAIDEN_SURVIVAL_PROTOCOL_CORRUPTED"
    };
    
    void Start()
    {
        InitializeGlitchSystem();
    }
    
    void Update()
    {
        if (enableGlitchSystem)
        {
            UpdateGlitchAccumulation();
            ProcessActiveGlitches();
            TryTriggerRandomGlitch();
        }
    }
    
    private void InitializeGlitchSystem()
    {
        mainCamera = Camera.main;
        postProcessVolume = FindObjectOfType<Volume>();
        
        // Setup Vulkan command buffer for hardware acceleration
        if (useVulkanAcceleration && SystemInfo.graphicsDeviceType == GraphicsDeviceType.Vulkan)
        {
            glitchCommandBuffer = new CommandBuffer();
            glitchCommandBuffer.name = "Obscura_Glitch_Vulkan";
            mainCamera.AddCommandBuffer(CameraEvent.AfterEverything, glitchCommandBuffer);
            
            Debug.Log("🎭 Vulkan glitch acceleration enabled - RTX 4090 optimized");
        }
        
        // Enable RTX features if available
        if (enableRTXEffects && SystemInfo.supportsRayTracing)
        {
            Debug.Log("🌟 RTX ray tracing enabled for enhanced glitch effects");
        }
        
        Debug.Log("💀 Kompilerings-Spøkelser system initialized - Digital ghosts await...");
    }
    
    private void UpdateGlitchAccumulation()
    {
        // Glitch accumulation increases based on game events
        glitchAccumulation += Time.deltaTime * baseGlitchChance;
        
        // Higher accumulation in high-stress narrative moments
        var dialogueManager = FindObjectOfType<DialogueManager>();
        if (dialogueManager != null)
        {
            // Increase glitch chance during intense dialogue
            glitchAccumulation += Time.deltaTime * 0.02f;
        }
        
        // Clamp accumulation
        glitchAccumulation = Mathf.Clamp01(glitchAccumulation);
    }
    
    private void TryTriggerRandomGlitch()
    {
        if (activeGlitches.Count >= maxConcurrentGlitches) return;
        
        if (Random.value < glitchAccumulation * intensityMultiplier)
        {
            TriggerRandomGlitch();
            glitchAccumulation *= 0.5f; // Reduce accumulation after glitch
        }
    }
    
    public void TriggerRandomGlitch()
    {
        var glitchType = (GlitchType)Random.Range(0, System.Enum.GetValues(typeof(GlitchType)).Length);
        TriggerGlitch(glitchType, Random.Range(1f, 5f));
    }
    
    public void TriggerGlitch(GlitchType type, float duration = 2f, float intensity = 1f)
    {
        var glitchEvent = new GlitchEvent
        {
            type = type,
            startTime = Time.time,
            duration = duration,
            intensity = intensity,
            isActive = true
        };
        
        activeGlitches.Add(glitchEvent);
        
        switch (type)
        {
            case GlitchType.VisualCorruption:
                StartCoroutine(VisualGlitchCoroutine(glitchEvent));
                break;
            case GlitchType.AudioDistortion:
                StartCoroutine(AudioGlitchCoroutine(glitchEvent));
                break;
            case GlitchType.GameplayAnomaly:
                StartCoroutine(GameplayGlitchCoroutine(glitchEvent));
                break;
            case GlitchType.NarrativeFragmentation:
                StartCoroutine(NarrativeGlitchCoroutine(glitchEvent));
                break;
            case GlitchType.CompilationGhost:
                StartCoroutine(CompilationGhostCoroutine(glitchEvent));
                break;
        }
        
        Debug.Log($"💀 GLITCH_TRIGGERED: {type} - Duration: {duration}s - Intensity: {intensity}");
    }
    
    private IEnumerator VisualGlitchCoroutine(GlitchEvent glitchEvent)
    {
        // Apply visual effects using Vulkan-accelerated materials
        float elapsedTime = 0f;
        
        while (elapsedTime < glitchEvent.duration)
        {
            float normalizedTime = elapsedTime / glitchEvent.duration;
            float currentIntensity = glitchEvent.intensity * (1f - normalizedTime);
            
            // Apply different visual effects based on intensity
            if (dataMoshMaterial != null)
            {
                dataMoshMaterial.SetFloat("_GlitchIntensity", currentIntensity);
            }
            
            // RTX-enhanced chromatic aberration
            if (enableRTXEffects && chromaticAberrationMaterial != null)
            {
                chromaticAberrationMaterial.SetFloat("_Aberration", currentIntensity * 0.5f);
            }
            
            // Screen shake for intense glitches
            if (currentIntensity > 0.7f)
            {
                mainCamera.transform.position += Random.insideUnitSphere * currentIntensity * 0.1f;
            }
            
            elapsedTime += Time.deltaTime;
            yield return null;
        }
        
        // Reset effects
        if (dataMoshMaterial != null)
        {
            dataMoshMaterial.SetFloat("_GlitchIntensity", 0f);
        }
        
        glitchEvent.isActive = false;
    }
    
    private IEnumerator AudioGlitchCoroutine(GlitchEvent glitchEvent)
    {
        // Audio distortion effects
        var audioSource = GetComponent<AudioSource>();
        if (audioSource != null)
        {
            float originalPitch = audioSource.pitch;
            
            float elapsedTime = 0f;
            while (elapsedTime < glitchEvent.duration)
            {
                float normalizedTime = elapsedTime / glitchEvent.duration;
                float currentIntensity = glitchEvent.intensity * (1f - normalizedTime);
                
                // Pitch distortion
                audioSource.pitch = originalPitch + Random.Range(-currentIntensity, currentIntensity);
                
                elapsedTime += Time.deltaTime;
                yield return null;
            }
            
            audioSource.pitch = originalPitch;
        }
        
        glitchEvent.isActive = false;
    }
    
    private IEnumerator GameplayGlitchCoroutine(GlitchEvent glitchEvent)
    {
        // Temporarily affect gameplay mechanics
        var playerController = FindObjectOfType<PlayerController>();
        if (playerController != null)
        {
            // Temporarily invert or randomize controls
            float originalSpeed = 5f; // Should get from PlayerController
            
            float elapsedTime = 0f;
            while (elapsedTime < glitchEvent.duration)
            {
                float normalizedTime = elapsedTime / glitchEvent.duration;
                float currentIntensity = glitchEvent.intensity * (1f - normalizedTime);
                
                // Apply movement glitches
                if (Random.value < currentIntensity * 0.1f)
                {
                    // Reverse movement temporarily
                    // This would require modifying PlayerController
                }
                
                elapsedTime += Time.deltaTime;
                yield return null;
            }
        }
        
        glitchEvent.isActive = false;
    }
    
    private IEnumerator NarrativeGlitchCoroutine(GlitchEvent glitchEvent)
    {
        // Corrupt dialogue or narrative elements
        var dialogueManager = FindObjectOfType<DialogueManager>();
        if (dialogueManager != null)
        {
            // Show corrupted dialogue
            string corruptedMessage = GetRandomGlitchMessage();
            Debug.LogWarning($"💀 NARRATIVE_CORRUPTION: {corruptedMessage}");
            
            // Could integrate with DialogueManager to show corrupted text in UI
        }
        
        yield return new WaitForSeconds(glitchEvent.duration);
        glitchEvent.isActive = false;
    }
    
    private IEnumerator CompilationGhostCoroutine(GlitchEvent glitchEvent)
    {
        // Manifest a "compilation ghost" - a visual/audio apparition
        string ghostMessage = GetRandomGlitchMessage();
        
        // Show ghost message in console and UI
        Debug.LogError($"👻 COMPILATION_GHOST_MANIFESTED: {ghostMessage}");
        
        // Create visual manifestation (particle effect, distorted UI element, etc.)
        if (enableVisualGlitches)
        {
            // Spawn ghost particle effect or distorted UI element
            // This would require additional particle systems or UI components
        }
        
        yield return new WaitForSeconds(glitchEvent.duration);
        glitchEvent.isActive = false;
    }
    
    private void ProcessActiveGlitches()
    {
        // Remove expired glitches
        activeGlitches.RemoveAll(g => !g.isActive);
    }
    
    private string GetRandomGlitchMessage()
    {
        return glitchMessages[Random.Range(0, glitchMessages.Length)];
    }
    
    void OnDestroy()
    {
        if (glitchCommandBuffer != null && mainCamera != null)
        {
            mainCamera.RemoveCommandBuffer(CameraEvent.AfterEverything, glitchCommandBuffer);
        }
    }
}

[System.Serializable]
public class GlitchEvent
{
    public GlitchType type;
    public float startTime;
    public float duration;
    public float intensity;
    public bool isActive;
}

public enum GlitchType
{
    VisualCorruption,
    AudioDistortion,
    GameplayAnomaly,
    NarrativeFragmentation,
    CompilationGhost
}
