from utils import config
from application.kafka_to_mysql_service import KafkaToMysqlService


if __name__ == '__main__':
    print('Starting process-file-request service...')
    kafka_to_mysql_service = KafkaToMysqlService(config.kafka_broker, config.kafka_topic, config.kafka_group_id, config.mysql_host, config.mysql_user, config.mysql_password, config.mysql_database, config.redis_host, config.redis_port, config.api_host)
    kafka_to_mysql_service.move_data_from_kafka_to_mysql()








