import mediapipe as mp
import cv2
from pynput import keyboard
import constants
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

current_color = constants.BLUE
current_mode = constants.FREE_DRAW_MODE
prev_mode = None

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


cap = cv2.VideoCapture(0)
points = []

def on_press(key):
    global current_mode
    global current_color
    global points
    global prev_mode

    if current_mode == constants.MODE_SWITCHER:
        if key == keyboard.KeyCode.from_char('f'):
            current_mode = constants.FREE_DRAW_MODE
        if key == keyboard.KeyCode.from_char('s'):
            current_mode = constants.SHAPE_MODE
        if key == keyboard.KeyCode.from_char('v'):
            current_mode = constants.VIEW_MODE

    if key == keyboard.Key.space:
        current_mode = constants.MODE_SWITCHER

    if current_mode == constants.FREE_DRAW_MODE or current_mode == constants.SHAPE_MODE:
        if key == keyboard.KeyCode.from_char('c'):
            prev_mode = current_mode
            current_mode = constants.COLOR_MODE

    if current_mode == constants.COLOR_MODE:
        if key == keyboard.KeyCode.from_char('r'):
            print ('Color changed to RED')
            current_color = constants.RED
            if prev_mode:
                current_mode = prev_mode
                prev_mode = None
        if key == keyboard.KeyCode.from_char('b'):
            print ('Color changed to BLUE')
            current_color = constants.BLUE
            if prev_mode:
                current_mode = prev_mode
                prev_mode = None
        if key == keyboard.KeyCode.from_char('g'):
            print ('Color changed to GREEN')
            current_color = constants.GREEN
            if prev_mode:
                current_mode = prev_mode
                prev_mode = None
        if key == keyboard.KeyCode.from_char('y'):
            print ('Color changed to YELLOW')
            current_color = constants.YELLOW
            if prev_mode:
                current_mode = prev_mode
                prev_mode = None
        if key == keyboard.KeyCode.from_char('p'):
            print ('Color changed to PURPLE')
            current_color = constants.PURPLE
            if prev_mode:
                current_mode = prev_mode
                prev_mode = None
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

            if current_mode == constants.FREE_DRAW_MODE and i == 0:
                points.append((x, y))

    for coord in points:
        cv2.circle(image, coord, 1, current_color, 12)

    if current_mode == constants.FREE_DRAW_MODE:
        cv2.putText(image, 'Free Draw Mode', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, current_color, 4, cv2.LINE_AA)

    if current_mode == constants.SHAPE_MODE:
        cv2.putText(image, 'Shape Mode', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, current_color, 4, cv2.LINE_AA)

    if current_mode == constants.COLOR_MODE:
        cv2.putText(image, 'Color Mode', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, current_color, 4, cv2.LINE_AA)
        cv2.putText(image, 'Press r for red', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.RED, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press b for blue', (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.BLUE, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press g for green', (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.GREEN, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press y for yellow', (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.YELLOW, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press p for purple', (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.PURPLE, 2, cv2.LINE_AA)

    if current_mode == constants.FREE_DRAW_MODE or current_mode == constants.SHAPE_MODE:
        cv2.putText(image, 'Press C to change color', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, current_color, 2, cv2.LINE_AA)

    if current_mode == constants.MODE_SWITCHER:
        cv2.putText(image, 'Mode Switcher', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, current_color, 4, cv2.LINE_AA)
        cv2.putText(image, 'Press F for free draw', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, current_color, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press S for shape drawing', (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, current_color, 2, cv2.LINE_AA)
        cv2.putText(image, "Press V for view only", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, current_color, 2, cv2.LINE_AA)

    cv2.putText(image, 'Press Space to Switch Mode', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.GREEN, 2, cv2.LINE_AA)

    image = cv2.resize(image, (width, height))
    cv2.imshow("Camera", image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()