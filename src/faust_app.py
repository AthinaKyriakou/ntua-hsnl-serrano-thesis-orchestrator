import faust

# import from file
VERSION = 1
PROJECT = 'ntua_diploma_thesis'
ORIGIN = 'src'
AUTODISCOVER = [f"{ORIGIN}.drivers",f"{ORIGIN}.orchestrator",]
BROKER = 'kafka://localhost:9092'

print('\nfaust_app - creating an instance of the faust library')
faust_app = faust.App(PROJECT, version=VERSION, autodiscover=AUTODISCOVER, origin=ORIGIN, broker=BROKER)

def main() -> None:
    faust_app.main()