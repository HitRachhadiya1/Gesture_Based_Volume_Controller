"""
Hand Tracking Module
====================
A reusable module that wraps MediaPipe Hands for real-time hand landmark
detection. Provides a clean API used by the main gesture controller.

Key classes
-----------
HandDetector  –  Detects hands and returns landmark positions.
"""

import cv2
import mediapipe as mp


class HandDetector:
    """Detect hands and extract landmark positions using MediaPipe Hands.

    Parameters
    ----------
    mode : bool
        If True, treats every frame as a static image (slower but more
        accurate).  Default is False (video / tracking mode).
    max_hands : int
        Maximum number of hands to detect.  Default is 2.
    detection_confidence : float
        Minimum confidence ([0.0, 1.0]) for the detection model.
    tracking_confidence : float
        Minimum confidence ([0.0, 1.0]) for the tracking model.
    """

    def __init__(
        self,
        mode: bool = False,
        max_hands: int = 2,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7,
    ):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        # MediaPipe utilities
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

        self.results = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def find_hands(self, img, draw: bool = True):
        """Detect hands in *img* and optionally draw landmarks.

        Parameters
        ----------
        img : numpy.ndarray
            BGR image from OpenCV.
        draw : bool
            If True, draw landmarks and connections on the image.

        Returns
        -------
        img : numpy.ndarray
            The (possibly annotated) image.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(
                        color=(0, 255, 0), thickness=2, circle_radius=4
                    ),
                    self.mp_draw.DrawingSpec(
                        color=(0, 200, 0), thickness=2
                    ),
                )
        return img

    def find_position(self, img, hand_no: int = 0, draw: bool = True):
        """Return a list of landmark positions for a specific hand.

        Parameters
        ----------
        img : numpy.ndarray
            BGR image (used only to get dimensions).
        hand_no : int
            Index of the hand whose landmarks are returned.
        draw : bool
            If True, draw small circles on the Thumb tip (4) and
            Index tip (8).

        Returns
        -------
        lm_list : list[list[int]]
            Each element is ``[landmark_id, x_pixel, y_pixel]``.
        """
        lm_list = []

        if (
            self.results
            and self.results.multi_hand_landmarks
            and hand_no < len(self.results.multi_hand_landmarks)
        ):
            target_hand = self.results.multi_hand_landmarks[hand_no]
            h, w, _ = img.shape

            for lm_id, lm in enumerate(target_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([lm_id, cx, cy])

                # Highlight the Thumb tip and Index tip
                if draw and lm_id in (4, 8):
                    cv2.circle(img, (cx, cy), 12, (128, 0, 255), cv2.FILLED)

        return lm_list
