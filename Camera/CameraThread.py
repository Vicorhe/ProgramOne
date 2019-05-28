import numpy as np
from threading import Thread
import Camera.mvsdk as mvsdk


class CameraThread(Thread):
    def __init__(self, session, is_training_session):
        Thread.__init__(self)
        self.session = session
        self.camera = None
        self.image_buffer = None
        if is_training_session:
            self.camera_mainloop = self.training_mainloop
        else:
            self.camera_mainloop = self.operating_mainloop
        self.start()

    def run(self):
        try:
            self.camera_setup()
            self.allocate_image_buffer()
            while True:
                if self.session.terminate_session:
                    print('Session Terminated')
                    break
                self.camera_mainloop()
        finally:
            self.camera_breakdown()

    def camera_setup(self):
        device_list = mvsdk.CameraEnumerateDevice()
        num_devices = len(device_list)
        if num_devices < 1:
            raise Exception("No Camera Connected")

        device_info = device_list[0]
        try:
            self.camera = mvsdk.CameraInit(device_info, -1, -1)
        except mvsdk.CameraException:
            raise Exception("Camera Init Failed")

        # run camera API
        mvsdk.CameraPlay(self.camera)

    def allocate_image_buffer(self):
        camera_capability_resolution = mvsdk.CameraGetCapability(self.camera).sResolutionRange
        frame_buffer_size = camera_capability_resolution.iWidthMax * camera_capability_resolution.iHeightMax * 3
        self.image_buffer = mvsdk.CameraAlignMalloc(frame_buffer_size, 16)

    def training_mainloop(self):
        try:
            p_raw_data, frame_head = mvsdk.CameraGetImageBuffer(self.camera, 500)
            mvsdk.CameraImageProcess(self.camera, p_raw_data, self.image_buffer, frame_head)
            mvsdk.CameraReleaseImageBuffer(self.camera, p_raw_data)

            # save the image to disk
            n = self.session.num_images_taken.get()
            image_name = 'image_%d.BMP' % n
            image_path = str(self.session.batch_path / image_name)
            status = mvsdk.CameraSaveImage(self.camera, image_path, self.image_buffer, frame_head, mvsdk.FILE_BMP, 100)
            if status == mvsdk.CAMERA_STATUS_SUCCESS:
                print("Image Save Success at", image_path)
            else:
                print("Image Save Fail")
            self.session.num_images_taken.set(n + 1)

        except mvsdk.CameraException:
            pass

    def operating_mainloop(self):
        try:
            p_raw_data, frame_head = mvsdk.CameraGetImageBuffer(self.camera, 500)
            mvsdk.CameraImageProcess(self.camera, p_raw_data, self.image_buffer, frame_head)
            mvsdk.CameraReleaseImageBuffer(self.camera, p_raw_data)

            # convert image to model friendly formats
            frame_data = (mvsdk.c_ubyte * frame_head.uBytes).from_address(self.image_buffer)
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape((frame_head.iHeight, frame_head.iWidth, 3))

            # make prediction
            p = self.session.predict(frame)
            self.session.highlight_shade(p)
            print(p)

        except mvsdk.CameraException:
            pass

    def camera_breakdown(self):
        print('cleanup ing')
        mvsdk.CameraUnInit(self.camera)
        mvsdk.CameraAlignFree(self.image_buffer)
