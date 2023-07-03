import cv2
import face_recognition
import numpy as np

class FaceRecognition:
    def __init__(self, db_conn, db_cursor):
        self.conn = db_conn
        self.cursor = db_cursor

    def add_face(self, face_name, encoding_blob):
        # Check if the user name already exists in the database
        self.cursor.execute(
            """
            SELECT * FROM users WHERE name = ?
        """,
            (face_name,),
        )
        result = self.cursor.fetchone()

        if result is not None:
            # User name already exists in the database
            return {"status": False}

        # Insert the user data into the database
        self.cursor.execute(
            """
            INSERT INTO users (name, face_encoding) VALUES (?, ?)
        """,
            (face_name, encoding_blob),
        )

        self.conn.commit()

        # Retrieve the ID of the inserted user
        user_id = self.cursor.lastrowid

        # Return the ID
        return {"status": True, "name":face_name ,"id": user_id}


    def run_identification(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        try:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encoding = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )[0]

            self.cursor.execute("SELECT * FROM users")
            rows = self.cursor.fetchall()

            matches = []
            face_distances = []

            for row in rows:
                encoding_blob = row[2]
                known_encoding = np.frombuffer(encoding_blob, dtype=np.float64)
                matches.append(
                    face_recognition.compare_faces([known_encoding], face_encoding)[0]
                )
                face_distances.append(
                    face_recognition.face_distance([known_encoding], face_encoding)[0]
                )
            face_distances = np.array(face_distances)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                user_id = rows[best_match_index][0]
                user_name = rows[best_match_index][1]
                return {"status": "known", "name": user_name, "id": user_id}

            # The face is unknown
            return {"status": "unknown", "face_encoding": face_encoding.tobytes()}

        except:
            # No face detected
            return {"status": "no_face_detected"}
