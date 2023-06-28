import os
from tqdm import tqdm

import logging
from log_config import configure_logging

# Configure logging
configure_logging()

folder_path = "download"
pwd = os.getcwd()
logging.info(f'Currently working on: {pwd}')

for root, dirs, files in tqdm(os.walk(folder_path)):

    # Remove non .py files
    for file in files:
        full_path = os.path.join(root, file)
        # Ignoring .py files
        if full_path.endswith(".py"):
            logging.info(f'retaining (.py file) {full_path}')
            pass
            # print(full_path)
        else:
            # print(f">>> Deleting >>> {full_path} ")
            # Set all permissions before deleting
            logging.info(f'Force deleting: {full_path}')
            os.chmod(full_path, 0o777)
            os.remove(full_path)

print("Completed... 🧹")
logging.info("Completed 🧹")
