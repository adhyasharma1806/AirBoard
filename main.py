import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import numpy as np
import time
import winsound
import random

# -----------------------------
# Camera setup
# -----------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.9, maxHands=1)
keyboard_controller = Controller()

# -----------------------------
# Keyboard layout
# -----------------------------
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
]

final_text = ""

# -----------------------------
# Button class
# -----------------------------
class Button:
    def __init__(self, pos, text, size=None):
        if size is None:
            size = [90, 90]
        self.pos = pos
        self.size = size
        self.text = text
        self.is_pressed = False
        self.press_color = (255, 0, 255)
        self.last_pressed = 0  # for cooldown

# -----------------------------
# Draw all buttons
# -----------------------------
def draw_all(frame, buttons):
    overlay = frame.copy()
    for btn in buttons:
        x, y = btn.pos
        w, h = btn.size
        color = btn.press_color if btn.is_pressed else (180, 0, 255)
        alpha = 0.3

        cv2.rectangle(overlay, btn.pos, (x + w, y + h), color, cv2.FILLED)
        cv2.rectangle(overlay, (x - 2, y - 2), (x + w + 2, y + h + 2), (255, 255, 255), 2)
        cv2.putText(overlay, btn.text, (x + 20, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    frame = cv2.addWeighted(overlay, alpha + 0.7, frame, 1 - (alpha + 0.7), 0)
    return frame

# -----------------------------
# Keyboard positioning
# -----------------------------
x_spacing = 120
y_spacing = 140
key_size = [90, 90]

button_list = []
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        x = x_spacing * j + 50
        y = y_spacing * i + 200
        button_list.append(Button([x, y], key, key_size))

# -----------------------------
# Spacebar: middle-bottom, wide
# -----------------------------
space_x = 200
space_y = y_spacing * 3 + 180  # ↓ lowered slightly from +140 to +180
space_width = 600
space_height = 100
button_list.append(Button([space_x, space_y], "Space", [space_width, space_height]))

# -----------------------------
# Backspace: move it near the spacebar
# -----------------------------
backspace_x = space_x + space_width + 50  # Position it to the right of the spacebar
backspace_y = space_y  # Align it with the spacebar's vertical position
backspace_width = 150
backspace_height = 90
button_list.append(Button([backspace_x, backspace_y],
                          "Backspace", [backspace_width, backspace_height]))

# -----------------------------
# Index finger smoothing
# -----------------------------
index_history = []
max_len = 5

# Track pinch state to prevent double typing
was_pinching = False

# -----------------------------
# Main loop
# -----------------------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, draw=True)
    frame = draw_all(frame, button_list)

    for btn in button_list:
        btn.is_pressed = False

    current_time = time.time()

    if hands:
        hand = hands[0]
        lm_list = hand["lmList"]

        if lm_list:
            index_tip = np.array(lm_list[8][:2])
            thumb_tip = np.array(lm_list[4][:2])

            # Smooth index finger
            index_history.append(index_tip)
            if len(index_history) > max_len:
                index_history.pop(0)
            smoothed_index = np.mean(index_history, axis=0)

            # Hover + pinch detection for typing
            for btn in button_list:
                x, y = btn.pos
                w, h = btn.size
                padding = 10

                if x + padding < smoothed_index[0] < x + w - padding and \
                   y + padding < smoothed_index[1] < y + h - padding:
                    # Hover effect
                    cv2.rectangle(frame, (x - 3, y - 3),
                                  (x + w + 3, y + h + 3), (0, 255, 255), 2)

                    # Pinch detection
                    hand_width = np.linalg.norm(
                        np.array(lm_list[0][:2]) - np.array(lm_list[5][:2])
                    )
                    pinch_dist = np.linalg.norm(smoothed_index - thumb_tip)
                    pinching = pinch_dist < hand_width * 0.3

                    if pinching and not was_pinching:
                        if current_time - btn.last_pressed > 0.3:
                            btn.is_pressed = True
                            btn.press_color = (
                                random.randint(100, 255),
                                random.randint(0, 150),
                                random.randint(150, 255),
                            )
                            btn.last_pressed = current_time
                            winsound.Beep(1200, 70)

                            if btn.text == "Space":
                                final_text += " "
                                keyboard_controller.type(" ")
                            elif btn.text == "Backspace":
                                final_text = final_text[:-1]
                                keyboard_controller.press(Key.backspace)
                                keyboard_controller.release(Key.backspace)
                            else:
                                final_text += btn.text
                                keyboard_controller.type(btn.text)

                    was_pinching = pinching
    else:
        was_pinching = False  # Reset if no hand detected

    # -----------------------------
    # Display typed text
    # -----------------------------
    cv2.rectangle(frame, (50, 70), (1200, 150), (50, 0, 80), cv2.FILLED)
    cv2.putText(frame, final_text[-40:], (60, 130),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("🪩 Air Pointer Keyboard 🪩", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
