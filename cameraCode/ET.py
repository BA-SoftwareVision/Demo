import os
import sys
import ctypes
import threading
import numpy as np
import cv2
from ctypes import *
import signal
import time




# ---- MVS SDK IMPORT ----
sys.path.append(os.getenv("MVCAM_COMMON_RUNENV") + "/Samples/Python/MvImport")
from CameraParams_header import *
from MvCameraControl_class import *
from MvErrorDefine_const import *

TARGET_SERIAL_NO = "747AV002"


class ETCamera:
    def __init__(self):
        self.cam = MvCamera()
        self.device_info = None
        self.running = False
        self.frame = None
        self.lock = threading.Lock()

    def connect(self):
        MvCamera.MV_CC_Initialize()

        device_list = MV_CC_DEVICE_INFO_LIST()
        ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, device_list)
        if ret != MV_OK or device_list.nDeviceNum == 0:
            raise RuntimeError("No ET cameras found")

        for i in range(device_list.nDeviceNum):
            info = cast(device_list.pDeviceInfo[i],
                        POINTER(MV_CC_DEVICE_INFO)).contents

            serial = ""
            if info.nTLayerType == MV_USB_DEVICE:
                serial = bytes(info.SpecialInfo.stUsb3VInfo.chSerialNumber)\
                            .split(b'\x00', 1)[0]\
                            .decode('utf-8', errors='ignore')\
                            .strip()

            elif info.nTLayerType == MV_GIGE_DEVICE:
                serial = bytes(info.SpecialInfo.stGigEInfo.chSerialNumber)\
                            .split(b'\x00', 1)[0]\
                            .decode('utf-8', errors='ignore')\
                            .strip()

            print(f"[DEBUG] Found camera serial: '{serial}'")

            if serial == TARGET_SERIAL_NO:
                self.device_info = info
                break


        if self.device_info is None:
            raise RuntimeError("Target ET camera not found")

        self.cam.MV_CC_CreateHandle(self.device_info)
        self.cam.MV_CC_OpenDevice()

        # ---- Camera Settings ----
        self.cam.MV_CC_SetEnumValueByString("TriggerMode", "Off")
        # self.cam.MV_CC_SetEnumValueByString("PixelFormat", "BayerRG8")
        self.cam.MV_CC_SetEnumValueByString("ExposureAuto", "Off")
        self.cam.MV_CC_SetFloatValue("ExposureTime", 5000.0)
        self.cam.MV_CC_SetEnumValueByString("GainAuto", "Off")
        self.cam.MV_CC_SetFloatValue("Gain", 1.0)

        self.cam.MV_CC_StartGrabbing()
        self.running = True

        threading.Thread(target=self._grab_loop, daemon=True).start()

    def _grab_loop(self):
        stFrame = MV_FRAME_OUT()

        while self.running:
            ret = self.cam.MV_CC_GetImageBuffer(stFrame, 1000)
            if ret == MV_OK:
                w = stFrame.stFrameInfo.nWidth
                h = stFrame.stFrameInfo.nHeight
                data = ctypes.string_at(stFrame.pBufAddr, stFrame.stFrameInfo.nFrameLen)

                img = np.frombuffer(data, dtype=np.uint8)

                if img.size == h * w:
                    img = img.reshape(h, w)               # MONO
                elif img.size == h * w * 3:
                    img = img.reshape(h, w, 3)             # BGR by default
                    
                    # NOTE: To use RGB, uncomment the following line:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                else:
                    raise ValueError(f"Unexpected frame size: {img.size}")


                with self.lock:
                    self.frame = img.copy()

                self.cam.MV_CC_FreeImageBuffer(stFrame)

    def get_frame(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def set_exposure(self, exposure_us):
        if not self.running:
            return False
        self.cam.MV_CC_SetEnumValueByString("ExposureAuto", "Off")
        ret = self.cam.MV_CC_SetFloatValue("ExposureTime", float(exposure_us))
        return ret == 0

    def set_gain(self, gain_db):
        if not self.running:
            return False
        self.cam.MV_CC_SetEnumValueByString("GainAuto", "Off")
        ret = self.cam.MV_CC_SetFloatValue("Gain", float(gain_db))
        return ret == 0

    def get_exposure(self):
        if not self.running:
            return None
        stFloatValue = MVCC_FLOATVALUE()
        memset(byref(stFloatValue), 0, sizeof(MVCC_FLOATVALUE))
        ret = self.cam.MV_CC_GetFloatValue("ExposureTime", stFloatValue)
        if ret == 0:
            return stFloatValue.fCurValue
        return None

    def get_gain(self):
        if not self.running:
            return None
        stFloatValue = MVCC_FLOATVALUE()
        memset(byref(stFloatValue), 0, sizeof(MVCC_FLOATVALUE))
        ret = self.cam.MV_CC_GetFloatValue("Gain", stFloatValue)
        if ret == 0:
            return stFloatValue.fCurValue
        return None


    def release(self):
        print("[ET CAMERA] Shutting down camera...")
        self.running = False
        time.sleep(0.2)

        try:
            self.cam.MV_CC_StopGrabbing()
            self.cam.MV_CC_CloseDevice()
            self.cam.MV_CC_DestroyHandle()
        except Exception as e:
            print("Camera shutdown error:", e)

        MvCamera.MV_CC_Finalize()
        print("[ET CAMERA] Camera released successfully")

