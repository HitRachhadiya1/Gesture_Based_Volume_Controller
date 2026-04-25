"""
AI-Based Touchless Volume Controller
=====================================
Main application — captures webcam frames, detects the hand, measures the
pinch distance between Thumb tip (Landmark 4) and Index tip (Landmark 8),
and maps it to the Windows system volume via PyCaw.

Controls
--------
- Pinch your thumb and index finger together  →  volume decreases.
- Spread them apart                           →  volume increases.
- Press **q** to quit.

Usage
-----
    python gesture_volume_controller.py
"""

import math
import time

import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from hand_tracking_module import HandDetector


# ── Colour palette ──────────────────────────────────────────────────────
COLOUR_GREEN   = (0, 255, 0)
COLOUR_LIME    = (0, 230, 118)
COLOUR_RED     = (0, 0, 255)
COLOUR_PURPLE  = (200, 0, 128)
COLOUR_WHITE   = (255, 255, 255)
COLOUR_DARK    = (40, 40, 40)
COLOUR_ORANGE  = (0, 165, 255)


def get_volume_interface():
    """Return the PyCaw IAudioEndpointVolume COM interface."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def draw_volume_bar(img, vol_pct, vol_bar_height, bar_colour):
    """Draw a vertical volume bar on the left side of the frame."""
    # Bar background
    cv2.rectangle(img, (30, 100), (65, 400), COLOUR_DARK, cv2.FILLED)
    cv2.rectangle(img, (30, 100), (65, 400), COLOUR_WHITE, 2)

    # Filled portion (bottom-up)
    cv2.rectangle(
        img,
        (30, int(vol_bar_height)),
        (65, 400),
        bar_colour,
        cv2.FILLED,
    )

    # Percentage label
    cv2.putText(
        img,
        f"{int(vol_pct)}%",
        (22, 430),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        COLOUR_WHITE,
        2,
    )


def draw_fps(img, fps):
    """Show FPS in the top-right corner."""
    cv2.putText(
        img,
        f"FPS: {int(fps)}",
        (img.shape[1] - 150, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        COLOUR_LIME,
        2,
    )


def main():
    # ── Camera setup ────────────────────────────────────────────────────
    cam_width, cam_height = 960, 540
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

    if not cap.isOpened():
        print("[ERROR] Cannot access the webcam. Please check your camera.")
        return

    # ── Hand detector ───────────────────────────────────────────────────
    detector = HandDetector(
        detection_confidence=0.7,
        tracking_confidence=0.7,
        max_hands=1,
    )

    # ── Volume interface (PyCaw / Windows) ──────────────────────────────
    volume = get_volume_interface()
    vol_range = volume.GetVolumeRange()        # typically (-65.25, 0.0, ...)
    min_vol = vol_range[0]
    max_vol = vol_range[1]

    # ── State variables ─────────────────────────────────────────────────
    prev_time = time.time()
    vol_pct = 0
    vol_bar_height = 400                       # visual bar (px), 400 = 0 %

    print("="*55)
    print("  AI-Based Touchless Volume Controller")
    print("  => Pinch thumb & index to control volume")
    print("  => Press 'q' to quit")
    print("="*55)

    # ── Main loop ───────────────────────────────────────────────────────
    while True:
        success, img = cap.read()
        if not success:
            print("[WARNING] Frame capture failed. Retrying...")
            continue

        # Flip horizontally for a mirror-like experience
        img = cv2.flip(img, 1)

        # 1. Detect hand landmarks
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=True)

        if lm_list:
            # 2. Get thumb tip (4) and index tip (8) coordinates
            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2   # midpoint

            # 3. Draw connecting line and centre dot
            cv2.line(img, (x1, y1), (x2, y2), COLOUR_LIME, 3)
            cv2.circle(img, (cx, cy), 8, COLOUR_PURPLE, cv2.FILLED)

            # 4. Calculate Euclidean distance between the two tips
            length = math.hypot(x2 - x1, y2 - y1)

            # 5. Map distance → volume
            #    Typical range: ~20 px (pinched) to ~200 px (spread)
            vol = np.interp(length, [20, 200], [min_vol, max_vol])
            vol_pct = np.interp(length, [20, 200], [0, 100])
            vol_bar_height = np.interp(length, [20, 200], [400, 100])

            # 6. Set system volume
            volume.SetMasterVolumeLevel(vol, None)

            # 7. Visual feedback — colour changes near minimum distance
            bar_colour = COLOUR_LIME
            if length < 30:
                cv2.circle(img, (cx, cy), 12, COLOUR_RED, cv2.FILLED)
                bar_colour = COLOUR_RED
            elif length < 80:
                bar_colour = COLOUR_ORANGE

        else:
            # No hand detected — keep last volume; dim the bar colour
            bar_colour = COLOUR_DARK

        # ── HUD elements ────────────────────────────────────────────────
        draw_volume_bar(img, vol_pct, vol_bar_height, bar_colour)

        # FPS calculation
        current_time = time.time()
        fps = 1 / (current_time - prev_time + 1e-9)
        prev_time = current_time
        draw_fps(img, fps)

        # Title overlay
        cv2.putText(
            img,
            "Gesture Volume Control",
            (img.shape[1] // 2 - 170, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            COLOUR_WHITE,
            2,
        )

        # ── Display ────────────────────────────────────────────────────
        cv2.imshow("AI Gesture Volume Controller", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ── Cleanup ─────────────────────────────────────────────────────────
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Application closed.")


if __name__ == "__main__":
    main()
