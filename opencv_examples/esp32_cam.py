import cv2

vcap = cv2.VideoCapture("rtsp://192.168.1.84:8554/mjpeg/1")
print("read stream")
while(1):
    has_frame, frame = vcap.read()
    print(has_frame)
    if has_frame:
        cv2.imshow('VIDEO', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vcap.release()
cv2.destroyAllWindows()
