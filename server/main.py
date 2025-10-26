import cv2
from pose_detector import PoseDetector
from utils.landmarks_utils import get_landmarks_dict, calculate_joint_angle
from exercises.squat import Squat
from exercises.pushup import Pushup
from exercises.tricep_dips import TricepDips
from exercise import RepType
from audio_cues import play_go_lower_sound, play_feedback_sound
import time
from typing import Generator


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
my_pose_detector = PoseDetector('model/pose_landmarker_full.task')
if not cap.isOpened():
    print("Cannot open camera")
    exit()

frame_count = 0
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30

squat = Squat()
pushup = Pushup()
tricep_dips = TricepDips()

last_audio_time = 0
audio_cooldown = 4
show_go_lower_message = False
message_start_time = 0


def generate_frames()-> Generator[bytes, None, None]:
    global last_audio_time, show_go_lower_message, message_start_time, frame_count
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        landmarks_dict = {}
        right_knee = None 
        left_knee = None   

        timestamp_ms = int(frame_count * 1000 / fps)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_with_landmarks, landmarks = my_pose_detector.detect_landmarks(
            data=rgb_frame, 
            timestamp_ms=timestamp_ms
        )
        if landmarks.pose_world_landmarks:
            pose_world_landmarks = landmarks.pose_world_landmarks[0]
            landmarks_dict = get_landmarks_dict(pose_world_landmarks)

        if landmarks_dict.get('right_hip') and landmarks_dict.get('right_knee') and landmarks_dict.get('right_ankle'):
            right_knee = calculate_joint_angle(landmarks_dict['right_hip'], landmarks_dict['right_knee'], landmarks_dict['right_ankle'])
        if landmarks_dict.get('left_hip') and landmarks_dict.get('left_knee') and landmarks_dict.get('left_ankle'):
            left_knee = calculate_joint_angle(landmarks_dict['left_hip'], landmarks_dict['left_knee'], landmarks_dict['left_ankle'])

        if(right_knee is not None or left_knee is not None):
            if landmarks_dict.get('right_shoulder') and landmarks_dict.get('left_shoulder') and landmarks_dict.get("right_ankle") and landmarks_dict.get("left_ankle"):
                right_shoulder = landmarks_dict.get('right_shoulder')
                left_shoulder = landmarks_dict.get('left_shoulder')
                right_ankle = landmarks_dict.get("right_ankle")
                left_ankle = landmarks_dict.get("left_ankle")
                
                feedback = squat.detect_common_mistakes({
                    'right_shoulder': right_shoulder, 
                    'left_shoulder': left_shoulder,
                    'right_ankle': right_ankle,
                    'left_ankle': left_ankle
                })
                
                if(feedback):
                    print(feedback)
                    play_feedback_sound(feedback)
                    cv2.putText(image_with_landmarks, f'{feedback}',
                        (50, 250),  
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 255, 255),
                        2,
                        cv2.LINE_AA)
            else:
                print("Missing landmarks for form check")
            
            rep_count, current_phase, rep_type = squat.update({'right_knee': right_knee, 'left_knee': left_knee})
            
            cv2.putText(image_with_landmarks, f'Reps: {squat.rep_count}', 
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    3,
                    cv2.LINE_AA)
            
            if squat.last_rep_type == RepType.PARTIAL:
                current_time = time.time()

                # Only play audio if enough time has passed
                if current_time - last_audio_time > audio_cooldown:
                    play_go_lower_sound()
                    last_audio_time = current_time
                    show_go_lower_message = True
                    message_start_time = current_time
                
                squat.last_rep_type = None
            
            if show_go_lower_message:
                if time.time() - message_start_time < 2:
                    cv2.putText(image_with_landmarks, f'Go Lower !', 
                                (700, 700),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.5,
                                (0, 0, 255),
                                2,
                                cv2.LINE_AA)
                else:
                    show_go_lower_message = False

            print(squat.phase_history)

        # if landmarks_dict.get('right_shoulder') and landmarks_dict.get('right_elbow') and landmarks_dict.get('right_wrist'):
        #     right_elbow = calculate_joint_angle(landmarks_dict['right_shoulder'], landmarks_dict['right_elbow'], landmarks_dict['right_wrist'])
        # if landmarks_dict.get('left_shoulder') and landmarks_dict.get('left_elbow') and landmarks_dict.get('left_wrist'):
        #     left_elbow = calculate_joint_angle(landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'], landmarks_dict['left_wrist'])

        # if(right_elbow is not None or left_elbow is not None):
        #     if landmarks_dict.get('right_shoulder') and landmarks_dict.get('left_shoulder') and landmarks_dict.get("right_wrist") and landmarks_dict.get("left_wrist") and landmarks_dict.get("right_knee") and landmarks_dict.get("left_knee") and landmarks_dict.get("right_hip") and landmarks_dict.get("left_hip"):
        #         right_shoulder = landmarks_dict.get('right_shoulder')
        #         left_shoulder = landmarks_dict.get('left_shoulder')
        #         right_wrist = landmarks_dict.get("right_wrist")
        #         left_wrist = landmarks_dict.get("left_wrist")
        #         right_knee = landmarks_dict.get("right_knee")
        #         left_knee = landmarks_dict.get("left_knee")
        #         right_hip = landmarks_dict.get("right_hip")
        #         left_hip = landmarks_dict.get("left_hip")
                
        #         feedback = pushup.detect_common_mistakes({
        #             'right_shoulder': right_shoulder, 
        #             'left_shoulder': left_shoulder,
        #             'right_wrist': right_wrist,
        #             'left_wrist': left_wrist,
        #             'right_knee': right_knee,
        #             'left_knee': left_knee,
        #             'right_hip': right_hip,
        #             'left_hip': left_hip
        #         })
                
        #         if(feedback):
        #             # play_feedback_async(feedback)
        #             cv2.putText(image_with_landmarks, f'{feedback}',
        #                 (50, 250),  
        #                 cv2.FONT_HERSHEY_SIMPLEX,
        #                 1.2,
        #                 (0, 255, 255),
        #                 2,
        #                 cv2.LINE_AA)
        #     else:
        #         print("Missing landmarks for form check")
            
        #     rep_count, current_phase, rep_type = pushup.update({'right_elbow': right_elbow, 'left_elbow': left_elbow})
            
        #     cv2.putText(image_with_landmarks, f'Reps: {pushup.rep_count}', 
        #             (50, 100),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             2,
        #             (0, 255, 0),
        #             3,
        #             cv2.LINE_AA)
            
        #     if pushup.last_rep_type == RepType.PARTIAL:
        #         current_time = time.time()
        
        #         # Only play audio if enough time has passed
        #         if current_time - last_audio_time > audio_cooldown:
        #             play_go_lower_sound()
        #             last_audio_time = current_time
        #             show_go_lower_message = True
        #             message_start_time = current_time
                
        #         pushup.last_rep_type = None
            
        #     if show_go_lower_message:
        #         if time.time() - message_start_time < 2:
        #             cv2.putText(image_with_landmarks, f'Go Lower !', 
        #                         (700, 700),
        #                         cv2.FONT_HERSHEY_SIMPLEX,
        #                         1.5,
        #                         (0, 0, 255),
        #                         2,
        #                         cv2.LINE_AA)
        #         else:
        #             show_go_lower_message = False

        #     print(pushup.phase_history)
            
        # cv2.imshow('frame', image_with_landmarks)
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', image_with_landmarks)
        frame_bytes = buffer.tobytes()
        
        # Yield frame in multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        frame_count += 1
        
        # if cv2.waitKey(1) == ord('q'):
        #     break

    # cap.release()
    # cv2.destroyAllWindows()