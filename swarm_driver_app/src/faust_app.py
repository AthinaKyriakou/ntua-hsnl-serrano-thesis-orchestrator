import faust
from config import kafka_cfg

print('swarm_driver_app - faust_app - creating an instance of the faust library')
#autodiscover = [kafka_cfg['origin'] + '.' + dir for dir in kafka_cfg['autodiscover']]

faust_app = faust.App(kafka_cfg['project'], version=kafka_cfg['version'], autodiscover=True, origin=kafka_cfg['origin'], broker=kafka_cfg['broker'])

def main() -> None:
    faust_app.main()