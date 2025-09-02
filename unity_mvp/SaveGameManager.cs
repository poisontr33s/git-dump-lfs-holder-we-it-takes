using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System;
using Newtonsoft.Json;

/// <summary>
/// Save Game Manager - Repurposed from session_backup_manager.py
/// Handles fragmented memory saves, narrative continuity, and glitch-corrupted data
/// Maintains psycho-noir theme of fractured identity and corrupted memories
/// </summary>
public class SaveGameManager : MonoBehaviour
{
    [Header("Save System Configuration")]
    public string saveDirectory = "SteamworksSaves";
    public bool enableFragmentedMemories = true;
    public float corruptionChance = 0.15f; // 15% chance of memory corruption
    public int maxBackupSlots = 5;
    
    [Header("Psycho-Noir Memory System")]
    public bool enableMemoryGlitches = true;
    public float memoryDegradation = 0.02f; // Memories fade over time
    
    private string savePath;
    private GameSaveData currentSave;
    
    void Awake()
    {
        InitializeSaveSystem();
    }
    
    private void InitializeSaveSystem()
    {
        savePath = Path.Combine(Application.persistentDataPath, saveDirectory);
        
        if (!Directory.Exists(savePath))
        {
            Directory.CreateDirectory(savePath);
        }
        
        Debug.Log($"🎭 Save system initialized - Fragmented memories stored at: {savePath}");
    }
    
    /// <summary>
    /// Save current game state with potential memory corruption
    /// Implements psycho-noir fragmentation mechanics
    /// </summary>
    public void SaveGame(string slotName = "autosave")
    {
        try
        {
            var saveData = GatherGameState();
            
            // Apply memory corruption if enabled
            if (enableFragmentedMemories && UnityEngine.Random.value < corruptionChance)
            {
                saveData = ApplyMemoryCorruption(saveData);
            }
            
            string fileName = $"{slotName}_{DateTime.Now:yyyyMMdd_HHmmss}.json";
            string fullPath = Path.Combine(savePath, fileName);
            
            string jsonData = JsonConvert.SerializeObject(saveData, Formatting.Indented);
            File.WriteAllText(fullPath, jsonData);
            
            // Create backup rotation
            ManageBackupRotation(slotName);
            
            Debug.Log($"🎭 Memory fragment saved: {fileName}");
            
            if (saveData.isCorrupted)
            {
                Debug.LogWarning("⚠️ MEMORY_CORRUPTION_DETECTED - Some memories may be lost...");
            }
        }
        catch (Exception e)
        {
            Debug.LogError($"💀 CRITICAL_SAVE_FAILURE: {e.Message}");
        }
    }
    
    /// <summary>
    /// Load game state with fragmented memory handling
    /// </summary>
    public bool LoadGame(string slotName = "autosave")
    {
        try
        {
            var saveFiles = GetSaveFiles(slotName);
            
            if (saveFiles.Count == 0)
            {
                Debug.LogWarning("🎭 No memory fragments found for restoration");
                return false;
            }
            
            // Load most recent save
            string latestSave = saveFiles[0];
            string jsonData = File.ReadAllText(latestSave);
            
            currentSave = JsonConvert.DeserializeObject<GameSaveData>(jsonData);
            
            // Apply memory degradation over time
            if (enableMemoryGlitches)
            {
                ApplyMemoryDegradation(currentSave);
            }
            
            RestoreGameState(currentSave);
            
            Debug.Log($"🎭 Memory fragment restored: {Path.GetFileName(latestSave)}");
            
            if (currentSave.isCorrupted)
            {
                Debug.LogWarning("⚠️ Corrupted memories detected - some data may be unreliable");
            }
            
            return true;
        }
        catch (Exception e)
        {
            Debug.LogError($"💀 CRITICAL_LOAD_FAILURE: {e.Message}");
            return false;
        }
    }
    
    private GameSaveData GatherGameState()
    {
        var saveData = new GameSaveData
        {
            timestamp = DateTime.Now,
            playerPosition = FindObjectOfType<PlayerController>()?.transform.position ?? Vector3.zero,
            currentScene = UnityEngine.SceneManagement.SceneManager.GetActiveScene().name,
            isCorrupted = false,
            memoryIntegrity = 1.0f
        };
        
        // Gather dialogue state
        var dialogueManager = FindObjectOfType<DialogueManager>();
        if (dialogueManager != null)
        {
            saveData.dialogueState = new DialogueState
            {
                currentConversation = "astrid_meeting", // Placeholder
                completedDialogues = new List<string>(),
                relationshipLevels = new Dictionary<string, float>
                {
                    {"astrid", 0.5f},
                    {"iron_maiden", 0.3f}
                }
            };
        }
        
        // Gather skill levels
        saveData.skillLevels = new Dictionary<string, float>
        {
            {"sensual_intelligence", 0.6f},
            {"survival_instinct", 0.4f},
            {"technical_mastery", 0.7f},
            {"obscura_sensitivity", 0.5f}
        };
        
        // Gather inventory and quest state
        saveData.inventoryItems = new List<string> { "corrupted_data_fragment", "steamworks_key" };
        saveData.questFlags = new Dictionary<string, bool>
        {
            {"met_astrid", true},
            {"discovered_glitch", false}
        };
        
        return saveData;
    }
    
    private GameSaveData ApplyMemoryCorruption(GameSaveData saveData)
    {
        saveData.isCorrupted = true;
        saveData.memoryIntegrity = UnityEngine.Random.Range(0.3f, 0.8f);
        
        // Randomly corrupt some data
        if (UnityEngine.Random.value < 0.3f)
        {
            // Corrupt position slightly
            saveData.playerPosition += new Vector3(
                UnityEngine.Random.Range(-2f, 2f),
                0,
                UnityEngine.Random.Range(-2f, 2f)
            );
        }
        
        if (UnityEngine.Random.value < 0.2f)
        {
            // Corrupt some skill levels
            var skills = new List<string>(saveData.skillLevels.Keys);
            foreach (var skill in skills)
            {
                if (UnityEngine.Random.value < 0.4f)
                {
                    saveData.skillLevels[skill] *= UnityEngine.Random.Range(0.7f, 1.3f);
                    saveData.skillLevels[skill] = Mathf.Clamp01(saveData.skillLevels[skill]);
                }
            }
        }
        
        saveData.corruptionLog.Add($"MEMORY_GLITCH_{DateTime.Now:HHmmss}: Data integrity compromised");
        
        return saveData;
    }
    
    private void ApplyMemoryDegradation(GameSaveData saveData)
    {
        TimeSpan timeSinceSave = DateTime.Now - saveData.timestamp;
        float degradationFactor = (float)timeSinceSave.TotalHours * memoryDegradation;
        
        saveData.memoryIntegrity = Mathf.Max(0.1f, saveData.memoryIntegrity - degradationFactor);
        
        if (degradationFactor > 0.1f)
        {
            saveData.corruptionLog.Add($"TEMPORAL_DECAY_{DateTime.Now:HHmmss}: Memory degradation detected");
        }
    }
    
    private void RestoreGameState(GameSaveData saveData)
    {
        // Restore player position
        var player = FindObjectOfType<PlayerController>();
        if (player != null)
        {
            player.transform.position = saveData.playerPosition;
        }
        
        // Restore dialogue state
        var dialogueManager = FindObjectOfType<DialogueManager>();
        if (dialogueManager != null && saveData.dialogueState != null)
        {
            // Apply relationship levels and dialogue state
            // This would integrate with your dialogue system
        }
        
        // Show corruption warnings if needed
        if (saveData.isCorrupted)
        {
            ShowCorruptionWarning(saveData);
        }
    }
    
    private void ShowCorruptionWarning(GameSaveData saveData)
    {
        // Display UI warning about corrupted memories
        // This adds to the psycho-noir atmosphere
        Debug.LogWarning($"🎭 MEMORY_INTEGRITY: {saveData.memoryIntegrity:P0}");
        
        foreach (var logEntry in saveData.corruptionLog)
        {
            Debug.LogWarning($"💀 {logEntry}");
        }
    }
    
    private List<string> GetSaveFiles(string slotName)
    {
        var files = new List<string>();
        
        if (Directory.Exists(savePath))
        {
            var pattern = $"{slotName}_*.json";
            files.AddRange(Directory.GetFiles(savePath, pattern));
            files.Sort((a, b) => File.GetCreationTime(b).CompareTo(File.GetCreationTime(a)));
        }
        
        return files;
    }
    
    private void ManageBackupRotation(string slotName)
    {
        var saveFiles = GetSaveFiles(slotName);
        
        while (saveFiles.Count > maxBackupSlots)
        {
            File.Delete(saveFiles[saveFiles.Count - 1]);
            saveFiles.RemoveAt(saveFiles.Count - 1);
        }
    }
}

[System.Serializable]
public class GameSaveData
{
    public DateTime timestamp;
    public Vector3 playerPosition;
    public string currentScene;
    public bool isCorrupted;
    public float memoryIntegrity;
    public List<string> corruptionLog = new List<string>();
    
    public DialogueState dialogueState;
    public Dictionary<string, float> skillLevels;
    public List<string> inventoryItems;
    public Dictionary<string, bool> questFlags;
}

[System.Serializable]
public class DialogueState
{
    public string currentConversation;
    public List<string> completedDialogues;
    public Dictionary<string, float> relationshipLevels;
}
