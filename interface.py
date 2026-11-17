"""
An ear training program. Uses synth.py to play tones that the user is then quizzed on.

contains the following options:
Pitch recognition with multiple notes (1)
Pitch recognition with one note (2)
Chord recognition (3)
QML application (4)
"""


from time import sleep
import random

import bridge
import synth
import utils


def test_single_note():
    """
    The purpose of this function is to test the user on single note recognition.
    This function asks for input within the command line using input()
    :return: None
    """
    note = random.choice(synth.listofnotes)
    synth.Tone(float(synth.notedict[note])).play(1)

    check_note(note, prompt="What was that note?\n")

    if ask_for_repeat():
        test_single_note()


def multi_note(num_of_notes: int, time_between: float):
    """
    Tests the user on recognition of several notes in succession.
    This function asks for input within the command line using input()

    :param num_of_notes: The number of notes to play
    :param time_between: The length (in seconds) of each note
    :return:
    """
    utils.check_param(int, ">0", p="num_of_notes")
    utils.check_param(int | float, ">0", p="time_between")

    note_list = synth.play_random_notes(num_of_notes, time_between)

    for i in range(len(note_list)):
        check_note(note_list[i], prompt=f"Note {i}:")

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

    check_note(synth.listofnotes[root][0], prompt="What was the root of that chord?")

    print("What kind of chord was that? \n (Maj, min, aug, dim, maj7, min7, or majmin7)")

    user_answer = input("").lower()
    if chord_type == user_answer:
        print("YAY you were right!")
    else:
        print(f"INCORRECT :( ({chord_type})")

    if ask_for_repeat():
        chord_recognition()


def tuning_practice(cent_range: int, absolute_pitch: bool=False):
    """
    Tests the user on more fine recognition of notes than test_single_note.
    This function plays a tone at different distances from the true tone, then asks the user if
    the note was flat or sharp. The goal is to be able to tune anything by ear.
    :return: None
    """
    # pick the note
    note = random.choice(synth.listofnotes)
    cent_offset = random.randint(-cent_range, cent_range)

    if not absolute_pitch: synth.Tone(synth.note_to_freq(note)).play(1)
    # play out of tune note (with variation on how far from the note it is)
    synth.Tone(synth.note_to_freq(note, cent_offset=cent_offset)).play(1)

    if absolute_pitch: user_input = input("Was that note sharp or flat?")
    else: user_input = input("Was the second note sharp (s) or flat (f)?")
    correct = user_input == "s" and cent_offset > 0 or user_input == "f" and cent_offset < 0
    if correct: print("YAY you got it right")
    else: print("Incorrect.")
    print(f"The cent offset was: {cent_offset}")

    if ask_for_repeat(): tuning_practice(cent_range, absolute_pitch=absolute_pitch)


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


def check_note(answer, prompt="Note:"):
    is_correct = "YAY you got it right"
    is_incorrect = f"dang the note was {answer}"

    user_answer = input(f"{prompt} ").upper()

    if answer[0] in user_answer and len(user_answer) <= 3:
        if "#" in answer:
            if "#" in user_answer:
                print(is_correct)
            else:
                print(is_incorrect)
        else:
            print(is_correct)
    else:
        print(is_incorrect)


def menu():
    print("Pick a program by entering its number:")
    print("Pitch recognition with multiple notes (1)")
    print("Pitch recognition with one note (2)")
    print("Chord recognition (3)")
    print("QML application (4)")
    print("Exit the program (0)")
    try:
        user_input = int(input("\n"))
    except:
        print("Please enter a number")

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
        bridge.load_qml_application()
        sleep(10)
    else:
        print("Please enter one of the numbers above")
        menu()



if __name__ == "__main__":
    menu()

