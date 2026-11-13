import QtQuick


Rectangle {
    id: root
    signal itemClicked()
    anchors {
        right: parent.right
        left: parent.left
    }
    radius: 5
    MouseArea {
        anchors.fill: parent
        onClicked: root.itemClicked()
    }
}
