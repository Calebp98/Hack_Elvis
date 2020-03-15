import os
import shutil
def output(timestamps):
    pathout = "/path/to/output/folder/"
    blurpath = "/path/to/blurs/"
    files = os.listdir(blurpath)
    for stamp in timestamps:
        print (stamp)
        if stamp > (len(files) - 5):
            stamp -= 2
        if stamp > 2:
            stamp -= 2
        elif stamp == 2:
            stamp -= 1
        print(files[(stamp - 1)])
        shutil.copy(blurpath + files[(stamp - 1)],pathout)
