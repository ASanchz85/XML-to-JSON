import os
import json


# Function to extract the required data
def extract_required_data(data):
    try:
        # Extract the desired fields
        quiz_modus = data["wpProQuiz"]["data"]["quiz"]["quizModus"][
            "quizModus"
        ]  # Extract quizModus value
        title = data["wpProQuiz"]["data"]["quiz"]["title"]["title"]

        # Extract questions if they exist
        questions = (
            data["wpProQuiz"]["data"]["quiz"].get("questions", {}).get("question", [])
        )

        # Check if 'questions' is a dictionary (single object), if so, wrap it in a list
        if isinstance(questions, dict):
            questions = [questions]

        # Filter the required fields from each question
        filtered_questions = []
        for question in questions:
            # Ensure the fields are dictionaries before trying to call .get()
            filtered_question = {
                "title": question.get("title", {}),
                "points": question.get("points", {}),
                "questionText": question.get("questionText", {}),
                "answers": question.get("answers", {}),
            }
            filtered_questions.append(filtered_question)

        # Create the final JSON structure
        extracted_data = {
            "quizModus": quiz_modus,
            "title": title,
            "questions": filtered_questions,
        }

        return extracted_data
    except KeyError as e:
        print(f"Missing key: {e}")
        return None


def filters_target_json(input_folder, output_folder):
    """Parses JSON files to the desired and filtered JSON format, while preserving folder structure."""
    file_counter = 0

    for root_dir, subdirs, files in os.walk(input_folder):
        # Calculate the relative path from the root directory
        relative_path = os.path.relpath(root_dir, input_folder)

        # Create the corresponding folder in the output directory
        output_subdir = os.path.join(output_folder, relative_path)
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)

        for filename in files:
            if filename.endswith(".json"):
                file_counter += 1
                input_file_path = os.path.join(root_dir, filename)

                # Read the input JSON file
                with open(input_file_path, "r") as input_file:
                    try:
                        data = json.load(input_file)

                        # Extract the required data
                        extracted_data = extract_required_data(data)

                        if extracted_data:
                            # Write the extracted data to the output folder, preserving folder structure
                            output_file_path = os.path.join(output_subdir, filename)
                            with open(output_file_path, "w") as output_file:
                                json.dump(extracted_data, output_file, indent=4)
                            print(f"Processed {filename}")
                        else:
                            print(f"Skipped {filename} due to missing keys")

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {filename}")

    return file_counter
