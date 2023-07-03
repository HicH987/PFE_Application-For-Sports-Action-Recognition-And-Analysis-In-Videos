from helpers.utils import (
    pose_detection,
    get_2d_landmarks,
    make_prediction,
)
from helpers.analyse import analyse
from helpers.global_vars import LABELS
from helpers.DeepFitClassifier import DeepFitClassifier


import cv2
import mediapipe as mp
from collections import deque

# --- GLOBAL VAR --------
mp_pose = mp.solutions.pose


clf_model_path = "./models/model_1_test.tflite"
CLF = DeepFitClassifier(clf_model_path, LABELS)

# K_NUM_FRAMES = 25
K_NUM_FRAMES = 5 # not 25 like in "test_ model + analyze" because there are some latency caused by the pyqt images canvas
frame_queue = deque(maxlen=K_NUM_FRAMES)


threshold = 0.75
prediction_proba = 0
predicted_label = ""
hist_perd = []


def prediction(image, draw=False):
    global hist_perd, predicted_label, prediction_proba
    
    frame = cv2.resize(image, (640, 480), interpolation=cv2.INTER_AREA)
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        enable_segmentation=False,
        smooth_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as POSE:
        frame, results = pose_detection(frame, pose_model=POSE)

    landmark_list = get_2d_landmarks(frame, results)
    if len(landmark_list) != 0:
        
        predicted_label, prediction_proba = make_prediction(
                CLF, landmark_list, frame_queue, threshold
            )

        if prediction_proba <= 0.0:
            if len(hist_perd) > 0:
                predicted_label = hist_perd[-1]
        else:
            hist_perd.append(predicted_label)

    dict_results, ok,  = analyse(results, predicted_label)
    
    return dict_results
