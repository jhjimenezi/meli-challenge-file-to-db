import json
from kafka import KafkaConsumer


class KafkaConsumerAdapter:
    broker = ""
    topic = ""
    group_id = ""
    logger = None

    def __init__(self, name, broker, topic, group_id):
        self.name = name
        self.broker = broker
        self.topic = topic
        self.group_id = group_id

    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                 group_id=self.group_id,
                                 consumer_timeout_ms=600000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))

        consumer.subscribe(self.topic)
        print("kafka listening to topic: ", self.topic)
        try:
            for message in consumer:
                print(self.name, "received message = ", message.value)
                consumer.commit()
                yield message.value
                #committing message manually after reading from the topic
                
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()