# baumer_camera.py
import neoapi
import cv2
import os


class BaumerCamera:
    def __init__(self):
        self.camera = None
        self.IP_Address = os.getenv("CAMERA_IP")
        self.connect()

    def connect(self):
        try:
            self.camera = neoapi.Cam()
            self.camera.Connect('')
            self.camera.f.ExposureTime.Set(50000)  # default exposure
            if self.camera.f.PixelFormat.GetEnumValueList().IsReadable("Mono8"):
                self.camera.f.PixelFormat.SetString("BGR8")
            print("Camera Connected!")
        except Exception as e:
            print(f"Error connecting to Baumer camera: {e}")
            self.camera = None

    def is_connected(self):
        return self.camera is not None and self.camera.IsConnected()

    def get_frame(self):
        if not self.is_connected():
            # print("Camera not connected.")
            return None
        try:
            img = self.camera.GetImage()
            if not img.IsEmpty():
                return img.GetNPArray()
        except Exception as e:
            print(f"Baumer frame capture error: {e}")
        return None

    def get_exposure(self):
        if self.is_connected():
            try:
                return self.camera.f.ExposureTime.Get()
            except Exception as e:
                print(f"Failed to get exposure: {e}")
        return None

    def set_exposure(self, exposure_value):
        if self.is_connected():
            try:
                # Disable auto exposure first
                if self.camera.f.ExposureAuto.IsWritable():
                    self.camera.f.ExposureAuto.SetString("Off")

                # Make sure exposure mode is Timed
                if self.camera.f.ExposureMode.IsWritable():
                    self.camera.f.ExposureMode.SetString("Timed")

                # Now set exposure time
                if self.camera.f.ExposureTime.IsWritable():
                    self.camera.f.ExposureTime.Set(float(exposure_value))
                    return True
                else:
                    print("ExposureTime is not writable")

            except Exception as e:
                print(f"Failed to set exposure: {e}")
        return False
    
    def get_gain(self):
        if self.is_connected():
            try:
                return self.camera.f.Gain.Get()
            except Exception as e:
                print(f"Failed to get gain: {e}")
        return None

    def set_gain(self, gain_value):
        if self.is_connected():
            try:
                if self.camera.f.GainAuto.IsWritable():
                    self.camera.f.GainAuto.SetString("Off")

                if self.camera.f.Gain.IsWritable():
                    self.camera.f.Gain.Set(float(gain_value))
                    return True
                else:
                    print("Gain is not writable")

            except Exception as e:
                print(f"Failed to set gain: {e}")
        return False

    def close(self):
        if self.camera is not None:
            try:
                if self.camera.IsConnected():
                    self.camera.Disconnect()
                    print("Camera disconnected")
            except Exception as e:
                print(f"Failed to disconnect camera: {e}")
            finally:
                self.camera = None
