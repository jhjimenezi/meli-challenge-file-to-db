import json
import asyncio

from utils.utildate import convert_to_datetime

from application.model.item import Item

from infraestructure.apiadapter import ApiAdapter
from infraestructure.redisadapter import RedisAdapter
from infraestructure.mysqladapter import MysqlAdapter
from infraestructure.kafkaconsumeradapter import KafkaConsumerAdapter

class KafkaToMysqlService:

    def __init__(self, broker, topic, group_id, mysql_host, mysql_user, mysql_password, mysql_database, redis_host, redis_port, api_host):
        self.consumer = KafkaConsumerAdapter(group_id, broker, topic, group_id)
        self.mysql_writer = MysqlAdapter(mysql_host, mysql_user, mysql_password, mysql_database)
        self.mysql_writer.connect()
        self.redis_client = RedisAdapter(redis_host, redis_port)
        self.redis_client.connect()
        self.meli_api = ApiAdapter(api_host)

    async def get_extra_data(self, item_api):
        loop = asyncio.get_event_loop()
        category_name_fut = loop.run_in_executor(None, self.get_value_from_redis_or_api, self.meli_api.get_category_name, item_api['category_id']) if 'category_id' in item_api else loop.run_in_executor(None, lambda: None)
        currency_description_fut = loop.run_in_executor(None, self.get_value_from_redis_or_api, self.meli_api.get_currency_description, item_api['currency_id']) if 'currency_id' in item_api else loop.run_in_executor(None, lambda: None)
        seller_nickname_fut = loop.run_in_executor(None, self.get_value_from_redis_or_api, self.meli_api.get_seller_nickname, item_api['seller_id']) if 'seller_id' in item_api else loop.run_in_executor(None, lambda: None)
        futures = [category_name_fut, currency_description_fut, seller_nickname_fut]
        result = await asyncio.gather(*futures)
        return result[0], result[1], result[2]
    
    def get_value_from_redis_or_api(self, api_method, key):
        print(f"trying to get value from redis {key}" )
        value = self.redis_client.get(key)
        if value is None:
            print(f"{key} not found in redis")
            api_result = api_method(key)
            if api_result is None:
                print(f"{key} not found in the api")
                return None
            else:
                print(f"{key} found in the api with value")
                if type(api_result) is dict:
                    api_result = json.dumps(api_result)
                self.redis_client.set(key, api_result)
                return api_result
        else:
            result = value.decode('utf-8')
            print(f"{key} found in redis with value")
            return result
    
    def move_data_from_kafka_to_mysql(self):
        result = self.consumer.activate_listener()
        try:
            items_to_db = [] 
            for item_kafka in result:
                print("-----------------")
                print(item_kafka)
                key = item_kafka['site'] + str(item_kafka['id'])
                if key is not None:
                    item = self.get_value_from_redis_or_api(self.meli_api.get_item, key)
                    if item is not None:
                        json_item = json.loads(item)    
                        price = json_item['price'] if 'price' in json_item else None
                        price = json_item['price'] if 'price' in json_item else None
                        start_time = convert_to_datetime(json_item['start_time']) if 'start_time' in json_item else None
                        category_name, currency_description, seller_nickname = asyncio.run(self.get_extra_data(json_item))
                        item = Item(item_kafka['site'], item_kafka['id'], price, start_time, category_name, currency_description, seller_nickname)
                        self.mysql_writer.write(item)
                
        except Exception as ex:
            print("error processing record...")
            print(ex)