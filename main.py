"""
An ear training program. Uses synth.py to play tones that the user is then quizzed on.

contains the following options:
Pitch recognition with multiple notes (1)
Pitch recognition with one note (2)
Chord recognition (3)
QML application (4)
"""

import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement

from time import sleep
import random
import synth
import utils

listoftones = ('130.8', '138.6', '146.8', '155.6', '164.8', '174.6', '185.0', '196.0', '207.7', '220.0', '233.1',
               '246.9', '261.6', '277.2', '293.7', '311.1', '329.6', '349.2', '370.0', '392.0', '415.3', '440.0',
               '466.2', '493.9', '523.3', '554.4', '587.3', '622.3', '659.3', '698.5', '740.0', '784.0', '830.6',
               '880.0', '932.3', '987.8')
listofnotes = ('C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4',
               'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5',
               'G#5', 'A5', 'A#5', 'B5')
notedict = {k: v for k, v in zip(listofnotes, listoftones)}

QML_IMPORT_NAME = "io.sound"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Bridge(QObject):
    """
    This class defines a qml object for use in Gui/Main.qml. It acts as a bridge
    between the graphical interface and the Python script.
    """

    @Slot(str, result=str)
    def exponentiate(self, s):
        the_integer = int(s)
        return str(the_integer*the_integer)

    @Slot(str)
    def triggerSound(self, s):
        synth.play_chord("random", random.randint(7, 15))
        print(s)

    @Slot()
    def triggerNoteRecognition(self):
        test_single_note()

    @Slot(str, result=str)
    def ghostlyWhispers(self, s):
        if "I'm" in s:
            return_string = "You're" + s[3:]
        else: return_string = s
        print(s)
        return return_string

    # The last note played in single note recognition for the qml side.
    qml_note = random.sample(listofnotes, 1)

    @Slot()
    def startSingleNote(self):
        self.qml_note = random.sample(listofnotes, 1)
        synth.Tone(float(notedict[self.qml_note[0]])).play(1)


    @Slot(str, result=str)
    def checkNote(self, s):
        """
        Takes the user input from the qml application and checks against
        self.qml_note (which should be the note that just played). Returns a
        message (either "" or a message about which note was actually correct)
        to the qml side.
        :param s: The user input from the qml GUI
        :return: "" or f"dang the note was {self.qml_note[0]}" based on whether the user was right.
        """
        s = s.upper()

        if self.qml_note[0][0] in s and len(s) <= 3:
            if "#" in self.qml_note[0]:
                if "#" in s:
                    return ""
                else:
                    return f"dang the note was {self.qml_note[0]}"
            else:
                return ""
        else:
            return f"dang the note was {self.qml_note[0]}"





def test_single_note():
    """
    The purpose of this function is to test the user on single note recognition.
    This function asks for input within the command line using input()
    :return: None
    """
    # get a random note from listofnotes
    note = random.choice(listofnotes)
    synth.Tone(float(notedict[note])).play(1)
    user_answer = input("What was that note?\n")
    is_correct = "YAY you got it right"
    is_incorrect = f"dang the note was {note[0]}"

    user_answer = user_answer.upper()

    if note[0][0] in user_answer and len(user_answer) <= 3:
        if "#" in note[0]:
            if "#" in user_answer:
                print(is_correct)
            else:
                print(is_incorrect)
        else:
            print(is_correct)
    else:
        print(is_incorrect)

    exit_or_continue = input("Press Enter to play again :D \n (or type \"exit\" to exit)\n")
    if exit_or_continue != "exit":
        test_single_note()
    else:
        print("Ok bye :(")
        return


def multi_note(num_of_notes: int, time_between: float):
    """
    Tests the user on recognition of several notes in succession.
    This function asks for input within the command line using input()

    :param num_of_notes: The number of notes to play
    :param time_between: The length (in seconds) of each note
    :return:
    """
    utils.check_param(int, p="num_of_notes")
    utils.check_param(int | float, p="time_between")

    note_list = synth.play_random_notes(num_of_notes, time_between)

    for i in range(len(note_list)):
        is_correct = "correct :D"
        is_incorrect = f"INCORRECT :( ({note_list[i]})"
        user_answer = input(f"Note {i + 1}: ").upper()
        if note_list[i][0] in user_answer and len(user_answer) <= 3:
            if "#" in note_list[i]:
                if "#" in user_answer:
                    print(is_correct)
                else:
                    print(is_incorrect)
            else:
                print(is_correct)
        else:
            print(is_incorrect)

    if ask_for_repeat():
        multi_note(num_of_notes, time_between)

def chord_recognition():
    """
    Tests the user on the recognition of chord quality and the root note of the chord.
    This function asks for input within the command line using input()

    :return: None
    """
    root = random.randint(7, 20)
    chord_type = synth.play_chord('random', root)
    print("What was the root of that chord?")
    correct = "correct :D"
    incorrect = f"INCORRECT :( ({listofnotes[root]})"
    user_answer1 = input(f"Note: ").upper()
    if listofnotes[root][0] not in user_answer1[:3]:
        print(incorrect)
    elif "#" in listofnotes[root]:
        if "#" not in user_answer1:
            print(incorrect)
        else:
            print(correct)
    else:
        print(correct)

    print("What kind of chord was that? \n (Maj, min, aug, dim, maj7, min7, or majmin7)")
    user_answer2 = input("").lower()
    if chord_type == user_answer2:
        print(correct)
    else:
        print(f"INCORRECT :( ({chord_type})")

    if ask_for_repeat():
        chord_recognition()




def ask_for_repeat():
    """
    Asks the user if they want to continue the program they are using
    :return: True when the
    """
    exit_or_continue = input("Press Enter to play again :D \n (or type \"exit\" to exit)\n").lower()
    if "exit" not in exit_or_continue:
        return True
    else:
        print("Ok bye :(")
        menu()


def menu():
    print("Pick a program by entering its number:")
    print("Pitch recognition with multiple notes (1)")
    print("Pitch recognition with one note (2)")
    print("Chord recognition (3)")
    print("QML application (4)")
    print("Exit the program (0)")
    user_input = int(input("\n"))

    if user_input == 0:
        assert False, "User has a life"
    elif user_input == 1:
        print("Enter parameters for the training below")
        input_num_of_notes = int(input("Enter the number of notes to be played: "))
        input_time_between = float(input("Enter the time in seconds between each note (0-1): "))
        multi_note(input_num_of_notes, input_time_between)
    elif user_input == 2:
        test_single_note()
    elif user_input == 3:
        chord_recognition()
    elif user_input == 4:
        load_qml_application()
        sleep(10)


def load_qml_application():
    """
    Loads the qml application defined in Gui/Main.qml
    :return:
    """
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.loadFromModule("Gui", "Main")
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)



if __name__ == "__main__":
    menu()

