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

# Pretty print the dictionary
logging.debug(json.dumps(obsidian_files_dict, indent=2))