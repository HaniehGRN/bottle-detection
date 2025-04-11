# import libraries
from PIL import Image
import cv2
import os
from google.colab import files
import shutil

# import yolo
# !pip install ultralytics  -->  terminal command to install ultralytics
from ultralytics import YOLO

# create instance
model = YOLO('yolov8n.pt')

# import dataset
# !pip install roboflow  -->  terminal command to install roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="9YOjdnw9e3p6Vq2jN5t5")
project = rf.workspace("project-pkoue").project("final_ds")
dataset = project.version(1).download("yolov8")

#         *********************************train********************************************

# train model using custom dataset
results = model.train(data='/content/datasets/data.yaml', epochs=60)

#         *********************************video prediction*********************************

# predict video using the best model generated after train
!yolo task=detect mode=predict model=best.pt conf=0.25 source='/content/test.mp4' #  -->  terminal command to predict video

#         *********************************test*********************************************

# function to create image from result array & save image into directory
def show_img(results, dir):
  for result, i in zip(results, range(len(results))):
    for part in result:
      im_array = part.plot()  # plot a BGR numpy array of predictions
      im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
      im.show()  # show image
      im.save(f'{dir}/result{i}.jpg')

# function to read test images from the directory
def load_images_from_folder(dir):
    images = []
    for filename in os.listdir(dir):
        img = cv2.imread(os.path.join(dir,filename))
        if img is not None:
            images.append(img)
    return images

test_img_dir = '/content/datasets/test/images'
test_imgs = load_images_from_folder(test_img_dir)

# function to detect images
def detect_imgs(imgs):
  results = []
  for img in imgs:
    result = model(img)
    results.append(result)
  return results

results = detect_imgs(test_imgs)
show_img(results, '/content/results_imgs')

# download test result images
shutil.make_archive("test_results", 'zip', "/content/results_imgs")
files.download("test_results.zip")



