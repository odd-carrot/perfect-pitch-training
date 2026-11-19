import QtQuick
import QtQuick.Controls
import io.sound 1.0
import "components"
import "widgets"

ApplicationWindow {
    id: root
    visible: true
    color: stack.currentItem.color
    Bridge {
        id: python
    }

    Connections {
        target: stack.currentItem
        ignoreUnknownSignals: true
        function onExitToMenu() { stack.popToIndex(0) }
    }

    StackView {
        id: stack 
        anchors.fill: parent
        initialItem: Rectangle {
            width: root.width; height: root.height
            color: "#110055"

            Column {
                anchors.centerIn: parent
                width: root.width / 2
                spacing: 5
                StyledButton {
                    text: "Single note recognition"
                    radius: 5
                    height: 30
                    anchors {left: parent.left; right: parent.right}

                    onPressed: ()=> {
                        stack.pushItem(Qt.resolvedUrl("widgets/SingleNoteInterface.qml"))
                        python.playSingleNote()
                    }
                }
                StyledButton {
                    text: "Sequence note recognition"
                    radius: 5
                    height: 30
                    anchors {left: parent.left; right: parent.right}

                    onPressed: ()=> {
                        stack.pushItem(Qt.resolvedUrl("widgets/SequenceInterface.qml"))
                        python.playMultiNote()
                    }
                }
            }
        }
    }
}
