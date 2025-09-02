using UnityEngine;
using UnityEngine.Rendering;

public class GlitchManager : MonoBehaviour
{
    public Material glitchMaterial; // Assign a shader material for distortions
    private CommandBuffer commandBuffer;

    void Start()
    {
        // Vulkan setup for GPU acceleration (upcycled from kompilerings_spokelser)
        commandBuffer = new CommandBuffer();
        commandBuffer.name = "Obscura Glitch";
        Camera.main.AddCommandBuffer(CameraEvent.AfterEverything, commandBuffer);
    }

    public void TriggerGlitch(float duration = 2f)
    {
        // Enable glitch shader (Vulkan-optimized for RTX 4090)
        glitchMaterial.SetFloat("_GlitchIntensity", 1f);
        Camera.main.renderingPath = RenderingPath.DeferredShading; // Vulkan-friendly
        Invoke("EndGlitch", duration);
    }

    private void EndGlitch()
    {
        glitchMaterial.SetFloat("_GlitchIntensity", 0f);
        Debug.Log("Glitch resolved: Obscura stabilized");
    }

    void OnDestroy()
    {
        if (commandBuffer != null)
        {
            Camera.main.RemoveCommandBuffer(CameraEvent.AfterEverything, commandBuffer);
        }
    }
}
