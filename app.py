import time
import os
import cv2
import threading
from flask import Flask, request, jsonify, render_template, Response, send_file

from cameraCode.ET import ETCamera
# from visionCodes.grayscale import convert_to_grayscale
import signal
import sys
import threading

from visionCodes.final_black import analyze_black_spot_defect
from visionCodes.final_scrach import analyze_scratch_defect
from visionCodes.final_white import analyze_white_spot
stop_event = threading.Event()

app = Flask(__name__)

# ---- Shared Frame ----
global_frame = None
frame_lock = threading.Lock()

# ---- Directories ----
captured_dir = "static/capturedImage"
detected_dir = "static/detectedImage"
os.makedirs(captured_dir, exist_ok=True)
os.makedirs(detected_dir, exist_ok=True)

# ---- Camera Init ----
et_cam = ETCamera()


def camera_grabber():
    global global_frame
    try:
        et_cam.connect()   # This already starts grabbing internally
        print("[ET] Camera connected and grabbing")

        while not stop_event.is_set():
            frame = et_cam.get_frame()
            if frame is not None:
                with frame_lock:
                    global_frame = frame.copy()
            
            time.sleep(0.01)

    except Exception as e:
        print("Camera error:", e)

    finally:
        print("Camera cleanup")

        # ONLY call what actually exists
        if hasattr(et_cam, "close"):
            et_cam.close()


def generate_frames():
    while True:
        with frame_lock:
            frame = None if global_frame is None else global_frame.copy()

        if frame is None:
            time.sleep(0.01)
            continue

        _, buf = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n"
        )


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/capture", methods=["POST"])
def capture_image():
    with frame_lock:
        frame = None if global_frame is None else global_frame.copy()

    if frame is None:
        return jsonify({"error": "No frame available"}), 500

    cap_path = os.path.join(captured_dir, "captured.jpg")
    cv2.imwrite(cap_path, frame)

    data = request.get_json() or {}
    button = int(data.get("button", 0))

    if button == 1:
        out_img, msg = analyze_black_spot_defect(cap_path, detected_dir)
    elif button == 2:
        out_img, msg = analyze_scratch_defect(cap_path)
    elif button == 3:
        out_img, msg = analyze_white_spot(cap_path)
    # elif button == 4:
    #     out_img, msg = analyze_cross_sectional_dimensions(cap_path)
    # elif button == 5:
    #     out_img, msg = extreme_distance_measurement(cap_path)
    # elif button == 6:
    #     out_img, msg = analyze_vertical_cross_section(cap_path)

    else:
        out_img, msg = frame, "No processing selected"

    det_path = os.path.join(detected_dir, "detected.jpg")
    cv2.imwrite(det_path, out_img)

    return jsonify(
        {
            "captured_image": "/static/capturedImage/captured.jpg",
            "detected_image": "/static/detectedImage/detected.jpg",
            "message": msg,
        }
    )


@app.route("/get_captured_image")
def get_captured_image():
    return send_file(os.path.join(captured_dir, "captured.jpg"))


@app.route("/get_detected_image")
def get_detected_image():
    return send_file(os.path.join(detected_dir, "detected.jpg"))


@app.route("/set_exposure", methods=["POST"])
def set_exposure():
    data = request.get_json()
    exposure = float(data.get("exposure", 10000))
    success = et_cam.set_exposure(exposure)
    return jsonify({"success": success, "exposure": exposure})


@app.route("/set_gain", methods=["POST"])
def set_gain():
    data = request.get_json()
    gain = float(data.get("gain", 5.0))
    success = et_cam.set_gain(gain)
    return jsonify({"success": success, "gain": gain})


@app.route("/get_settings", methods=["GET"])
def get_settings():
    exposure = et_cam.get_exposure()
    gain = et_cam.get_gain()
    return jsonify({
        "exposure": exposure if exposure is not None else "Error",
        "gain": gain if gain is not None else "Error"
    })


def signal_handler(sig, frame):
    print("Ctrl+C detected, shutting down...")
    stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



if __name__ == "__main__":
    cam_thread = threading.Thread(target=camera_grabber, daemon=True)
    cam_thread.start()

    app.run(debug=False, use_reloader=False,port=8000)
