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
    """Converts all XML files in the xml_folder to JSON and saves them in the output_folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)
            
            # Parse the XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Convert the XML tree to a dictionary
            xml_dict = xml_to_dict(root)

            # Convert the dictionary to JSON
            json_data = json.dumps(xml_dict, indent=4)

            # Create the corresponding JSON file
            json_filename = filename.replace(".xml", ".json")
            json_path = os.path.join(output_folder, json_filename)
            with open(json_path, "w") as json_file:
                json_file.write(json_data)
            
            print(f"Converted {filename} to {json_filename}")

# Specify the input XML folder and output JSON folder
xml_folder = "./A1-grammar"
output_folder = "output_json-A1-grammar"

# Convert all XML files in the input folder to JSON
convert_xml_to_json(xml_folder, output_folder)
