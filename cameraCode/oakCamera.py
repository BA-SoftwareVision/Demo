#!/usr/bin/env python3

import cv2
import depthai as dai
import threading


class OAKCamera:
    def __init__(self):
        self.pipeline = None
        self.device = None
        self.video_queue = None
        self.ctrl_queue = None
        self.frame_thread = None
        self.running = False
        self.latest_frame = None
        self.frame_lock = threading.Lock()

    def connect(self):
        """Initialize and start the OAK camera pipeline."""
        try:
            # Create pipeline
            self.pipeline = dai.Pipeline()

            # Define source and output
            cam = self.pipeline.create(dai.node.Camera).build()
            self.video_queue = cam.requestOutput((1240, 1080)).createOutputQueue()
            self.ctrl_queue = cam.inputControl.createInputQueue()

            # Camera settings
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(10000, 400)
            ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.OFF)
            ctrl.setManualFocus(120)

            # Start the pipeline
            self.pipeline.start()

            # Send camera control settings
            self.ctrl_queue.send(ctrl)
            self.ctrl_queue.send(ctrl)

            self.running = True

            # Start frame grabbing thread
            self.frame_thread = threading.Thread(target=self._grab_frames, daemon=True)
            self.frame_thread.start()

            print("[OAK] Camera connected and grabbing")
            return True

        except Exception as e:
            print(f"[OAK] Error connecting camera: {e}")
            return False

    def _grab_frames(self):
        """Background thread to continuously grab frames."""
        while self.running and self.pipeline.isRunning():
            try:
                video_in = self.video_queue.get()
                if isinstance(video_in, dai.ImgFrame):
                    frame = video_in.getCvFrame()
                    with self.frame_lock:
                        self.latest_frame = frame.copy()
            except Exception as e:
                print(f"[OAK] Frame grab error: {e}")
                break

    def get_frame(self):
        """Get the latest frame from the camera."""
        with self.frame_lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def set_exposure(self, exposure_time, iso=400):
        """Set camera exposure."""
        try:
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(int(exposure_time), int(iso))
            self.ctrl_queue.send(ctrl)
            return True
        except Exception as e:
            print(f"[OAK] Error setting exposure: {e}")
            return False

    def get_exposure(self):
        """Get current exposure setting (not directly supported, return default)."""
        return 10000  # Default value

    def set_gain(self, gain):
        """Set camera ISO/gain."""
        try:
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(10000, int(gain))
            self.ctrl_queue.send(ctrl)
            return True
        except Exception as e:
            print(f"[OAK] Error setting gain: {e}")
            return False

    def get_gain(self):
        """Get current gain setting (not directly supported, return default)."""
        return 400  # Default value

    def close(self):
        """Stop the camera and clean up resources."""
        print("[OAK] Closing camera...")
        self.running = False

        if self.frame_thread and self.frame_thread.is_alive():
            self.frame_thread.join(timeout=2)

        if self.pipeline:
            try:
                self.pipeline.stop()
            except:
                pass

        print("[OAK] Camera closed")
