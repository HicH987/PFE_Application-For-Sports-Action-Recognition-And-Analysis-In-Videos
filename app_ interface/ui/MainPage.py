from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from ui.Tabs import WelcomeTab, RealtimeTab, RecordedTab, StatisticTab, LogoutTab


class MainPage(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, db_conn, db_cursor, parent=None):
        super().__init__(parent)
        self.logout_tab = LogoutTab(self.logout_requested)
        self.tab_widget = QTabWidget()
        self.main_page_layout = QVBoxLayout()
        self.db_conn = db_conn
        self.db_cursor = db_cursor

    def setup_ui(self):
        welcome_tab = WelcomeTab(self.current_username)
        realtime_tab = RealtimeTab(self.db_conn, self.db_cursor, self.current_user_id)
        recorded_tab = RecordedTab(self.db_conn, self.db_cursor, self.current_user_id)
        statistic_tab = StatisticTab(self.db_conn, self.db_cursor, self.current_user_id)
        self.logout_tab.init_ui(self.current_username)

        self.tab_widget.addTab(welcome_tab, "Welcome")
        self.tab_widget.addTab(realtime_tab, "Realtime")
        self.tab_widget.addTab(recorded_tab, "Recorded")
        self.tab_widget.addTab(statistic_tab, "Statistic")
        self.tab_widget.addTab(self.logout_tab, "Logout")

        self.main_page_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_page_layout)

        # Connect the results_added signal of RealtimeTab to update_table_on_commit method
        realtime_tab.results_added.connect(statistic_tab.update_table_on_commit)
        recorded_tab.results_added.connect(statistic_tab.update_table_on_commit)


    def set_current_user(self, user):
        self.current_user_id = user["id"]
        # print(self.current_user_id)
        self.current_username = user["name"]
        # print(self.current_username)

    def clear_tabs(self):
        while self.tab_widget.count() > 0:
            widget = self.tab_widget.widget(0)
            self.tab_widget.removeTab(0)
            widget.deleteLater()
        self.logout_tab = LogoutTab(self.logout_requested)
        self.main_page_layout.removeWidget(self.tab_widget)
        self.tab_widget.setParent(None)
