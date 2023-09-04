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

@app.route('/file/<filename>', methods=['POST'])
async def process_file(filename):
    print(f"processing file... {filename}", flush=True)
    try:
        process_file_service = ProcessFileService()
        process_file_service.process_csv_file(filename, *load_config())
        return '',200
    except FileNotFoundError as e:
        print(f"File not found: {e}", flush=True)
        return f"File not found: {e}", 404