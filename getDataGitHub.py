from github import Github 
import os
# from tqdm import tqdm
import time
from datetime import datetime 


ACCESS_TOKEN = open("secrets.config","r").read()
g = Github(ACCESS_TOKEN)


end_time = time.time()
start_time = end_time - 86400 

# for day in tqdm(range(2),desc="Fetching repos for 50 days from today:"):
for day in range(10):
    
    start_selector = datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d')
    end_selector = datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d')

    query = f"language:python created:{start_selector}..{end_selector}"

    result = g.search_repositories(query)
    print(f"Fetching for 10 days from {start_selector} ...")
    print(f"Number of repors during {start_selector}..{end_selector} >>> {result.totalCount}")

    start_time = start_time - 86400
    end_time = end_time - 86400

    for repo in result:

        dirname = f"./download/{repo.full_name}"
        command = f"git clone {repo.clone_url} {dirname}"

        print(f"====================== Puling {repo.full_name} ======================")
        print(f">>> {dirname}")
        print(f">>> {command}")
        os.system(command)
        print("============================= Completed ==============================")

    
