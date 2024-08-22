import cv2

# change your IP
cap = cv2.VideoCapture('http://192.168.2.115:8080/video')


while(cap.isOpened()):

    ret, frame = cap.read()

    try:
        cv2.imshow('temp', cv2.resize(frame, (600,400)))

        key = cv2.waitKey(1)
        if key == ord('q') or cv2.getWindowProperty('temp', cv2.WND_PROP_VISIBLE) < 1:
            break
    except cv2.error:
        print("Stream ended...")
        break

cap.release()
cv2.destroyAllWindows()