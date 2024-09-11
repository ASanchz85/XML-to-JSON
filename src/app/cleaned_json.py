import os
import json
import re


# Function to clean up the nested structure in the JSON
def clean_json_structure(data):
    try:
        quiz_modus = data.get("quizModus", "")
        title = data.get("title", "")
        questions = data.get("questions", [])

        # Parse and format the title
        activity_id, description = parse_title(title)

        cleaned_questions = []

        for question in questions:
            # Clean the question text
            question_description, question_text = clean_question_text(
                question.get("questionText", {}).get("questionText", "")
            )

            if question_text is None:
                question_text = ""

            if question_description is None:
                question_description = ""

            # Determine if the question has audio or video
            has_audio, audio_link = check_for_audio(activity_id, question_text)
            has_video, video_link = check_for_video(activity_id, question_text)

            cleaned_question = {
                "title": question.get("title", {}).get("title", ""),
                "points": question.get("points", {}).get("points", ""),
                "questionText": question_text,
                "questionDescription": question_description,
                "hasAudio": has_audio,
                "audioLink": audio_link,
                "hasVideo": has_video,
                "videoLink": video_link,
                "answers": [],
            }

            # Clean up the answers structure
            answers = question.get("answers", {}).get("answer", [])

            if answers is None:
                answers = []

            # If 'answers' is a dictionary, wrap it in a list to handle both cases
            if isinstance(answers, dict):
                answers = [answers]

            for answer in answers:
                answer_text = answer.get("answerText", {}).get("answerText", "")
                stort_text = answer.get("stortText", {}).get("stortText", "")

                # Handle potential null values by replacing them with an empty string
                if answer_text is None:
                    answer_text = ""
                if stort_text is None:
                    stort_text = ""

                cleaned_answer = {"answerText": answer_text, "stortText": stort_text}
                cleaned_question["answers"].append(cleaned_answer)

            cleaned_questions.append(cleaned_question)

        # Return the cleaned structure
        cleaned_data = {
            "quizModus": quiz_modus,
            "activity_id": activity_id,  # Add activity_id
            "description": description,  # Add description
            "questions": cleaned_questions,
        }

        return cleaned_data, activity_id

    except KeyError as e:
        print(f"Missing key: {e}")
        return None, None
    except Exception as e:
        print(
            f"An error occurred: {e}, while processing the JSON file: {data.get('title')}"
        )
        return None, None


# Function to clean the questionText by extracting text between <h3> and <h4> tags
def clean_question_text(question_text):
    if question_text is None:
        return [], ""  # Return empty array and empty string if questionText is None

    # Find all <h3> and <h4> content
    matches = re.findall(r"<h[34]>(.*?)<\/h[34]>", question_text, re.DOTALL)

    # Clean up and remove unnecessary whitespace from the matches
    cleaned_matches = [match.strip() for match in matches]

    # Combine all matches into a single string as questionText
    combined_text = " ".join(cleaned_matches)

    return cleaned_matches, combined_text


# Function to parse the title and split it into activity_id and description
def parse_title(title):
    description = title.split(" ", 1)
    parts = title.split(".")

    if len(description) > 1:
        description = description[1].strip()
    else:
        description = ""

    # Handle cases where there might be an empty part due to trailing period
    if len(parts) == 5:
        activity_id = parts[0] + "." + "".join(parts[1:4])
    elif len(parts) == 4:
        activity_id = parts[0] + "." + "".join(parts[1:3])
    elif len(parts) == 3:
        activity_id = parts[0] + "." + parts[1]
    else:
        activity_id = parts[0]

    # Remove any trailing periods just in case
    activity_id = activity_id.rstrip(".")
    return activity_id, description


# Function to check if questionText has "listen" and return appropriate audio info
def check_for_audio(title, question_text):
    if re.search(r"listen", question_text, re.IGNORECASE):
        return True, f"{title}.mp3"
    return False, None


# Function to check if questionText has "watch" and return appropriate video info
def check_for_video(title, question_text):
    if re.search(r"watch", question_text, re.IGNORECASE):
        return True, f"{title}.mp4"
    return False, None


# Function to clean all JSON files in the directory and subdirectories
# Function to clean all JSON files in the directory and subdirectories
def clean_json_files(
    input_folder, output_folder, error_log_file="error_cleaned_log.txt"
):
    file_counter = 0

    with open(error_log_file, "w") as log_file:
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
                    try:
                        with open(input_file_path, "r") as input_file:
                            data = json.load(input_file)

                            # Clean the JSON structure and get formatted title
                            cleaned_data, formatted_title = clean_json_structure(data)

                            if cleaned_data and formatted_title:
                                # Use formatted title for the output file name
                                output_file_name = f"{formatted_title}.json"
                                output_file_path = os.path.join(
                                    output_subdir, output_file_name
                                )

                                # Write the cleaned data to the output folder, preserving folder structure
                                with open(output_file_path, "w") as output_file:
                                    json.dump(cleaned_data, output_file, indent=4)
                                print(f"Processed {filename} -> {output_file_name}")
                            else:
                                print(f"Skipped {filename} due to missing keys\n")
                                log_file.write(
                                    f"Skipped {filename} in path {input_file_path} due to missing keys\n"
                                )

                    except json.JSONDecodeError:
                        log_file.write(f"Error decoding JSON in file: {filename}\n")
                    except Exception as e:
                        log_file.write(f"Error processing {filename}: {str(e)}\n")

    return file_counter
