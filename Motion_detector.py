import cv2
import pandas as pd
from datetime import datetime as dt


video = cv2.VideoCapture(0)
first_frame = None
status_list = [None, None]
df = pd.DataFrame(columns =["start","end"])
time_list = []

while True:
    check , frame = video.read()
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray , (21,21),0)
    status = 0

    if first_frame == None:
        first_frame = gray

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame= cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame,None, iterations = 3)


    (_,cnt,_) = cv2.findContours(thresh_frame.copy() ,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )
    for contour in cnt:
        if cv2.contourArea(contour)<1000:
            continue
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),1)
        status = 1

    status_list = status_list[-2:]
    status_list.append(status)

    if status_list[-1]==1 and status_list[-2]==0:
        time_list.append(dt.now()) # time the object enters the border
    if status_list[-1]==0 and status_list[-2]==1:
        time_list.append(dt.now()) # time the object exits the border

    cv2.imshow("frame",frame)
    cv2.imshow("delta",delta_frame)
    if cv2.waitKey(1) == ord("q"):
        if status ==1:
            time_list.append(dt.now())
        break


for i in range(0 , len(time_list),2):
    df = df.append({"start":time_list[i],"end":time_list[i+1]}, ignore_index = True)

print(df)
video.release()
cv2.destroyAllWindows()
