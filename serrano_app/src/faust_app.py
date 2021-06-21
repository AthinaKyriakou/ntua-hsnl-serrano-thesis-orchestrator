import faust
from config import kafka_cfg

print('faust_app - creating an instance of the faust library')
autodiscover = [kafka_cfg['origin'] + '.' + dir for dir in kafka_cfg['autodiscover']]
faust_app = faust.App(kafka_cfg['project'], version=kafka_cfg['version'], autodiscover=autodiscover, origin=kafka_cfg['origin'], broker=kafka_cfg['broker'])

print('faust_app - done')


def main() -> None:
    faust_app.main()