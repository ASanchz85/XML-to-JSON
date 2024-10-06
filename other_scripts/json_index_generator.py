import os
import json
import sys


def create_index_for_folder(parent_folder):
    # Iterate through the folders inside the parent folder
    for folder_name in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder_name)

        if os.path.isdir(folder_path):
            # Create a list to hold all JSON filenames in the subfolder
            json_files = sorted(
                [f for f in os.listdir(folder_path) if f.endswith(".json")]
            )

            # Create the JSON structure
            index = {
                "unit_name": os.path.basename(parent_folder),
                "course_type": folder_name,
                "activity_index": json_files,
            }

            # Define the output path
            output_file_path = os.path.join(parent_folder, f"{folder_name}_index.json")

            # Write the index JSON to a file
            with open(output_file_path, "w") as json_file:
                json.dump(index, json_file, indent=4)

            print(f"Index for '{folder_name}' saved to: {output_file_path}")


# Check if the path argument was provided
if len(sys.argv) < 2:
    print("Usage: python3 json_index_summary.py /path/to/parent/folder")
    sys.exit(1)

# Get the parent folder path from the command-line argument
parent_folder_path = os.path.expanduser(sys.argv[1])

# Call the function
create_index_for_folder(parent_folder_path)


# how to use ?

# go to the folder in which you want to apply the effect of the script.
# python3 ~/path-to-use/json_index_generator.py $(pwd)
