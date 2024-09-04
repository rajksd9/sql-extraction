import re
import json
import sys

def extract_sql_information(sql_content):
    output_data = []
    statement_id = 0
    create_insert_update_regex = re.compile(r'^\s*(CREATE|INSERT|UPDATE)\s+', re.IGNORECASE)
    table_name_regex = re.compile(r'\b(FROM|JOIN)\s+(\w+)', re.IGNORECASE)
    target_table_regex = re.compile(r'^\s*(INSERT\s+INTO|UPDATE)\s+(\w+)', re.IGNORECASE)

    # Split the SQL file into statements (assuming ';' is the delimiter)
    sql_statements = sql_content.split(';')
    for statement in sql_statements:
        statement = statement.strip()
        if not statement:
            continue

        statement_id += 1
        statement_type = None
        target_table = None
        source_tables = []

        # Check if it's a CREATE, INSERT, or UPDATE statement
        if create_insert_update_regex.search(statement):
            match_type = create_insert_update_regex.search(statement)
            statement_type = match_type.group(1).lower()

            target_match = target_table_regex.search(statement)
            if target_match:
                target_table = target_match.group(2)
            source_matches = table_name_regex.findall(statement)
            source_tables.extend([{"type": match[0].lower(), "source_table_name": match[1]} for match in source_matches])

        if statement_type and (target_table or source_tables):
            entry = {
                "statement_id": statement_id,
                "statement_type": statement_type,
                "table_name": []
            }

            if target_table:
                entry["table_name"].append({"target_table_name": target_table})

            if source_tables:
                entry["table_name"].extend(source_tables)

            output_data.append(entry)

    return output_data

def main():
    
    sql_file =input("Enter the path to the file.")
    with open(sql_file, 'r') as file:
        sql_content = file.read()
    extracted_data = extract_sql_information(sql_content)
    output_filename = sql_file.replace('.sql', '.json')
    with open(output_filename, 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print(f"Extraction complete. Output written to {output_filename}")

if __name__ == "__main__":
    main()
