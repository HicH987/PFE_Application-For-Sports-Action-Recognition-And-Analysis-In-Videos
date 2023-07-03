import os
from helpers.utils import (
    pose_detection, 
    get_2d_landmarks,
    make_prediction,
    append_multi,     
    result_window,
    show_prediction,
    main_execution_count,
    )
from helpers.analyse import analyse

from helpers.global_vars import LABELS
from helpers.DeepFitClassifier import DeepFitClassifier


import cv2
import mediapipe as mp
from collections import deque
from glob import glob
import numpy as np
# --- GLOBAL VAR --------
mp_pose = mp.solutions.pose

clf_model_path = "./models/model_2_test.tflite"
CLF = DeepFitClassifier(clf_model_path, LABELS)

K_NUM_FRAMES = 25
frame_queue = deque(maxlen=K_NUM_FRAMES)

output_videos_dir = "outputs_videos"
os.makedirs(output_videos_dir ,exist_ok=1)

count = main_execution_count("helpers/main_count.txt")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = f"{output_videos_dir}/output_video_{count}.avi"
frame_rate = 30.0
frame_size = (640, 480)
video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, frame_size)


def main():
    cap = cv2.VideoCapture(0)

    threshold = 0.75
    prediction_proba = 0
    predicted_label = ""

    hist_perd = []

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        enable_segmentation=False,
        smooth_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as POSE: 
        i=0
        while cap.isOpened() and i< 1:
            ret, img = cap.read()
            if not ret :
                break
            
            frame = cv2.resize(img,(640, 480), interpolation=cv2.INTER_AREA)
            frame, results = pose_detection(frame, pose_model=POSE)
            landmark_list = get_2d_landmarks(frame, results)

            if results.pose_landmarks:
                predicted_label, prediction_proba = make_prediction(
                    CLF, landmark_list, frame_queue, threshold 
                )

                """ For drawing angels on the frame """
                # lShoulder_angel, img = get_angle(img, landmark_list, 13, 11, 23)
                # lShoulder_angel, img = get_angle(img, landmark_list, 11, 13, 15)
                # rHip_angel, img = get_angle(img, landmark_list, 12, 24, 26)
                # lHip_angel, img = get_angle(img, landmark_list, 11, 23, 25)
                # lHip_ankel_angel, img = get_angle(img, landmark_list, 11, 23, 27)

                # rShoulder_angel, img = get_angle(img, landmark_list, 14, 12, 24)
                # rHip_angel, img = get_angle(img, landmark_list, 12, 24, 26)

                if prediction_proba <= 0.0 :
                    if len(hist_perd) > 0:
                        predicted_label = hist_perd[-1]
                else:
                    hist_perd.append(predicted_label)
                
            result_win = result_window(
                append_multi(
                    [],
                    ("label", predicted_label),
                    ("proba", prediction_proba),
                )
            )

            cv2.imshow("window", img)
            cv2.imshow("result_win", result_win)
            
            show_prediction(img, predicted_label, prediction_proba)
            video_writer.write(img)
            
            analyse(results, predicted_label)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()
