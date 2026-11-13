import QtQuick
import "../components"

FancyMenu {
    id: mainMenu
    menuWidth: 60
    header: Text {
        text: "Menu"
        color: "black"
    }
    menu: ListView {
        visible: false
        clip: true
        spacing: 2
        width: mainMenu.menuWidth-6; height: mainMenu.menuHeight-5
        model: 5 
        delegate: ToggleButton {}
    }
    onMenuClicked: this.openMenu()
}
