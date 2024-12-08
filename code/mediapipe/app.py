import cv2
import time
import PoseModule as pm
import math

def getXY(img, coord):
    h, w, c = img.shape
    return (int(coord[0]*w), int(coord[1]*h))

def calculate_3d_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)

def calculate_angle(pointA, pointB, pointC):
    # 벡터 AB와 BC를 정의
    AB = [pointA[0] - pointB[0], pointA[1] - pointB[1], pointA[2] - pointB[2]]
    BC = [pointC[0] - pointB[0], pointC[1] - pointB[1], pointC[2] - pointB[2]]
    # 벡터 AB와 BC의 내적 계산
    dot_product = AB[0] * BC[0] + AB[1] * BC[1] + AB[2] * BC[2]
    # 벡터 AB와 BC의 크기 계산
    magnitude_AB = math.sqrt(AB[0]**2 + AB[1]**2 + AB[2]**2)
    magnitude_BC = math.sqrt(BC[0]**2 + BC[1]**2 + BC[2]**2)
    # 두 벡터 사이의 각도 계산 (라디안)
    angle_rad = math.acos(dot_product / (magnitude_AB * magnitude_BC))
    # 각도를 도(degree) 단위로 변환
    angle_deg = math.degrees(angle_rad)
    return angle_deg

#가동범위
def checkShallowSquat(lmList, mod_2d=False):
    # 골반-발목 거리 & 무릎-발목 거리 비교
    if mod_2d == False:
        left_hip_c, right_hip_c = lmList[23][1], lmList[24][1]
        left_knee_c, right_knee_c = lmList[25][1], lmList[26][1]
        left_ankel_c, right_ankel_c = lmList[27][1], lmList[28][1]

        left_knee_ankel = calculate_3d_distance(left_knee_c, left_ankel_c)
        left_hip_ankel = calculate_3d_distance(left_hip_c, left_ankel_c)
        right_knee_ankel = calculate_3d_distance(right_knee_c, right_ankel_c)
        right_hip_ankel = calculate_3d_distance(right_hip_c, right_ankel_c)
        return False if left_hip_ankel <= left_knee_ankel or right_hip_ankel <= right_knee_ankel else True
    # 단순 Y좌표 비교
    else:
        return False if lmList[23][1][1]>=lmList[25][1][1]*0.95 or lmList[24][1][1] >= lmList[26][1][1]*0.95 else True

#무릎모임
def checkKneeValgus(lmList):
    left_foot_c, right_foot_c = lmList[27][1], lmList[28][1]
    left_knee_c, right_knee_c = lmList[25][1], lmList[26][1]
    feet_lenght = calculate_3d_distance(left_foot_c, right_foot_c)
    knee_lenght = calculate_3d_distance(left_knee_c, right_knee_c)
    return True if feet_lenght > knee_lenght else False

#척추정렬
def checkWrongSpinalAlignment(lmList):
    left_shoulder_c = lmList[11][1]
    left_hip_c = lmList[23][1]
    left_knee_c = lmList[25][1]
    
    angle = calculate_angle(left_shoulder_c, left_hip_c, left_knee_c)
        # 각도에 따른 상태 판단

    if angle < 40:
        return True  # 허리가 과도하게 굽혀진 상태
    elif angle > 80:
        return True  # 허리가 과도하게 펴진 상태
    else:
        return False  # 허리가 정상적인 각도 범위 내에 있음

folders_name = ["Shallow Squat","Knee Valgus","Wrong Spinal Alignment","Right Form"]
result = []


for folder in folders_name:
    temp_str = f"[{folder}]"
    result.append(temp_str)
    print(temp_str)
    
    temp_str = "  FULL  KNEE  SPINE"
    result.append(temp_str)
    print(temp_str)
    for i in range(1,11):
        
        file_name = "squat_img\\"+folder+"\\test set\\"+str(i)+".jpg"
        cap = cv2.VideoCapture(file_name) #"squat3.mp4" or 1
        pTime = 0
        detector = pm.poseDetector(model_complexity=1)

        #video output
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec
        # out = cv2.VideoWriter('output_squat.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

        is_shallow_squat , is_knee_valgus , is_wrong_spinal_alignment = False, True, False


        while True:
            success, img = cap.read()
            if success==False:
                break
            img = detector.findPose(img)
            lmList = detector.findPosition(img, False)
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            
            if lmList:
                
                #FullSquat
                is_shallow_squat = checkShallowSquat(lmList, True)
                if is_shallow_squat == False:
                    cv2.putText(img,"FullSquat",(10,70),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
                    for idx in range(23,27):
                        pass
                        #cv2.circle(img, getXY(img, lmList[idx][1]), 5, (0,255,0),cv2.FILLED)
                else:
                    cv2.putText(img,"FullSquat",(10,70),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
                    
                #KneeValgus
                is_knee_valgus = checkKneeValgus(lmList)
                if is_knee_valgus==False:
                    cv2.putText(img,"KneeValgus",(10,90),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
                else:
                    cv2.putText(img,"KneeValgus",(10,90),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
                    for idx in range(25,27):
                        cv2.circle(img, getXY(img, lmList[idx][1]), 10, (0,0,255),cv2.FILLED)
                
                #SpinalAlignment
                is_wrong_spinal_alignment = checkWrongSpinalAlignment(lmList)
                if is_wrong_spinal_alignment == True:
                    cv2.putText(img,"SpinalAlignment",(10,110),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
                else:
                    cv2.putText(img,"SpinalAlignment",(10,110),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
                
                
            cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
            
            #output video
            # out.write(img)
            
            cv2.imshow("image",img)
            #shut if press q button
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        # out.release()
        cv2.destroyAllWindows()
        temp_str = f"{i} {is_shallow_squat} {is_knee_valgus} {is_wrong_spinal_alignment} "
        print(i, is_shallow_squat , is_knee_valgus , is_wrong_spinal_alignment, end=" ")
        if is_shallow_squat or is_knee_valgus or is_wrong_spinal_alignment:
            pass
        else:
            temp_str += "[Right Form]"
        result.append(temp_str)
        print(temp_str)

print()
print()
print("RESULT##################################")
for x in result:
    print(x)
print("########################################")