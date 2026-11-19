import QtQuick

Rectangle {
    id: root
    property string text
    signal pressed()
    Text {
        anchors.centerIn: root
        width: root.width * 0.9
        text: root.text
        elide: Text.ElideRight
    }
    MouseArea {
        anchors.fill: parent
        onClicked: root.pressed()
    }
}
