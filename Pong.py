import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

#you can change your webcam frame  for bigger screen but if your webcam support
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# importing all the images
imgBackground = cv2.imread("Resources/imgBg.png")
imgGameOver = cv2.imread("Resources/game_Over.png")
imgbat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgbat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)
imgball = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)

imgbat1 = cv2.resize(imgbat1, (10, 120))
imgbat2 = cv2.resize(imgbat2, (10, 120))
imgball = cv2.resize(imgball, (30, 30))

detector = HandDetector(detectionCon=0.8, maxHands=2)

ballPos = [100, 100]
gameOver = False
speedX = 7
speedY = 7
score = [0, 0]

while True:
    _, img = cap.read()

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # control bats with hand
    if hands:
        for hand in hands:
            x, y, w, h = hand["bbox"]  # x,y coordinate of bats position and w,h= width and height of bats
            h1, w1, _ = imgbat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 6, 270)  # bat min and max distance from above and below screen

            if hand["type"] == "Left":
                img = cvzone.overlayPNG(img, imgbat1, pos=[15, y1])
                # To check whether the bat hits  to left bat or not
                if 15 < ballPos[0] < 15 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 20
                    score[0] += 1

            if hand["type"] == "Right":
                img = cvzone.overlayPNG(img, imgbat2, pos=[615, y1])
                # To check whether the bat hits right bat  or not
                if 580 < ballPos[0] < 595 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[1] -= 20
                    score[1] += 1

    # Game over
    if ballPos[0] < 10 or ballPos[0] > 600:
        gameOver = True
    if gameOver:
        img = imgGameOver
        cv2.putText(img, str(score[0] + score[1]).zfill(2), (263, 290), cv2.FONT_HERSHEY_COMPLEX, 3, (251, 220, 200), 5)


    else:
        # move ball
        if ballPos[1] >= 365 or ballPos[1] <= 10:
            speedY = -speedY
        ballPos[0] += speedX
        ballPos[1] += speedY

        # draw ball
        img = cvzone.overlayPNG(img, imgball, pos=ballPos)
        cv2.putText(img, str(score[0]), (160, 460), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 5)
        cv2.putText(img, str(score[1]), (420, 460), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 5)

    cv2.imshow("My Ping Pong Game", img)
    key = cv2.waitKey(1)
    if key == ord("r"):
        ballPos = [100, 100]
        speedX = 10
        speedY = 10
        gameOver = False
        imgGameOver = cv2.imread("Resources/Game_Over.png")
        score = [0, 0]
