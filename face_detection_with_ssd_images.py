# MIT License
#
# Copyright (c) 2018 Peter Tanugraha
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import glob

import numpy as np
import tensorflow as tf
import cv2

import _init_paths
from src.utils import post_process_ssd_predictions,run_inference_for_single_image_through_ssd,load_tf_ssd_detection_graph

def run_tf_object_detection_images(input_graph,image_tensor, tensor_dict,path_to_images_dir=None):

  image_list = glob.glob(path_to_images_dir+'*.jpg')
  print(image_list)

  with input_graph.as_default():
    with tf.Session() as sess:
      for cur_image_path in image_list:
        while True:
            image = cv2.imread(cur_image_path)
            image_np = (cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).astype(np.uint8) #Convert to RGB and convert to uint8
            output_dict = run_inference_for_single_image_through_ssd(sess,image_np,image_tensor,tensor_dict)
            dets = post_process_ssd_predictions(image_np,output_dict,threshold=0.25)

            for cur_det in dets:
              boxes = cur_det[:4]
              ymin = boxes[0]
              xmin = boxes[1]
              ymax = boxes[2]
              xmax = boxes[3]
              conf_score = cur_det[4]
              cv2.rectangle(image_np,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(255,0,0),3) #This is still RGB here,that's why the first element is Red

            image_np_bgr = image_np[..., ::-1]
            cv2.imshow('face-detection-ssd', image_np_bgr)
            print("Press Escape to go to next image")
            if cv2.waitKey(1) == 27:
              break

  cv2.destroyAllWindows()
  return

if __name__ == "__main__":
  PATH_TO_FROZEN_GRAPH = './model/ssd_models/ssd_mobilenet_v1_focal_loss_face_mark_2.pb'
  PATH_TO_IMAGES_DIR = './images/'

  main_graph = tf.Graph()
  image_tensor,tensor_dict=load_tf_ssd_detection_graph(PATH_TO_FROZEN_GRAPH,input_graph = main_graph)
  run_tf_object_detection_images(main_graph,image_tensor, tensor_dict,path_to_images_dir=PATH_TO_IMAGES_DIR)


