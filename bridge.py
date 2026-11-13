
import sys
import random

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement

import synth
import interface

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
        interface.test_single_note()

    @Slot(str, result=str)
    def ghostlyWhispers(self, s):
        if "I'm" in s:
            return_string = "You're" + s[3:]
        else: return_string = s
        print(s)
        return return_string

    # The last note played in single note recognition for the qml side.
    qml_note = random.sample(synth.listofnotes, 1)

    @Slot()
    def playSingleNote(self):
        self.qml_note = random.sample(synth.listofnotes, 1)
        synth.Tone(float(synth.notedict[self.qml_note[0]])).play(1, block=False)


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
