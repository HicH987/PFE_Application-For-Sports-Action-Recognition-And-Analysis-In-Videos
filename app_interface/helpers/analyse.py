import math
import cv2
import numpy as np
import time

import mediapipe as mp

mp_pose = mp.solutions.pose
height = 480



def get_angle(point1, point2, point3):
    # Retrieve landmark coordinates from point identifiers
    x1, y1, _ = point1
    x2, y2, _ = point2
    x3, y3, _ = point3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

    # Handling angle edge cases: Obtuse and negative angles
    if angle < 0:
        angle += 360
        if angle > 180:
            angle = 360 - angle
    elif angle > 180:
        angle = 360 - angle

    return angle

def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    
    if angle > 180.0:
        angle = 360 - angle

    return angle


def detection_body_part(landmarks, body_part_name):
    return [
        landmarks[mp_pose.PoseLandmark[body_part_name].value].x,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].y,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].visibility,
    ]


def init_analyse_vars():
    global counter, l_status, r_status, status, action, past_exercice, nochrono,t, total_chrono, t_chrono, start_time,start_time_total
    global straightness,straightness2
    counter = 0  
    status = True
    l_status = True
    r_status = True
    action = "no"  

    past_exercice = None

    nochrono = True
    t = "00:00"

    total_chrono = None
    t_chrono = None
    start_time = None
    start_time_total = time.time()

    straightness = None
    straightness2 = None


def analyse(mdp_results, nom_exercice):
    global counter, l_status, r_status, status, action, past_exercice, nochrono,t, total_chrono, t_chrono, start_time, start_time_total
    global straightness,straightness2
    
    total_chrono = time.time() - start_time_total
    
    minutes_t = int((total_chrono % 3600) / 60)
    seconds_t = int(total_chrono % 60)
    t_chrono = f"{minutes_t:02d}:{seconds_t:02d}"

    try:
        if mdp_results.pose_landmarks and nom_exercice != "":
            landmarks = mdp_results.pose_landmarks.landmark
            if nom_exercice != past_exercice:
                counter = 0  
                status = True
                l_status = True
                r_status = True
                action = "no"
                nochrono =True
                straightness = None
                straightness2 = None


            if nom_exercice == "pushup":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_knee = detection_body_part(landmarks, "LEFT_KNEE")

                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_knee = detection_body_part(landmarks, "RIGHT_KNEE")

                r_angle_bras = calculate_angle(r_shoulder, r_elbow, r_wrist)
                l_angle_bras = calculate_angle(l_shoulder, l_elbow, l_wrist)

                avg_arm_angle = (l_angle_bras + r_angle_bras) // 2

                lHip_angel = get_angle(l_shoulder, l_hip, l_knee)
                rHip_angel = get_angle(r_shoulder, r_hip, r_knee)

                if lHip_angel >= 130:
                    if lHip_angel>= 165 and lHip_angel< 180:
                        straightness = True
                    else:
                        straightness = False
                else:
                    straightness = None

                if status:
                    if avg_arm_angle < 100:
                        counter = counter + 1
                        action = "UP"

                        status = False
                else:
                    if avg_arm_angle > 150:
                        action = "DOWN"
                        status = True

                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    
                past_exercice = "pushup"

            if nom_exercice == "pullup":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")
                l_hip = detection_body_part(landmarks, "LEFT_WRIST")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")

                r_angle_bras = calculate_angle(r_shoulder, r_elbow, r_wrist)
                l_angle_bras = calculate_angle(l_shoulder, l_elbow, l_wrist)

                avg_arm_angle = (l_angle_bras + r_angle_bras) // 2

                if status:
                    if avg_arm_angle < 25:
                        counter = counter + 1
                        action = "DOWN"

                        status = False
                else:
                    if avg_arm_angle > 155:
                        action = "UP"
                        status = True
                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    
                past_exercice = "pullup"

            if nom_exercice == "plank":
                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    
                past_exercice = "plank"

            if nom_exercice == "squat":
                nose = detection_body_part(landmarks, "NOSE")
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_knee = detection_body_part(landmarks, "LEFT_KNEE")
                l_ankle = detection_body_part(landmarks, "LEFT_ANKLE")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")

                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_knee = detection_body_part(landmarks, "RIGHT_KNEE")
                r_ankle = detection_body_part(landmarks, "RIGHT_ANKLE")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")

                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")

                angle4 = calculate_angle(r_hip, r_knee, r_ankle)
                angle5 = calculate_angle(l_hip, l_knee, l_ankle)
                angle = (angle4 + angle5) // 2

                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                
                lHip_angel = get_angle(l_shoulder, l_hip, l_knee)
                rHip_angel = get_angle(r_shoulder, r_hip, r_knee)

                lHip_ankle_angel = get_angle(l_shoulder, l_hip, l_ankle)

                if status:
                    if angle < 110:
                        counter = counter + 1
                        action = "UP"
                        status = False
                    straightness = None

                else:
                    if angle > 165:
                        action = "DOWN"
                        status = True
                    if lHip_angel < 90:
                        # if lHip_ankle_angel >= 116 and lHip_ankle_angel < 130:
                        if lHip_angel >= 60 and lHip_angel < 90:
                            straightness = True
                        else:
                            straightness = False
                    else:
                        straightness = None
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    
                past_exercice = "squat"

            if nom_exercice == "overhead-press":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                angle4 = calculate_angle(r_hip, r_shoulder, r_elbow)
                
                angle5 = calculate_angle(l_hip, l_shoulder, l_elbow)
                

                angle = (angle4 + angle5) // 2
                

                if status:
                    if angle > 150:
                        action = "DOWN"
                        status = False

                else:
                    if angle < 95:
                        counter = counter + 1
                        action = "UP"
                        status = True
                        
                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    
                        
                        
                past_exercice = "overhead-press"

            if nom_exercice == "deadlift":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_knee = detection_body_part(landmarks, "LEFT_KNEE")
                l_ankle = detection_body_part(landmarks, "LEFT_ANKLE")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")

                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_knee = detection_body_part(landmarks, "RIGHT_KNEE")
                r_ankle = detection_body_part(landmarks, "RIGHT_ANKLE")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")


                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                
                angle4 = calculate_angle(r_hip, r_knee, r_ankle)
                angle5 = calculate_angle(l_hip, l_knee, l_ankle)
                angle = (angle4 + angle5) // 2


                lHip_angel = get_angle(l_shoulder, l_hip, l_knee)
                rHip_angel = get_angle(r_shoulder, r_hip, r_knee)
                
                lShouler_angel = get_angle(l_elbow, l_shoulder, l_hip)
                rShouler_angel = get_angle(r_elbow,r_shoulder, r_hip)
                
                lHip_ankle_angel = get_angle(l_shoulder, l_hip, l_ankle)

                if status:
                    if angle < 110:
                        counter = counter + 1
                        action = "UP"
                        status = False
                    straightness = None

                else:
                    if angle > 165:
                        action = "DOWN"
                        status = True

                    if (lHip_ankle_angel >= 98 and lHip_ankle_angel < 110):
                        straightness = True
                    else:
                        straightness = False

                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    

                past_exercice = "deadlift"

            if nom_exercice == "bench-press":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")

                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")

                r_angle_bras = calculate_angle(r_shoulder, r_elbow, r_wrist)
                l_angle_bras = calculate_angle(l_shoulder, l_elbow, l_wrist)

                avg_arm_angle = (l_angle_bras + r_angle_bras) // 2
                

                if status:
                    if avg_arm_angle < 72:
                        counter = counter + 1
                        action = "UP"
                        status = False
                else:
                    if avg_arm_angle > 155:
                        action = "DOWN"
                        status = True

                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    

                past_exercice = "bench-press"

            if nom_exercice == "biceps-curl-bar":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")

                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")

                r_angle_bras = calculate_angle(r_shoulder, r_elbow, r_wrist)
                l_angle_bras = calculate_angle(l_shoulder, l_elbow, l_wrist)

                avg_arm_angle = (l_angle_bras + r_angle_bras) // 2

                

                if status:
                    # if avg_arm_angle > 163:
                    if l_angle_bras > 163 or r_angle_bras > 163:
                        action = "UP"
                        status = False

                else:
                    # if avg_arm_angle < 30:
                    if l_angle_bras < 30 or r_angle_bras < 30:
                        counter = counter + 1
                        action = "DOWN"
                        status = True
                        
                        
                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    
                        
                past_exercice = "biceps-curl-bar"

            if nom_exercice == "arm-raise":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                angle4 = calculate_angle(r_hip, r_shoulder, r_elbow)
                
                angle5 = calculate_angle(l_hip, l_shoulder, l_elbow)
                

                angle = (angle4 + angle5) // 2
                

                if status:
                    if angle < 16:
                        action = "UP"
                        status = False
                else:
                    if angle > 80:
                        counter = counter + 1
                        action = "DOWN"
                        status = True
                        
                        
                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    
                        
                past_exercice = "arm-raise"

            if nom_exercice == "leg-raise":
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_knee = detection_body_part(landmarks, "LEFT_KNEE")
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_knee = detection_body_part(landmarks, "RIGHT_KNEE")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")

                angle4 = calculate_angle(r_knee, r_hip, r_shoulder)
                # # print(angle4)
                angle5 = calculate_angle(l_knee, l_hip, l_shoulder)
                # # print(angle5+"L")

                angle = (angle4 + angle5) // 2
                # print(angle)

                if status:
                    # if angle >= 70 and angle < 90 :
                    if angle < 90 :
                        action = "DOWN"

                        counter = counter + 1
                        status = False
                else:
                    if angle >= 150 and angle < 180:
                        action = "UP"

                        status = True

                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    

                past_exercice = "leg-raise"

            if nom_exercice == "bird-dog":
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_knee = detection_body_part(landmarks, "LEFT_KNEE")
                l_ankle = detection_body_part(landmarks, "LEFT_ANKLE")

                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_knee = detection_body_part(landmarks, "RIGHT_KNEE")
                r_ankle = detection_body_part(landmarks, "RIGHT_ANKLE")

                angle4 = calculate_angle(r_hip, r_knee, r_ankle)
                angle5 = calculate_angle(l_hip, l_knee, l_ankle)
                angle = (angle4 + angle5) // 2

                lHip_angel = get_angle(l_shoulder, l_hip, l_knee)
                rHip_angel = get_angle(r_shoulder, r_hip, r_knee)

                lHip_ankle_angel = get_angle(l_shoulder, l_hip, l_ankle)
                
                if status:
                    if lHip_angel < 110:
                        action = "UP"
                        status = False
                    if  lHip_angel>=165:
                        straightness = True
                    else:
                        straightness = False
                else:
                    straightness= None
                    if lHip_angel > 110:
                        counter = counter + 1
                        action = "DOWN"
                        status = True

                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    

                past_exercice = "bird-dog"

            if nom_exercice == "basic-curl":
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")

                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")

                
                r_angle_bras = calculate_angle(r_shoulder, r_elbow, r_wrist)
                l_angle_bras = calculate_angle(l_shoulder, l_elbow, l_wrist)

                avg_arm_angle = (l_angle_bras + r_angle_bras) // 2
                
                if l_status and l_angle_bras > 160:
                    counter += 1
                    action = "UP Left"
                    l_status = False
                elif not l_status and l_angle_bras < 50:
                    action = "NEXT HAND"
                    l_status = True 
                    
                if r_status and r_angle_bras > 160:
                    counter += 1
                    action = "UP Right"
                    r_status = False
                elif not r_status and r_angle_bras < 50:
                    action = "NEXT HAND"
                    r_status = True 

                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    

                past_exercice = "basic-curl"
                
            if nom_exercice == "bicycle-crunch":
                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_knee = detection_body_part(landmarks, "LEFT_KNEE")
                l_ankle = detection_body_part(landmarks, "LEFT_ANKLE")
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_knee = detection_body_part(landmarks, "RIGHT_KNEE")
                r_ankle = detection_body_part(landmarks, "RIGHT_ANKLE")

                r_angle_bras = calculate_angle(r_hip, r_knee, r_ankle)
                l_angle_bras = calculate_angle(l_hip, l_knee, l_ankle)
                
                if l_status and l_angle_bras < 70:
                    counter += 1
                    action = "Push Right"
                    l_status = False
                elif not l_status and l_angle_bras  > 96:
                    action = "NEXT LEG"
                    l_status = True 
                    
                if r_status and r_angle_bras < 70:
                    counter += 1
                    action = "Push Left"
                    r_status = False
                elif not r_status and r_angle_bras > 96:
                    action = "NEXT LEG"
                    r_status = True 
                    
                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    

                past_exercice = "bicycle-crunch"
                
            if nom_exercice == "fly":
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")

                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")

                # r_x_dist = abs(r_shoulder[0] - r_wrist[0])
                # l_x_dist = abs(l_shoulder[0] - l_wrist[0])
                
                r_angle_bras = calculate_angle(r_hip, r_shoulder, r_elbow)
                l_angle_bras = calculate_angle(l_hip, l_shoulder, l_elbow)


                # if status and (r_x_dist < 0.09 or l_x_dist< 0.09 ):
                if status and (r_angle_bras <= 26 ) and  (l_angle_bras <= 26 ):
                        action = "Open"
                        status = False

                elif not status and (r_angle_bras > 26 or l_angle_bras > 26 ):
                        counter = counter + 1
                        action = "Close"
                        status = True
                    
                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    


                past_exercice = "fly"
                
            if nom_exercice == "russian-twist":
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")

                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")
                
                r_angle_bras = calculate_angle(r_hip, r_shoulder, r_elbow)
                l_angle_bras = calculate_angle(l_hip, l_shoulder, l_elbow)


                # if status and (r_angle_bras <= 27) or (l_angle_bras <= 27):
                if status and (r_angle_bras < 27):
                        action = "Next Hip"
                        status = False

                # elif not status and (r_angle_bras >= 28 and r_angle_bras <= 60) or (l_angle_bras >= 28 and l_angle_bras <= 60):
                # elif not status and (r_angle_bras >= 28 and r_angle_bras <= 60):
                elif not status and (r_angle_bras >= 30):
                        counter = counter + 1
                        action = "Next Hip"
                        status = True

                if nochrono:
                    start_time = time.time()
                    nochrono = False
                    
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    


                past_exercice = "russian-twist"
                
            if nom_exercice == "superman":
                r_hip = detection_body_part(landmarks, "RIGHT_HIP")
                r_shoulder = detection_body_part(landmarks, "RIGHT_SHOULDER")
                r_elbow = detection_body_part(landmarks, "RIGHT_ELBOW")
                r_wrist = detection_body_part(landmarks, "RIGHT_WRIST")
                r_ankel = detection_body_part(landmarks, "RIGHT_ANKLE")

                l_hip = detection_body_part(landmarks, "LEFT_HIP")
                l_shoulder = detection_body_part(landmarks, "LEFT_SHOULDER")
                l_elbow = detection_body_part(landmarks, "LEFT_ELBOW")
                l_wrist = detection_body_part(landmarks, "LEFT_WRIST")
                l_ankel = detection_body_part(landmarks, "LEFT_ANKLE")


                angle_shoulder_hip_left = calculate_angle(l_shoulder, l_hip, l_ankel)
                angle_shoulder_hip_right = calculate_angle(r_shoulder, r_hip, r_ankel)

                # if angle_shoulder_hip_left > 168 or angle_shoulder_hip_right > 168:
                if angle_shoulder_hip_right > 168:
                    if status:
                        counter += 1
                        action = "up"
                        status = False
                        
                else:
                    action = "down"
                    status = True


                if nochrono:
                    start_time = time.time()
                    nochrono = False
                if not nochrono:
                    try:
                        elapsed_time = time.time() - start_time

                        minutes = int((elapsed_time % 3600) / 60)
                        seconds = int(elapsed_time % 60)

                        t = f"{minutes:02d}:{seconds:02d}"
                        
                    except:
                        print("Error")    


                past_exercice = "superman"



            results = {
                "current_exercise": nom_exercice,
                "rep_counter": counter,
                "next_action": action,
                "chrono": t,
                "total_chrono": t_chrono,
                "straightness": str(straightness),
            }
            # straightness =None
            return results, True
        else:
            return {}, False
    except:
        return {}, False




def display_analyse_result(
    nom_exercice,
):
    global nochrono, counter, action, t_chrono, t
    
    score_table = np.ones((210,360), dtype=np.uint8)
    cv2.putText(
        score_table,
        "Activity : " + nom_exercice,
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (182, 158, 128),
        2,
        cv2.LINE_AA,
    )

    if nochrono:
        cv2.putText(
            score_table,
            "Counter : " + str(counter),
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (182, 158, 128),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            score_table,
            "Action : " + str(action),
            (10, 135),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (182, 158, 128),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            score_table,
            "Chrono Total : " + str(t_chrono),
            (10, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (182, 158, 128),
            2,
            cv2.LINE_AA,
        )

    else:
        cv2.putText(
            score_table,
            "Chrono : " + str(t),
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (182, 158, 128),
            2,
            cv2.LINE_AA,
        )

    cv2.imshow("Score Table", score_table)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
