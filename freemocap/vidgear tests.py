# import required libraries
from vidgear.gears import CamGear, WriteGear
from pathlib import Path
import cv2
import time
import pandas as pd

from webcam import timesync
from tkinter import Tk

num_range = 3
cam_names = []
frames = {}
times = {}
for n in range(num_range):
    one_name = 'cam{}'.format(n)
    cam_names.append(one_name)
    times[one_name] = []
    frames[one_name] = []
stream_list = []
writer_list = []
# define and start the stream on first source ( For e.g #0 index device)
options = {"CAP_PROP_FRAME_WIDTH":640, "CAP_PROP_FRAME_HEIGHT":480, 'CAP_PROP_FPS':30, 'CAP_PROP_EXPOSURE':-5}
output_params = {"-fourcc":"mp4v","-fps":30} 

save_path = Path(r'C:\Users\aaron\Documents\Python')


beginTime = time.time()


for n in range(num_range):
    videoPath = str(save_path/'video{}.mp4'.format(n))
    writer = WriteGear(output_filename=videoPath, compression_mode=False,**output_params)
    writer_list.append(writer)

    stream = CamGear(source=n, logging=False, **options).start() 
    stream_list.append(stream)


# define and start the stream on second source ( For e.g #1 index device)
#stream2 = CamGear(source=1, logging=True, **options).start() 
#frames = {'cam0':[],'cam1':[]}

f = 2
# infinite loop
while True:

    for stream, writer, cam_name in zip(stream_list, writer_list, cam_names):
        frame = stream.read()
        times[cam_name].append(time.time() - beginTime)
        cv2.imshow(cam_name, frame)
        frames[cam_name].append(frame)
        writer.write(frame)

    #frames[0]
    # read frames from stream1

    #frameB = stream2.read()
    # read frames from stream2

    # check if any of two frame is None
    #if frameA is None or frameB is None:
        #if True break the infinite loopq
    #    break

    # do something with both frameA and frameB here

    #cv2.imshow("Output Frame1", frameA)
    #cv2.imshow("Output Frame2", frameB)
    # Show output window of stream1 and stream 2 separately

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break

    if key == ord("w"):
        f = 2 
        #if 'w' key-pressed save both frameA and frameB at same time
        #cv2.imwrite("Image-1.jpg", frameA)
        #cv2.imwrite("Image-2.jpg", frameB)
        #break   #uncomment this line to break out after taking images


cv2.destroyAllWindows()
# close output window

# safely close both video streams
for stream,writer in zip(stream_list,writer_list):
    stream.stop()
    writer.close()

df = pd.DataFrame.from_dict(times, orient="index")  # create a data frame from this dictionary
timeStampData = df.transpose()
csvName = "_timestamps.csv" 
csvPath = save_path/csvName
timeStampData.to_csv(csvPath)  # turn dataframe into a CSV

frameTable,timeTable,frameRate,resultsTable,plots = timesync.TimeSync([],timeStampData,range(num_range),cam_names)
root = Tk()
proceed = timesync.proceedGUI(
    root, resultsTable, plots
)  # create a GUI instance called proceed
root.mainloop()
f = 2