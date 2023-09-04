import os
from ..infrastructure.kafkaproducer import ProducerKafka
from ..infrastructure.readcsv import ReadFile

class ProcessFileService:
    def __init__(self):
        pass

    def process_csv_file(self, filename, file_path, broker, topic, chunk_size):
        read_file = ReadFile(self.get_file_path(file_path, filename), chunk_size)
        resp = read_file.read_file()
        message_producer = ProducerKafka(broker, topic)
        for item in resp:
            if isinstance(item['site'], str):
                print(item, flush=True)
                resp = message_producer.send_msg(item)
            else:
                print("not valid item json", flush=True) 

    def get_file_path(self, file_path, filename):
        final_path = os.path.join(file_path, filename)
        print(f"final path to read: {final_path}", flush=True)
        if os.path.exists(final_path):
            return final_path
        else:
            raise FileNotFoundError(f"File {final_path} not found")