import faust
from config import kafka_cfg

print('kubernetes_driver_app - faust_app - creating an instance of the faust library')
faust_app = faust.App(kafka_cfg['project'], broker=kafka_cfg['broker'])

def main() -> None:
    faust_app.main()