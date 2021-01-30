import cv2
import json
import constants
import os, shutil

def video_to_frames():
    vidcap = cv2.VideoCapture(constants.VIDEO_FILE)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("framegen/frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        count += 1
    return count


def clear_folder():
    folder = './framegen'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':
    if(constants.CLEAR_BEFORE_GEN):
        clear_folder()

    fcount = video_to_frames()
    d = dict(framecount=fcount)
    with open("framegen/data.json", "wt+") as file:
        file.write(json.dumps(d))