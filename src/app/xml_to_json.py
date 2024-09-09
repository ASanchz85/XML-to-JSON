import os
import json
import xml.etree.ElementTree as ET


def xml_to_dict(element):
    """Converts an XML element and its children to a dictionary."""
    node = {}
    # If the element has child elements, recursively call xml_to_dict on the children.
    if len(element):
        for child in element:
            child_dict = xml_to_dict(child)
            # Handle repeated tags as lists in the dictionary.
            if child.tag in node:
                if type(node[child.tag]) is list:
                    node[child.tag].append(child_dict[child.tag])
                else:
                    node[child.tag] = [node[child.tag], child_dict[child.tag]]
            else:
                node.update(child_dict)
    # If the element has no children, just store its text.
    else:
        node[element.tag] = element.text
    return {element.tag: node}


def convert_xml_to_json(xml_folder, output_folder):
    """Converts all XML files in the xml_folder to JSON and saves them in the output_folder, preserving folder structure."""
    file_counter = 0

    for root_dir, subdirs, files in os.walk(xml_folder):
        # Create the corresponding output folder structure
        relative_path = os.path.relpath(root_dir, xml_folder)
        output_subdir = os.path.join(output_folder, relative_path)

        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)

        for filename in files:
            if filename.endswith(".xml"):
                file_counter += 1
                xml_path = os.path.join(root_dir, filename)

                # Parse the XML file
                tree = ET.parse(xml_path)
                root = tree.getroot()

                # Convert the XML tree to a dictionary
                xml_dict = xml_to_dict(root)

                # Convert the dictionary to JSON
                json_data = json.dumps(xml_dict, indent=4)

                # Create the corresponding JSON file in the same folder structure
                json_filename = filename.replace(".xml", ".json")
                json_path = os.path.join(output_subdir, json_filename)

            with open(json_path, "w") as json_file:
                json_file.write(json_data)

            print(f"Converted {filename} to {json_filename}")

    return file_counter
