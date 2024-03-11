## Logging Setup
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s')

logging.debug('Starting pipeline...')

## Importing Libraries
import configparser
import os

## Setting up Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

## Pulling in obsidian_dir from config.ini
obsidian_dir = config['pipeline']['obsidian_dir']
hugo_dir = config['pipeline']['hugo_dir']

## Checking if the directories exist
if not os.path.exists(obsidian_dir):
    logging.error(f"Obsidian directory does not exist at {obsidian_dir}")
    raise SystemExit