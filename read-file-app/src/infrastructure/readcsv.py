import pandas as pd

class ReadFile:
    file_path = ""
    chunk_size = 0

    def __init__(self, file_path, chunk_size):
        self.file_path = file_path
        self.chunk_size = chunk_size
    
    def read_file(self):
        try:
            for chunk in pd.read_csv(self.file_path, 
                         chunksize=self.chunk_size, 
                         iterator=True):
                for item in chunk.itertuples(name="item"):
                    yield {
                        "site": item.site,
                        "id": item.id
                    }
        except Exception as ex:
            print(ex, flush=True)