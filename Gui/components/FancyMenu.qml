import QtQuick

Rectangle {
    id: root
    required property Item header
    property Item menu
    property int menuHeight: 190
    property int menuWidth: 200
    signal menuClicked()
    implicitHeight: 25
    implicitWidth: header.width + 14
    color: "#232D3D"
    states: State {
        name: "MenuOpen"
        PropertyChanges {target: menu; visible: true}
        PropertyChanges {target: root; implicitHeight: menuHeight; implicitWidth: menuWidth}
    }
    transitions: Transition {
        NumberAnimation { property: "implicitHeight"; easing.type: Easing.InOutQuad }
        NumberAnimation { property: "implicitWidth"; easing.type: Easing.InOutQuad }
    }
    function openMenu() {
        if (root.state) {
            root.state = ""
        }
        else {
            root.state = "MenuOpen"
            }
        }
    MouseArea {
        anchors.fill: root
        onClicked: root.menuClicked()
    }
    Item {
        y: (25-header.implicitHeight)/2
        Item {
            id: headerSlot
            children: header
            x: (root.width-header.width)/2
            anchors.top: parent.top
            height: 25
        }
        Item {
            id: menuSlot
            children: menu
            implicitWidth: parent.width
            x: (root.width-menu?.width)/2
            anchors {
                top: headerSlot.bottom
                bottom: parent.bottom
            }
        }
    }

}
