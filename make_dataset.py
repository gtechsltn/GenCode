import os
from tqdm import tqdm

import logging
from log_config import configure_logging

# Configure logging
configure_logging()

MAX_CHAR_LENGTH = 512  # Maximum context length
MIN_CHAR_LENGTH = 400  # Minimum context length
NEW_LINE = "<N>"

folder_path = "download" # source 

file_list = []
# prepare the list of files to process
# print(f"Scanning files under {folder_path} ...")
logging.debug(f"Scanning files under {folder_path} ...")
for root, dirs, files in tqdm(os.walk(folder_path)):
    for f in files:
        full_path = os.path.join(root, f)
        file_list.append(full_path)
# print(f"Scanned {len(file_list)} items")
logging.debug(f"Scanned {len(file_list)} items")
read_e_file_count = 0

# Create the directory if it does not exist
GCodeT = os.path.dirname("data/GCodeT.txt")
if not os.path.exists(GCodeT):
    os.makedirs(GCodeT)

file_counter = 0
GCodeTFile = f"data/GCodeT_{file_counter}.txt"
with open(GCodeTFile, "a", encoding="utf-8") as datasetFile:
    # Read each file, try to make the data fall in bounds with MAX_CHAR_LENGTH and MIN_CHAR_LENGTH
    try:
        for file in tqdm(file_list):
            # Check if the file has exceeded the read count
            if file_counter %5 ==0:
                datasetFile.close()
                GCodeTFile = f"data/GCodeT_{file_counter}.txt"
                # Create a new dataset file
                datasetFile = open(GCodeTFile,"a",encoding='utf-8')
            
            try:
                py_file_data = open(file, "r", encoding="utf-8").read()
            except Exception as ex:
                datasetFile.close()
                logging.error(f'Read error {file}. Refer to make_dataset_ReadError.txt for more inormation')
                make_dataset_ReadError = os.path.dirname('error/make_dataset_ReadError.txt"')
                
                if not os.path.exists(make_dataset_ReadError):
                    os.makedirs(make_dataset_ReadError)
                with open(
                    "error/make_dataset_ReadError.txt", "a"
                ) as make_dataset_ReadError:
                    make_dataset_ReadError.write(f"{file}\n{str(ex)}")
                    make_dataset_ReadError.write(str(ex) + "\n")
                continue

            formated_data = py_file_data.replace("\n", NEW_LINE)
            if 100 < len(py_file_data) <= MAX_CHAR_LENGTH:
                datasetFile.write(formated_data + "\n")
                
                # break
            # Removes the extra white spaces
            else:
                sd = formated_data.split(f"{NEW_LINE}{NEW_LINE}")
                substring = ""
                for splite in sd:
                    substring += splite + f"{NEW_LINE}{NEW_LINE}"
                    if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                        datasetFile.write(substring + "\n")
                
                    # print(substring)
                    # break
            logging.debug(f"Processing: {file}")
            logging.debug(f"Written to: {GCodeTFile}")
            file_counter+=1
    except Exception as e:
        datasetFile.close()
        logging.error(f'Error while processing:\n{GCodeTFile}. Refer to GCodeT_WriteError.txt for more information')
        
        GCodeT_WriteError = os.path.dirname("error/GCodeT_WriteError.txt")
        if not os.path.exists(GCodeT_WriteError):
            os.makedirs(GCodeT_WriteError)
        with open("error/GCodeT_WriteError.txt", "a") as GCodeT_WriteError:
            GCodeT_WriteError.write(f"Error while processing:\n")
            GCodeT_WriteError.write(f"{str(e)}")
            
        # print(file)
        # print(str(e))
    finally:
        logging.info(f'Dataset created 🥳')