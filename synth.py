"""
Synth module for playing sine wave tones.
"""
import random
from itertools import accumulate

import sounddevice as sd
import numpy as np
import time
import utils
import interface

SAMPLERATE = 44100

listoftones = ('130.8', '138.6', '146.8', '155.6', '164.8', '174.6', '185.0', '196.0', '207.7', '220.0', '233.1',
               '246.9', '261.6', '277.2', '293.7', '311.1', '329.6', '349.2', '370.0', '392.0', '415.3', '440.0',
               '466.2', '493.9', '523.3', '554.4', '587.3', '622.3', '659.3', '698.5', '740.0', '784.0', '830.6',
               '880.0', '932.3', '987.8')
listofnotes = ('C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4',
               'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5',
               'G#5', 'A5', 'A#5', 'B5')
notedict = {k: v for k, v in zip(listofnotes, listoftones)}


class Sine:
    """
    The smallest repeatable snippet of a given frequency sine wave

    Arrays have length (1/hz)*SAMPLERATE
    Can be concatenated to form various tone lengths
    """
    def __init__(self, hz: float):
        custom_sin = lambda x: (400/hz)*np.sin((hz * np.pi * 2 / SAMPLERATE) * x)
        self.hz = hz
        self.period = float(1/hz)
        self.snippet = np.fromfunction(custom_sin, (int(self.period*SAMPLERATE),), dtype=np.float32)


    def __str__(self):
        return f"hz:{self.hz}"


class Tone:
    """
    Each object contains the first cycle of each component (Sine types) of the tone.
    The components are then tiled together to the required length, and added together
    in order to be played.
    """

    def __init__(self, *args):
        self.tones = []
        for x in args:
            self.tones.append(Sine(x))


    def play(self, length: float, loudness=1.0, block=True):
        utils.check_param(int | float, p="length")
        utils.check_param(int | float, "< 3", "> 0", p="loudness")

        array_len = int(length*SAMPLERATE)
        a = np.tile(self.tones[0].snippet,int(length*1.1/self.tones[0].period))[:array_len]

        for x in self.tones[1:]:
            a = np.add(a, np.tile(x.snippet,int(length*1.1/x.period)+2)[:array_len])

        sd.play(a*loudness/len(self.tones), SAMPLERATE, blocking=block)
        if block:
            time.sleep(length)


def play_random_notes(n: int, seconds: float) -> list:
    """
    Plays random notes using Tone.play

    :param n: The number of notes to play
    :param seconds: The length of each note in seconds (total time played = seconds*n)
    :return: Note names of the notes played. Sharps only. example: ["A3", "D#4", "D2"]
    """
    utils.check_param(int, ">= 0", p="n")

    random_notes = random.sample(interface.listofnotes, n)

    for i in random_notes:
        Tone(float(interface.notedict[i])).play(seconds)

    return random_notes


def play_chord(chord_type, root):
    """
    Plays maj, min, aug, dim, maj7, min7, and majmin7 chords.
    :param chord_type:
    :param root:
    :return:
    """
    utils.check_param(str, p="chord_type")
    utils.check_param(int, p="root")

    chord_dict = {
        "maj": [0, 4, 3],
        "min": [0, 3, 4],
        "aug": [0, 4, 4],
        "dim": [0, 3, 3],
        "maj7": [0, 4, 3, 4],
        "min7": [0, 3, 4, 3],
        "majmin7": [0, 4, 3, 3]
    }

    if chord_type == "random":
        chord_type = random.choice(list(chord_dict))

    chord_notes = tuple(float(notedict[listofnotes[root+x]]) for x in accumulate(chord_dict[chord_type]))
    Tone(*chord_notes).play(1)

    return chord_type

if __name__ == "__main__":
    Tone(440, 523, 622, 740, 880).play(1)
