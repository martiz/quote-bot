import random
import sys
import textwrap
import re # Import the regular expression module

FILENAME = "quotes.txt"
BOX_WIDTH = 80 # Total width for the box including borders


def get_random_quote(filename):
    """
    Reads quotes from a file, selects one randomly, and returns it
    along with the total count.

    Args:
        filename (str): The path to the file containing quotes.

    Returns:
        tuple: A tuple containing (random_quote, total_count),
               or (None, 0) if an error occurs or no quotes are found.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        quotes = [
            block.strip()
            for block in content.split("\n\n")
            if block.strip()
        ]

        if not quotes:
            print(f"Error: No quotes found in '{filename}'.")
            return None, 0

        random_quote = random.choice(quotes)
        total_count = len(quotes)

        return random_quote, total_count

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, 0


# Updated main function with Markdown link filtering
def main():
    quote, count = get_random_quote(FILENAME)

    if quote:
        # --- Filter out Markdown links ---
        # Pattern: \[   Match a literal '['
        #          (.+?) Match any character (.), one or more times (+), non-greedily (?)
        #                and capture it in group 1 ()
        #          \]   Match a literal ']'
        #          \(   Match a literal '('
        #          .+?  Match any character, one or more times, non-greedily (the URL)
        #          \)   Match a literal ')'
        markdown_link_pattern = r'\[(.+?)\]\(.+?\)'
        # Replace the matched pattern with just the captured link text (group 1)
        cleaned_quote = re.sub(markdown_link_pattern, r'\1', quote)
        # --- End filtering ---

        # Calculate the width available for text inside the box
        text_width = BOX_WIDTH - 6
        if text_width <= 0:
            print("Error: BOX_WIDTH is too small to display text.")
            sys.exit(1)

        # Create the horizontal border string (+---+ style)
        border_top = "┌" + "─" * (BOX_WIDTH - 2) + "┐"
        border_bottom = "└" + "─" * (BOX_WIDTH - 2) + "┘"

        # Prepare lines for wrapping using the CLEANED quote
        original_lines = cleaned_quote.split('\n')
        wrapped_lines = []
        for line in original_lines:
            # Wrap each original line if it's too long
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


        print("\n=== Random Quote ===")
        print(border_top) # Top border
        for line in wrapped_lines:
            # Print each line formatted within the fixed-width box
            print(f"│  {line:<{text_width}}  │") # Add 2 spaces padding
        print(border_bottom) # Bottom border

        print(f"\n(Total quotes found in '{FILENAME}': {count})\n")
    else:
        # Error message already printed by the function
        sys.exit(1)


# Call main() ONLY when the script is executed directly
if __name__ == "__main__":
    main()
