import os
import json

# Define the input and output folder paths
input_folder = './output_json-A1-grammar'
output_folder = './parsed_json-A1-grammar'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to extract the required data
def extract_required_data(data):
    try:
        # Extract the desired fields
        quiz_modus = data["wpProQuiz"]["data"]["quiz"]["quizModus"]["quizModus"]  # Extract quizModus value
        title = data["wpProQuiz"]["data"]["quiz"]["title"]["title"]
        
        # Extract questions if they exist
        questions = data["wpProQuiz"]["data"].get("questions", {}).get("question", [])

        # Create the final JSON structure
        extracted_data = {
            "quizModus": quiz_modus,
            "title": title,
            "questions": questions  # Include questions if they exist, otherwise leave empty
        }

        return extracted_data
    except KeyError as e:
        print(f"Missing key: {e}")
        return None

# Iterate over all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        input_file_path = os.path.join(input_folder, filename)
        
        # Read the input JSON file
        with open(input_file_path, 'r') as input_file:
            try:
                data = json.load(input_file)
                
                # Extract the required data
                extracted_data = extract_required_data(data)
                
                if extracted_data:
                    # Write the extracted data to the output folder
                    output_file_path = os.path.join(output_folder, filename)
                    with open(output_file_path, 'w') as output_file:
                        json.dump(extracted_data, output_file, indent=4)
                    print(f"Processed {filename}")
                else:
                    print(f"Skipped {filename} due to missing keys")
            
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")
