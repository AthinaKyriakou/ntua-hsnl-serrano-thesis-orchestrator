import faust

VERSION = 1
PROJECT = 'ntua_diploma_thesis'
ORIGIN = 'src'
AUTODISCOVER = [f"{ORIGIN}.drivers",f"{ORIGIN}.orchestrator",]
BROKER = 'kafka://localhost:9092'

print('\nCreating an instance of the faust library.')
app = faust.App(PROJECT, version=VERSION, autodiscover=AUTODISCOVER, origin=ORIGIN, broker=BROKER)

def main() -> None:
    app.main()