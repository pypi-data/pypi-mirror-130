import audio_metadata
import os
import shutil
import typer
from typer import Argument

from pathlib import Path

app = typer.Typer()


def move_song(basepath, metadata):

    artist = metadata['tags']['artist']
    album = metadata['tags']['album']
    title = metadata['tags']['title']
    location = metadata['filepath']
    original_path = os.getcwd()
    os.chdir(basepath)
    cwd = os.getcwd()
    os.chdir(original_path)
    path = f'{cwd}/{artist[0]}/{album[0]}/'
    os.makedirs(path, exist_ok=True)
    shutil.move(location, path)


@app.command(help='Walk a directory and Organizes the music')
def process_folder(path: Path = Argument(
    default='.',
    exists=True,
    file_okay=True,
    dir_okay=True,
    readable=True,
    resolve_path=True
)):
    for cp, dir, files in os.walk(path):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.aac'):
                metadata = audio_metadata.load(os.path.join(cp, file))
                move_song(path, metadata)


if __name__ == "__main__":
    app()
