# coding=utf-8
import mvsdk


def camera_setup():
    device_list = mvsdk.CameraEnumerateDevice()
    num_devices = len(device_list)
    if num_devices < 1:
        raise Exception("No Camera Connected")

    device_info = device_list[0]
    try:
        camera = mvsdk.CameraInit(device_info, -1, -1)
    except mvsdk.CameraException as e:
        raise Exception("Camera Init Failed")

    # run camera API
    mvsdk.CameraPlay(camera)

    return camera


def main():
    try:
        camera = camera_setup()

        # allocate memory for frame buffer
        camera_capability = mvsdk.CameraGetCapability(camera)
        frame_buffer_size = camera_capability.sResolutionRange.iWidthMax * camera_capability.sResolutionRange.iHeightMax * 3
        p_frame_buffer = mvsdk.CameraAlignMalloc(frame_buffer_size, 16)

        counter = 0

        while True:
            try:
                print('blocking before CameraGetImageBuffer')
                p_raw_data, frame_head = mvsdk.CameraGetImageBuffer(camera, 300)
                print('blocking before CameraImageProcess')
                mvsdk.CameraImageProcess(camera, p_raw_data, p_frame_buffer, frame_head)
                print('blocking before CameraReleaseImageBuffer')
                mvsdk.CameraReleaseImageBuffer(camera, p_raw_data)
                print('success image process')

                # save the image to disk
                image_path = "C:\\Users\\van32\\Pictures\\grab_%d.BMP" % counter
                status = mvsdk.CameraSaveImage(camera, image_path, p_frame_buffer, frame_head, mvsdk.FILE_BMP, 100)
                if status == mvsdk.CAMERA_STATUS_SUCCESS:
                    print("Image Save Success")
                else:
                    print("Image Save Fail")

                counter += 1
            except mvsdk.CameraException as e:
                print(e.message)
    finally:
        # clean up
        print('clean up code called')
        mvsdk.CameraUnInit(camera)
        mvsdk.CameraAlignFree(p_frame_buffer)


main()
