from app.utils.landmarks_utils import calculate_joint_angle
from app.utils.audio_feedback import play_feedback_sound

def process_squat(landmarks_dict, squat):
    right_knee = None 
    left_knee = None  
    feedback = None
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

        else:
            print("Missing landmarks for form check")
        
        squat.update({'right_knee': right_knee, 'left_knee': left_knee})
    return squat, feedback