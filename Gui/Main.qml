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

    StackView {
        id: stack 
        anchors.fill: parent
        initialItem: Rectangle {
            width: root.width; height: root.height
            color: "#110055"

            Column {
                anchors.centerIn: parent
                width: root.width / 2
                RoundButton {
                    text: "Single note recognition"
                    radius: 5
                    height: 30
                    anchors {left: parent.left; right: parent.right}

                    onPressed: ()=> {
                        stack.pushItem(Qt.resolvedUrl("widgets/RegularInterface.qml"))
                        python.playSingleNote()
                    }
                }
            }
        }
    }
}
