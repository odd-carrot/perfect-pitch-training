
import sys
import random

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement

import synth
import interface

QML_IMPORT_NAME = "io.sound"
QML_IMPORT_MAJOR_VERSION = 1

setting_in_question = "volume"

settings = {
    "volume": 1.0,
    "note_number": 3,
    "absolute_pitch": True
}

qml_note = None

@QmlElement
class Bridge(QObject):
    """
    This class defines a qml object for use in Gui/Main.qml. It acts as a bridge
    between the graphical interface and the Python script.
    """

    @Slot()
    def playSingleNote(self):
        global qml_note
        qml_note = random.choice(synth.listofnotes)
        note = synth.Tone(float(synth.notedict[qml_note]))
        note.play(1, volume=settings["volume"], block=False)


    @Slot()
    def playMultiNote(self):
        global qml_note
        qml_note = synth.play_random_notes(3, 1, volume=settings["volume"])


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
        global qml_note
        s = s.upper()

        # support for multiple notes
        answer = qml_note if type(qml_note) == str else qml_note.pop(0)

        if answer[0] in s and len(s) <= 3:
            if "#" in answer:
                if "#" in s:
                    return ""
                else:
                    return f"dang the note was {answer}"
            else:
                return ""
        else:
            return f"dang the note was {answer}"


    @Slot(bool)
    def setBool(self, b):
        global settings
        if type(settings[setting_in_question]) != bool:
            print("ERROR: The setting in question is not a boolean")

        try:
            settings[setting_in_question] = b
        except:
            print("ERROR: The setting in question does not exist")


    @Slot(int)
    def setInt(self, i):
        global settings
        if type(settings[setting_in_question]) != int:
            print("ERROR: The setting in question is not an int")

        try:
            settings[setting_in_question] = i
        except:
            print("ERROR: The setting in question does not exist")


    @Slot(float)
    def setFloat(self, f):
        global settings
        if type(settings[setting_in_question]) != float:
            print("ERROR: The setting in question is not a float")

        try:
            settings[setting_in_question] = f
        except:
            print("ERROR: The setting in question does not exist")


    @Slot(str)
    def sendSetting(self, s):
        global setting_in_question
        setting_in_question = s


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
