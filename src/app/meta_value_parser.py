import os
import json

def parse_meta_value(meta_value):
    """
    Parses the meta_value string into a proper JSON format if it is a string.
    """
    try:
        # Try to load the meta_value as JSON
        parsed_value = json.loads(meta_value)
        return parsed_value
    except json.JSONDecodeError:
        # If it's not a JSON string, return the value unchanged
        return meta_value

def process_json_file(json_data):
    """
    Processes a single JSON data object and parses the meta_value strings into JSON objects.
    """
    # Traverse the JSON structure and locate 'meta_value'
    if 'wpProQuiz' in json_data:
        if 'data' in json_data['wpProQuiz']:
            if 'quiz' in json_data['wpProQuiz']['data']:
                if 'post_meta' in json_data['wpProQuiz']['data']['quiz']:
                    for meta_item in json_data['wpProQuiz']['data']['quiz']['post_meta']:
                        if 'meta_value' in meta_item:
                            # Parse the meta_value as JSON if it's a string
                            meta_item['meta_value']['meta_value'] = parse_meta_value(meta_item['meta_value']['meta_value'])

    return json_data

def process_json_files_in_folder(input_folder, output_folder):
    """
    Iterates over all JSON files in a folder, processes each one, and saves the updated files to a new folder.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load JSON data from the file
            with open(input_path, "r") as json_file:
                json_data = json.load(json_file)

            # Process the JSON data
            updated_data = process_json_file(json_data)

            # Save the updated JSON to the output folder
            with open(output_path, "w") as output_file:
                json.dump(updated_data, output_file, indent=4)

            print(f"Processed and saved: {output_path}")

# Set the input and output folder paths
input_folder = "./output_json-A1-grammar"       # Replace with your input folder containing the JSON files
output_folder = "./mata_values-parsed"     # Replace with the folder where you want to save the updated JSON files

# Process the files
process_json_files_in_folder(input_folder, output_folder)
