import cv2
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
    QDialog,
)

from ui.CustomStuffs import CustomButton, CustomInputDialog
from ui.Config import DIM_CAM, DIM_LOGIN_CAM, CSS

from helpers.face_id import FaceRecognition


class LoginPage(QWidget):
    login_successful = pyqtSignal(dict)

    def __init__(self, db_conn, db_cursor, parent=None):
        super().__init__(parent)

        self.face_id = FaceRecognition(db_conn, db_cursor)

        # Webcam setup
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, DIM_CAM[0])
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, DIM_CAM[1])

        # Timer to update webcam frame
        self.timer = QTimer()

        # Login button
        self.login_button = CustomButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.login_button.hide()

        # Webcam canvas
        self.webcam_canvas = QLabel(self)
        self.webcam_canvas.setFixedSize(DIM_LOGIN_CAM[0], DIM_LOGIN_CAM[1])
        self.webcam_canvas.setAlignment(Qt.AlignHCenter)
        self.webcam_canvas.setStyleSheet(CSS.canvas)
        self.webcam_canvas.hide()

        # Logo image
        logo_image = QPixmap("ui/assets/logo.png")
        logo_label = QLabel(self)
        logo_label.setPixmap(logo_image)
        logo_label.setAlignment(Qt.AlignCenter)

        # Get Started button
        self.get_started_button = CustomButton("Get Started", self)
        self.get_started_button.clicked.connect(self.show_webcam_and_login_button)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(self.get_started_button, alignment=Qt.AlignHCenter)

        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        layout.addWidget(self.webcam_canvas, alignment=Qt.AlignCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignHCenter)
        self.setLayout(layout)

    def start_webcam(self):
        self.timer.start(30)

    def update_frame(self, dim=None):
        ret, frame = self.webcam.read()
        if dim is None:
            dim = DIM_CAM
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(
                frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(dim[0], dim[1], aspectRatioMode=True)

            self.webcam_canvas.setPixmap(pixmap)

    def login(self):
        ret, frame = self.webcam.read()
        if ret:
            face_result = self.face_id.run_identification(frame)
            # face_result = {"status": "known", "name":"test"}
            # print(face_result)

            if face_result["status"] == "no_face_detected":
                QMessageBox.critical(self, "Error", "No face detected")
                
            else:
                if face_result["status"] == "known":
                    user_info, ok = face_result, True
                else:
                    while True:
                        name, ok = self.ask_for_name()
                        if ok and name:
                            user_info = self.face_id.add_face(
                                name, face_result["face_encoding"]
                            )

                            if not user_info["status"]:
                                QMessageBox.critical(
                                    self, "Error", "This username is already taken"
                                )
                            else:
                                break
                if ok:
                    self.login_successful.emit(user_info)
                    self.webcam.release()
                    self.timer.stop()
                    self.reset_login_page()
                

    def ask_for_name(self):
        dialog = CustomInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.getText()
        return "", False

    def show_webcam_and_login_button(self):
        self.timer.timeout.connect(lambda: self.update_frame(DIM_LOGIN_CAM))
        self.webcam_canvas.show()
        self.login_button.show()
        self.get_started_button.hide()
        self.start_webcam()

    def reset_login_page(self,):

        # Webcam setup
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, DIM_CAM[0])
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, DIM_CAM[1])


        self.get_started_button.show()
        # Login button
        self.login_button.hide()

        # Webcam canvas
        self.webcam_canvas.hide()
