from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QStackedWidget
from ui.LoginPage import LoginPage
from ui.MainPage import MainPage

class PageController(QObject):
    def __init__(self, db_conn, db_cursor):
        super().__init__()

        self.stacked_widget = QStackedWidget()

        self.login_page = LoginPage(db_conn, db_cursor)
        self.main_page = MainPage(db_conn, db_cursor)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.main_page)

        self.login_page.login_successful.connect(self.show_main_page)
        self.main_page.logout_tab.logout_requested.connect(self.show_login_page)

        
    # def show_login_page(self):
    #     self.stacked_widget.setCurrentWidget(self.login_page)

    def show_login_page(self):
        self.main_page.clear_tabs()
        self.stacked_widget.setCurrentWidget(self.login_page)
        
    def show_main_page(self, user):
        self.main_page.set_current_user(user)
        self.main_page.setup_ui()
        self.stacked_widget.setCurrentWidget(self.main_page)

        # Remove login page from memory
        # self.stacked_widget.removeWidget(self.login_page)
        # self.login_page.deleteLater()
        # del self.login_page
