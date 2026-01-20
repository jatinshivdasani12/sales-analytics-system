# utils/file_handler.py

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """

    encodings = ["utf-8", "latin-1", "cp1252"]
    lines = None

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    if not lines:
        return []

    # Skip header + remove empty lines
    cleaned_lines = []
    for line in lines[1:]:
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines
