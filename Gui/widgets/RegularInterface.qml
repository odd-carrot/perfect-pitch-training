import QtQuick
import QtQuick.Controls

Item {
    id: root
    anchors.centerIn: parent
    property string color: "black"
    signal answerEvaluated(isCorrect: bool)
    
    TextField {
        anchors.centerIn: parent
        placeholderText: qsTr("Welcome")
        height: 40
        width: root.width / 2
        onAccepted: ()=> {
            if (this.text) {

                var msg = python.checkNote(this.text)

                root.color = msg ? "red" : "green"

                if (msg) this.placeholderText = msg
                else this.placeholderText = "YAY"

                this.clear()
            }
            else {
                python.playSingleNote()
            }
            }
        }
}
