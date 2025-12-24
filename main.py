import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)

# Pycaw audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# For visual volume bar
vol_bar = 400
vol_perc = 0

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                x1, y1 = lm_list[4][1], lm_list[4][2]  # Thumb tip
                x2, y2 = lm_list[8][1], lm_list[8][2]  # Index tip
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                # Draw interaction visuals
                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

                # Calculate distance
                length = math.hypot(x2 - x1, y2 - y1)

                # Convert to volume
                vol = min_vol + (length / 200) * (max_vol - min_vol)
                vol = max(min(vol, max_vol), min_vol)
                volume.SetMasterVolumeLevel(vol, None)

                # Volume % for UI
                vol_perc = int((vol - min_vol) / (max_vol - min_vol) * 100)
                vol_bar = 400 - int((vol_perc / 100) * 300)

    # Draw volume bar background
    cv2.rectangle(img, (50, 100), (85, 400), (255, 255, 255), 2)
    cv2.rectangle(img, (50, vol_bar), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{vol_perc} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Hand Gesture Volume Controller", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
