import cv2
import sys
from pygrabber.dshow_graph import FilterGraph
from ultralytics import YOLO
import torch
import time

def perceive_logo():
    perceive = ("""
                                   .....                                   
                               ...       ...                               
                            ...             ...                            
                        ...                     ...                        
                     ...                           ....                    
                  ..                                  ..:.                 
              ...                                         .:..             
           ..                                                .::.          
       ...                                                       .:..      
    ..                  .::::::::.....                              .::.   
 ..                ..:-==-::..::      ....:::::.....                   .:: 
..             ....  .+=. .:    .:.               ..:===-:::.            ::
.         ....     .==.   ..      ..:.        .::--=++==-:----.          .-
.        ....    .==.     ..         .:::====--:..   .:.   -. :-.        .-
.       .     ..:=.       :.       .-=++-:.       .::.     -.   ::.      .-
.     ..       --..       :.    .-=-.  +:  .:...::.        ::     ::     .-
.    ..        +:   ..    :. :-=-.    .*.    ----:.        ::      .-:   .-
.   ...       :+:....:::::::=:.       :+     ::   .:::.    .-        .-. .-
..  ...:--------:::::::::::..:..      -+    .:        .:-:::-         -. .-
..   ..  ....           :.     ..:.   == .:=:----------==-----.       -. .-
..    .       ....    .:          ..:.+++=::.             -:+-.::.    -. .-
:.    ..          .::::::..        .-=::. .:            .-. =+   .-:..-. .-
:.     ..     .:-==-::.:-:--====-=+-.    :::.          ::   .*.     :--. .-
:.      .:--=+=.    ..  .:.     :=+      :-+..::..   .-.     +-     :-.  .-
:.         .........:      ..     ==    .: +-    .:::-:      -*  .-:.    .-
:.                  :.......:-:.::=+:   :. :*.     :: ..:::::-+=-:       .-
:.                  .:=+-:::::..::.:+. ::   ==    ::       :++=-         .-
:.                    .:.        .:.=+.:    .*.  ::    .-==-..-:         .-
:.                      .:.        ::-:.     =+ :: .-==-.   .::.         .-
:.                        ............:::::...+-===-.    .::.            .-
:.                                    .:     .:---     .::               .-
.:                                     .:     .-..:::::.                 --
 .:..                                   ::     -.                     .:-: 
    ..:.                                 ::    ::                  .-:.    
        .:..                               .:..:-              .:-:.       
           .::.                               .:-.          .::.           
               .:..                                     .:-:.              
                  .::.                               .::.                  
                     ..::.                       .:::.                     
                         .::.                 .::.                         
                            .:::.         .:::.                            
                                .::.   .::.                               
                        Made with <3 in PeRCeiVe Lab
                           (www.perceivelab.com)
    """)

    print(perceive)
    time.sleep(5)

    return

def get_camera():
    devices = FilterGraph().get_input_devices()
    camera_dict = {}

    for i, name in enumerate(devices):
        camera_dict[i] = name

    print(camera_dict)

    return

def main(): 
    try:
        camera_device = int(input('Select camera device (use integers): '))
    except ValueError:
        print("ERROR: Enter a valid camera device (use integers)")
        sys.exit(1)

    inference_device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Inference device: {inference_device}")

    print("Loading YOLO models...")
    model = 'n'
    segment = YOLO(f"yolov8{model}-seg.pt").to(inference_device)
    pose = YOLO(f"yolov8{model}-pose.pt").to(inference_device)

    print("Starting camera device...")
    cap = cv2.VideoCapture(camera_device)

    while True:
        ret, frame = cap.read() # Capture frame from webcam
        if not ret:
            print("The video capture has ended")
            break
    
        frame = cv2.flip(frame, 1) # Flip frame

        # Inference
        res_segment = segment.predict(source=frame)
        pose_segment = pose.predict(source=frame)
        
        # Plot
        segment_frame = res_segment[0].plot(labels=True, line_width=3)
        pose_frame = pose_segment[0].plot(labels=False)     
        cv2.namedWindow("Segmentation", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Pose", cv2.WINDOW_NORMAL)
        cv2.imshow("Segmentation", segment_frame)
        cv2.imshow("Pose", pose_frame)

        if (cv2.waitKey(1) == 27):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    perceive_logo()
    get_camera()
    main()
