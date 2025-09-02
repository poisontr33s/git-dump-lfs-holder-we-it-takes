using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

public class DialogueManager : MonoBehaviour
{
    public Text dialogueText;
    public Button[] choiceButtons;
    private Dictionary<string, string[]> dialogueTree = new Dictionary<string, string[]>();
    private int currentSkillLevel = 5; // Placeholder for "Sensual Intelligence" skill

    void Start()
    {
        // Upcycled from psycho_sensual_sexual_genre_implementation.py
        dialogueTree["greeting"] = new string[] {
            "Astrid: 'Welcome to the Steamworks, darling. Shall we explore your desires?'",
            "1. Flirt back (Sensual Check)", "2. Stay professional"
        };
        dialogueTree["flirt_success"] = new string[] {
            "Astrid: 'Mmm, your touch ignites the obscura... Let's delve deeper.' (NSFW+ branch unlocked)",
            "Continue exploration"
        };
        dialogueTree["flirt_fail"] = new string[] {
            "Astrid: 'Too timid. The magick fades.' (Glitch triggered)",
            "Retry"
        };
    }

    public void StartDialogue(string key)
    {
        if (dialogueTree.ContainsKey(key))
        {
            dialogueText.text = dialogueTree[key][0];
            for (int i = 0; i < choiceButtons.Length; i++)
            {
                if (i < dialogueTree[key].Length - 1)
                {
                    choiceButtons[i].gameObject.SetActive(true);
                    choiceButtons[i].GetComponentInChildren<Text>().text = dialogueTree[key][i + 1];
                }
                else
                {
                    choiceButtons[i].gameObject.SetActive(false);
                }
            }
        }
    }

    public void MakeChoice(int choiceIndex, string currentKey)
    {
        // Skill check simulation (upcycled logic)
        if (currentKey == "greeting" && choiceIndex == 0)
        {
            if (currentSkillLevel > 3)
            {
                StartDialogue("flirt_success");
            }
            else
            {
                StartDialogue("flirt_fail");
                TriggerGlitch(); // Link to GlitchManager
            }
        }
    }

    private void TriggerGlitch()
    {
        // Placeholder for glitch event
        Debug.Log("ERROR: REALITY_INTEGRITY_COMPROMISED");
    }
}
