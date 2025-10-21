import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2


class PoseDetector:

  def __init__(self, modelPath, use_tracking=False):
    self.BaseOptions = mp.tasks.BaseOptions
    self.PoseLandmarker = mp.tasks.vision.PoseLandmarker
    self.PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    self.VisionRunningMode = mp.tasks.vision.RunningMode
    self.model_path = modelPath
    self.use_tracking = use_tracking
    running_mode = self.VisionRunningMode.VIDEO if use_tracking else self.VisionRunningMode.IMAGE

    self.options = self.PoseLandmarkerOptions(
        base_options=self.BaseOptions(model_asset_path=self.model_path),
        running_mode=running_mode,  
        min_pose_detection_confidence=0.5,  
        min_pose_presence_confidence=0.5,   
        # min_tracking_confidence=0.5        
    )
    self.detector = vision.PoseLandmarker.create_from_options(self.options)

  def draw_landmarks_on_image(self, rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
      pose_landmarks = pose_landmarks_list[idx]

      # Draw the pose landmarks.
      pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
      pose_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
      ])
      solutions.drawing_utils.draw_landmarks(
        annotated_image,
        pose_landmarks_proto,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image

  def detect_landmarks(self, data, timestamp_ms=None):
      image = mp.Image(image_format=mp.ImageFormat.SRGB, data=data)
      detection_result = self.detector.detect(image)
      annotated_image = self.draw_landmarks_on_image(image.numpy_view(), detection_result)
      annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
      return annotated_image_bgr, detection_result