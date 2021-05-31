import faust

print('\nCreating an instance of the faust library!')

app = faust.App(version=1, autodiscover=True, origin='project', id="1", broker='kafka://localhost:9092')

def main() -> None:
    app.main()