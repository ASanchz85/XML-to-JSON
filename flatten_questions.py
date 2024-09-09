import os
import json
import re
from bs4 import BeautifulSoup

# Function to parse and flatten the `questionText`
def flatten_question_text(question_text):
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(question_text, 'html.parser')
    
    # Prepare a dictionary to store the extracted elements
    result = {}

    # Extract image tags
    images = []
    for img in soup.find_all('img'):
        images.append({
            'src': img.get('src'),
            'alt': img.get('alt'),
            'width': img.get('width'),
            'height': img.get('height')
        })
    if images:
        result['images'] = images

    # Extract audio tags
    audio = []
    for tag in re.findall(r'\[audio.*?mp3="(.*?)"\]', question_text):
        audio.append({
            'src': tag
        })
    if audio:
        result['audio'] = audio

    # Extract headings (h3, h4)
    headings = {}
    if soup.find('h3'):
        headings['h3'] = soup.find('h3').text.strip()
    if soup.find('h4'):
        headings['h4'] = [h4.text.strip() for h4 in soup.find_all('h4')]
    
    if headings:
        result['headings'] = headings

    return result

# Function to process JSON files in a folder
def process_json_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            
            # Load the JSON content
            with open(input_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            
            # Process the questionText fields
            for question in data.get('questions', []):
                question_text = question.get('questionText', {})
                
                # Check if `questionText` is a string or a dictionary
                if isinstance(question_text, dict):
                    question_text = question_text.get('questionText', "")
                elif isinstance(question_text, str):
                    # In case it's already a string, use it directly
                    question_text = question_text
                
                if question_text:
                    flattened_text = flatten_question_text(question_text)
                    question['questionText'] = {'flattened': flattened_text}  # Replace with flattened data

            # Save the modified JSON file to the output folder
            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(data, output_file, ensure_ascii=False, indent=4)

# Define the input and output folders
input_folder = "./parsed_json-A1-grammar"
output_folder = "./flatten_json-A1-grammar"

# Run the processing function
process_json_files(input_folder, output_folder)
