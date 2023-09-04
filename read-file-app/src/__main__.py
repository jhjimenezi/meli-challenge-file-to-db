import os
from flask import Flask
from .application.process_file_service import ProcessFileService

app = Flask(__name__)
app.config.from_pyfile(os.path.join("../", "conf/app.conf"), silent=False)

def load_config():
    input_file_path = app.config['INPUT_FILE_LOCATION']
    kafka_broker = app.config['KAFKA_BROKER']
    kafka_topic = app.config['KAFKA_TOPIC']
    chunk_size = app.config['CHUNK_SIZE']
    return input_file_path, kafka_broker, kafka_topic, chunk_size

@app.route('/file', methods=['POST'])
async def process_file():
    print("processing file...", flush=True)
    process_file_service = ProcessFileService()
    print(load_config())
    process_file_service.process_csv_file(*load_config())
    return '',200