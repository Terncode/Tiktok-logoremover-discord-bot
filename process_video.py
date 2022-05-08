import joblib
import os
import cv2
import temp
from skimage import feature
from numba import jit

model = joblib.load("model.pkl")

def process_video(temp_folder, video_name_details):
    CUT_FRAMES = 130;
    name = video_name_details[0]
    ex = video_name_details[1]
    full_name = video_name_details[2]
    #temp_folder  temp
    downloaded_file = temp_folder + os.path.sep + "download" + os.path.sep + full_name
    
    relative_frames_dir = name + os.path.sep + "output"
    absolute_frames_dir =  temp.create_temp_directory(relative_frames_dir, True)
    output = absolute_frames_dir + os.path.sep + name + "." + "avi"

    capture = cv2.VideoCapture(downloaded_file)
    fps = capture.get(cv2.CAP_PROP_FPS)
    frames_count = round(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width =  round(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
  
    multiplayer = height / 512
    new_height = round(height / multiplayer)
    new_width = round(width / multiplayer)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output, fourcc, fps, [new_width, new_height] )
    max_frames = frames_count - CUT_FRAMES
    frames = 0
    while(True):
        ret, frame = capture.read()
        if (frame is None):
            break
        if frames > max_frames:
            return output

        #print(f"{str(frames)}/{str(frames_count)} | {max_frames}")

        ret = process_frame(frame, model)
        out.write(ret)

        frames = frames + 1
    return output



def get_padding(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    padding_left = round(width * 0.15)
    padding_right = width - padding_left

    return [padding_left, padding_right]


def crop_image(image, x, y, width, height):
  return image[y:y + height, x:x + width]

def blur_section(frame, x, y, width, height, blured_frame):
    for i in range(width):
        for j in range(height):
            try:
                frame[y + j][x + i][0] = blured_frame[y + j][x + i][0]
                frame[y + j][x + i][1] = blured_frame[y + j][x + i][1]
                frame[y + j][x + i][2] = blured_frame[y + j][x + i][2]
            except:
                pass
        #print(round(i / width * 100), i, width)

frames = 0
def process_frame(image, model):
    frame = image.copy()
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
    cr = []

    cr.append([crop_image(cc, 0, 0, 50, 50),                        [0, 0, 50, 50]])
    cr.append([crop_image(cc, 0, py, 50, 50),                       [0, py, 50, 50]])
    cr.append([crop_image(cc, padding_right, py2, 50, 50),          [padding_right, py2, 50, 50]])
    cr.append([crop_image(cc, padding_right, width - 50, 50, 50),   [padding_right, width - 50, 50, 50]])

    for i in range(len(cr)):
        cropped_frame = cr[i][0]
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        grayed_border = cv2.resize(gray, (200, 100))

        # Calculate Histogram of Test Image
        hist =  feature.hog(
                    grayed_border, 
                    orientations=9,
                    pixels_per_cell=(10, 10),
                    cells_per_block=(2, 2), 
                    transform_sqrt=True, 
                    block_norm="L1"
                )
        #cv2.imwrite("a", grayed_border)
        # Predict in model
        predict = model.predict(hist.reshape(1, -1))[0]
        if predict == "yes":
            x =         cr[i][1][0]
            y =         cr[i][1][1]
            width =     cr[i][1][2]
            height =    cr[i][1][3]
            blured_frame = cv2.GaussianBlur(frame, (25, 25), 0)
            blur_section(frame,x, y, width, height, blured_frame)

    return frame
