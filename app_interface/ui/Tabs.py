import cv2
import json
import threading
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal, QSize, QDateTime
from PyQt5.QtGui import QImage, QPixmap, QMovie, QColor, QPainter
from PyQt5.QtChart import (
    QChart,
    QChartView,
    QPieSeries,
    QPieSlice,
    QValueAxis,
    QDateTimeAxis,
    QLineSeries,
    QBarCategoryAxis,
    QBarSet,
    QBarSeries,
)
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QFileDialog,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QFrame,
    QGridLayout,
    QCheckBox
)
# from playsound import playsound
import pygame

from ui.CustomStuffs import CustomButton
from ui.Config import DIM_CAM, CSS

from helpers.prediction import prediction
from helpers.analyse import init_analyse_vars

import datetime
import pandas as pd


def play_audio(path):
    pygame.mixer.music.load(path)  # Load the beep sound file
    pygame.mixer.music.play()  # Play the beep sound
    
def convert_to_seconds(time_string):
    minutes, seconds = map(int, time_string.split(':'))
    total_seconds = (minutes * 60) + seconds
    return total_seconds


class CardItem(QWidget):
    def __init__(self, title, initial_value):
        super().__init__()

        self.title = title
        self.value = initial_value

        self.init_ui()

    def init_ui(self):
        item_layout = QHBoxLayout()

        item_label = QLabel(self.title)
        item_label.setStyleSheet(CSS.score_item_label)
        item_layout.addWidget(item_label)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        item_layout.addItem(spacer)

        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(CSS.score_value_label)
        item_layout.addWidget(self.value_label)

        self.setLayout(item_layout)

    def update_value(self, value, color = "#fff"):
        self.value = value
        self.value_label.setText(str(value))
        self.value_label.setStyleSheet(f"""
                                        color: {color}; 
                                        border-style: none;
                                        font-size:15px; 
                                        font-weight: bold;
                                        """)


class ScoreCard(QWidget):
    def __init__(self):
        super().__init__()
        self.previous_value= 0
        self.previous_exercise= ""
        pygame.init()
        self.init_ui()
        
    def init_ui(self):
        # Create the main layout for the score card
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a card for the header and items
        card = QWidget()
        card.setFixedHeight(DIM_CAM[1])
        card.setStyleSheet(CSS.card_div)
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        # Create the card header
        header = QLabel("Score Result")
        header.setAlignment(Qt.AlignHCenter)
        header.setStyleSheet(CSS.card_header)
        card_layout.addWidget(header)

        # Create the items inside the card
        self.items = {
            "current_exercise": CardItem("Current exercise:", ""),
            "rep_counter": CardItem("Repetition:", ""),
            "next_action": CardItem("Next Action:", ""),
            "chrono": CardItem("Exercise Duration:", ""),
            "total_chrono": CardItem("Total Workout Duration:", ""),
            "straightness": CardItem("Back straightness:", ""),
        }
        for item in self.items.values():
            card_layout.addWidget(item)

        card_layout.setContentsMargins(2, 1, 2, 2)

        # Add the container to the main layout
        layout.addWidget(card)


    def update_results(self, results, with_sound=False):
        
        for key, value in results.items():
            if key in self.items:
                item = self.items[key]
                if key == "straightness":
                    if value == "False":
                        item.update_value(value, color = "#A52F2F")
                    elif value == "True":
                        item.update_value(value, color = "#2fa572")
                    else :
                        item.update_value(value, color = "#fff")
                        
                else:
                    item.update_value(value)
                

                if with_sound:
                    if key == "current_exercise" and value != self.previous_exercise:
                        self.text_to_speech(value)
                        self.previous_exercise = value
                    if key=="rep_counter" and value != "":
                        if self.previous_value < int(value):
                            item.update_value(value)
                            play_audio("./ui/assets/beep.mp3")              

                        self.previous_value = int(value) 
        # pygame.quit()

    def text_to_speech(self, text):
        if text != "":
            text = text.replace("-", " ")
            play_audio(f"./ui/assets/exercises_audio/{text}.mp3")
    


class RealtimeTab(QWidget):
    results_added = pyqtSignal()

    def __init__(self, db_conn, db_cursor, user_id):
        super().__init__()
        self.sound_on = False
        
        self.temp_results_df = None

        self.db_conn = db_conn
        self.db_cursor = db_cursor
        self.user_id = user_id

        self.prediction_thread = None

        self.analyze_results = {
            "current_exercise": "",
            "rep_counter": "",
            "next_action": "",
            "chrono": "",
            "total_chrono": "",
            "straightness": "",
        }

        self.is_streaming = False

        self.start_stop_button = CustomButton("Start Stream", self)
        self.start_stop_button.clicked.connect(self.toggle_stream)
        # ---------------------------------------------------------------

        self.score_card = ScoreCard()
        self.score_card.hide()

        # ---------------------------------------------------------------

        self.webcam_canvas = QLabel(self)
        self.webcam_canvas.setFixedSize(DIM_CAM[0], DIM_CAM[1])
        self.webcam_canvas.setAlignment(Qt.AlignHCenter)
        self.webcam_canvas.setStyleSheet(CSS.canvas)
        self.webcam_canvas.hide()

        self.webcam = None  # Initialize webcam variable

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        
        self.checkbox = QCheckBox("Sound Off")
        self.checkbox.setCheckState(0) 
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox.hide()
        
        # ---------------------------------------------------------------
        layout_score_cam = QHBoxLayout()
        layout_score_cam.addWidget(self.webcam_canvas)
        layout_score_cam.addWidget(self.score_card)


        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addLayout(layout_score_cam)
        layout.addWidget(self.start_stop_button, alignment=Qt.AlignHCenter)
        self.setLayout(layout)

    def toggle_stream(self):
        if self.is_streaming:
            self.stop_stream()
        else:
            self.start_stream()

    def start_stream(self):
        self.layout().setAlignment(self.start_stop_button, Qt.Alignment())
        self.start_stop_button.setStyleSheet(CSS.danger_btn)
        self.is_streaming = True
        self.start_stop_button.setText("Stop Stream")
        self.webcam_canvas.show()
        self.score_card.show()
        self.checkbox.show()
        
        # Create new webcam object and release any previous one
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, DIM_CAM[0])
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, DIM_CAM[1])
        self.webcam.set(cv2.CAP_PROP_BUFFERSIZE, 3)

        self.timer.start(40)

        self.lock = threading.Lock()
        init_analyse_vars()
        self.prediction_thread = threading.Thread(target=self.process_frames)
        self.prediction_thread.start()

    def stop_stream(self):
        self.layout().setAlignment(self.start_stop_button, Qt.AlignHCenter)
        self.start_stop_button.setStyleSheet(CSS.btn)
        self.is_streaming = False
        self.start_stop_button.setText("Start Stream")
        self.webcam_canvas.hide()
        self.score_card.hide()
        self.checkbox.hide()

        if self.webcam is not None:
            self.webcam.release()
            self.webcam = None

        self.timer.stop()
        if self.prediction_thread is not None:
            self.prediction_thread.join()
            self.prediction_thread = None

        self.init_results()
        self.add_results_db()

    def process_frames(self):
        while self.is_streaming:
            if self.webcam is not None:
                ret, frame = self.webcam.read()
                if ret:
                    dict_results = prediction(frame)
                    if len(dict_results) > 0:
                        with self.lock:
                            self.analyze_results = dict_results
                            if dict_results["rep_counter"] > 3 or dict_results["current_exercise"] == "plank" :
                                self.update_temp_df(dict_results)

        self.init_results()
        
    def checkbox_state_changed(self, state):
        if state == 2:  # Checked state
            self.checkbox.setText("Sound On")
            self.sound_on=True
        else:
            self.checkbox.setText("Sound Off")
            self.sound_on=False
    
    def update_temp_df(self, dict_results):
        if self.temp_results_df is None:
            self.temp_results_df = pd.DataFrame(
                columns=["exercise", "rep_counter", "duration"]
            )

        # Append dict_results as a row to self.temp_results_df
        data_row = {
            "exercise": dict_results["current_exercise"],
            "rep_counter": int(dict_results["rep_counter"]),
            "duration": dict_results["chrono"],
        }
        # print(data_row)

        # Convert the dictionary to a DataFrame
        new_row = pd.DataFrame(
            [data_row], columns=["exercise", "rep_counter", "duration"]
        )
        # Concatenate the new row with the existing temp_results_df
        self.temp_results_df = pd.concat(
            [self.temp_results_df, new_row], ignore_index=True
        )

    def add_results_db(self):
        if self.temp_results_df is None:
            return
        # Convert "rep_counter" column to numeric data type
        self.temp_results_df["rep_counter"] = pd.to_numeric(
            self.temp_results_df["rep_counter"]
        )

        # Update the temp_results_df by taking the highest row for each consecutive row with the same exercise
        self.temp_results_df["consecutive_group"] = (
            self.temp_results_df["exercise"]
            != self.temp_results_df["exercise"].shift(1)
        ).cumsum()
        self.temp_results_df = (
            self.temp_results_df.groupby("consecutive_group")
            .apply(lambda x: x.loc[x["rep_counter"].idxmax()])
            .reset_index(drop=True)
        )

        for _, row in self.temp_results_df.iterrows():
            exercise = row["exercise"]
            num_repetition = row["rep_counter"]
            duration = row["duration"]

            # Retrieve the relevant data from self.analyze_results
            date = datetime.date.today().strftime("%a %d %B %y")
            hour = datetime.datetime.now().strftime("%H:%M:%S")

            # Insert the data into the workouts table
            self.db_cursor.execute(
                """
                INSERT INTO workouts (user_id, date, hour, exercise, num_repetition, duration)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (self.user_id, date, hour, exercise, num_repetition, duration),
            )

        self.db_conn.commit()
        self.temp_results_df = None
        print("Results added to the database successfully.")

        # Emit the results_added signal
        self.results_added.emit()

    def update_frame(self):
        if self.webcam is not None:
            ret, frame = self.webcam.read()
            if ret:
                with self.lock:
                    dict_results = self.analyze_results

                self.score_card.update_results(dict_results, with_sound=self.sound_on)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(
                    frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(image)
                pixmap = pixmap.scaled(DIM_CAM[0], DIM_CAM[1], aspectRatioMode=True)
                self.webcam_canvas.setPixmap(pixmap)

    def init_results(self):
        self.analyze_results = {
            "current_exercise": "",
            "rep_counter": "",
            "next_action": "",
            "chrono": "",
            "total_chrono": "",
            "straightness": "",
        }
        self.score_card.update_results(self.analyze_results)


class PredictionWorker(QThread):
    prediction_result = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.frame = None
        self.running = True
        

    def set_frame(self, frame):
        self.frame = frame
            
    def run(self):
        while self.running:
            if self.frame is not None:
                dict_results = prediction(self.frame)
                self.prediction_result.emit(dict_results)

    def stop(self):
        self.running = False


class RecordedTab(QWidget):
    results_added = pyqtSignal()

    def __init__(self, db_conn, db_cursor, user_id):
        super().__init__()
        
        self.temp_results_df = None

        self.db_conn = db_conn
        self.db_cursor = db_cursor
        self.user_id = user_id

        self.prediction_worker = None

        self.analyze_results = {
            "current_exercise": "",
            "rep_counter": "",
            "next_action": "",
            "chrono": "",
            "total_chrono": "",
        }

        self.is_playing = False
        self.is_stopped = False

        self.video_path = ""
        self.video_capture = None
        self.frame_rate = 0
        self.current_frame = None

        self.choose_file_button = CustomButton("Choose Video", self)
        self.choose_file_button.clicked.connect(self.choose_video_file)

        self.start_stop_button = CustomButton("Start Video", self)
        self.start_stop_button.clicked.connect(self.toggle_video)
        self.start_stop_button.hide()

        # ---------------------------------------------------------------

        self.score_card = ScoreCard()
        self.score_card.hide()

        # ---------------------------------------------------------------

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # ---------------------------------------------------------------
        self.close_button = CustomButton("Close Video", self)
        self.close_button.setStyleSheet(CSS.danger_btn)
        self.close_button.clicked.connect(self.close_video)
        self.close_button.hide()

        self.video_canvas = QLabel(self)
        self.video_canvas.setFixedSize(DIM_CAM[0], DIM_CAM[1])
        self.video_canvas.setAlignment(Qt.AlignHCenter)
        self.video_canvas.setStyleSheet(CSS.canvas)
        self.video_canvas.hide()
        # ---------------------------------------------------------------
        button_layout = QHBoxLayout()
        # button_layout.addWidget(self.start_stop_button, alignment=Qt.AlignHCenter)
        # button_layout.addWidget(self.close_button, alignment=Qt.AlignHCenter)
        button_layout.addWidget(self.start_stop_button)
        button_layout.addWidget(self.close_button)

        video_buttons_layout = QVBoxLayout()
        video_buttons_layout.addWidget(self.video_canvas)
        video_buttons_layout.addLayout(button_layout)
        video_buttons_layout.setAlignment(Qt.AlignCenter)

        score_card_layout = QVBoxLayout()
        score_card_layout.addWidget(self.score_card)
        spacer = QSpacerItem(
            0, 50, QSizePolicy.Minimum, QSizePolicy.Fixed
        )  # Create a vertical spacer with a fixed height of 20
        score_card_layout.addItem(spacer)  # Add the spacer to the score_card_layout
        score_card_layout.setAlignment(Qt.AlignCenter)

        layout_score_video = QHBoxLayout()
        layout_score_video.addLayout(video_buttons_layout)
        layout_score_video.addLayout(score_card_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.choose_file_button, alignment=Qt.AlignCenter)

        layout.addLayout(layout_score_video)
        self.setLayout(layout)

    def choose_video_file(self):
        self.close_video()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi)")
        if file_dialog.exec_():
            self.video_path = file_dialog.selectedFiles()[0]
            self.start_stop_button.show()

            self.video_canvas.show()
            self.close_button.show()
            self.layout().setAlignment(self.choose_file_button, Qt.AlignVCenter)

            temp_cap = cv2.VideoCapture(self.video_path)
            while temp_cap.isOpened():
                ret, frame = temp_cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                    image = QImage(
                        frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB32
                    )
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(DIM_CAM[0], DIM_CAM[1], aspectRatioMode=True)
                    self.video_canvas.setPixmap(pixmap)
                    self.video_canvas.repaint()
                    QApplication.processEvents()
                break
            temp_cap.release()

    def toggle_video(self):
        if self.is_playing:
            self.stop_video()
        else:
            self.start_video()

    def start_video(self):
        if not self.is_stopped:
            self.video_capture = cv2.VideoCapture(self.video_path)
            init_analyse_vars()

        self.is_playing = True
        self.is_stopped = False
        self.start_stop_button.setText("Stop Video")
        self.video_canvas.show()
        self.score_card.show()

        self.timer.start(50)

        # Start the worker thread for predictions
        self.prediction_worker = PredictionWorker()
        self.prediction_worker.prediction_result.connect(self.handle_prediction_result)
        self.prediction_worker.start()

    def stop_video(self):
        self.is_playing = False
        if self.video_capture is not None:
            self.start_stop_button.setText("Continue Video")
        else:
            self.start_stop_button.setText("Start Video")

        self.is_stopped = True
        if self.prediction_worker is not None:
            self.prediction_worker.stop()
            self.prediction_worker.wait()  # Wait for the thread to finish
            self.prediction_worker = None

    def update_frame(self):
        if self.is_playing and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                image = QImage(
                    frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB32
                )
                pixmap = QPixmap.fromImage(image)
                pixmap = pixmap.scaled(DIM_CAM[0], DIM_CAM[1], aspectRatioMode=True)
                self.video_canvas.setPixmap(pixmap)

                # Update the frame in the worker thread
                self.prediction_worker.set_frame(frame)

            else:
                self.video_capture = None
                self.stop_video()
                self.start_stop_button.setEnabled(False)
                self.start_stop_button.setStyleSheet(CSS.disabled_btn)
                # self.add_results_db()

    def close_video(self):
        self.start_stop_button.hide()
        self.close_button.hide()
        self.video_canvas.hide()
        self.score_card.hide()
        self.layout().setAlignment(self.choose_file_button, Qt.AlignCenter)

        self.start_stop_button.setEnabled(True)
        self.start_stop_button.setStyleSheet(CSS.btn)
        self.start_stop_button.setText("Start Video")

        # init all vars
        self.is_playing = False
        self.is_stopped = False

        self.video_path = ""
        self.current_frame = None

        # self.video_capture.release()
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None

        self.timer.stop()

        if self.prediction_worker is not None:
            self.prediction_worker.stop()
            self.prediction_worker.wait()  # Wait for the thread to finish
            self.prediction_worker = None

        self.analyze_results = {
            "current_exercise": "",
            "rep_counter": "",
            "next_action": "",
            "chrono": "",
            "total_chrono": "",
        }
        self.score_card.update_results(self.analyze_results)
        # self.add_results_db()

    def handle_prediction_result(self, result):
        self.analyze_results = result
        self.score_card.update_results(self.analyze_results)
        if len(result) > 0:
            if result["rep_counter"] >= 3 or result["current_exercise"] == "plank" :
                self.update_temp_df(result)

    def update_temp_df(self, dict_results):
        if self.temp_results_df is None:
            self.temp_results_df = pd.DataFrame(
                columns=["exercise", "rep_counter", "duration"]
            )

        # Append dict_results as a row to self.temp_results_df
        
        data_row = {
            "exercise": dict_results["current_exercise"],
            "rep_counter": int(dict_results["rep_counter"]),
            "duration": dict_results["chrono"],
        }
        # print(data_row)

        # Convert the dictionary to a DataFrame
        new_row = pd.DataFrame(
            [data_row], columns=["exercise", "rep_counter", "duration"]
        )
        # Concatenate the new row with the existing temp_results_df
        self.temp_results_df = pd.concat(
            [self.temp_results_df, new_row], ignore_index=True
        )

    def add_results_db(self):
        if self.temp_results_df is None:
            return

        # Convert "rep_counter" column to numeric data type
        self.temp_results_df["rep_counter"] = pd.to_numeric(
            self.temp_results_df["rep_counter"]
        )

        # Update the temp_results_df by taking the highest row for each consecutive row with the same exercise
        self.temp_results_df["consecutive_group"] = (
            self.temp_results_df["exercise"]
            != self.temp_results_df["exercise"].shift(1)
        ).cumsum()
        self.temp_results_df = (
            self.temp_results_df.groupby("consecutive_group")
            .apply(lambda x: x.loc[x["rep_counter"].idxmax()])
            .reset_index(drop=True)
        )

        for _, row in self.temp_results_df.iterrows():
            exercise = row["exercise"]
            num_repetition = row["rep_counter"]
            duration = row["duration"]

            # Retrieve the relevant data from self.analyze_results
            date = datetime.date.today().strftime("%a %d %B %y")
            hour = datetime.datetime.now().strftime("%H:%M:%S")

            # Insert the data into the workouts table
            self.db_cursor.execute(
                """
                INSERT INTO workouts (user_id, date, hour, exercise, num_repetition, duration)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (self.user_id, date, hour, exercise, num_repetition, duration),
            )

        self.db_conn.commit()
        self.temp_results_df = None
        print("Results added to the database successfully.")

        # Emit the results_added signal
        self.results_added.emit()


class StatisticTab(QWidget):
    def __init__(self, db_conn, db_cursor, user_id):
        super().__init__()

        self.db_conn = db_conn
        self.db_cursor = db_cursor
        self.user_id = user_id

        self.data = self.get_data()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Create a QScrollArea instance
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_area_content = QWidget()

        scroll_area_content.setLayout(self.layout)
        scroll_area.setWidget(scroll_area_content)

        self.avg_time_title = QLabel("- " + "History Table")
        self.avg_time_title.setStyleSheet(
            "color: #fff; font-weight: bold; font-size:20px"
        )
        self.avg_time_title.setText(self.average_workout_time())

        self.headers = ["Date", "Hour", "Exercise", "Repetitions", "Duration"]
        table_title = QLabel("- " + "History Table")
        table_title.setStyleSheet(
            """
            QLabel{
                color: #fff; font-weight: bold; font-size: 18px
                }
            QLabel:hover{
                color: #2fa572;
                }"""
        )
        table_title.mousePressEvent = lambda event: self.toggle_visibility(
            table_title, self.table_widget
        )
        self.table_widget = QTableWidget()
        self.table_widget.hide()

        self.refresh_table()

        self.visualization_layout = QVBoxLayout()

        # Add
        self.layout.addWidget(self.avg_time_title)
        self.create_charts()
        self.layout.addWidget(table_title)
        self.layout.addWidget(self.table_widget)

        # Set the layout of the StatisticTab to a QVBoxLayout containing the QScrollArea
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def average_workout_time(
        self,
    ):
        total_duration = 0
        total_days = 0
        for row in self.data:
            date, time, exercise, repetitions, duration = row
            duration_parts = duration.split(":")
            duration_seconds = 0

            if len(duration_parts) == 3:
                duration_seconds = (
                    int(duration_parts[0]) * 3600
                    + int(duration_parts[1]) * 60
                    + int(duration_parts[2])
                )
            elif len(duration_parts) == 2:
                duration_seconds = int(duration_parts[0]) * 60 + int(duration_parts[1])
            else:
                raise ValueError(f"Invalid duration format: {duration}")

            total_duration += duration_seconds

        total_days = len(set([row[0] for row in self.data]))
        try:
            avg_duration_per_day = total_duration / total_days
        except:
            avg_duration_per_day = 0

        avg_time_per_day_str = f"- Average Time Spent per Day on Workout: <font color='#2fa572'> {avg_duration_per_day:.2f} seconds </font>"

        return avg_time_per_day_str

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())

    def refresh_table(self):
        # Fetch data from the database
        data = self.get_data()

        # Clear the existing table
        self.table_widget.clear()

        # Set the headers for the table
        self.table_widget.setColumnCount(len(self.headers))
        self.table_widget.setHorizontalHeaderLabels(self.headers)

        # Set the number of rows
        self.table_widget.setRowCount(len(data))

        # Populate the table with data
        for row, rowData in enumerate(data):
            for col, text in enumerate(rowData):
                item = QTableWidgetItem(str(text))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(row, col, item)

        # Set table alignment to centered
        self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table_widget.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Set the table to fit the content
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        # Calculate the total height of the table
        total_height = (
            self.table_widget.horizontalHeader().height() + 4
        )  # Add extra space for the header
        for row in range(self.table_widget.rowCount()):
            total_height += self.table_widget.rowHeight(row)

        # Set the minimum height of the table
        self.table_widget.setMinimumHeight(total_height)

        # Set the table to stretch in the layout
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_table_on_commit(self):
        self.data = self.get_data()
        self.clear_layout(self.visualization_layout)

        self.avg_time_title.setText(self.average_workout_time())
        self.create_charts()
        self.refresh_table()

    def toggle_visibility(self, chart_title, chart_view, list_component=None):
        chart_view.setVisible(not chart_view.isVisible())
        if list_component is not None:
            for comp in list_component:
                comp.setVisible(not comp.isVisible())
        chart_title.setStyleSheet(
            """
            QLabel{
                color:#2fa572; font-weight: bold; font-size: 18px
                }
            QLabel:hover{
                color: #fff;
                }"""
        )

    def get_data(self):
        self.db_cursor.execute(
            "SELECT date, hour, exercise, num_repetition, duration FROM workouts WHERE user_id = ?",
            (self.user_id,),
        )
        data = self.db_cursor.fetchall()
        # print(data)
        return data

    def create_charts(self):
        self.create_exercise_frequency_chart()
        self.create_exercise_duration_chart()
        unique_exercises = set(exercise[2] for exercise in self.data)
        for exercise in unique_exercises:
            self.create_exercise_progression_chart(exercise)

        self.create_time_of_day_chart()
        self.create_exercise_types_chart()
        self.create_exercise_repetitions_chart()

        self.layout.addLayout(self.visualization_layout)

    def create_chart_view(self, chart, title, exercise_types=None):
        chart.setBackgroundBrush(QColor("#1E1E1E"))

        chart_view = QChartView(chart)
        chart_view.setFixedHeight(350)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.hide()

        chart_title = QLabel("- " + title)
        chart_title.setStyleSheet(
            """
            QLabel{
                color: #fff; font-weight: bold; font-size: 18px
                }
            QLabel:hover{
                color: #2fa572;
                }"""
        )

        if exercise_types:
            type_layout = QVBoxLayout()
            list_component = []

            for exercise_category, exercises in exercise_types.items():
                tmp_layout = QHBoxLayout()
                category_label = QLabel(exercise_category)
                category_label.setStyleSheet(
                    """
                    QLabel{
                        color: #fff; font-weight: bold; font-size: 15px
                        }"""
                )
                category_label.hide()
                list_component.append(category_label)
                tmp_layout.addWidget(category_label)

                for exercise in exercises:
                    exercise_label = QLabel(exercise)
                    exercise_label.setStyleSheet(
                        """
                        QLabel{
                            color: #2fa572; font-weight: bold; font-size: 14px
                            min-width: 100px; max-width: 100px;}"""
                    )
                    exercise_label.hide()
                    list_component.append(exercise_label)
                    tmp_layout.addWidget(exercise_label, alignment=Qt.AlignCenter)

                type_layout.addLayout(tmp_layout)

            chart_title.mousePressEvent = lambda event: self.toggle_visibility(
                chart_title, chart_view, list_component
            )
        else:
            chart_title.mousePressEvent = lambda event: self.toggle_visibility(
                chart_title, chart_view
            )

        # Create the layout for the chart
        chart_layout = QVBoxLayout()

        # chart_layout.addWidget(chart_title, alignment=Qt.AlignCenter)
        chart_layout.addWidget(chart_title)
        if exercise_types:
            chart_layout.addLayout(type_layout)
        chart_layout.addWidget(chart_view)

        # return chart_layout
        self.visualization_layout.addLayout(chart_layout)

    def create_exercise_frequency_chart(self):
        exercise_frequency = self.calculate_exercise_frequency()

        chart = QChart()
        chart.legend().setShowToolTips(True)
        series = QBarSeries()

        for exercise, frequency in exercise_frequency.items():
            set1 = QBarSet(exercise)
            set1.append(frequency)
            series.append(set1)

        chart.addSeries(series)
        chart.setTitle("Exercise Frequency")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.setLabelsVisible(True)
        axisX.setTitleText("Exercise")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        # axisX.setLabelsAngle(-90)  # Add this line

        axisY = QValueAxis()
        axisY.setTitleText("Frequency")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.create_chart_view(chart, "Exercise Frequency")

    def calculate_exercise_frequency(self):
        exercise_frequency = {}

        for exercise in self.data:
            exercise_name = exercise[2]
            exercise_frequency[exercise_name] = (
                exercise_frequency.get(exercise_name, 0) + 1
            )
        # print(f"exercise_frequency: {exercise_frequency}")
        return exercise_frequency

    def create_exercise_duration_chart(self):
        exercise_duration = self.calculate_exercise_duration()

        chart = QChart()
        chart.legend().setShowToolTips(True)
        series = QBarSeries()

        for exercise, durations in exercise_duration.items():
            set1 = QBarSet(exercise)
            set1.append(sum(durations) / len(durations))
            series.append(set1)

        chart.addSeries(series)
        chart.setTitle("Exercise Average Duration")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.setLabelsVisible(True)
        axisX.setTitleText("Exercise")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Duration (sec)")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.create_chart_view(chart, "Exercise Average Duration")

    def calculate_exercise_duration(self):
        exercise_duration = {}

        for exercise in self.data:
            exercise_name = exercise[2]
            duration = exercise[4]
            minutes, seconds = map(int, duration.split()[0].split(":"))
            total_seconds = minutes * 60 + seconds
            exercise_duration[exercise_name] = exercise_duration.get(
                exercise_name, []
            ) + [total_seconds]
        # print(f"exercise_duration: {exercise_duration}")
        return exercise_duration

    def create_exercise_progression_chart(self, exercise: str):
        exercise_progression = self.calculate_exercise_progression(exercise)
        if len(exercise_progression) <= 1:
            return
        chart = QChart()
        chart.legend().setShowToolTips(True)
        series = QLineSeries()

        for date, repetitions in sorted(exercise_progression.items()):
            series.append(
                QDateTime.fromString(date, "yyyy-MM-dd").toMSecsSinceEpoch(),
                repetitions,
            )

        chart.addSeries(series)
        chart.setTitle(f"{exercise.capitalize()} Progression")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QDateTimeAxis()
        axisX.setFormat("dd-MM-yyyy")
        axisX.setTitleText("Date")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Repetitions")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.create_chart_view(chart, f"{exercise.capitalize()} Progression")

    def calculate_exercise_progression(self, exercise: str):
        exercise_progression = {}

        for exer in self.data:
            date_object = datetime.datetime.strptime(exer[0], "%a %d %B %y")
            exercise_date = str(date_object.strftime("%Y-%m-%d"))
            exercise_name = exer[2]
            repetitions = int(exer[3])
            if exercise_name.lower() == exercise.lower():
                exercise_progression[exercise_date] = (
                    exercise_progression.get(exercise_date, 0) + repetitions
                )
        # print(f"exercise_progression: {exercise_progression}")
        return exercise_progression

    def create_time_of_day_chart(self):
        time_of_day = self.calculate_time_of_day()
        if len(time_of_day) <= 1:
            return
        chart = QChart()
        chart.legend().setShowToolTips(True)
        series = QLineSeries()

        for hour, frequency in sorted(time_of_day.items()):
            series.append(hour, frequency)

        chart.addSeries(series)
        chart.setTitle("Time of Day")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setTitleText("Hour of the Day")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Frequency")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.create_chart_view(chart, "Most Frequent Training Time")

    def calculate_time_of_day(self):
        time_of_day = {}

        for exercise in self.data:
            time = exercise[1]
            hour = int(time.split(":")[0])
            time_of_day[hour] = time_of_day.get(hour, 0) + 1
        # print(f"time_of_day: {time_of_day}")
        return time_of_day

    def create_exercise_types_chart(self):
        exercise_types = {
            "Strength Training": [
                "pushup",
                "squat",
                "deadlift",
                "biceps-curl-bar",
                "leg-raise",
                "arm-raise",
            ],
            "Cardio": [
                "basic-curl",
                "fly",
                "overhead-press",
                "plank",
                "russian-twist",
                "bicycle-crunch",
                "bird-dog",
            ],
        }
        exercise_type_counts = self.calculate_exercise_type_counts()

        chart = QChart()
        chart.legend().setShowToolTips(True)
        series = QPieSeries()

        for category, count in exercise_type_counts.items():
            slice1 = QPieSlice(category, count)
            series.append(slice1)

        chart.addSeries(series)
        chart.setTitle("Exercise Types")

        self.create_chart_view(chart, "Exercise Types", exercise_types)

    def calculate_exercise_type_counts(self):
        exercise_types = {
            "Strength Training": [
                "pushup",
                "squat",
                "deadlift",
                "biceps-curl-bar",
                "leg-raise",
                "arm-raise",
            ],
            "Cardio": [
                "basic-curl",
                "fly",
                "overhead-press",
                "plank",
                "russian-twist",
                "bicycle-crunch",
                "bird-dog",
            ],
        }

        exercise_type_counts = {category: 0 for category in exercise_types}

        for exercise in self.data:
            exercise_name = exercise[2]
            for category, exercises in exercise_types.items():
                if exercise_name.lower() in [ex.lower() for ex in exercises]:
                    exercise_type_counts[category] += 1
                    break
        # print(f"exercise_type_counts: {exercise_type_counts}")
        return exercise_type_counts

    def create_exercise_repetitions_chart(self):
        exercise_repetitions = self.calculate_exercise_repetitions()
        # print("exercise_repetitions: ", exercise_repetitions)
        chart = QChart()
        chart.legend().setShowToolTips(True)
        series = QBarSeries()

        for exercise, repetitions in exercise_repetitions.items():
            set1 = QBarSet(exercise)
            # set1.append(sum(repetitions) / len(repetitions))
            set1.append(sum(repetitions))
            series.append(set1)

        chart.addSeries(series)
        chart.setTitle("Exercise Repetitions")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.setLabelsVisible(True)
        axisX.setTitleText("Exercise")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Repetitions")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.create_chart_view(chart, "Exercise Repetitions")

    def calculate_exercise_repetitions(self):
        exercise_repetitions = {}
        # print(self.data)
        for exercise in self.data:
            exercise_name = exercise[2]
            repetitions = int(exercise[3])

            exercise_repetitions[exercise_name] = exercise_repetitions.get(
                exercise_name, []
            ) + [repetitions]

        # print(f"exercise_repetitions: {exercise_repetitions}")
        return exercise_repetitions


class WelcomeTab(QWidget):
    def __init__(self, username):
        super().__init__()

        with open("ui/assets/tuto.json") as file:
            exercises = json.load(file)

        welcome_label = QLabel(f"Welcome, <font color='#1E1E1E'>{username}</font>  !")
        welcome_label.setAlignment(Qt.AlignHCenter)
        welcome_label.setStyleSheet(
            """
            font-size: 30px; 
            font-weight: bold;
            background-color:  #2fa572;
        """
        )

        supported_exercises_label = QLabel("Supported Exercises")
        supported_exercises_label.setStyleSheet(
            """
            font-size: 20px; 
            font-weight: bold;
        """
        )

        exercises_layout = QGridLayout()

        column_count = 2  # Number of columns in the grid
        row = 0
        col = 0
        for exercise in exercises:
            exercise_name_label = QLabel(exercise["name"])
            exercise_name_label.setAlignment(Qt.AlignHCenter)
            exercise_name_label.setStyleSheet(
                f"""
                border-style: none;
                
                color: white; 
                background-color: #2fa572; 
                
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px; 
                border-bottom-left-radius: 0px; 
                border-bottom-right-radius: 0px; 
                
                font-weight: bold;
                font-size: 18px; 
                padding: 5px;
                max-height: 20px;
                min-height: 20px;
                qproperty-alignment: 'AlignVCenter | AlignHCenter';

            
            """
            )

            exercise_description_label = QLabel(exercise["description"])
            exercise_description_label.setWordWrap(True)
            exercise_description_label.setStyleSheet(
                """
                font-size: 14px; 
                border-style:none;
                padding:10px;
            """
            )

            exercise_gif_label = QLabel()
            exercise_gif_movie = QMovie(exercise["gif_path"])
            exercise_gif_movie.setScaledSize(QSize(200, 200))
            exercise_gif_label.setMovie(exercise_gif_movie)
            exercise_gif_label.setAlignment(Qt.AlignHCenter)
            exercise_gif_label.setStyleSheet(
                """
                border-style:none;
                padding:10px;
            """
            )
            exercise_gif_movie.start()

            exercise_frame = QFrame()
            exercise_frame.setStyleSheet(
                """
                border: 2px solid #2fa572; 
                border-radius:9px;
                max-width: 600px;
                min-width: 450px;
            """
            )
            # exercise_frame.setContentsMargins(50, 20, 50, 20)

            exercise_frame_layout = QVBoxLayout(exercise_frame)
            exercise_frame_layout.setContentsMargins(0, 0, 0, 2)
            exercise_frame_layout.addWidget(exercise_name_label)
            exercise_frame_layout.addWidget(exercise_gif_label)
            exercise_frame_layout.addWidget(exercise_description_label)

            # exercises_layout.addWidget(exercise_frame)
            exercises_layout.addWidget(exercise_frame, row, col)

            col += 1
            if col >= column_count:
                col = 0
                row += 1

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setLayout(exercises_layout)
        scroll_area.setWidget(scroll_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(welcome_label)
        main_layout.addWidget(supported_exercises_label)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)


class LogoutTab(QWidget):
    def __init__(self, logout_requested, parent=None):
        super().__init__(parent)
        self.logout_requested = logout_requested

    def init_ui(self, username):
        self.username = username
        label = QLabel(
            f"<font color='#2fa572'>{self.username}</font> do you want to Logout?"
        )
        label.setStyleSheet("font-size:25px; font-weight: bold;")

        logout_button = CustomButton("Logout")
        logout_button.clicked.connect(self.emit_logout_requested)

        layout = QVBoxLayout()
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(logout_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def emit_logout_requested(self):
        self.logout_requested.emit()
