import time
import signal
import sys

from src.config.config import (
    INPUT_XML_FOLDER,
    JSON_FOLDER,
    OUTPUT_FOLDER,
    CLEANED_FOLDER,
)
from src.utils.utils import clear_screen

from src.app.xml_to_json import convert_xml_to_json
from src.app.parsed_json import filters_target_json
from src.app.cleaned_json import clean_json_files


def signal_handler(sig, frame):
    """Handle the Ctrl+C signal."""
    print("\n\nCtrl+C detected! Exiting the program gracefully.")
    sys.exit(0)


def main():
    """Main function to convert XML files to JSON and filter the target JSON format"""

    signal.signal(signal.SIGINT, signal_handler)
    start_time = time.time()
    clear_screen()

    while True:
        print("XML to JSON converter and JSON filter\n\n")
        print(
            """
            Choose between the following options: \n
                1. Convert XML files to JSON
                2. Filter the target JSON format
                3. Clean up the JSON structure
                \nAll the above options [A]
            """
        )
        input_options = input("\n\nEnter the option number(s) to proceed: ")

        if "1" in input_options:
            total_files_converted = convert_xml_to_json(INPUT_XML_FOLDER, JSON_FOLDER)
            print(
                f"\nConversion completed! Total files converted: {total_files_converted}"
            )
            break

        elif "2" in input_options:
            total_files_parsed = filters_target_json(JSON_FOLDER, OUTPUT_FOLDER)
            print(f"Parsing completed! Total files parsed: {total_files_parsed}")
            break

        elif "3" in input_options:
            cleaned_files_count = clean_json_files(OUTPUT_FOLDER, CLEANED_FOLDER)
            print(f"Total files processed: {cleaned_files_count}")
            break

        elif "A" in input_options or "a" in input_options:
            total_files_converted = convert_xml_to_json(INPUT_XML_FOLDER, JSON_FOLDER)
            total_files_parsed = filters_target_json(JSON_FOLDER, OUTPUT_FOLDER)
            cleaned_files_count = clean_json_files(OUTPUT_FOLDER, CLEANED_FOLDER)
            print(
                f"\nConversion completed! Total files converted: {total_files_converted}"
            )
            print(f"Parsing completed! Total files parsed: {total_files_parsed}")
            print(f"Total files processed: {cleaned_files_count}")
            break

        else:
            print("Invalid option! Please try again.")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(
        f"Job completed in {elapsed_time:.2f} seconds! Check the output folders for the results."
    )


if __name__ == "__main__":
    main()
