import os
from tqdm import tqdm


folder_path = "download"
pwd = os.getcwd()

for root, dirs, files in tqdm(os.walk(folder_path)):
    """
    # Remove the .git folders
    if ".git" in dirs:
        #remove_readonly_attribute = f"attrib -r -s -h /s {folder_path}\*.*"
        #print(f"Read-only attribute command >>> {remove_readonly_attribute}")
        #os.system(remove_readonly_attribute)

        dot_git_folder = f"{pwd}\{root}\{dirs[dirs.index('.git')]}"
        print(dot_git_folder)
        os.chmod(dot_git_folder,0o777)
        rdcmd = f"rd /s /q {dot_git_folder}"
        print(f"Remove command >>> {rdcmd}")
        os.system(rdcmd)
    """
    # Remove non .py files
    for file in files:
        full_path = os.path.join(root, file)
        # Ignoring .py files
        if full_path.endswith(".py"):
            pass
            # print(full_path)
        else:
            # print(f">>> Deleting >>> {full_path} ")
            # Set all permissions before deleting
            os.chmod(full_path, 0o777)
            os.remove(full_path)

print("Completed...")
