import time

from src.config.config import INPUT_XML_FOLDER, JSON_FOLDER, OUTPUT_FOLDER
from src.utils.utils import clear_screen
from src.app.xml_to_json import convert_xml_to_json
from src.app.parsed_json import filters_target_json


def main():
    """Main function to convert XML files to JSON and filter the target JSON format"""

    start_time = time.time()
    clear_screen()

    total_files_converted = convert_xml_to_json(INPUT_XML_FOLDER, JSON_FOLDER)
    total_files_parsed = filters_target_json(JSON_FOLDER, OUTPUT_FOLDER)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nConversion completed! Total files converted: {total_files_converted}")
    print(f"Parsing completed! Total files parsed: {total_files_parsed}")
    print(
        f"Job completed in {elapsed_time:.2f} seconds! Check the output folder: {OUTPUT_FOLDER}"
    )


if __name__ == "__main__":
    main()
