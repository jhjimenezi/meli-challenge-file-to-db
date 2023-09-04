from ..infrastructure.kafkaproducer import ProducerKafka
from ..infrastructure.readcsv import ReadFile

class ProcessFileService:
    def __init__(self):
        pass

    def process_csv_file(self, file_path, broker, topic, chunk_size):
        read_file = ReadFile(file_path, chunk_size)
        resp = read_file.read_file()
        message_producer = ProducerKafka(broker, topic)
        for item in resp:
            if isinstance(item['site'], str):
                print(item, flush=True)
                resp = message_producer.send_msg(item)
                print(resp, flush=True)
            else:
                print("not valid", flush=True) 