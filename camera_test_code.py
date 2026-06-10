import attollo_camera_toolbox as atcam

camera = atcam.AttolloCamera()

camera.set_gain(3)
camera.set_exposure(1)
camera.set_image_dtype(16)
camera.return_image()
camera.close()
                    