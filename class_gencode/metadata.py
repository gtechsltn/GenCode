import tqdm, os


class GCodeUtils:
    def __init__(self, source: str) -> None:
        self.sourcefolder = source

    def scan_files(self, scanFilesUnder=None):
        '''
        Scans the files in the given folder or gets the folder name to scan from the class constructor
        
        total size of the files in the folder, returns a 3-tuple followed by the list of full path of the files
             `(size_in_kb, size_in_mb, size_in_gb)`, `[filepath]`
        '''
        if scanFilesUnder is None:
            scanFilesUnder = self.sourcefolder

        source_file_list = []
        size_in_bytes = 0

        for root, dirs, files in os.walk(scanFilesUnder):
            for f in files:
                #  Get the py file full path
                full_path = os.path.join(root, f)
                # Get the size of individual files
                size_in_bytes += os.path.getsize(full_path)
                # Add file full path to a list
                source_file_list.append(full_path)
        
        sizeinfo = self._clculate_file_size(size_in_bytes)

        return sizeinfo, source_file_list
    
    def _clculate_file_size(self,size_in_bytes):
        '''
        Translates a byte info into KB, MB and GB. 
        '''
        size_in_kb = size_in_bytes / 1024
        size_in_mb = size_in_kb / 1024
        size_in_gb = size_in_mb / 1024
        print(size_in_kb, size_in_mb, size_in_gb)
        return (size_in_kb, size_in_mb, size_in_gb)

if __name__ =='__main__':
    GUtils = GCodeUtils(source="download")

    print(GUtils.scan_files())