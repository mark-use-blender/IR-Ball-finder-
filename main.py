import cv2
import numpy as np
import math as m

def daytime():
    #gpio=HIGH
    return
def nightime():
    #gpio=LOW
    return
def go_up():
    #goup
    return
def go_down():
    #godown
    return
def go_left():
    #goleft
    return
def go_right():
    #goright
    return
def no_track():
    #notrack
    return



def find_cir(con):
    balllist = []
    if (len(con)>0):
        for contour in con:
            (loc, (width, height), angle) = cv2.minAreaRect(contour)
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            area = cv2.contourArea(contour)
            if ((len(approx) > 8) & (area > 30) & 0.8<np.abs(width/height)<1.2):
                balllist.append(contour,area,loc)
    return balllist

def core(cam):
    daytime()
    ret,dayimg= cam.read()
    nightime()
    ret,nighting=cam.read()
    grayday = cv2.cvtColor(dayimg,cv2.COLOR_BGR2GRAY)
    graynight = cv2.cvtColor(nighting,cv2.COLOR_BGR2GRAY)
    adapt_type = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    thresh_type = cv2.THRESH_BINARY_INV
    diff = cv2.bitwise_xor(grayday,graynight)
    blur = cv2.medianBlur(diff, 1)
    contress = cv2.adaptiveThreshold(blur, 255, adapt_type, thresh_type, 21, 7)
    con = cv2.findContours(contress)
    lcon = []
    lar = 0
    lpos = [0,0]
    h,w = diff.shape
    balllist = find_cir(con)
    tracking = (len(balllist)>0)
    if (tracking):
        balllist=balllist[balllist[:, 1].argsort()]
        lcon,lar,lpos=balllist[0]

        apos = lpos[0]-(h/2),lpos[1]-(w/2)
        if (abs(apos[0])>20):
            if (apos[0]<0):
                go_down()
            else:
                go_up()
        if (abs(apos[1])>20):
            if (apos[1]<0):
                go_left()
            else:
                go_right()
    else:
        no_track()
cam = cv2.VideoCapture(2)
while (True):
    core(cam)

    

