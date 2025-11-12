from app.utils.landmarks_utils import calculate_joint_angle
from app.utils.audio_feedback import play_feedback_sound

def process_pushup(landmarks_dict, pushup):
    right_elbow = None 
    left_elbow = None  
    feedback = None
    if landmarks_dict.get('right_shoulder') and landmarks_dict.get('right_elbow') and landmarks_dict.get('right_wrist'):
        right_elbow = calculate_joint_angle(landmarks_dict['right_shoulder'], landmarks_dict['right_elbow'], landmarks_dict['right_wrist'])
    if landmarks_dict.get('left_shoulder') and landmarks_dict.get('left_elbow') and landmarks_dict.get('left_wrist'):
        left_elbow = calculate_joint_angle(landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'], landmarks_dict['left_wrist'])

    if(right_elbow is not None or left_elbow is not None):
        if landmarks_dict.get('right_shoulder') and landmarks_dict.get('left_shoulder') and landmarks_dict.get("right_wrist") and landmarks_dict.get("left_wrist"):
            right_shoulder = landmarks_dict.get('right_shoulder')
            left_shoulder = landmarks_dict.get('left_shoulder')
            right_wrist = landmarks_dict.get("right_wrist")
            left_wrist = landmarks_dict.get("left_wrist")
            
            feedback = pushup.detect_common_mistakes({
                'right_shoulder': right_shoulder, 
                'left_shoulder': left_shoulder,
                'right_elbow': right_elbow,
                'left_elbow': left_elbow
            })
            
            if(feedback):
                print(feedback)
                play_feedback_sound(feedback)

        else:
            print("Missing landmarks for form check")
        
        pushup.update({'right_elbow': right_elbow, 'left_elbow': left_elbow})
    return pushup, feedback