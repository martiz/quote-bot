import random
import sys
import textwrap

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
        # Read the entire file content.
        # Using utf-8 encoding is safer for diverse characters.
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # Split the content by two or more newlines (blank lines).
        # Filter out any empty strings that might result from splitting.
        quotes = [
            block.strip()
            for block in content.split("\n\n")
            if block.strip()
        ]

        if not quotes:
            print(f"Error: No quotes found in '{filename}'.")
            return None, 0

        # Select a random quote from the list
        random_quote = random.choice(quotes)
        total_count = len(quotes)

        return random_quote, total_count

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, 0

"""
# Define the main execution logic within a function
def main():
    quote, count = get_random_quote(FILENAME) # Capture return values

    if quote:
        print("--- Random Quote ---")
        print(quote)
        print("--------------------")

*****

# Updated main function with box drawing
def main():
    quote, count = get_random_quote(FILENAME)
    if quote:
        lines = quote.split("\n")
        # Find the widest line to set the box width
        # Add 2 for padding spaces inside the box (| quote |)
        if lines:
             # Calculate max_len based on actual lines
             max_len = max(len(line) for line in lines)
        else:
             # Handle case where quote might be empty after split (unlikely here)
             max_len = 0

        # Create the horizontal border string (+---+ style)
        # Width is max_len + 2 spaces inside
        border = "+" + "-" * (max_len + 2) + "+"

        print("\n--- Random Quote ---")
        print(border) # Top border
        for line in lines:
            # Print each line formatted within the box
            # Pad the line with spaces to match max_len for alignment
            print(f"| {line:<{max_len}} |")
        print(border) # Bottom border
"""

def main():
    quote, count = get_random_quote(FILENAME)
    if quote:
        # Calculate the width available for text inside the box
        # BOX_WIDTH - 2 for '+', - 2 for '|', - 2 for spaces ' ' = BOX_WIDTH - 6
        text_width = BOX_WIDTH - 6
        if text_width <= 0:
             print("Error: BOX_WIDTH is too small to display text.")
             sys.exit(1)

        # Create the horizontal border string (+---+ style)
        # Width is BOX_WIDTH - 2 for the '+' corners
        border = "+" + "-" * (BOX_WIDTH - 2) + "+"

        # Prepare lines for wrapping
        original_lines = quote.split('\n')
        wrapped_lines = []
        for line in original_lines:
            # Wrap each original line if it's too long
            # drop_whitespace=False prevents collapsing multiple spaces
            # replace_whitespace=False keeps existing spaces
            wrapped = textwrap.wrap(
                line,
                width=text_width,
                replace_whitespace=False,
                drop_whitespace=False,
                break_long_words=True, # Break words if necessary
                break_on_hyphens=True # Allow breaks at hyphens
            )
            # If a line was empty originally, wrap returns [], add an empty line back
            if not line.strip() and not wrapped:
                 wrapped_lines.append("")
            else:
                 wrapped_lines.extend(wrapped) # Add the wrapped lines to our list

        print("\n=== Random Quote ===")
        print(border) # Top border
        for line in wrapped_lines:
            # Print each line formatted within the fixed-width box
            # Pad the line with spaces to match text_width for alignment
            print(f"|  {line:<{text_width}}  |") # Add 2 spaces padding
        print(border) # Bottom border
        
        print(f"\n(Total quotes found in '{FILENAME}': {count})\n")
    else:
        # Error message already printed by the function
        sys.exit(1) # Exit with a non-zero code to indicate failure


# Call main() ONLY when the script is executed directly
if __name__ == "__main__":
    main()
