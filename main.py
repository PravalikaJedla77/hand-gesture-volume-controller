import cv2
import mediapipe as mp
import math
import time
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# -------------------- Open YouTube for Demo --------------------
webbrowser.open("https://www.youtube.com/watch?v=5qap5aO4i9A")
time.sleep(5)  # Allow video to load before starting gesture control

# -------------------- MediaPipe Hand Setup --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# -------------------- Webcam Setup --------------------
cap = cv2.VideoCapture(0)

# -------------------- Pycaw Audio Setup --------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))

vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# -------------------- Volume UI Variables --------------------
vol_bar = 400
vol_perc = 0

# -------------------- Main Loop --------------------
while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                img, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            lm_list = []
            h, w, _ = img.shape

            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                # Thumb tip (4) and Index finger tip (8)
                x1, y1 = lm_list[4][1], lm_list[4][2]
                x2, y2 = lm_list[8][1], lm_list[8][2]

                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                # Draw visuals
                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

                # Distance between fingers
                length = math.hypot(x2 - x1, y2 - y1)

                # Map distance to volume range
                vol = min_vol + (length / 200) * (max_vol - min_vol)
                vol = max(min(vol, max_vol), min_vol)
                volume.SetMasterVolumeLevel(vol, None)

                # Volume percentage
                vol_perc = int((vol - min_vol) / (max_vol - min_vol) * 100)
                vol_bar = 400 - int((vol_perc / 100) * 300)

    # -------------------- Volume Bar UI --------------------
    cv2.rectangle(img, (50, 100), (85, 400), (255, 255, 255), 2)
    cv2.rectangle(img, (50, vol_bar), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(
        img, f'{vol_perc} %', (40, 450),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )

    cv2.imshow("Hand Gesture Volume Controller", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------- Cleanup --------------------
cap.release()
cv2.destroyAllWindows()

