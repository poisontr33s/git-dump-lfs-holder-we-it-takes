# dialogue_analyzer_pnc.py
"""
Psycho-Noir Kontrapunkt: Dialogue Analyzer

Verktøy for å lese, analysere og strukturere dialogdata fra
de_structured_dialogue.csv for bruk i Psycho-Noir Kontrapunkt-prosjektet.
"""

import csv
import os
import re
import logging
import pandas as pd
from collections import defaultdict, Counter

# Konfigurer logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class DialogueEntry:
    def __init__(
        self,
        id,
        conversation_id,
        actor_id,
        is_group,
        sequence,
        condition_string,
        user_script,
        dialogue_text,
    ):
        self.id = int(id)
        self.conversation_id = int(conversation_id)
        self.actor_id = int(actor_id)
        self.is_group = bool(int(is_group))
        self.sequence = sequence
        self.condition_string = condition_string
        self.user_script = user_script
        self.dialogue_text = dialogue_text


class DialogueNode:
    def __init__(self, entry: DialogueEntry):
        self.entry = entry
        self.entry_id = entry.id  # Unik ID for selve dialoglinjen
        self.original_sequence = entry.sequence  # Behold original sekvensstreng
        self.children = []
        self.parent = None
        self.is_structural = (
            False  # Er denne noden en del av hovedstrukturen (f.eks. "1.2.3")?
        )

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self


def load_dialogue_data(file_path):
    dialogue_entries = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                logging.error(f"CSV-filen {file_path} er tom eller har ingen header.")
                return []

            for row in reader:
                try:
                    entry = DialogueEntry(
                        id=row["id"],
                        conversation_id=row["conversationid"],
                        actor_id=row["actor"],
                        is_group=row["isgroup"],
                        sequence=row["sequence"],
                        condition_string=row.get("conditionstring", "0"),
                        user_script=row.get("userscript", "0"),
                        dialogue_text=row["dialoguetext"],
                    )
                    dialogue_entries.append(entry)
                except ValueError as e:
                    logging.error(f"Kunne ikke parse rad: {row}. Feil: {e}")
                except KeyError as e:
                    logging.error(f"Mangler forventet kolonne {e} i rad: {row}")
        logging.info(
            f"INFO: Lastet {len(dialogue_entries)} dialogoppføringer fra {file_path}"
        )
    except FileNotFoundError:
        logging.error(f"Fil ikke funnet: {file_path}")
    except Exception as e:
        logging.error(f"En feil oppstod under lasting av dialogdata: {e}")
    return dialogue_entries


def load_actor_names_from_csv(csv_file_path):
    actor_names = {}
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            if (
                not reader.fieldnames
                or "id" not in reader.fieldnames
                or "name" not in reader.fieldnames
            ):
                logging.error(
                    f"CSV-filen for aktørnavn {csv_file_path} mangler 'id' eller 'name' kolonne i header."
                )
                return {}

            for row in reader:
                try:
                    actor_id_val = row.get("id")
                    actor_name_val = row.get("name")
                    if actor_id_val is not None and actor_name_val is not None:
                        actor_id = int(actor_id_val)
                        actor_names[actor_id] = actor_name_val
                    else:
                        logging.warning(
                            f"Manglende 'id' eller 'name' i rad: {row} i {csv_file_path}"
                        )
                except ValueError:
                    logging.warning(
                        f"Kunne ikke parse actor_id '{row.get('id')}' til int i {csv_file_path}."
                    )
        logging.info(f"INFO: Lastet {len(actor_names)} aktørnavn fra {csv_file_path}")
    except FileNotFoundError:
        logging.error(f"Aktørnavn CSV-fil ikke funnet: {csv_file_path}")
    except Exception as e:
        logging.error(f"En feil oppstod under lasting av aktørnavn fra CSV: {e}")
    return actor_names


def analyze_sequence_patterns(dialogue_data):
    logging.info("\n--- Analyse av 'sequence'-kolonnen ---")
    if not dialogue_data:
        logging.info("Ingen dialogdata å analysere.")
        return

    sequences = [
        entry.sequence for entry in dialogue_data if entry.sequence is not None
    ]
    if not sequences:
        logging.info("Ingen 'sequence'-verdier funnet i dialogdataene.")
        return

    total_sequences = len(sequences)
    logging.info(
        f"Totalt antall 'sequence'-verdier (inkludert duplikater): {total_sequences}"
    )

    unique_sequences = set(sequences)
    logging.info(f"Antall unike 'sequence'-verdier: {len(unique_sequences)}")

    sequence_counts = Counter(sequences)
    logging.info("\nTopp 20 mest vanlige 'sequence'-verdier:")
    for seq, count in sequence_counts.most_common(20):
        logging.info(f"  '{seq}': {count} ganger")

    numeric_hierarchical_pattern = re.compile(r"^\d+(\.\d+)*$")
    alphanumeric_hierarchical_pattern = re.compile(r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*$")

    categorized_counts = {
        "Continue()": 0,
        "Repeat()": 0,
        "Numerisk-hierarkisk": 0,
        "Alfanumerisk-hierarkisk": 0,
    }
    max_depth = 0
    other_formats_examples = []
    unique_categorized_sequences = set()

    for seq, count in sequence_counts.items():
        matched_category = False
        if seq == "Continue()":
            categorized_counts["Continue()"] += count
            unique_categorized_sequences.add(seq)
            matched_category = True
        elif seq == "Repeat()":
            categorized_counts["Repeat()"] += count
            unique_categorized_sequences.add(seq)
            matched_category = True
        elif numeric_hierarchical_pattern.match(seq):
            categorized_counts["Numerisk-hierarkisk"] += count
            unique_categorized_sequences.add(seq)
            matched_category = True
            current_depth = seq.count(".")
            if current_depth > max_depth:
                max_depth = current_depth
        elif alphanumeric_hierarchical_pattern.match(seq):
            if not numeric_hierarchical_pattern.match(
                seq
            ):  # For å unngå dobbelttelling hvis en numerisk også matcher alfanumerisk
                categorized_counts["Alfanumerisk-hierarkisk"] += count
                unique_categorized_sequences.add(seq)
                matched_category = True
                current_depth = seq.count(".")
                if current_depth > max_depth:
                    max_depth = current_depth

        if not matched_category:
            if len(other_formats_examples) < 10 and seq:  # Sjekk for tom streng `seq`
                other_formats_examples.append(f"'{seq}' (forekomster: {count})")

    logging.info(
        "\nKategorisering av 'sequence'-verdier (basert på antall forekomster):"
    )
    for category, count in categorized_counts.items():
        logging.info(f"  {category}: {count} forekomster")
    logging.info(f"  Maksimal hierarkisk dybde observert (antall '.'): {max_depth}")

    if other_formats_examples:
        num_other_unique_formats = len(unique_sequences) - len(
            unique_categorized_sequences
        )
        logging.info(
            f"\n  {num_other_unique_formats} unike 'sequence'-formater som ikke matchet kategoriene over (viser opptil 10):"
        )
        for ex in other_formats_examples:
            logging.info(f"    {ex}")
    logging.info("------------------------------")


def build_conversation_tree(
    conversation_id: int, all_dialogues: list[DialogueEntry]
) -> list[DialogueNode]:
    conversation_lines = sorted(
        [entry for entry in all_dialogues if entry.conversation_id == conversation_id],
        key=lambda e: e.id,
    )

    if not conversation_lines:
        return []

    root_nodes = []
    nodes_by_key = {}
    all_nodes_in_this_conversation = []
    last_structural_node = None
    numeric_hierarchical_pattern = re.compile(r"^\d+(\.\d+)*$")

    for entry in conversation_lines:
        node = DialogueNode(entry)
        all_nodes_in_this_conversation.append(node)

        if numeric_hierarchical_pattern.match(node.original_sequence):
            node.is_structural = True
            nodes_by_key[node.original_sequence] = node
            last_structural_node = node

            if "." in node.original_sequence:
                parent_key = node.original_sequence.rpartition(".")[0]
                if parent_key in nodes_by_key:
                    parent_node = nodes_by_key[parent_key]
                    parent_node.add_child(node)
        else:
            node.is_structural = False
            if last_structural_node:
                last_structural_node.add_child(node)

    for node in all_nodes_in_this_conversation:
        if node.parent is None:
            root_nodes.append(node)

    root_nodes.sort(key=lambda n: n.entry.id)
    return root_nodes


def print_conversation_tree_recursive(
    nodes: list[DialogueNode],
    actor_mapping: dict,
    prefix: str = "",
    is_last_sibling: bool = True,
):
    for i, node in enumerate(nodes):
        is_current_last = i == len(nodes) - 1
        connector = "└─ " if is_current_last else "├─ "

        actor_name = actor_mapping.get(
            node.entry.actor_id, f"Ukjent Aktør (ID: {node.entry.actor_id})"
        )
        if node.entry.is_group:
            actor_name += " (Gruppe)"

        dialogue_preview = node.entry.dialogue_text.replace("\n", " ").strip()
        if len(dialogue_preview) > 70:
            dialogue_preview = dialogue_preview[:67] + "..."
        if not dialogue_preview:
            dialogue_preview = node.entry.dialogue_text

        conditions = (
            f" [Cond: {node.entry.condition_string}]"
            if node.entry.condition_string and node.entry.condition_string != "0"
            else ""
        )
        script = (
            f" [Script: {node.entry.user_script}]"
            if node.entry.user_script and node.entry.user_script != "0"
            else ""
        )
        structural_marker = "*" if node.is_structural else " "

        print(
            f'{prefix}{connector}[ID:{node.entry_id:04d}|Seq:{node.original_sequence:<15}|S:{structural_marker}] Aktør {actor_name}: "{dialogue_preview}"{conditions}{script}'
        )

        if node.children:
            new_prefix = prefix + ("    " if is_current_last else "│   ")
            print_conversation_tree_recursive(
                node.children, actor_mapping, new_prefix, True
            )


def find_conversations_for_actor(
    all_dialogues: list[DialogueEntry],
    actor_id_to_find: int,
    actor_mapping: dict,
    top_n: int = 10,
):
    logging.info(
        f"--- Søker etter samtaler for Aktør ID: {actor_id_to_find} ({actor_mapping.get(actor_id_to_find, 'Ukjent Navn')}) ---"
    )

    actor_conversations = defaultdict(list)
    for entry in all_dialogues:
        if entry.actor_id == actor_id_to_find:
            actor_conversations[entry.conversation_id].append(entry)

    if not actor_conversations:
        logging.info(f"Ingen samtaler funnet for Aktør ID: {actor_id_to_find}.")
        logging.info("------------------------------")
        return

    sorted_conversations = sorted(
        actor_conversations.items(), key=lambda item: len(item[1]), reverse=True
    )

    logging.info(
        f"Topp {top_n} mest aktive samtaler for Aktør ID: {actor_id_to_find} (sortert etter antall linjer av denne aktøren):"
    )
    for i, (conv_id, entries) in enumerate(sorted_conversations[:top_n]):
        total_lines_in_conv = sum(
            1 for e in all_dialogues if e.conversation_id == conv_id
        )
        logging.info(
            f"  {i + 1}. Samtale ID: {conv_id} (Aktøren har {len(entries)} linjer her, totalt {total_lines_in_conv} linjer i samtalen)"
        )
        for entry_idx, entry_line in enumerate(entries[:2]):
            dialogue_preview = entry_line.dialogue_text.replace("\n", " ").strip()
            if len(dialogue_preview) > 50:
                dialogue_preview = dialogue_preview[:47] + "..."
            logging.info(
                f'    Linje ID {entry_line.id} (Seq: {entry_line.sequence}): "{dialogue_preview}"'
            )

    logging.info(
        f"  (Totalt {len(sorted_conversations)} samtaler funnet med Aktør ID: {actor_id_to_find})"
    )
    logging.info("------------------------------")


def analyze_actor_condition_script_frequency(enriched_file_path):
    """
    Analyzes the enriched dialogue data to find the frequency of conditions
    and user scripts associated with each actor.

    Args:
        enriched_file_path (str): Path to the de_dialogue_enriched.csv file.
    """
    try:
        df_enriched = pd.read_csv(enriched_file_path)
    except FileNotFoundError:
        print(f"ERROR: Enriched dialogue file not found at: {enriched_file_path}")
        return
    except Exception as e:
        print(f"ERROR: Could not read enriched dialogue file: {e}")
        return

    # Fill NaN actor_names to avoid issues in grouping, replace with a placeholder
    df_enriched["actor_name"] = df_enriched["actor_name"].fillna("UNKNOWN_ACTOR")

    print("\n--- Psycho-Noir Kontrapunkt: Actor Condition/Script Analysis ---")
    print(f"Analyzing data from: {enriched_file_path}\n")

    # Calculate frequency of has_conditions per actor
    condition_counts = df_enriched[df_enriched["has_conditions"]][
        "actor_name"
    ].value_counts()

    # Calculate frequency of has_userscript per actor
    script_counts = df_enriched[df_enriched["has_userscript"]][
        "actor_name"
    ].value_counts()

    print(
        "--- Top 20 Actors by Frequency of Conditional Dialogues (has_conditions == True) ---"
    )
    if not condition_counts.empty:
        print(condition_counts.head(20).to_string())
    else:
        print("No conditional dialogues found.")
    print(
        "\n------------------------------------------------------------------------------------"
    )

    print(
        "\n--- Top 20 Actors by Frequency of Scripted Dialogues (has_userscript == True) ---"
    )
    if not script_counts.empty:
        print(script_counts.head(20).to_string())
    else:
        print("No scripted dialogues found.")
    print(
        "\n----------------------------------------------------------------------------------"
    )


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    actor_file_path = os.path.join(script_dir, "de_actors.csv")
    dialogue_file_path = os.path.join(script_dir, "de_structured_dialogue.csv")

    actor_mapping = load_actor_names_from_csv(actor_file_path)
    all_dialogues = load_dialogue_data(dialogue_file_path)

    if not all_dialogues:
        logging.error("Ingen dialogdata lastet. Avslutter.")
        return

    analyze_sequence_patterns(all_dialogues)

    find_conversations_for_actor(
        all_dialogues, actor_id_to_find=15, actor_mapping=actor_mapping
    )
    find_conversations_for_actor(
        all_dialogues, actor_id_to_find=3, actor_mapping=actor_mapping
    )
    find_conversations_for_actor(
        all_dialogues, actor_id_to_find=1, actor_mapping=actor_mapping
    )

    conversation_id_to_display = 1315  # Endret til 1315 for The Deserter
    logging.info(
        f"--- Forsøker å bygge og vise tre for Samtale ID: {conversation_id_to_display} ---"
    )
    conversation_tree_roots = build_conversation_tree(
        conversation_id_to_display, all_dialogues
    )

    if conversation_tree_roots:
        logging.info(
            f"--- Trestruktur for Samtale ID: {conversation_id_to_display} (med aktørnavn) ---"
        )
        print_conversation_tree_recursive(conversation_tree_roots, actor_mapping)
    else:
        logging.info(
            f"Ingen trestruktur kunne bygges for samtale ID: {conversation_id_to_display}."
        )

    enriched_dialogue_file = (
        "de_dialogue_enriched.csv"  # Assuming it's in the same directory
    )
    analyze_actor_condition_script_frequency(enriched_dialogue_file)


if __name__ == "__main__":
    main()
