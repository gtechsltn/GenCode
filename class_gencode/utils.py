import os, math


class GCodePreprocessingUtils:
    def __init__(self, source: str) -> None:
        self.sourcefolder = source

    def scan_files(self, scanFilesUnder=None):
        """
        Scans the files in the given folder or gets the folder name to scan from the class constructor

        total size of the files in the folder, returns a 3-tuple followed by the list of full path of the files
             `(size_in_kb, size_in_mb, size_in_gb)`, `[filepath]`
        """
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

    def _clculate_file_size(self, size_in_bytes):
        """
        Translates a byte info into KB, MB and GB.
        """
        size_in_kb = size_in_bytes / 1024
        size_in_mb = size_in_kb / 1024
        size_in_gb = size_in_mb / 1024
        print(size_in_kb, size_in_mb, size_in_gb)
        return (size_in_kb, size_in_mb, size_in_gb)


class GCodeModelUtils:
    @staticmethod
    def model_metrics(batchSize: int, datasetRoot: str = None):
        """
        Returns a 3-tuple
        `Number of training samples`, `batch size`, `Number of training steps`
        """
        if datasetRoot is None:
            datasetRoot = "data/"
            files = os.listdir(datasetRoot[-1])
        else:
            if datasetRoot.endswith("/"):
                #  list of all the files in the data directory
                files = os.listdir(datasetRoot[-1])

            else:
                #  list of all the files in the data directory
                files = os.listdir(datasetRoot)
                datasetRoot = datasetRoot + "/"

        num_lines: int = 0
        for file in files:
            file = datasetRoot + file
            # Count the number of lines in each files
            num_lines += sum(1 for _ in open(file))

        num_training_steps = math.ceil(num_lines / batchSize)

        return (num_lines, batchSize, num_training_steps)


if __name__ == "__main__":
    GUtils = GCodePreprocessingUtils(source="download")
    
    print(GCodeModelUtils.model_params(batchSize=60, datasetRoot="data"))
