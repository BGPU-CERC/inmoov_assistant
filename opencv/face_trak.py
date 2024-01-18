import cv2
import threading

from inmoov.head_controller import HeadController

modelFile = "opencv/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "opencv/models/deploy.prototxt"


class FaceTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.head_controller = HeadController()
        self.x_center = None
        self.y_center = None
        self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.thread = None
        self.is_tracking = False

    def detect_face_openCV_dnn(self, net, frame, conf_threshold=0.7):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        blob = cv2.dnn.blobFromImage(
            frame,
            1.0,
            (300, 300),
            [104, 117, 123],
            False,
            False,
        )

        net.setInput(blob)
        detections = net.forward()
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    int(round(frameHeight / 150)),
                    8,
                )

                # determine the center of the rectangle
                # self.x_center = x1 + (x2 - x1) / 2
                # self.y_center = y1 + (y2 - y1) / 2

                self.x_center = int((x1 + x2) / 2)
                self.y_center = int((y1 + y2) / 2)

                # errorX = int(frameWidth / 2) - self.x_center
                # errorY = int(frameHeight / 2) - self.y_center

                print(f"x: {self.x_center} y: {self.y_center}")
                # print(f"errX: {errorX} errY: {errorY}")

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.circle(frame, (self.x_center, self.y_center), 5, (0, 0, 255), -1)

                # Центральные линии
                cv2.line(
                    frame,
                    (int(frameWidth / 2), 0),
                    (int(frameWidth / 2), frameHeight),
                    (0, 0, 0),
                    1,
                )
                cv2.line(
                    frame,
                    (0, int(frameHeight / 2)),
                    (frameWidth, int(frameHeight / 2)),
                    (0, 0, 0),
                    1,
                )

                # # вставляем значение ошибки по X
                # cv2.putText(
                #     frame,
                #     str(errorX),
                #     (self.x_center + 20, self.y_center - 5),
                #     font,
                #     0.5,
                #     (0, 0, 0),
                #     1,
                # )

                # # вставляем значение ошибки по Y
                # cv2.putText(
                #     frame,
                #     str(errorY),
                #     (self.x_center - 30, self.y_center + 20),
                #     font,
                #     0.5,
                #     (0, 0, 0),
                #     1,
                # )

                # # рисуем линию "ошибки" по X
                # cv2.line(
                #     frame,
                #     (int(frameWidth / 2), self.y_center),
                #     (self.x_center, self.y_center),
                #     (0, 255, 0),
                #     1,
                # )

                # # рисуем линию "ошибки" по Y
                # cv2.line(
                #     frame,
                #     (self.x_center, int(frameHeight / 2)),
                #     (self.x_center, self.y_center),
                #     (0, 255, 0),
                #     1,
                # )

                self.head_controller.adjust_head_position(
                    self.x_center, self.y_center, frameWidth, frameHeight
                )

                top = x1
                right = y1
                bottom = x2 - x1
                left = y2 - y1

                #  blurry rectangle to the detected face
                face = frame[right : right + left, top : top + bottom]
                frame[right : right + face.shape[0], top : top + face.shape[1]] = face

        return frame, bboxes

    def process_next_frame(self):
        self.is_tracking = True
        frame_counter = 0  # Счетчик кадров
        process_every_n_frames = 4  # Обработка каждого n-го кадра
        while self.is_tracking:
            try:
                _, frameOrig = self.cap.read()

                # if self.x_center is not None and self.y_center is not None:
                #     self.head_controller.move_head(self.x_center, 640, 480, 26)
                #     self.head_controller.move_head(self.y_center, 640, 480, 13)

                frame_counter += 1
                if frame_counter % process_every_n_frames != 0:
                    continue

                resize_frame = cv2.resize(frameOrig, (640, 480))
                outOpencvDnn, bboxes = self.detect_face_openCV_dnn(
                    self.net, resize_frame
                )
                cv2.imshow("frame", resize_frame)

            except Exception as e:
                print(f"exc: {e}")
                pass

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    def start_video_tracking(self):
        self.thread = threading.Thread(target=self.process_next_frame)
        self.thread.start()

    def stop_video_tracking(self):
        self.is_tracking = False
        self.thread.join()
        cv2.destroyAllWindows()

    def release_capture(self):
        self.cap.release()
