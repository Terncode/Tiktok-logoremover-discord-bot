from pathlib import Path

import cv2
import os

SKIP_FRAMES = 300

dataset_dir = "./tiktok_samples"
samples = []
for child in Path(dataset_dir).iterdir():
    if child.is_file():
        samples.append(dataset_dir + "/" + child.name);


folder_name = "dataset"
dataset_path = "./" + folder_name
if os.path.exists(dataset_path):
  pass
else: 
  os.mkdir("./" + folder_name)

dir = {
 110: "no",
 121: "yes",
}


def next_sample():
  if len(samples) == 0:
    return None
  return samples.pop()

image_index = 0
def ask_for_image(img):
  global image_index
  cv2.imshow("Is ticktok?", img)
  key = cv2.waitKey(0)
  try:
   pressed_key = dir[key];
   print("Selected:" + pressed_key)
   name = str(image_index) + "-" + pressed_key + ".png"
   image_index = image_index + 1
   path = "./" + folder_name + "/" + name
   print(path)
   cv2.imwrite(path, img)
  except:
    print("Wrong key! Use [Y/n] to confirm your change")
    ask_for_image(img)



def get_padding(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    padding_left = round(width * 0.15)
    padding_right = width - padding_left

    return [padding_left, padding_right]


def get_cutout(image, padding_left, padding_right):
    height = image.shape[0]
    #width = image.shape[1]
    chunks = 8
    chunk_size = height // chunks
    cuts = []
    for y in range(chunks * 2):
      yy = y * (chunk_size // 2)
      cropped_left = crop(image, 0, yy, padding_left, chunk_size)
      cropped_right = crop(image, padding_right, yy, padding_left, chunk_size)

      cuts.append(cropped_left)
      cuts.append(cropped_right)
    return cuts


def crop(image, x, y, width, height):
  return image[y:y + height, x:x + width]

def process_frame(frame):
  multiplayer = frame.shape[0] / 512
  new_height = round(frame.shape[0] / multiplayer)
  new_width = round(frame.shape[1] / multiplayer)
  frame = cv2.resize(frame, (new_width, new_height))
  padding_left, padding_right = get_padding(frame)
  cuts = get_cutout(frame, padding_left, padding_right)
  for img in cuts:
    ask_for_image(img)

ll = 0
def process_video(sample):
  global ll
  capture = cv2.VideoCapture(sample)
  
  total_frames = round(capture.get(cv2.CAP_PROP_FRAME_COUNT))
  skip_frame = round(total_frames * 0.60)
  frames = 0;
  
  s = 0
  while(True):
    _, frame = capture.read()  
    if (frame is None):
      break

    if s > skip_frame:
      s = 0;
    if s == 0:
      ll = ll + 1
      multiplayer = frame.shape[0] / 512
      new_height = round(frame.shape[0] / multiplayer)
      new_width = round(frame.shape[1] / multiplayer)
      frame = cv2.resize(frame, (new_width, new_height))

      height = frame.shape[0]
      width = frame.shape[1]
      
      padding_left = round(width * 0.15)
      padding_right = width - padding_left

      cc = frame.copy()

      py = round(new_height * 0.45)
      py2 = round(new_height * 0.75)
      cr = [
        crop(cc, 0, 0, 50, 50),
        crop(cc, 0, py, 50, 50),
        crop(cc, padding_right, py2, 50, 50),
        crop(cc, padding_right, width - 50, 50, 50)
        ]

      for c in cr:
        ask_for_image(c)
        #cv2.imshow("crop", c)
        #cv2.imshow("crop2", frame)
        #cv2.waitKey(0)
        #cv2.imwrite("./temp/" + str(ll) + ".png", c)
      #process_frame(frame)


    s = s + 1
    frames = frames + 1


i = 0
samples_count = len(samples)
while(True):
  print(str(i) + "/" + str(samples_count))
  i = i + 1

  sample = next_sample()
  if sample is None:
    print("Done")
    break;

  process_video(sample)



