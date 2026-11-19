pragma NativeMethodBehavior: AcceptThisObject
import QtQuick
import QtQuick.Controls
import io.sound 1.0
import "../components"

Item {
    id: root
    property string color: "black"
    signal playNoteSeq()
    signal exitToMenu()

    function changeVolume(value) {
        python.sendSetting("volume")
        python.setFloat(value)
    }

    Bridge { id: python }

    Row {
        height: 30
        width: 300
        spacing: 8
        StyledButton {
            height: 30; width: 50
            text: "Main Menu"
            onPressed: root.exitToMenu()
        }
        Slider {
            id: volumeControl
            height: 30; width: 50
            to: 1.0
            value: 1.0
            stepSize: 0.1
            onValueChanged: root.changeVolume(this.value)
        }
    }
    
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
                playNoteSeq()
            }
        }
    }
}
