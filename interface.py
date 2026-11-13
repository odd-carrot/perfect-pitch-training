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
    # get a random note from listofnotes
    note = random.choice(synth.listofnotes)
    synth.Tone(float(synth.notedict[note])).play(1)
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
    incorrect = f"INCORRECT :( ({synth.listofnotes[root]})"
    user_answer1 = input(f"Note: ").upper()
    if synth.listofnotes[root][0] not in user_answer1[:3]:
        print(incorrect)
    elif "#" in synth.listofnotes[root]:
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
        bridge.load_qml_application()
        sleep(10)





if __name__ == "__main__":
    menu()

