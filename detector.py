import cv2
import time
import pose_estimation_class as pm
import mediapipe as mp
import argparse
import numpy as np

import os
from werkzeug.utils import secure_filename
from flask import g,app

from exts import db
from setting import Config

'''
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to our input video")
ap.add_argument("-o", "--output", required=True,
	help="path to our output video")
ap.add_argument("-s", "--fps", type=int, default=30,
	help="set fps of output video")
ap.add_argument("-b", "--black", type=str, default=False,
	help="set black background")
#args = vars(ap.parse_args())
'''
def actions(video):
    


    #pTime = 0
    #black_flag = eval(args["black"])
    cap = cv2.VideoCapture(video)
    #out = cv2.VideoWriter('videos/output_video1.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 30 ,
    #                   (int(cap.get(3)), int(cap.get(4))))

    detector = pm.PoseDetector()
    new_video_name = 'new_video.mp4'
    new_video_name = secure_filename(new_video_name)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    file_path = os.path.join(Config.UPLOAD_VIDEO_DIR, new_video_name)
    #video_writer = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(width), int(height)))
    video_writer = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc('H','2','6','4'), fps, (int(width), int(height)))

    while(cap.isOpened()):
        success, img = cap.read()
        
        if success == False:
            break
        
        img, p_landmarks, p_connections = detector.findPose(img, False)
        
        # use black background
        #if black_flag:
        #    img = img * 0
        
        # draw points
        mp.solutions.drawing_utils.draw_landmarks(img, p_landmarks, p_connections)
        lmList = detector.getPosition(img)


        #cTime = time.time()
        #fps = 1 / (cTime - pTime)
        #pTime = cTime
        video_writer.write(img)
        #out.write(img)
        #cv2.imshow("Image", img)
        #cv2.waitKey(1)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    user = g.user
    path = 'upload/video/'
    user.new_video = os.path.join(path, new_video_name)
    print('2='+user.new_video)
    db.session.commit()
    cap.release()
    video_writer.release()
    #cap.release()
    #out.release()
    #cv2.destroyAllWindows()
    return 0


def imgaction(img,k):
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    with mp_holistic.Holistic(
          static_image_mode=True,
          ) as holistic:


        image = cv2.imread(img)
        image_height, image_width, _ = image.shape
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        '''
        if results.pose_landmarks:
            print(
            f'Nose coordinates: ('
            f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, '
            f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
            )
        '''
        # 在图片上画身体、左右手、面部关节点
        #annotated_image = image.copy()
        annotated_image = np.zeros(image.shape,np.uint8)
        '''    mp_drawing.draw_landmarks(
        annotated_image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        mp_drawing.draw_landmarks(
        annotated_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
        annotated_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)'''
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        #img_name=img.split('/')[-1]
        if k=='wopai':
            #user = g.user
            path = 'static/dealwith/wopaiing.jpg'
        
            #path=os.path.join(path, img_name)
            #user.picture_wopai = #根据model改属性名
            cv2.imwrite(path,annotated_image)
            #db.session.commit()
        elif k=='jiqiu':
            path = 'static/dealwith/jiqiuing.jpg'
        
            #path=os.path.join(path, img_name)
            #user.picture_wopai = #根据model改属性名
            cv2.imwrite(path,annotated_image)
    return 0   
   
