import os
import json
from collections import defaultdict

def count_keys_in_json(obj, key_counter):
    """
    Recursively traverse a dictionary or list and count occurrences of each key.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_counter[key] += 1
            count_keys_in_json(value, key_counter)
    elif isinstance(obj, list):
        for item in obj:
            count_keys_in_json(item, key_counter)

def get_unique_keys_with_counts(json_folder):
    """
    Iterate over all JSON files in a folder and return a dictionary of key counts.
    """
    key_counter = defaultdict(int)  # To store the count of each key

    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            json_path = os.path.join(json_folder, filename)

            # Load JSON data from the file
            with open(json_path, "r") as json_file:
                json_data = json.load(json_file)

            # Recursively count keys
            count_keys_in_json(json_data, key_counter)

    return key_counter

def save_key_summary_to_json(output_path, key_counts):
    """
    Save the key count summary to a new JSON file.
    """
    with open(output_path, "w") as json_output_file:
        json.dump(key_counts, json_output_file, indent=4)

# Specify the folder containing the JSON files and the output path for the summary file
json_folder = "./output_json-A1-grammar"       # Update with your JSON folder path
output_summary_file = "summary_output-A1-grammar.json"  # Path to save the summary JSON file

# Get the key counts
key_counts = get_unique_keys_with_counts(json_folder)

# Save the key summary to a new JSON file
save_key_summary_to_json(output_summary_file, key_counts)

print(f"Summary of keys has been saved to {output_summary_file}")
