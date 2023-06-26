import os
from tqdm import tqdm

''' Performance information:
Size before scanning        : 36.2 GB (38,89,35,27,040 bytes)
Size after scanning         : 1.28 GB (1,38,36,69,760 bytes)
Files cleaned               : ~ 34.94 GB (37,50,98,57,280 bytes)
Number of folders at root   : 1899
Total item scanned          : 149243 items 
Total time taken            : 08:22
Rate of processing          : 296.79 items/seccond
Processor                   : Intel64 Family 6 Model 142 Stepping 9 GenuineIntel ~2701 Mhz
Total Physical Memory       : 8,058 MB
Available Physical Memory   : 2,020 MB
Virtual Memory: Max Size    : 13,946 MB
Virtual Memory: Available   : 6,617 MB
Virtual Memory: In Use      : 7,329 MB
OS                          : Microsoft Windows 11
OS Version                  : 10.0.22631 N/A Build 22631
'''

folder_path = "download"
pwd  = os.getcwd()

for root, dirs, files in tqdm(os.walk(folder_path)):
    '''
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
    '''        
    # Remove non .py files
    for file in files:
        full_path =  os.path.join(root, file)
        # Ignoring .py files
        if full_path.endswith(".py"):
            pass
            #print(full_path)
        else:
            # print(f">>> Deleting >>> {full_path} ")
            # Set all permissions before deleting
            os.chmod(full_path,0o777)
            os.remove(full_path)
    
print("Completed...")