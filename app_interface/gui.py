import sys
import sqlite3
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from ui.Config import CUSTOM_FONT
from ui.PageController import PageController

def cleanup():
    db_cursor.close()
    db_conn.close()

if __name__ == "__main__":
    db_conn = sqlite3.connect("data/database.db")
    db_cursor = db_conn.cursor()
    
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="ui/assets/custom_dark_teal.xml")
    app.setFont(CUSTOM_FONT)  # Set the default font for the app to "Poppins"
    app.setWindowIcon(QIcon("ui/assets/icon.png"))  # Set the custom icon
    app.aboutToQuit.connect(cleanup)

    page_controller = PageController(db_conn, db_cursor)
    page_controller.stacked_widget.setWindowTitle("DeepTrain")
    page_controller.stacked_widget.setGeometry(100, 100, 1000, 600)
    page_controller.stacked_widget.show()

    page_controller.show_login_page()

    sys.exit(app.exec_())
    