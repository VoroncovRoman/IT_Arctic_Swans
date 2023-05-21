"""
Модуль содержить "проигрывать" нейронной сети. Функция принимает картинку и модель и возвращает количество распознных
классов.
"""

from ultralytics import YOLO
import cv2

classNames = ["klikun", "maliy", "shipun"]

def activate_yolo(model_path, image_path):
    # a = 0
    # b = 0
    # c = 0
    model = YOLO(model_path)
    cap = cv2.VideoCapture(image_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    while True:
        success, img = cap.read()
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            print(len(boxes))
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                # conf=math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                # label=f'{class_name}{conf}'
                label = f'{class_name}'
                t_size = cv2.getTextSize(label, 0, fontScale=0.1, thickness=1)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                color = (255, 255, 255)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1,y1-2),0, 1, color, thickness=1, lineType=cv2.LINE_AA)

        #     print(int(boxes.cls[0].item()))
        #     i = len(boxes)
        #     while i > 0:
        #         if (int(boxes.cls[0].item())) == 2 or (int(boxes.cls[1].item())) == 2 or (int(boxes.cls[2].item())) == 2:
        #             c += 1
        #             i -= 1
        #         elif (int(boxes.cls[0].item())) == 1 or (int(boxes.cls[1].item())) == 1 or (int(boxes.cls[2].item())) == 1:
        #             b += 1
        #             i -= 1
        #         elif (int(boxes.cls[0].item())) == 0 or (int(boxes.cls[1].item())) == 0 or (int(boxes.cls[2].item())) == 0:
        #             a += 1
        #             i -= 1
        #     print("Количество кликунов -", a)
        #     print("Количество малых -", b)
        #     print("Количество шипунов -", c)
        # cv2.imshow("Image", img)
        # cv2.imwrite(r"D:\Users\d.petrov\Downloads\Приложение\YOLOv8 App\Webapp\output.jpg", img)
        # if cv2.waitKey(0) & 0xFF == ord('1'):
        #     break

        return (len(boxes), boxes.cls)

if __name__ == '__main__':
    model_path = "best.pt"
    image_path = r"C:\Users\sinni\OneDrive\Изображения\Saved Pictures\4026cf5ed681283828a6fe37303b6cdf.jpg"
    print(activate_yolo(model_path, image_path))