import cv2,mediapipe
__title__ = "bodytracking"
__version__ = "1.02"
__author__ = "Suprime"
class Hand:
    def __init__(self,n_hand:int,lm:list,handLms):
        self.hand_n = n_hand
        self.sol = mediapipe.solutions
        self.lm_list = lm
        self.hand_lms = handLms
        self.mpHands = self.sol.hands
        self.WRIST = self.lm_list[0]
        self.THUMB_CMC = self.lm_list[1]
        self.THUMB_MCP = self.lm_list[2]
        self.THUMB_IP = self.lm_list[3]
        self.THUMB_TIP = self.lm_list[4]
        self.INDEX_FINGER_MCP = self.lm_list[5]
        self.INDEX_FINGER_PIP = self.lm_list[6]
        self.INDEX_FINGER_DIP = self.lm_list[7]
        self.INDEX_FINGER_TIP = self.lm_list[8]
        self.MIDDLE_FINGER_MCP = self.lm_list[9]
        self.MIDDLE_FINGER_PIP = self.lm_list[10]
        self.MIDDLE_FINGER_DIP = self.lm_list[11]
        self.MIDDLE_FINGER_TIP = self.lm_list[12]
        self.RING_FINGER_MCP = self.lm_list[13]
        self.RING_FINGER_PIP = self.lm_list[14]
        self.RING_FINGER_DIP = self.lm_list[15]
        self.RING_FINGER_TIP = self.lm_list[16]
        self.PINKY_MCP = self.lm_list[17]
        self.PINKY_PIP = self.lm_list[18]
        self.PINKY_DIP = self.lm_list[19]
        self.PINKY_TIP = self.lm_list[20]
        self.THUMB = [self.THUMB_CMC,self.THUMB_MCP,self.THUMB_IP,self.THUMB_TIP]
        self.INDEX = [self.INDEX_FINGER_MCP,self.INDEX_FINGER_PIP,self.INDEX_FINGER_DIP,self.INDEX_FINGER_TIP]
        self.MIDDLE = [self.MIDDLE_FINGER_MCP,self.MIDDLE_FINGER_PIP,self.MIDDLE_FINGER_DIP,self.MIDDLE_FINGER_TIP]
        self.RING = [self.RING_FINGER_MCP,self.RING_FINGER_PIP,self.RING_FINGER_DIP,self.RING_FINGER_TIP]
        self.PINKY = [self.PINKY_MCP,self.PINKY_PIP,self.PINKY_DIP,self.PINKY_TIP]
class Pose:
    def __init__(self,lm_list:list,res):
        self.lm_list = lm_list
        self.results = res
        self.nose = lm_list[0]
        self.left_eye_inner = lm_list[1]
        self.left_eye = lm_list[2]
        self.left_eye_outer = lm_list[3]
        self.right_eye_inner = lm_list[4]
        self.right_eye = lm_list[5]
        self.right_eye_outer = lm_list[6]
        self.left_ear = lm_list[7]
        self.right_ear = lm_list[8]
        self.mouth_left = lm_list[9]
        self.mouth_right = lm_list[10]
        self.left_shoulder = lm_list[11]
        self.right_shoulder = lm_list[12]
        self.left_elbow = lm_list[13]
        self.right_elbow = lm_list[14]
        self.left_wrist = lm_list[15]
        self.right_wrist = lm_list[16]
        self.left_pinky = lm_list[17]
        self.right_pinky = lm_list[18]
        self.left_index = lm_list[19]
        self.right_index = lm_list[20]
        self.left_thumb = lm_list[21]
        self.right_thumb = lm_list[22]
        self.left_hip = lm_list[23]
        self.right_hip = lm_list[24]
        self.left_knee = lm_list[25]
        self.right_knee = lm_list[26]
        self.left_ankle = lm_list[27]
        self.right_ankle = lm_list[28]
        self.left_heel = lm_list[29]
        self.right_heel = lm_list[30]
        self.left_foot_index = lm_list[31]
        self.right_foot_index = lm_list[32]
class HandDetector:
    def __init__(self,mode=False,maxHands=2,detectionConfidence=0.5,trackConfidence=0.5):
        """
        Sets all the values for mediapipe and the other HandDetector functions.
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectConf = detectionConfidence
        self.trackConf = trackConfidence
        self.sol = mediapipe.solutions
        self.mpHands = self.sol.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectConf,self.trackConf)
        self.mpDraw = self.sol.drawing_utils
        self.nt_list = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    def get_Hands(self,img):
        """
        Finds the hands img the given img, needs RGB img
        to find the hands, so it first converts them.
        Returns the Hand object with all the landmarks for each hand.
        !!! ONLY INITIALIZE THIS ONCE!!!
        """
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        res = self.hands.process(imgRGB)
        HAND = 0
        if res.multi_hand_landmarks:
            for handLms in res.multi_hand_landmarks:
                HAND = HAND + 1
                List = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    List.append((cx,cy))
                yield Hand(HAND,List,handLms)
        else:
            return Hand(1,self.nt_list,[])
    def draw_hand(self,img,hand:Hand):
        """
        Draws the Landmarks and connections on the image.
        """
        self.mpDraw.draw_landmarks(img,hand.hand_lms ,self.mpHands.HAND_CONNECTIONS)
        return True
class PoseDetector:
    def __init__(self,static_image_mode=False,model_complexity=1,smooth_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        """
        Sets all the values for mediapipe and the other PoseDetector functions.
        !!! ONLY INITIALIZE THIS ONCE!!!
        """
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_conf = min_detection_confidence
        self.min_tracking_conf = min_tracking_confidence
        self.sol = mediapipe.solutions
        self.mpPose = self.sol.pose
        self.pose = self.mpPose.Pose()
        self.nt_list = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),]
        self.mpDraw = self.sol.drawing_utils
    def get_Pose(self,img,wd=True):
        """
        Transforms the img to RGB and then builds the Pose object
        based off all the landmarks on the frame.
        Returns the Pose object with the complete list of landmarks.
        """
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        res = self.pose.process(imgRGB).pose_landmarks
        if res:
            List = []
            if wd:
                for id, lm in enumerate(res.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    List.append((cx,cy))
                try:
                    return Pose(List, res)
                except IndexError:
                    return Pose(self.nt_list, [])
            else:
                return Pose(self.nt_list, res)
        else:
            return Pose(self.nt_list,[])
    def draw_pose(self,img,pose:Pose):
        """
        Draws the Landmarks and connections on the image.
        """
        self.mpDraw.draw_landmarks(img,pose.results,self.mpPose.POSE_CONNECTIONS)