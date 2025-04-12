import mediapipe as mp
import cv2
import constants
import time
import key_handler
from state import state

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 120)

key_handler.enable_keyboard()

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

            if state["current_mode"] == constants.FREE_DRAW_MODE and i == 0:
                state["points"].append([(x, y), state["current_color"] ])

    for coord in state["points"]:
        cv2.circle(image, coord[0], 1, coord[1], 24)

    if state["current_mode"] == constants.FREE_DRAW_MODE:
        cv2.putText(image, 'Free Draw Mode', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, state["current_color"], 4, cv2.LINE_AA)

    if state["current_mode"] == constants.SHAPE_MODE:
        cv2.putText(image, 'Shape Mode', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, state["current_color"], 4, cv2.LINE_AA)

    if state["current_mode"] == constants.COLOR_MODE:
        cv2.putText(image, 'Color Mode', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, state["current_color"], 4, cv2.LINE_AA)
        cv2.putText(image, 'Press r for red', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.RED, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press b for blue', (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.BLUE, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press g for green', (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.GREEN, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press y for yellow', (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.YELLOW, 2, cv2.LINE_AA)
        cv2.putText(image, 'Press p for purple', (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.PURPLE, 2, cv2.LINE_AA)

    if state["current_mode"] == constants.FREE_DRAW_MODE or state["current_mode"] == constants.SHAPE_MODE:
        cv2.putText(image, 'Press C to change color', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, state["current_color"], 2, cv2.LINE_AA)

    if state["current_mode"] == constants.MODE_SWITCHER:
        cv2.putText(image, 'Mode Switcher', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, state["current_color"], 4, cv2.LINE_AA)
        cv2.putText(image, 'Press F for free draw', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, state["current_color"], 2, cv2.LINE_AA)
        cv2.putText(image, 'Press S for shape drawing', (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, state["current_color"], 2, cv2.LINE_AA)
        cv2.putText(image, "Press V for view only", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, state["current_color"], 2, cv2.LINE_AA)

    cv2.putText(image, 'Press Space to Switch Mode', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, constants.GREEN, 2, cv2.LINE_AA)

    image = cv2.resize(image, (width, height))
    cv2.imshow("Camera", image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()