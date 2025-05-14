"""
Script for enriching dialogue data from Disco Elysium.

This script reads the structured dialogue data and actor information,
and then generates a new CSV file with additional, derived columns
to aid in analysis. These new columns include resolved actor names,
categorized sequence types, hierarchical depth of dialogue lines,
and flags for conditions and user scripts.
"""

import pandas as pd
import re


def enhance_dialogue_data(dialogue_file_path, actors_file_path, output_file_path):
    """
    Reads dialogue and actor data, enriches it, and saves it to a new CSV file.

    Args:
        dialogue_file_path (str): Path to the structured dialogue CSV file.
        actors_file_path (str): Path to the actors CSV file.
        output_file_path (str): Path for the enriched output CSV file.
    """
    try:
        df_dialogue = pd.read_csv(dialogue_file_path)
        df_actors = pd.read_csv(actors_file_path)
    except FileNotFoundError as e:
        print(f"ERROR: Input file not found: {e.filename}")
        return
    except Exception as e:
        print(f"ERROR: Could not read input files: {e}")
        return

    actors_map = df_actors.set_index("id")["name"].to_dict()

    enriched_rows = []

    # Ensure conversationid is suitable for grouping (e.g., handle potential NaN or float issues if any)
    df_dialogue["conversationid"] = df_dialogue["conversationid"].fillna(-1).astype(int)

    for conv_id, group in df_dialogue.groupby("conversationid"):
        last_non_continue_depth = 0  # Reset for each conversation

        for index, row in group.iterrows():
            actor_name = actors_map.get(row["actor"])

            sequence_str = str(
                row["sequence"]
            ).strip()  # Changed "Sequence" to "sequence"

            current_category = "OTHER"
            current_depth = -1  # Default for unparseable or truly 'other'

            if not sequence_str:  # Handle empty sequence strings
                current_category = "EMPTY_SEQUENCE"
                current_depth = last_non_continue_depth  # Or a specific value like -2
            elif sequence_str == "0":
                current_category = "ROOT"
                current_depth = 0
            elif sequence_str == "Continue()":
                current_category = "CONTINUE"
                current_depth = last_non_continue_depth
            elif re.fullmatch(r"\d+(\.\d+)*", sequence_str):
                current_category = "NUMERIC_HIERARCHY"
                current_depth = sequence_str.count(".")
            # Example for a potential alphanumeric hierarchy if discovered later
            # elif re.fullmatch(r'[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*', sequence_str):
            #     current_category = 'ALPHANUMERIC_HIERARCHY'
            #     current_depth = sequence_str.count('.')
            else:
                # For 'OTHER' sequences, attempt to infer depth by dots
                # If no dots, and it's a non-empty, non-special string, treat as a base level item
                if "." in sequence_str:
                    current_depth = sequence_str.count(".")
                elif sequence_str:  # Non-empty, not matching other patterns, no dots
                    current_depth = 0
                # Category remains 'OTHER'

            # Update last_non_continue_depth if the current line establishes its own depth
            if current_category != "CONTINUE" and current_category != "EMPTY_SEQUENCE":
                last_non_continue_depth = current_depth

            has_conditions = (
                pd.notna(row["conditionstring"])
                and str(row["conditionstring"]).strip()
                != ""  # Changed "Condition" to "conditionstring"
            )
            has_userscript = (
                pd.notna(row["userscript"])
                and str(row["userscript"]).strip()
                != ""  # Changed "UserScript" to "userscript"
            )

            new_row = row.to_dict()
            new_row["actor_name"] = actor_name
            new_row["sequence_category"] = current_category
            new_row["hierarchical_depth"] = current_depth
            new_row["has_conditions"] = has_conditions
            new_row["has_userscript"] = has_userscript
            enriched_rows.append(new_row)

    df_enriched = pd.DataFrame(enriched_rows)

    try:
        df_enriched.to_csv(output_file_path, index=False, encoding="utf-8")
        print(f"Successfully transmuted data. Enriched file: {output_file_path}")
    except Exception as e:
        print(f"ERROR: Could not write output file: {e}")


if __name__ == "__main__":
    # File paths relative to the script's location or an absolute path
    # Assuming the script is in the same directory as the CSV files
    dialogue_file = "de_structured_dialogue.csv"
    actors_file = "de_actors.csv"
    output_file = "de_dialogue_enriched.csv"

    print("Initiating Psycho-Noir Kontrapunkt Data Transmutation Protocol...")
    enhance_dialogue_data(dialogue_file, actors_file, output_file)
    print("Protocol complete. Reality matrix updated.")
