from concurrent import futures
from tqdm import tqdm
import os
from typing import Union


class GCodePreprocessingUtils:
    def __init__(self, source: str) -> None:
        self.sourcefolder = source

    def scan_files(self, scanFilesUnder: Union[str, None]):
        """
        Scans the files in the given folder or gets the folder name to scan from the class constructor
        
        Makes use of the available CPU cores

        total size of the files in the folder, returns a 3-tuple followed by the list of full path of the files
        `(size_in_kb, size_in_mb, size_in_gb)`, `[filepath]`
        """
        if scanFilesUnder is None:
            scanFilesUnder = self.sourcefolder

        source_file_list = []
        size_in_bytes = 0

        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_path = {
                executor.submit(self._scan_folder, folder, scanFilesUnder): folder
                for folder in tqdm(
                    os.listdir(scanFilesUnder),
                    desc=f"Scanning folder: {scanFilesUnder}",
                )
            }

            for future in tqdm(
                futures.as_completed(future_to_path), desc="Scanning files"
            ):
                folder = future_to_path[future]
                try:
                    result = future.result()
                    size_in_bytes += result[0]
                    source_file_list.extend(result[1])
                except Exception as exc:
                    print(f"Exception occurred while scanning folder {folder}: {exc}")

        sizeinfo = self._calculate_file_size(size_in_bytes)

        return sizeinfo, source_file_list

    def _calculate_file_size(self, size_in_bytes):
        """
        Translates a byte info into KB, MB and GB.
        """
        size_in_kb = size_in_bytes / 1024
        size_in_mb = size_in_kb / 1024
        size_in_gb = size_in_mb / 1024
        print(size_in_kb, size_in_mb, size_in_gb)
        return (size_in_kb, size_in_mb, size_in_gb)

    def _scan_folder(self, folder, scanFilesUnder):
        folder_path = os.path.join(scanFilesUnder, folder)
        folder_size = 0
        file_paths = []

        for root, dirs, files in os.walk(folder_path):
            for f in files:
                full_path = os.path.join(root, f)
                folder_size += os.path.getsize(full_path)
                file_paths.append(full_path)

        return folder_size, file_paths


if __name__ == "__main__":
    GUtils = GCodePreprocessingUtils(source="download")
    GUtils.scan_files(scanFilesUnder="download")
