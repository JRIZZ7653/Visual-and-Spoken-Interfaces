import cv2
import mediapipe as mp
from time import sleep

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


x1 = y1 = x2 = y2 = 0

cap.set(3, 1280)
cap.set(4, 720)

finalText = ""

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
		["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
		["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"]]

def drawALL(img, buttonList):
	for button in buttonList:
		x, y = button.pos
		w, h = button.size

		cv2.rectangle(img, button.pos, (x + w, y + h), (128, 128, 128), cv2.FILLED)
		cv2.putText(img, button.text, (x + 20, y + 65), 
			cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
	return img

class Button():
	def __init__(self,pos,text,size=[85,85]):
		self.pos = pos
		self.size = size
		self.text = text
		
buttonList = []
for i in range(len(keys)):
		for j, key in enumerate(keys [i]):
			buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:

	success, img=cap.read()
	img = cv2.flip(img, 1)
	imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)

	img = drawALL(img, buttonList)

	#cv2.rectangle(img, (100, 600), (800, 500), (128, 128, 128), cv2.FILLED)

	if results.multi_hand_landmarks:
		for handLms in results.multi_hand_landmarks:  
			for id,lm in enumerate(handLms.landmark):

				for button in buttonList:
					xa, ya = button.pos
					wa, ha = button.size

					h, w, c = img.shape
					cx,cy = int(lm.x*w),int(lm.y*h)

					if id == 4: # for id 12, x1 and y1 are equal to its co ordinates
						x1 = cx
						y1 = cy

					dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4 # work out the distance between point 8 and 12
					cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)  # draw a line at those points
					#print(dist)

					if id == 8:

						x2 = cx  # for id 8, x2 and y2 are equal to its co ordinates
						y2 = cy

						if xa < cx < xa + wa and ya < cy < ya + ha:	  # if point 8 is in the same place as the text box, then highlight it
							cv2.rectangle(img, button.pos, (xa + wa, ya + ha), (0, 0, 0), cv2.FILLED)
							cv2.putText(img, button.text, (xa + 20, ya + 65), 
								cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

							if dist < 6:
								cv2.rectangle(img, button.pos, (xa + wa, ya + ha), (255, 255, 255), cv2.FILLED)
								cv2.putText(img, button.text, (xa + 20, ya + 65), 
										cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
								finalText += button.text
								#print(button.text)
								sleep(0.15)

			mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

	cv2.rectangle(img, (50, 350), (700, 450), (128, 128, 128), cv2.FILLED)
	cv2.putText(img, finalText, (68, 425), 
			cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
	
	cv2.imshow("img",img)
	cv2.waitKey(1)