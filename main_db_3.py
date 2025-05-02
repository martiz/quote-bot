import random
import sys
import textwrap
import re
import sqlite3
import os # Import os module

# Constants (BOX_WIDTH can remain)
TABLE_NAME = "quotes" # Assuming the table name is consistent
BOX_WIDTH = 80
ALLOWED_DB_EXTENSIONS = ('.db', '.sqlite', '.sqlite3')


def find_quote_databases(directory="."):
    """
    Scans the specified directory for files with SQLite extensions.

    Args:
        directory (str): The directory path to scan. Defaults to current dir.

    Returns:
        list: A sorted list of filenames matching the allowed extensions.
    """
    found_dbs = []
    try:
        for filename in os.listdir(directory):
            # Check if it's a file and has the right extension
            if os.path.isfile(os.path.join(directory, filename)):
                _ , ext = os.path.splitext(filename)
                if ext.lower() in ALLOWED_DB_EXTENSIONS:
                    found_dbs.append(filename)
    except FileNotFoundError:
        print(f"Error: Directory not found: {directory}")
        return []
    except Exception as e:
        print(f"Error scanning directory '{directory}': {e}")
        return []
    return sorted(found_dbs) # Return sorted list


def display_menu_and_get_choice(db_list):
    """
    Displays a numbered menu of database files and prompts the user
    for a selection.

    Args:
        db_list (list): A list of database filenames.

    Returns:
        str: The filename chosen by the user, or None if invalid input/exit.
    """
    print("\n--- Available Quote Databases ---")
    for i, db_name in enumerate(db_list, start=1):
        print(f"{i}. {db_name}")
    print("-------------------------------")

    while True:
        try:
            choice_str = input(f"Enter the number of the database to use (1-{len(db_list)}): ")
            choice = int(choice_str)
            if 1 <= choice <= len(db_list):
                # Adjust index for 0-based list
                selected_db = db_list[choice - 1]
                return selected_db
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(db_list)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except (EOFError, KeyboardInterrupt): # Handle Ctrl+D or Ctrl+C
             print("\nExiting.")
             return None


# --- Function to get quote from DB (mostly unchanged) ---
def get_random_quote_from_db(db_filename):
    """
    Connects to the SQLite database, selects a random quote,
    and returns it along with the total count.

    Args:
        db_filename (str): The path to the SQLite database file.

    Returns:
        tuple: A tuple containing (random_quote_text, total_count),
               or (None, 0) if an error occurs or no quotes are found.
    """
    conn = None
    try:
        # Basic check if file exists before connecting
        if not os.path.exists(db_filename):
             print(f"Error: Database file '{db_filename}' not found.")
             return None, 0

        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Check if the table exists first
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (TABLE_NAME,))
        if cursor.fetchone() is None:
            print(f"Error: Table '{TABLE_NAME}' not found in database '{db_filename}'.")
            print("Was this database created correctly with the conversion script?")
            return None, 0

        # Get total count
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count_result = cursor.fetchone()
        total_count = count_result[0] if count_result else 0

        if total_count == 0:
            print(f"Error: No quotes found in table '{TABLE_NAME}' in database '{db_filename}'.")
            return None, 0

        # Select a random quote text
        cursor.execute(f"SELECT text FROM {TABLE_NAME} ORDER BY RANDOM() LIMIT 1")
        quote_result = cursor.fetchone()

        if quote_result:
            random_quote_text = quote_result[0]
            return random_quote_text, total_count
        else:
            print("Error: Could not fetch a random quote despite count > 0.")
            return None, total_count

    except sqlite3.Error as e:
        print(f"Database error accessing '{db_filename}': {e}")
        return None, 0
    except Exception as e:
        print(f"An unexpected error occurred with '{db_filename}': {e}")
        return None, 0
    finally:
        if conn:
            conn.close()
# --- End of DB function ---


# --- Main execution logic ---
def main():
    # 1. Find available databases
    available_databases = find_quote_databases()

    if not available_databases:
        print("No SQLite quote databases (.db, .sqlite, .sqlite3) found in the current directory.")
        print("Please run the conversion script first or place a database file here.")
        sys.exit(1)

    # 2. Display menu and get user choice
    selected_db_file = display_menu_and_get_choice(available_databases)

    if selected_db_file is None:
        # User chose to exit or input was invalid repeatedly
        sys.exit(1)

    print(f"\nUsing database: '{selected_db_file}'")

    # 3. Get quote from the selected database
    quote, count = get_random_quote_from_db(selected_db_file)

    # 4. Process and display the quote (if found)
    if quote:
        # Filter Markdown links
        markdown_link_pattern = r'\[(.+?)\]\(.+?\)'
        cleaned_quote = re.sub(markdown_link_pattern, r'\1', quote)

        # Prepare for boxing
        text_width = BOX_WIDTH - 6
        if text_width <= 0:
            print("Error: BOX_WIDTH is too small to display text.")
            sys.exit(1)

        border = "+" + "-" * (BOX_WIDTH - 2) + "+"

        # Wrap text
        original_lines = cleaned_quote.split('\n')
        wrapped_lines = []
        for line in original_lines:
            wrapped = textwrap.wrap(
                line,
                width=text_width,
                replace_whitespace=False,
                drop_whitespace=False,
                break_long_words=True,
                break_on_hyphens=True
            )
            if not line.strip() and not wrapped:
                wrapped_lines.append("")
            else:
                wrapped_lines.extend(wrapped)

        # Print boxed quote
        print("\n--- Random Quote ---")
        print(border)
        for line in wrapped_lines:
            print(f"|  {line:<{text_width}}  |")
        print(border)

        # Print count info
        print(f"\nTotal quotes found in database '{selected_db_file}': {count}")
    else:
        # Error messages printed within get_random_quote_from_db
        print(f"Could not retrieve a quote from '{selected_db_file}'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
