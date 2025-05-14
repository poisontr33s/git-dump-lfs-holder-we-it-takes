import sqlite3
import os
import csv

# Define paths
db_path = r"c:\Users\eldno\Downloads\PROJECTS\LÆRE_HTML\dealogue-db-tfc-21-03-30\discobase3-29-2021-9-32-09-PM.db"
# Output path for the new CSV file
output_csv_path = (
    r"c:\Users\eldno\Downloads\PROJECTS\LÆRE_HTML\de_structured_dialogue.csv"
)

# Columns to extract from the dentries table
columns_to_extract = [
    "id",
    "conversationid",
    "actor",
    "conversant",
    "dialoguetext",
    "sequence",
    "conditionstring",
    "userscript",
    "isgroup",
    "hascheck",
    "hasalts",
]


def extract_dialogue_data(conn, output_csv_path):
    """Extracts dialogue data from the dentries table and saves to CSV."""
    cursor = conn.cursor()

    # Construct the SQL query dynamically
    sql_query = f"SELECT {', '.join(columns_to_extract)} FROM dentries"
    print(
        f"INFO: Henter strukturerte data fra tabellen 'dentries' med spørringen: {sql_query}"
    )
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    if not rows:
        print(
            "ADVARSEL: Ingen rader hentet fra dentries. Sjekk tabellnavn og kolonnenavn."
        )

    # Write the data to a CSV file
    with open(output_csv_path, "w", encoding="utf-8", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(columns_to_extract)

        if rows:
            for row_data in rows:
                # Process each piece of data in the row
                processed_row = []
                for item in row_data:
                    if isinstance(item, str):
                        # Replace escaped newlines and carriage returns for string items
                        processed_item = item.replace("\\n", "\n").replace("\\r", "")
                        processed_row.append(processed_item)
                    elif item is None:
                        processed_row.append(
                            ""
                        )  # Represent None as an empty string in CSV
                    else:
                        processed_row.append(item)  # Keep other types (int, bool) as is
                csv_writer.writerow(processed_row)

    if rows:
        print(f"Strukturerte data hentet og skrevet til {output_csv_path}")
    else:
        print(
            f"Ingen data ble skrevet til {output_csv_path} da ingen rader ble hentet."
        )

    # Check file size
    if os.path.exists(output_csv_path):
        file_size = os.path.getsize(output_csv_path)
        print(f"Størrelsen på {output_csv_path} er {file_size} bytes.")
        if file_size == 0 and rows:
            print(
                f"ADVARSEL: {output_csv_path} er tom, selv om rader ble hentet. Sjekk datainnhold og skriveprosess."
            )
        elif file_size == 0 and not rows:
            print(
                f"INFO: {output_csv_path} er tom, som forventet da ingen rader ble hentet."
            )
        elif file_size < 1000 and rows:  # Arbitrary small size, adjust as needed
            print(
                f"INFO: {output_csv_path} er ganske liten ({file_size} bytes). Verifiser at dette er forventet."
            )


def extract_actors_data(conn, output_csv_path):
    """Extracts actor ID and name from the actors table and saves to CSV."""
    print(f"INFO: Starter uthenting av aktørdata til {output_csv_path}")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name FROM actors;")
        actors_data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"ERROR: Kunne ikke hente data fra actors tabellen: {e}")
        return

    if not actors_data:
        print("INFO: Ingen data funnet i actors tabellen.")
        return

    with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["id", "name"])  # Header
        csv_writer.writerows(actors_data)
    print(f"INFO: {len(actors_data)} aktører lagret i {output_csv_path}")


def main():
    db_path = r"c:\Users\eldno\Downloads\PROJECTS\LÆRE_HTML\dealogue-db-tfc-21-03-30\discobase3-29-2021-9-32-09-PM.db"
    output_dialogue_csv_path = (
        r"c:\Users\eldno\Downloads\PROJECTS\LÆRE_HTML\de_structured_dialogue.csv"
    )
    output_actors_csv_path = (
        r"c:\Users\eldno\Downloads\PROJECTS\LÆRE_HTML\de_actors.csv"
    )

    if not os.path.exists(db_path):
        print(f"ERROR: Databasen ble ikke funnet på {db_path}")
        return

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        print(f"INFO: Koblet til database: {db_path}")

        extract_dialogue_data(conn, output_dialogue_csv_path)
        extract_actors_data(conn, output_actors_csv_path)  # Nytt kall

    except sqlite3.Error as e:
        print(f"ERROR: Databasefeil: {e}")
    finally:
        if conn:
            conn.close()
            print("INFO: Databasetilkobling lukket.")


if __name__ == "__main__":
    main()
