def read_sales_data(filename):
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                lines = file.readlines()

            cleaned_lines = [
                line.strip() for line in lines[1:]
                if line.strip()
            ]
            return cleaned_lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")
            return []

    print("Error: unable to read file with supported encodings.")
    return []


# ✅ ADD THIS WRAPPER FUNCTION (IMPORTANT)
def read_sales_file(filename):
    return read_sales_data(filename)
