# import cv2
# import numpy as np
# import os


# def detect_white_spot(input_img, output_path):
#     """
#     Detect white spot based on hull area and bounding box logic

#     Returns:
#         status (str): 'WHITE SPOT FOUND' or 'OK'
#     """

#     os.makedirs(output_path, exist_ok=True)

#     img = cv2.imread(input_img)
#     if img is None:
#         raise FileNotFoundError("Input image not found")

#     result_img = img.copy()

#     # -------------------- HSV MASK --------------------
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     lower = np.array([0, 185, 35])
#     upper = np.array([179, 255, 255])
#     mask = cv2.inRange(hsv, lower, upper)
#     filtered = cv2.bitwise_and(img, img, mask=mask)

#     # -------------------- EDGE + MORPH --------------------
#     gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     edges = cv2.Canny(blur, 120, 40)

#     kernel = np.ones((7, 7), np.uint8)
#     morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

#     # -------------------- FIND CONTOURS --------------------
#     contours, _ = cv2.findContours(
#         morph, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
#     )

#     bbox_found = False

#     for cnt in contours:
#         area = cv2.contourArea(cnt)

#         # Base contour area filter
#         if 150 < area < 300:

#             hull = cv2.convexHull(cnt)
#             hull_area = cv2.contourArea(hull)

#             # Hull area condition
#             if 200 <= hull_area <= 300:
#                 bbox_found = True

#                 # Draw contour & hull
#                 cv2.drawContours(result_img, [cnt], -1, (0, 255, 0), 2)
#                 cv2.drawContours(result_img, [hull], -1, (255, 0, 0), 1)

#                 # Bounding box
#                 x, y, w, h = cv2.boundingRect(cnt)
#                 cv2.rectangle(
#                     result_img, (x, y), (x + w, y + h),
#                     (0, 0, 255), 2
#                 )

#                 cv2.putText(
#                     result_img,
#                     f"HullA:{int(hull_area)}",
#                     (x, y - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.4,
#                     (255, 0, 0),
#                     1
#                 )

#     # -------------------- FINAL STATUS --------------------
#     if bbox_found:
#         status = "WHITE SPOT FOUND"
#         color = (0, 0, 255)
#     else:
#         status = "OK"
#         color = (0, 255, 0)

#     cv2.putText(
#         result_img,
#         status,
#         (30, 40),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         1.0,
#         color,
#         2
#     )

#     # -------------------- SAVE OUTPUTS --------------------
#     cv2.imwrite(os.path.join(output_path, "01_original.jpg"), img)
#     cv2.imwrite(os.path.join(output_path, "02_mask.jpg"), mask)
#     cv2.imwrite(os.path.join(output_path, "03_filtered.jpg"), filtered)
#     cv2.imwrite(os.path.join(output_path, "04_gray.jpg"), gray)
#     cv2.imwrite(os.path.join(output_path, "05_edges.jpg"), edges)
#     cv2.imwrite(os.path.join(output_path, "06_morph.jpg"), morph)
#     cv2.imwrite(os.path.join(output_path, "07_result.jpg"), result_img)

#     return status


# status = detect_white_spot(
#     input_img=r"D:\POC\marelli_poc\27_12_25\whitespot\1.bmp",
#     output_path=r"D:\poc\marelli_poc\27_12_25\whitespot\output"
# )

# print("Inspection Result:", status)


import cv2
import numpy as np
import os

# -------------------- THRESHOLDS & CONSTANTS --------------------
MIN_CONTOUR_AREA = 150
MAX_CONTOUR_AREA = 300

MIN_HULL_AREA = 200
MAX_HULL_AREA = 300

HSV_LOWER = np.array([0, 185, 35])
HSV_UPPER = np.array([179, 255, 255])


def analyze_white_spot(image_path, detected_dir=None):
    """
    White spot detection with UI-ready structure.

    - HSV based masking
    - Edge + morphology processing
    - Contour & convex hull filtering
    - Status decision (OK / WHITE SPOT FOUND)

    Returns:
        annotated_img, results_dict
    """

    # -------------------- 1. LOAD IMAGE --------------------
    img = image_path
    if img is None:
        raise FileNotFoundError(f"Could not read: {image_path}")

    vis_img = img.copy()
    results = {"white_spot_found": False, "count": 0}

    # -------------------- 2. HSV MASK --------------------
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)
    filtered = cv2.bitwise_and(img, img, mask=mask)

    # -------------------- 3. EDGE + MORPH --------------------
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 120, 40)

    kernel = np.ones((7, 7), np.uint8)
    morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # -------------------- 4. FIND & FILTER CONTOURS --------------------
    contours, _ = cv2.findContours(morph, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    idx = 1
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if MIN_CONTOUR_AREA < area < MAX_CONTOUR_AREA:
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)

            if MIN_HULL_AREA <= hull_area <= MAX_HULL_AREA:
                results["white_spot_found"] = True
                results["count"] += 1

                # Draw contour & hull
                cv2.drawContours(vis_img, [cnt], -1, (0, 255, 0), 2)
                cv2.drawContours(vis_img, [hull], -1, (255, 0, 0), 1)

                # Bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Index label
                cv2.putText(
                    vis_img,
                    str(idx),
                    (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2,
                )
                idx += 1

    # -------------------- 5. UI STATUS OVERLAY --------------------
    if results["white_spot_found"]:
        status_text = "WHITE SPOT FOUND"
        color = (0, 0, 255)
    else:
        status_text = "OK"
        color = (0, 255, 0)

    cv2.putText(vis_img, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    # -------------------- 6. SAVE OUTPUTS --------------------
    # if detected_dir:
    #     os.makedirs(detected_dir, exist_ok=True)
    #     base = os.path.splitext(os.path.basename(image_path))[0]

    #     cv2.imwrite(os.path.join(detected_dir, f"{base}_mask.png"), mask)
    #     cv2.imwrite(os.path.join(detected_dir, f"{base}_edges.png"), edges)
    #     cv2.imwrite(os.path.join(detected_dir, f"{base}_morph.png"), morph)
    #     cv2.imwrite(os.path.join(detected_dir, f"{base}_final.png"), vis_img)

    return vis_img, results


# -------------------- MAIN RUNTIME (UI / API READY) --------------------
if __name__ == "__main__":
    test_image = r"D:\POC\marelli_poc\27_12_25\whitespot\3.bmp"
    output_dir = r"D:\poc\marelli_poc\27_12_25\whitespot\output"

    try:
        processed_img, data = analyze_white_spot(test_image, output_dir)
        print(data)

        # Optional UI preview
        # cv2.imshow("White Spot Result", cv2.resize(processed_img, (800, 800)))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {e}")
