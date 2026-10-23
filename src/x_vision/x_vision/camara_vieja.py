# Primera version para abrir la camara. Ya no se usa, el driver
# de la camara publica directo en /x/camera/image_raw.
import cv2


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        cv2.imshow('camara', frame)
        if cv2.waitKey(1) == 27:
            break
