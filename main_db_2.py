import random
import sys
import textwrap
import re
import sqlite3 # Import the sqlite3 module

# Change filename constant
DB_FILENAME = "quotes_2.db"
TABLE_NAME = "quotes" # Added table name constant
BOX_WIDTH = 80


# --- Updated function to get quote from DB ---
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
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Get total count first
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count_result = cursor.fetchone()
        total_count = count_result[0] if count_result else 0

        if total_count == 0:
            print(f"Error: No quotes found in table '{TABLE_NAME}' in database '{db_filename}'.")
            print("Did you run the conversion script first?")
            return None, 0

        # Select a random quote text
        # ORDER BY RANDOM() is a simple way to get a random row in SQLite
        cursor.execute(f"SELECT text FROM {TABLE_NAME} ORDER BY RANDOM() LIMIT 1")
        quote_result = cursor.fetchone()

        if quote_result:
            random_quote_text = quote_result[0] # fetchone returns a tuple
            return random_quote_text, total_count
        else:
            # Should not happen if count > 0, but good to handle
            print("Error: Could not fetch a random quote despite count > 0.")
            return None, total_count

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        # Check if the error is because the table doesn't exist
        if "no such table" in str(e).lower():
             print(f"Error: Table '{TABLE_NAME}' not found in '{db_filename}'.")
             print("Please run the conversion script first.")
        return None, 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, 0
    finally:
        if conn:
            conn.close()
# --- End of updated function ---


# Main function now calls the DB function
def main():
    # Call the new function using the DB filename
    quote, count = get_random_quote_from_db(DB_FILENAME)

    if quote:
        # --- Filter out Markdown links (same as before) ---
        markdown_link_pattern = r'\[(.+?)\]\(.+?\)'
        cleaned_quote = re.sub(markdown_link_pattern, r'\1', quote)
        # --- End filtering ---

        text_width = BOX_WIDTH - 6
        if text_width <= 0:
            print("Error: BOX_WIDTH is too small to display text.")
            sys.exit(1)

        border = "+" + "-" * (BOX_WIDTH - 2) + "+"

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


        print("\n--- Random Quote ---")
        print(border)
        for line in wrapped_lines:
            print(f"|  {line:<{text_width}}  |")
        print(border)

        # Update the source filename in the output message
        print(f"\nTotal quotes found in database '{DB_FILENAME}': {count}")
    else:
        # Error messages are now printed within get_random_quote_from_db
        sys.exit(1)


if __name__ == "__main__":
    main()
