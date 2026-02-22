# import cv2
# import numpy as np
# import os
# import math

# def detect_scratch_defect(input_img, output_path):
#     os.makedirs(output_path, exist_ok=True)

#     # -------------------- LOAD IMAGE --------------------
#     img = cv2.imread(input_img)
#     if img is None:
#         raise FileNotFoundError("Image not found")

#     orig = img.copy()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # -------------------- PREPROCESS --------------------
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     edges = cv2.Canny(blur, 60, 180)

#     kernel = np.ones((5, 5), np.uint8)
#     morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

#     # -------------------- FIND CONTOURS --------------------
#     contours, _ = cv2.findContours(
#         morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#     )

#     result_img = orig.copy()
#     defect_found = False

#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if 80 < area < 500:

#             hull = cv2.convexHull(cnt)
#             hull_area = cv2.contourArea(hull)

#             # FILTER CONDITION
#             if hull_area < 850:
#                 defect_found = True

#                 # Bounding box
#                 x, y, w, h = cv2.boundingRect(cnt)

#                 # Draw bounding box
#                 cv2.rectangle(result_img,(x, y),(x + w, y + h),(0, 0, 255),2)

#     # -------------------- PUT TEXT AT TOP --------------------
#     if defect_found:
#         cv2.putText(result_img,"SCRATCH DEFECT FOUND",(20, 40),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0, 0, 255),3, cv2.LINE_AA)

#     # -------------------- SAVE OUTPUTS --------------------
#     cv2.imwrite(os.path.join(output_path, "01_gray.png"), gray)
#     cv2.imwrite(os.path.join(output_path, "02_edges.png"), edges)
#     cv2.imwrite(os.path.join(output_path, "03_morph.png"), morph)
#     cv2.imwrite(
#         os.path.join(output_path, "04_scratch_defect_final.png"),
#         result_img
#     )

#     print("Scratch Defect Found" if defect_found else "No Scratch Defect Found")
#     print("Processing completed and images saved.")

#     return defect_found

# # -------------------- FUNCTION CALL --------------------
# if __name__ == "__main__":
#     input_img = r"D:\poc\marelli_poc\27_12_25\scrach\3.bmp"
#     output_path = r"D:\poc\marelli_poc\27_12_25\scrach\output"

#     detect_scratch_defect(input_img, output_path)


# import cv2
# import numpy as np
# import os
# import math

# def detect_scratch_defect(input_img, output_path):
#     os.makedirs(output_path, exist_ok=True)

#     # -------------------- LOAD IMAGE --------------------
#     img = cv2.imread(input_img)
#     if img is None:
#         raise FileNotFoundError("Image not found")

#     orig = img.copy()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # -------------------- PREPROCESS --------------------
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     edges = cv2.Canny(blur, 60, 180)

#     kernel = np.ones((5, 5), np.uint8)
#     morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

#     # -------------------- FIND CONTOURS --------------------
#     contours, _ = cv2.findContours(
#         morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#     )

#     result_img = orig.copy()
#     bbox_found = False

#     for cnt in contours:
#         area = cv2.contourArea(cnt)

#         if 80 < area < 500:
#             hull = cv2.convexHull(cnt)
#             hull_area = cv2.contourArea(hull)

#             # ---- FILTER CONDITION ----
#             if hull_area < 850:
#                 bbox_found = True

#                 x, y, w, h = cv2.boundingRect(cnt)
#                 cv2.rectangle(
#                     result_img,
#                     (x, y),
#                     (x + w, y + h),
#                     (0, 0, 255),
#                     2
#                 )

#     # -------------------- FINAL STATUS TEXT --------------------
#     if bbox_found:
#         status_text = "SCRATCH FOUND"
#         color = (0, 0, 255)
#     else:
#         status_text = "OK"
#         color = (0, 255, 0)

#     cv2.putText(
#         result_img,
#         status_text,
#         (20, 40),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         1.0,
#         color,
#         3,
#         cv2.LINE_AA
#     )

#     # -------------------- SAVE OUTPUTS --------------------
#     cv2.imwrite(os.path.join(output_path, "01_gray.png"), gray)
#     cv2.imwrite(os.path.join(output_path, "02_edges.png"), edges)
#     cv2.imwrite(os.path.join(output_path, "03_morph.png"), morph)
#     cv2.imwrite(
#         os.path.join(output_path, "04_scratch_defect_final.png"),
#         result_img
#     )

#     print("SCRATCH FOUND" if bbox_found else "OK")
#     print("Processing completed and images saved.")

#     return bbox_found


# # -------------------- FUNCTION CALL --------------------
# if __name__ == "__main__":
#     input_img = r"D:\poc\marelli_poc\27_12_25\scrach\3.bmp"
#     output_path = r"D:\poc\marelli_poc\27_12_25\scrach\output"

#     detect_scratch_defect(input_img, output_path)


import cv2
import numpy as np
import os
import math

# -------------------- SCRATCH FILTER CONSTANTS --------------------
MIN_CONTOUR_AREA = 80
MAX_CONTOUR_AREA = 500
MAX_HULL_AREA = 850


# -------------------- MAIN ANALYSIS FUNCTION --------------------
def analyze_scratch_defect(image_path, detected_dir=None):
    """
    Scratch defect detection with UI-ready structure.

    - Edge based detection
    - Area + Hull-area filtering
    - Bounding box visualization
    - UI overlay text

    Returns:
        annotated_img, results_dict
    """

    # 1. Load Image
    img = image_path
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    orig = img.copy()
    vis_img = img.copy()

    # Results container
    results = {"scratch_found": False, "scratch_count": 0}

    # 2. Preprocessing
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 60, 180)

    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 3. Find Contours
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. Contour Filtering & Drawing
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if MIN_CONTOUR_AREA < area < MAX_CONTOUR_AREA:

            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)

            # Scratch filter condition
            if hull_area < MAX_HULL_AREA:
                results["scratch_found"] = True
                results["scratch_count"] += 1

                x, y, w, h = cv2.boundingRect(cnt)

                # Draw bounding box
                cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 5. UI Overlay Text
    if results["scratch_found"]:
        cv2.putText(
            vis_img,
            f"SCRATCH DEFECT FOUND : {results['scratch_count']}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3,
            cv2.LINE_AA,
        )
    else:
        cv2.putText(
            vis_img,
            "NO SCRATCH DEFECT",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3,
            cv2.LINE_AA,
        )

    # 6. Save Outputs (Optional)
    # if detected_dir:
    #     os.makedirs(detected_dir, exist_ok=True)
    #     base_name = os.path.splitext(os.path.basename(image_path))[0]

    #     cv2.imwrite(os.path.join(detected_dir, f"{base_name}_01_gray.png"), gray)
    #     cv2.imwrite(os.path.join(detected_dir, f"{base_name}_02_edges.png"), edges)
    #     cv2.imwrite(os.path.join(detected_dir, f"{base_name}_03_morph.png"), morph)
    #     cv2.imwrite(os.path.join(detected_dir, f"{base_name}_04_scratch_result.png"), vis_img)

    return vis_img, results


if __name__ == "__main__":

    test_image = r"D:\poc\marelli_poc\27_12_25\scrach\2.bmp"
    output_dir = r"D:\poc\marelli_poc\27_12_25\scrach\output"

    try:
        processed_img, data = analyze_scratch_defect(
            image_path=test_image, detected_dir=output_dir
        )

        print("Results:", data)

        # Optional UI display
        # cv2.imshow("Scratch Detection", cv2.resize(processed_img, (800, 600)))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error encountered: {e}")
