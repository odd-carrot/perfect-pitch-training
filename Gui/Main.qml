import QtQuick
import QtQuick.Controls
import io.sound 1.0

ApplicationWindow {
    id: root
    visible: true
    color: "black"
    Bridge {
        id: python
    }
    Connections {
        target: python
        function onIsCorrectSignal(correct) {root.color = correct ? "green" : "red"}
    }
    property string pythonNumber: "2"
    Rectangle {
        id: fancyButton
        width: parent.width; height: 20
        Text {
            id: numberDisplay
            anchors.centerIn: parent
            text: pythonNumber
        }
        MouseArea {
            anchors.fill: parent
            onClicked: pythonNumber = python.exponentiate(pythonNumber)
        }
    }
    Rectangle {
        id: playSoundButton
        width: parent.width; height: 20
        color: "green" 
        anchors.top: fancyButton.bottom
        MouseArea {
            anchors.fill: parent
            onClicked: python.triggerSound("sound played")
        }
        TextField {
            placeholderText: qsTr("note")
            height: parent.height
            width: parent.width / 3
            onAccepted: ()=>{
                this.placeholderText = python.ghostlyWhispers(this.text)
                this.clear()
            }
        }
    }
    Rectangle {
        id: singleNote
        color: "blue"
        width: parent.width; height: 20
        anchors.top: playSoundButton.bottom
        MouseArea {
            anchors.fill: parent
            onClicked: python.startSingleNote()
        }
        TextField {
            placeholderText: qsTr("Single Note Recognition")
            height: parent.height
            width: parent.width / 2
            onAccepted: ()=>{
                var msg = python.checkNote(this.text)
                singleNote.color = msg ? "red" : "green"
                if (msg) this.placeholderText = msg
                else this.placeholderText = "YAY"
                this.clear()
                python.startSingleNote()
            }
        }
    }
}
