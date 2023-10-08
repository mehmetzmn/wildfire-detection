"""
TODO: 

- In this part, model takes input images and outputs the predicted 
  bounding boxes and classes. 
- For output images, this part ask users to input the which camera they want to
  save the output images to. Output images are saved that respective camera's folder
  in the static/images folder.
- If the camera folder not created, it will create one.
- For test purposes, I wrote this comment
"""

import os
import shutil
import cv2
from ultralytics import YOLO

PATH_MODEL = "/Users/archosan/Desktop/Python projects/wildfire detection/models/runs/detect/train/weights/last.pt"

def check_camera_id(PATH_OUTPUT: str, folder_name: str = "camera") -> int:
    
    extracted_camera_folder_name = PATH_OUTPUT.split("/")[-1]
    folder_name_length = len(folder_name)
    extracted_camera_id = extracted_camera_folder_name[folder_name_length:]

    return extracted_camera_id


def detect(PATH_MODEL: str, folder_name: str) -> None:
    PATH_IMAGE = input("Enter the path of the image: ")
    PATH_OUTPUT = input("Enter the path of the output image: ")

    model = YOLO(PATH_MODEL)
    model.to('mps')

    img = cv2.imread(PATH_IMAGE)

    width = 1280
    height = 720
    dim = (width, height)

    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # Run YOLOv8 inference on the frame
    extracted_camera_id = check_camera_id(PATH_OUTPUT)
    # model.predict(img, project=f'static/images/{folder_name}{extracted_camera_id}')
    # model.predict(img, project=PATH_OUTPUT, save=True)

    for path in os.listdir(PATH_OUTPUT):
        if path == 'predict':
            src_path = os.path.join(PATH_OUTPUT, path)
            dst_path = os.path.join(PATH_OUTPUT)
            if os.listdir(src_path) != []:
              for file in os.listdir(src_path):
                  shutil.move(os.path.join(src_path, file), dst_path)
            os.rmdir(src_path)
            
            
detect(PATH_MODEL, "camera")
# print(check_camera_id("/Users/archosan/Desktop/Python projects/wildfire detection/UI/static/images/camera1"))
