# coding=utf-8
import mvsdk


def main():
    device_list = mvsdk.CameraEnumerateDevice()
    num_devices = len(device_list)
    if num_devices < 1:
        print("No camera was found!")
        return

    device_info = device_list[0]

    # initialize camera
    try:
        camera = mvsdk.CameraInit(device_info, -1, -1)
    except mvsdk.CameraException as e:
        print("CameraInit Failed({}): {}".format(e.error_code, e.message))
        return

    camera_capability = mvsdk.CameraGetCapability(camera)

    # run camera API
    mvsdk.CameraPlay(camera)

    # frame buffer size for highest resolution
    frame_buffer_size = camera_capability.sResolutionRange.iWidthMax * camera_capability.sResolutionRange.iHeightMax * 3

    # allocate memory for frame buffer
    p_frame_buffer = mvsdk.CameraAlignMalloc(frame_buffer_size, 16)

    # take one image
    try:
        p_raw_data, frame_head = mvsdk.CameraGetImageBuffer(camera, 2000)
        mvsdk.CameraImageProcess(camera, p_raw_data, p_frame_buffer, frame_head)
        mvsdk.CameraReleaseImageBuffer(camera, p_raw_data)

        # save the image to disk
        status = mvsdk.CameraSaveImage(camera, "z:\\grab.bmp", p_frame_buffer, frame_head, mvsdk.FILE_BMP, 100)
        if status == mvsdk.CAMERA_STATUS_SUCCESS:
            print("Save image successfully. image_size = {}X{}".format(frame_head.iWidth, frame_head.iHeight))
        else:
            print("Save image failed. err={}".format(status))
    except mvsdk.CameraException as e:
        print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message))

    # close camera
    mvsdk.CameraUnInit(camera)

    # free frame buffer memory
    mvsdk.CameraAlignFree(p_frame_buffer)


main()
