import cv2
import mediapipe as mp
import time

vid = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = vid.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(idx, cx, cy)
                if idx == 0:
                    cv2.circle(img, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
            
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), 
        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
