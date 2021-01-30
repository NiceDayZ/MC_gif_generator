import image
import threading
import json
import os, shutil

s = threading.Semaphore(1) #to make it multi-threaded
rgb_color_bin = b''
width = 0
height = 0
last_matrix = []

color_to_names = [
    "white_wool",
    "orange_wool",
    "magenta_wool",
    "light_blue_wool",
    "yellow_wool",
    "lime_wool",
    "pink_wool",
    "gray_wool",
    "light_gray_wool",
    "cyan_wool",
    "purple_wool",
    "blue_wool",
    "brown_wool",
    "green_wool",
    "red_wool",
    "black_wool",
    "white_terracotta",
    "orange_terracotta",
    "magenta_terracotta",
    "light_blue_terracotta",
    "yellow_terracotta",
    "lime_terracotta",
    "pink_terracotta",
    "gray_terracotta",
    "light_gray_terracotta",
    "cyan_terracotta",
    "purple_terracotta",
    "blue_terracotta",
    "brown_terracotta",
    "green_terracotta",
    "red_terracotta",
    "black_terracotta",
    "birch_planks"
]

def make_block_image_thread(frame_name, number_of_frames, frame_number):
    global s

    with s:
        print(f"[LOG] Thread for frame {frame_number} started")
        assert(number_of_frames > 0)
        img = image.Image(f"framegen/{frame_name}{frame_number}.jpg")

        total_string = ""
        for row in range(height):
            for col in range(width):
                p = img.get_pixel(col, row)
                new_color_id = (rgb_color_bin[rgb_to_index((p.get_red(), p.get_green(), p.get_blue()))])

                string = ''

                if last_matrix[row][col] != new_color_id:
                    string = f'setblock {row} {3} {col} minecraft:{color_to_names[new_color_id]}\n'
                    last_matrix[row][col] = new_color_id

                total_string += string

        print(f"[LOG] Thread for frame {frame_number} ended, now writing")

        with open(f"tickgen/tick{frame_number}.mcfunction", "wt+") as file:
            string = f'schedule function video_to_sheep:tick{(frame_number + 1) % (number_of_frames + 1)} 1t\n'
            file.write(string)
            file.write(total_string)


def rgb_to_index(rgb):
    return rgb[0]*(256**2) + rgb[1]*256 + rgb[2]


def clear_old():
    folder = './tickgen'
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
    fcount = 0
    with open("framegen/data.json", "rt") as file:
        js = json.loads(file.read())
        fcount = js["framecount"]


    with open("colors.binary", "rb") as file:
        rgb_color_bin = file.read()

    img = image.Image(f"framegen/frame0.jpg")
    width = img.width
    height = img.height

    for i in range(height):
        single_row = [-1 for j in range(width)]
        last_matrix.append(single_row)

    clear_old()

    t = []
    for i in range(fcount):
       t += [threading.Thread(target=make_block_image_thread, args=("frame", fcount-1, i))]

    for _th in t: _th.start()
    for _th in t: _th.join()
