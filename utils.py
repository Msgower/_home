import cv2
import numpy as np

def warp_overlay(base, overlay, dst_points, opacity=1.0):
    """
    Warp a PNG overlay (vinyl artwork) onto a base image using 4 clicked points.
    
    Parameters:
    - base      : RGB image (numpy array)
    - overlay   : RGBA image (numpy array)
    - dst_points: list of 4 points [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
                  in order: top-left, top-right, bottom-right, bottom-left
    - opacity   : float (0.1 - 1.0), scales transparency of the overlay
    """

    h, w = overlay.shape[:2]

    # Source points from artwork corners
    src = np.array([
        [0, 0],
        [w, 0],
        [w, h],
        [0, h]
    ], dtype=np.float32)

    # Destination points (clicked on base image)
    dst = np.array(dst_points, dtype=np.float32)

    # Compute perspective transform
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(overlay, M, (base.shape[1], base.shape[0]))

    # Alpha blending with slider opacity
    alpha = (warped[:, :, 3] / 255.0) * opacity

    result = base.copy()

    for c in range(3):  # RGB channels
        result[:, :, c] = alpha * warped[:, :, c] + (1 - alpha) * result[:, :, c]

    return result.astype(np.uint8)
