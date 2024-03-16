## Logging Setup
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

logging.debug('Starting pipeline...')

## Importing Libraries
import configparser
import os
# pip install pyyaml
import yaml
import json

## Setting up Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

## Pulling in obsidian_dir and hugo_dir from config.ini
obsidian_dir = config['pipeline']['obsidian_dir']
hugo_dir = config['pipeline']['hugo_dir']

## Checking if the directories exist
if not os.path.exists(obsidian_dir):
    logging.error(f"Obsidian directory does not exist at {obsidian_dir}")
    raise SystemExit

if not os.path.exists(hugo_dir):
    logging.error(f"Hugo directory does not exist at {hugo_dir}")
    raise SystemExit

## Function to set the status of a file
def set_status(file, status, current_check, reason):
    # Check if the required arguments are present
    if not all([file, status, current_check]):
        logging.error("All arguments are required")
        raise ValueError("All arguments are required")
    
    # If the "reason" argument is not present, set it to "None"
    if not reason:
        reason = "None"
    
    obsidian_files_dict[file]["reason"] = reason

    # Set the status of the file
    if status == "success":
        obsidian_files_dict[file]["status"] = "success"
    else:
        obsidian_files_dict[file]["status"] = "failed"
    
    # Set the current check
    # If a current check already exists, move it to "last_check"
    if "current_check" in obsidian_files_dict[file]:
        obsidian_files_dict[file]["last_check"] = obsidian_files_dict[file]["current_check"]
    
    obsidian_files_dict[file]["current_check"] = current_check
    return

## Build Dictionary of Obsidian Files with metadata
### Make a dictionary of all the .md files in the obsidian directory
### Also add metadata about the file
### This is the general structure of the dictionary
# obsidian_files_dict = {
#     "cleaned_file_name": {
#         "path": "path/to/file1.md",
#         "title": "Title of file1",
#         "status": "success",
#         "last_check": "not empty",
#         "current_check": "has frontmatter"
#     }

obsidian_files_dict = {}

for root, dirs, files in os.walk(obsidian_dir):
    for file in files:
        if file.endswith('.md'):
            # Make a cleaned version of the filename
            cleaned_file_name = file.replace(".md", "")
            # Add the file to the dictionary
            obsidian_files_dict[cleaned_file_name] = {
                "path": os.path.join(root, file)
            }

### Check if the files are empty
for file in obsidian_files_dict:
    with open(obsidian_files_dict[file]["path"], 'r') as f:
        file_contents = f.read()
        if len(file_contents) == 0:
            obsidian_files_dict[file]["status"] = "failed"
            obsidian_files_dict[file]["current_check"] = "Check if the file is empty"
            obsidian_files_dict[file]["reason"] = "File is empty"
        else:
            obsidian_files_dict[file]["status"] = "success"
            obsidian_files_dict[file]["current_check"] = "Check if the file is empty"

### Check if the files have frontmatter
for file in obsidian_files_dict:
    # Check if the file has a "success" status before checking for frontmatter
    if obsidian_files_dict[file]["status"] == "failed":
        continue
    with open(obsidian_files_dict[file]["path"], 'r') as f:
        file_contents = f.read()
        if file_contents.startswith("---"):
            obsidian_files_dict[file]["status"] = "success"
            obsidian_files_dict[file]["current_check"] = "Check if the file has frontmatter"
        else:
            obsidian_files_dict[file]["status"] = "failed"
            obsidian_files_dict[file]["current_check"] = "Check if the file has frontmatter"
            obsidian_files_dict[file]["reason"] = "File does not have frontmatter"

### Check if the frontmatter is valid YAML
for file in obsidian_files_dict:
    # Check if the file has a "success" status before checking for frontmatter
    if obsidian_files_dict[file]["status"] == "failed":
        continue
    with open(obsidian_files_dict[file]["path"], 'r') as f:
        file_contents = f.read()
        if file_contents.startswith("---"):
            try:
                yaml_contents = yaml.safe_load(file_contents.split("---")[1])
                obsidian_files_dict[file]["status"] = "success"
                obsidian_files_dict[file]["current_check"] = "Check if the frontmatter is valid YAML"
            except yaml.YAMLError as exc:
                obsidian_files_dict[file]["status"] = "failed"
                obsidian_files_dict[file]["current_check"] = "Check if the frontmatter is valid YAML"
                obsidian_files_dict[file]["reason"] = "Frontmatter is not valid YAML"

### Check if the required frontmatter fields are present
excepted_frontmatter_fields = config['frontmatter']['required_fields'].split(",")

#### Removing whitespace from the list
excepted_frontmatter_fields = [field.strip() for field in excepted_frontmatter_fields]

for file in obsidian_files_dict:
    # Check if the file has a "success" status before checking for frontmatter
    if obsidian_files_dict[file]["status"] == "failed":
        continue
    # Parse the frontmatter
    with open(obsidian_files_dict[file]["path"], 'r') as f:
        file_contents = f.read()
        if file_contents.startswith("---"):
            yaml_contents = yaml.safe_load(file_contents.split("---")[1])
            # Check if the required fields are present
            for field in excepted_frontmatter_fields:
                if field not in yaml_contents:
                    set_status(file, "failed", "Check if the required frontmatter fields are present", f"Frontmatter does not have the required field: {field}")
                else:
                    obsidian_files_dict[file]["status"] = "success"
                    obsidian_files_dict[file]["current_check"] = "Check if the required frontmatter fields are present"

### Pull the required frontmatter fields into the dictionary
for file in obsidian_files_dict:
    # Check if the file has a "success" status before checking for frontmatter
    if obsidian_files_dict[file]["status"] == "failed":
        continue
    with open(obsidian_files_dict[file]["path"], 'r') as f:
        file_contents = f.read()
        if file_contents.startswith("---"):
            yaml_contents = yaml.safe_load(file_contents.split("---")[1])
            for field in excepted_frontmatter_fields:
                obsidian_files_dict[file][field] = yaml_contents[field]


# Print the files in a list format
for file in obsidian_files_dict:
    print(f"File: {file}")
    print(f"- Status: {obsidian_files_dict[file]['status']}")
    print(f"- Current Check: {obsidian_files_dict[file]['current_check']}")
    if obsidian_files_dict[file]['status'] == "failed":
        print(f"- Reason: {obsidian_files_dict[file]['reason']}")
    for field in excepted_frontmatter_fields:
        print(f"- {field}: {obsidian_files_dict[file].get(field, '')}")
    print()
