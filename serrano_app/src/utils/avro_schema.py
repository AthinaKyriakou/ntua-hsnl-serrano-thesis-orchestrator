import json
from confluent_kafka import avro
from src.config import kafka_cfg

# used when calling utls/test.py
#from config import kafka_cfg

def load_avro_schema_from_file(schema_file_path):
    # schema for the record key is of type string
    key_schema_string = """
    {"type": "string"}
    """
    key_schema = avro.loads(key_schema_string)
    # TODO: check that the path is ok
    value_schema = avro.load(schema_file_path)
    return key_schema, value_schema


def send_avro_record(schema_file_path, topic, key, value):
    key_schema, value_schema = load_avro_schema_from_file(schema_file_path)
    producer_config = {
        'bootstrap.servers': kafka_cfg['bootstrap.servers'],
        'schema.registry.url': kafka_cfg['schema.registry.url']
    }
    producer = avro.AvroProducer(producer_config, default_key_schema=key_schema, default_value_schema=value_schema)
    value_json = json.loads(value)
    try:
        producer.produce(topic=topic, key=key, value=value_json)
    except Exception as e:
        raise Exception(e)
    #else:
    #    print(f"Successfully producing record value - {value_json} to topic - {topic}")
    #producer.flush()
