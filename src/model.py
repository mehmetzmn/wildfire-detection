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

PATH_MODEL = "./models/runs/detect/train/weights/last.pt"


def check_camera_id(PATH_OUTPUT: str, folder_name: str = "camera") -> int:

    extracted_camera_folder_name = PATH_OUTPUT.split("/")[-1]
    folder_name_length = len(folder_name)
    extracted_camera_id = extracted_camera_folder_name[folder_name_length:]

    return extracted_camera_id


def detect(PATH_MODEL: str) -> None:
    PATH_IMAGE = input("Enter the path of the image: ")
    PATH_OUTPUT = input("Enter the path of the output image: ")

    model = YOLO(PATH_MODEL)
    model.to('mps')

    def image_transform(img_path):
        print("Image path: ", img_path)
        img = cv2.imread(img_path)

        width = 1280
        height = 720
        dim = (width, height)

        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        return img

    # Run YOLOv8 inference on the frame

    if os.path.isdir(PATH_IMAGE):
        for img in os.listdir(PATH_IMAGE):
            if img == '.DS_Store':
                continue
            img_path = os.path.join(PATH_IMAGE, img)
            img = image_transform(img_path)
            img_name = os.path.splitext(os.path.basename(img_path))[0]
            # model.predict(img, project=os.path.join(PATH_OUTPUT, img_name), save=True)
            model.predict(img, project=PATH_OUTPUT,
                          name=f'{img_name}', save=True, exist_ok=True)
    else:
        img = image_transform(PATH_IMAGE)
        img_name = os.path.splitext(os.path.basename(PATH_IMAGE))[0]
        # model.predict(img, project=os.path.join(PATH_OUTPUT, img_name), save=True)
        model.predict(img, project=PATH_OUTPUT,
                      name=f'{img_name}', save=True, exist_ok=True)

    for pth in os.listdir(PATH_OUTPUT):
        if pth == ".DS_Store":
            continue
        elif os.path.isdir(os.path.join(PATH_OUTPUT, pth)):
            for img in os.listdir(os.path.join(PATH_OUTPUT, pth)):
                if img == ".DS_Store":
                    continue
                else:
                    old_name = os.path.join(PATH_OUTPUT, pth, img)
                    new_name = os.path.join(PATH_OUTPUT, pth, pth + '.jpg')
                    os.rename(old_name, new_name)
                    shutil.move(new_name, os.path.join(PATH_OUTPUT))
                    os.rmdir(os.path.join(PATH_OUTPUT, pth))


detect(PATH_MODEL)
