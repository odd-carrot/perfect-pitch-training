import QtQuick


Rectangle {
    id: root
    property bool selected: False
    height: 20; width: 50
    radius: 5
    border {
        width: 4
        color: selected ? "black" : "transparent"
    }
    MouseArea {
        anchors.fill: parent
        onClicked: root.selected = !root.selected
    }
}
