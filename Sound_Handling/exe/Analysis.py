
def Sound(file):
	import sys
	import scipy.io.wavfile
	sys.path.append("../api")
	import Vokaturi
	
	path = __file__                                     #Gathers the file path for this script
	toRemove = "exe/Analysis.py"                                #Variable for the part of the path we don't want to get to the analysis file
	root = (path[:(len(path)-len(toRemove))])  #Cuts down the file path and adds the path to the analysis file

	Vokaturi.load(root + "/lib/open/win/OpenVokaturi-3-4-win64.dll")
	file_name = (root + "/sounds/cut/"+ str(file))

	(sample_rate, samples) = scipy.io.wavfile.read(file_name)
	buffer_length = len(samples)
	c_buffer = Vokaturi.SampleArrayC(buffer_length)

	if samples.ndim == 1:  # mono
		c_buffer[:] = samples[:] / 32768.0
	else:  # stereo
		c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0
	
	voice = Vokaturi.Voice (sample_rate, buffer_length)
	voice.fill(buffer_length, c_buffer)
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voice.extract(quality, emotionProbabilities)

	output = {"Neutral": 0 ,"Happy": 0 , "Sad": 0 , "Angry": 0 , "Fear": 0, "Valid":False}
	if quality.valid:
		output["Valid"] = True
		output["Neutral"] = emotionProbabilities.neutrality
		output["Happy"] = emotionProbabilities.happiness
		output["Sad"] = emotionProbabilities.sadness
		output["Angry"] = emotionProbabilities.anger
		output["Fear"] = emotionProbabilities.fear
	
	return (output)
	voice.destroy()