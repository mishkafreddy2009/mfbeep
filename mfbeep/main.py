import os
import time
import platform
from typing import Annotated
from pathlib import Path

import typer
from rich.progress import track
from anyplayer import get_player

from mfbeep.models import Sounds

BASE_DIRECTORY = Path(__file__).resolve().parent
SOUNDS_DIRECTORY = Path.joinpath(BASE_DIRECTORY, "sounds")


class Sound:
    def __init__(self, sound_file: str) -> None:
        self.sound_file = sound_file

    def play_wait(self) -> None:
        player = get_player("auto", self.sound_file)
        player.start()
        player.wait()

    def play(self) -> None:
        player = get_player("auto", self.sound_file)
        player.start()


class SoundsManager:
    mp3_sounds = [
        f"{SOUNDS_DIRECTORY}/{file}"
        for file in os.listdir(SOUNDS_DIRECTORY)
        if file.endswith(".mp3")
    ]

    def get_sound(self, title: str) -> Sound:
        for sound in self.mp3_sounds:
            if title in sound:
                return Sound(sound)
        return Sound(self.mp3_sounds[0])


class Beep:
    def __init__(self, sound_title: str = SoundsManager.mp3_sounds[0]) -> None:
        self.sounds_manager = SoundsManager()
        self.sound = self.sounds_manager.get_sound(sound_title)

    def test_sound(self) -> None:
        self.sound.play_wait()

    def start(
        self,
        sessions_amount: int,
        work_duration_minutes: int,
        break_duration_minutes: int,
    ) -> None:
        for session_number in range(1, sessions_amount + 1):
            for _ in track(
                range(work_duration_minutes * 60),
                description=f"working... [{session_number}/{sessions_amount}]",
            ):
                time.sleep(1)
            self.sound.play()
            for _ in track(
                range(break_duration_minutes * 60),
                description=f"chilling... [{session_number}/{sessions_amount}]",
            ):
                time.sleep(1)
            self.sound.play()
            input("ready for work? ")


def main(
    sound: Annotated[Sounds, typer.Option(help="select beep sound")] = Sounds.nya,
    sessions_amount: Annotated[
        int, typer.Argument(help="work and break cycles amount")
    ] = 4,
    work_duration_minutes: Annotated[
        int, typer.Argument(help="one work session duration in minutes")
    ] = 30,
    break_duration_minutes: Annotated[
        int, typer.Argument(help="one break session duration in minutes")
    ] = 5,
) -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    beep = Beep(sound)
    beep.start(sessions_amount, work_duration_minutes, break_duration_minutes)


def app():
    raise SystemExit(typer.run(main))
