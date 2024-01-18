import cv2
import dlib
import time
import requests


# from inmoov import inmoov_commands
from inmoov import server_config

# inmoov_commands.serial_open()
# time.sleep(1)
# inmoov_commands.servo_attach()

cap = cv2.VideoCapture("")  # replace with USB camera
# new_width = 640
# new_height = 480

face_detector = dlib.get_frontal_face_detector()
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)


def move_head(angle, pin):
    requests.post(
        f"{server_config.BASE_URL}/serial/ports/lt_port/set_angle",
        json={
            "angle": angle,
            "pin": pin,
            "speed": 30,
        },
    )


def keep_x(current):
    erX = 320 - current
    angleX = map(erX, 0, current, 60, 130)
    move_head(angleX, 26)


def keep_y(current):
    erY = 180 - current
    angleY = map(erY, 0, current, 50, 140)
    move_head(angleY, 13)


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def main():
    frame_counter = 0  # Счетчик кадров
    process_every_n_frames = 4  # Обработка каждого n-го кадра
    # previous_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()

        frame_counter += 1
        if frame_counter % process_every_n_frames != 0:
            continue  # Пропуск обработки кадра

        # resize_frame = cv2.resize(frame, (new_width, new_height))
        # Уменьшение размера кадра

        resize_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        height, width, _ = resize_frame.shape

        # Преобразование кадра в формат RGB
        frame_rgb = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)

        # # Обнаружение лиц с помощью нейронной сети
        # if time.time() - previous_time > 5000:
        #     previous_time = time.time()
        faces = face_detector(frame_rgb)

        # Отрисовка прямоугольных областей вокруг лиц
        for rect in faces:
            x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
            cv2.rectangle(resize_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            x *= 2
            y *= 2
            w *= 2
            h *= 2

            # first
            # center_x = x + w // 2
            # center_y = y + h // 2

            # second best
            new_x = x * 0.5
            new_y = y * 0.5
            center_x = new_x + (w * 0.5)
            center_y = new_y + (h * 0.5)

            # # third
            # center_x = x + (w // 2)
            # center_y = y + (h // 2)

            print("Центр лица: ({}, {})".format(center_x, center_y))

            print(f"y: {resize_frame.shape[0]}")
            print(f"x: {resize_frame.shape[1]}")

            # first
            # angle_y = 50 + (center_y / resize_frame.shape[0]) * 90
            # angle_x = 60 + (center_x / resize_frame.shape[1]) * 70

            # second
            angle_x = map(center_x, 0, resize_frame.shape[1], 60, 130)
            angle_y = map(center_y, 0, resize_frame.shape[0], 50, 140)
            move_head(angle_x, 26)
            move_head(angle_y, 13)

            # # fourth
            # keep_x(center_x)
            # keep_y(center_y)

        cv2.imshow("frame", resize_frame)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
