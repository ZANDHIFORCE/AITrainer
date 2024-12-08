import cv2
import mediapipe as mp
import time
import math

class poseDetector():
    
    def __init__(self, static_image_mode=False, model_complexity = 1, smooth_landmarks = True, enable_segmentation=False, 
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        
        # static_image_mode=False,
        # model_complexity=1,
        # smooth_landmarks=True,
        # enable_segmentation=False,
        # min_detection_confidence=0.5,
        # min_tracking_confidence=0.5
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.min_detection_confidence,self.min_tracking_confidence)
        
        #draw or not
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if draw:
            if self.results.pose_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
    
        return img
    
    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h ,w ,c = img.shape
                #23 24 25 26
                cx, cy, cz= lm.x, lm.y, lm.z  #pixel value for int
                lmList.append([id, (cx, cy, cz)])
                if draw:
                    cv2.circle(img, (cx*w, cy*h), 10, (0,0,255),cv2.FILLED)
        return lmList
                
def main():
    pass
    cap = cv2.VideoCapture("dance.mp4")
    pTime = 0
    detector = poseDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, False)
        
        if lmList:
            print(lmList[23])
            cv2.circle(img, lmList[23][1], 10, (0,0,255),cv2.FILLED)
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("image",img)

        cv2.waitKey(1)
    
if __name__ == "__main__":
    main()