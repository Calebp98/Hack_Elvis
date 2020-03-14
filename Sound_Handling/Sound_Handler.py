res = 5000              #The length of each snippet [ms]
blursize = 6                #The number of snippets in each blur

import os                                           #Enables file manipulation
import sys                                          #Enables further manipulation
import pydub
path = __file__                                     #Gathers the file path for this script
toRemove = "Test.py"                                #Variable for the part of the path we don't want to get to the analysis file
root = (path[:(len(path)-len(toRemove))])           #Cuts down the file path and adds the path to the analysis file
sys.path.insert(1,root + "exe")                     #Allows importing from the 'exe' folder
import Analysis                                     #Imports the analysis module

soundpath = (root + "sounds/raw/" + os.listdir(root + "/sounds/raw")[0])    #Creates the path for the full recording
print (soundpath)
sound = pydub.AudioSegment.from_file(soundpath)                             #opens the full recording as the sound variable
sound = sound[len(sound) % res:]                                            #Removes excess length from the start to limit the files to a multiple of the resolution
for n in range(1,(len(sound)//res)):                                        #iterates through the 
    snippet = sound[(n-1)*res:n*res]
    snippath = (root +"/sounds/cut/" + str(n) + ".wav")
    snippet.export(snippath, format = "wav")

for n in range(1,(len(sound)//res)-(blursize-1)):
    blur = sound[(n-1)*res:(n+(blursize-1))*res]
    blurpath = (root +"/sounds/blur/" + str(n) + ".wav")
    blur.export(blurpath, format = "wav")


for file in os.listdir("Test/sounds/cut"):              #Iterates for each audio file in the sounds folder
    output = Analysis.Sound(file)
    filename = str(file)
    filename = filename[:len(filename)-4]
    output["n"] = filename
    print(output)                                   #Returns the analysis for that audio file