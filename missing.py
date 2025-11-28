import logging
import yaml
from aoc import copy_and_modify_template, create_init_file, create_directory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

with open('run_all.yaml', 'r') as file:
    data = yaml.safe_load(file)

results = data.get('results', [])
for result in results:
    logger.debug(f"Result: {result}")
    if result.get('status') == 'missing':
        for path in [f'{result["year"]}', f'{result["year"]}/{result["day"]}']:
            logger.debug(f"Creating directory: {path}")
            create_directory(path)
            logger.debug(f"Creating __init__.py in: {path}")
            create_init_file(path)
        copy_and_modify_template(result['year'], result['day'], 'solution_template.py', f'{result["year"]}/{result["day"]}/solution.py')
