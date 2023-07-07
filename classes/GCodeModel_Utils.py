import os, math


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
            files, datasetRoot = (
                (os.listdir(datasetRoot[-1]), datasetRoot)
                if datasetRoot.endswith("/")
                else (os.listdir(datasetRoot), datasetRoot + "/")
            )

        num_lines: int = 0
        for file in files:
            file = datasetRoot + file
            # Count the number of lines in each files
            num_lines += sum(1 for _ in open(file))

        num_training_steps = math.ceil(num_lines / batchSize)

        return (num_lines, batchSize, num_training_steps)
    
if __name__ == '__main__':

    print(GCodeModelUtils.model_params(batchSize=60, datasetRoot="data"))