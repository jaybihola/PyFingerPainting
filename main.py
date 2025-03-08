import mediapipe as mp
import cv2
from pynput import keyboard
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
PURPLE = (255, 0, 255)

current_color = BLUE


hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


cap = cv2.VideoCapture(0)
draw_mode = True
points = []

def on_press(key):
    global draw_mode
    global current_color
    global points
    if key == keyboard.Key.space:
        draw_mode = not draw_mode
    if key == keyboard.KeyCode.from_char('r'):
        print ('Color changed to RED')
        current_color = RED
    if key == keyboard.KeyCode.from_char('b'):
        print ('Color changed to BLUE')
        current_color = BLUE
    if key == keyboard.KeyCode.from_char('g'):
        print ('Color changed to GREEN')
        current_color = GREEN
    if key == keyboard.KeyCode.from_char('y'):
        print ('Color changed to YELLOW')
        current_color = YELLOW
    if key == keyboard.KeyCode.from_char('p'):
        print ('Color changed to PURPLE')
        current_color = PURPLE
    if key == keyboard.Key.esc:
        print ("Clearing")
        points.clear()


def on_release(key):
    pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    height, width = image.shape[:2]
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for i in range(len(results.multi_hand_landmarks)):
            main_hand = results.multi_hand_landmarks[i]
            index_finger = main_hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            x = int(round(index_finger.x * width))
            y = int(round(index_finger.y * height))

            mp_drawing.draw_landmarks(image, main_hand, mp_hands.HAND_CONNECTIONS)

            if draw_mode and i == 0:
                points.append((x, y))

    for coord in points:
        cv2.circle(image, coord, 1, current_color, 12)

    if draw_mode:
        cv2.putText(image, 'Draw Mode', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, current_color, 4, cv2.LINE_AA)

    image = cv2.resize(image, (width, height))
    cv2.imshow("Camera", image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()