# ##-- FINAL FUNCTION FOR INTEGRATION--
# import cv2
# import numpy as np
# import os
# import math


# def detect_black_spot(input_img, output_path,
#                       area_min=100, area_max=1000,
#                       circ_min=0.33, circ_max=0.48,
#                       show_result=True):

#     # ---------------- Read image ----------------
#     img = cv2.imread(input_img)
#     if img is None:
#         raise FileNotFoundError(f"Image not found: {input_img}")

#     orig = img.copy()

#     # ---------------- HSV filtering ----------------
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     lower = np.array([0, 185, 35])
#     upper = np.array([179, 255, 255])

#     mask = cv2.inRange(hsv, lower, upper)
#     filtered = cv2.bitwise_and(img, img, mask=mask)

#     # ---------------- Threshold ----------------
#     gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 27, 255, cv2.THRESH_BINARY)

#     # ---------------- Contours ----------------
#     contours, _ = cv2.findContours(
#         thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
#     )

#     black_spot_found = False

#     # ---------------- Analyze contours ----------------
#     for cnt in contours:
#         area = cv2.contourArea(cnt)

#         if area_min < area < area_max:
#             perimeter = cv2.arcLength(cnt, True)
#             if perimeter == 0:
#                 continue

#             circularity = 4 * math.pi * area / (perimeter * perimeter)

#             if circ_min <= circularity <= circ_max:
#                 black_spot_found = True

#                 # Bounding box
#                 x, y, w, h = cv2.boundingRect(cnt)
#                 cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 255, 0), 2)

#                 # Circularity text
#                 cv2.putText(
#                     orig,
#                     f"C={circularity:.2f}",
#                     (x, y - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.45,
#                     (255, 0, 0),
#                     1,
#                     cv2.LINE_AA
#                 )

#                 print(f"Black spot detected | Area={area:.1f} | Circularity={circularity:.2f}")

#     # ---------------- Final status text ----------------
#     if black_spot_found:
#         cv2.putText(
#             orig,
#             "Black spot defect found",
#             (70, 55),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             2.0,
#             (0, 0, 255),
#             2,
#             cv2.LINE_AA
#         )

#     # ---------------- Save result ----------------
#     os.makedirs(output_path, exist_ok=True)
#     output_file = os.path.join(output_path, "black_spot_result.jpg")
#     cv2.imwrite(output_file, orig)

#     # ---------------- Display ----------------
#     if show_result:
#         cv2.imshow("Black Spot Detection", cv2.resize(orig, (300, 300)))
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

#     return black_spot_found, output_file

# # ======================= MAIN ============================
# if __name__ == "__main__":

#     input_img = r"D:\poc\marelli_poc\27_12_25\blackspot\3" \
#     ".bmp"
#     output_path = r"D:\poc\marelli_poc\27_12_25\blackspot\output"

#     found, result_path = detect_black_spot(
#         input_img=input_img,
#         output_path=output_path,
#         show_result=True
#     )

#     print("\n================ RESULT =================")
#     if found:
#         print("✅ Black spot defect FOUND")
#     else:
#         print("❌ Black spot defect NOT found")

#     print("Saved output:", result_path)





##-- FINAL FUNCTION FOR INTEGRATION--
# import cv2
# import numpy as np
# import os
# import math


# def detect_black_spot(input_img, output_path,
#                       area_min=100, area_max=1000,
#                       circ_min=0.33, circ_max=0.48,
#                       show_result=True):

#     # ---------------- Read image ----------------
#     img = cv2.imread(input_img)
#     if img is None:
#         raise FileNotFoundError(f"Image not found: {input_img}")

#     orig = img.copy()

#     # ---------------- HSV filtering ----------------
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     lower = np.array([0, 185, 35])
#     upper = np.array([179, 255, 255])

#     mask = cv2.inRange(hsv, lower, upper)
#     filtered = cv2.bitwise_and(img, img, mask=mask)

#     # ---------------- Threshold ----------------
#     gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 27, 255, cv2.THRESH_BINARY)

#     # ---------------- Contours ----------------
#     contours, _ = cv2.findContours(
#         thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
#     )

#     black_spot_found = False

#     # ---------------- Analyze contours ----------------
#     for cnt in contours:
#         area = cv2.contourArea(cnt)

#         if area_min < area < area_max:
#             perimeter = cv2.arcLength(cnt, True)
#             if perimeter == 0:
#                 continue

#             circularity = 4 * math.pi * area / (perimeter * perimeter)

#             if circ_min <= circularity <= circ_max:
#                 black_spot_found = True

#                 x, y, w, h = cv2.boundingRect(cnt)
#                 cv2.rectangle(
#                     orig, (x, y), (x + w, y + h),
#                     (0, 255, 0), 2
#                 )

#                 cv2.putText(
#                     orig,
#                     f"C={circularity:.2f}",
#                     (x, y - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.45,
#                     (255, 0, 0),
#                     1,
#                     cv2.LINE_AA
#                 )

#                 print(
#                     f"Black spot detected | Area={area:.1f} | Circularity={circularity:.2f}"
#                 )

#     # ---------------- Final status text ----------------
#     if black_spot_found:
#         status_text = "BLACK SPOT FOUND"
#         color = (0, 0, 255)
#     else:
#         status_text = "OK"
#         color = (0, 255, 0)

#     cv2.putText(
#         orig,
#         status_text,
#         (70, 55),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         2.0,
#         color,
#         2,
#         cv2.LINE_AA
#     )

#     # ---------------- Save result ----------------
#     os.makedirs(output_path, exist_ok=True)
#     output_file = os.path.join(output_path, "black_spot_result.jpg")
#     cv2.imwrite(output_file, orig)

#     # ---------------- Display ----------------
#     if show_result:
#         cv2.imshow("Black Spot Detection", cv2.resize(orig, (300, 300)))
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

#     return black_spot_found, output_file


# # ======================= MAIN ============================
# if __name__ == "__main__":

#     input_img = r"D:\poc\marelli_poc\27_12_25\blackspot\3.bmp"
#     output_path = r"D:\poc\marelli_poc\27_12_25\blackspot\output"

#     found, result_path = detect_black_spot(
#         input_img=input_img,
#         output_path=output_path,
#         show_result=True
#     )

#     print("\n================ RESULT =================")
#     print("BLACK SPOT FOUND" if found else "OK")
#     print("Saved output:", result_path)































import cv2
import numpy as np
import os
import math

# -------------------- THRESHOLDS --------------------
HSV_LOWER = np.array([0, 185, 35])
HSV_UPPER = np.array([179, 255, 255])

BIN_THRESH = 27

MIN_AREA = 100
MAX_AREA = 1000

MIN_CIRCULARITY = 0.33
MAX_CIRCULARITY = 0.48


def analyze_black_spot_defect(image_path, detected_dir=None):
    """
    Black spot defect detection using HSV + shape filtering.

    - HSV masking
    - Area & circularity filtering
    - Bounding box annotation
    - UI-ready overlay

    Returns:
        annotated_img, results_dict
    """

    # 1. Read Image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read: {image_path}")

    vis_img = img.copy()
    black_spot_found = False
    defect_count = 0

    # 2. Preprocessing (HSV Mask)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOWER, HSV_UPPER)
    filtered = cv2.bitwise_and(img, img, mask=mask)

    # 3. Binary Threshold
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, BIN_THRESH, 255, cv2.THRESH_BINARY)

    # 4. Find Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Area filter
        if MIN_AREA < area < MAX_AREA:

            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue

            circularity = 4 * math.pi * area / (perimeter ** 2)

            # Circularity filter
            if MIN_CIRCULARITY <= circularity <= MAX_CIRCULARITY:
                black_spot_found = True
                defect_count += 1

                # Bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Circularity label
                cv2.putText(
                    vis_img,
                    f"C={circularity:.2f}",
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA
                )

    # 5. Results Dictionary (UI friendly)
    results = {
        "black_spot_found": black_spot_found,
        "defect_count": defect_count
    }

    # 6. UI Overlay
    if black_spot_found:
        cv2.putText(
            vis_img,
            "Black spot defect found",
            (70, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (0, 0, 255),
            3,
            cv2.LINE_AA
        )
    else:
        cv2.putText(
            vis_img,
            "No black spot defect",
            (70, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (0, 255, 0),
            3,
            cv2.LINE_AA
        )

    # 7. Save Logic
    # if detected_dir:
    #     os.makedirs(detected_dir, exist_ok=True)
    #     base_name = os.path.splitext(os.path.basename(image_path))[0]
    #     save_path = os.path.join(detected_dir, f"{base_name}_blackspot.png")
    #     cv2.imwrite(save_path, vis_img)

    return vis_img, results


# -------------------- MAIN RUNTIME (UI / TEST) --------------------
if __name__ == "__main__":

    test_image = r"D:\poc\marelli_poc\27_12_25\blackspot\2.bmp"
    output_dir = r"D:\poc\marelli_poc\27_12_25\blackspot\output"

    try:
        processed_img, data = analyze_black_spot_defect(
            image_path=test_image,
            detected_dir=output_dir
        )

        print("Results:", data)

        # Optional UI Preview
        # cv2.imshow("Black Spot Detection", cv2.resize(processed_img, (300, 300)))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error encountered: {e}")
