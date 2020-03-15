import os
import numpy as np
from flask import Flask, request, jsonify, render_template, flash,redirect,send_file
import pickle
from werkzeug.utils import secure_filename
import pandas as pd
import librosa
import glob
import numpy as np
import keras
import pydub            #Enables the basics
import tensorflow as tf
import shutil



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)

# for file uploding stuff
app.secret_key = "78929"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

loaded_model = keras.models.load_model('saved_models/Emotion_Voice_Detection_Model.h5')
graph = tf.get_default_graph()


# model = pickle.load(open('model.pkl', 'rb'))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def loadModel:
# 	return	loaded_model = keras.models.load_model('saved_models/Emotion_Voice_Detection_Model.h5')

def predictEmotion(path):
	# path = 'cuts/001.wav'

	# loaded_model = model

	# code for tf model
	global graph
	with graph.as_default():
		data, sampling_rate = librosa.load(path)

		X, sample_rate = librosa.load(path, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
		sample_rate = np.array(sample_rate)
		mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
		featurelive = mfccs
		livedf2 = featurelive
		livedf2= pd.DataFrame(data=livedf2)
		twodimNew = livedf2.values
		twodimNew =np.expand_dims(twodimNew, axis=0)
		livepreds = loaded_model.predict(twodimNew, batch_size=32, verbose=1)

		return livepreds

def analysis(data):
	timestamps = []
	total = [0,0,0,0,0,0,0,0,0,0]
	for frame in data:
		n = 0
		for point in frame:
			# print(n)
			total[n] += float(point)
			n +=1
	maximum=0
	index = 0
	for i,value in enumerate(total):
		if value>maximum:
			maximum=value
			index=i
	highflag = 0
	N = 0
	for frame in data:
		normal = True
		for i,point in enumerate(frame):
			if i != index:
				if point > frame[index]:
					normal = False
					if highflag <1:
						highflag = 6
						timestamps.append(N+1)
		if normal:
			highflag -= 1
		N +=1

	return (timestamps)


def output(timestamps):
	pathout = "output/"
	blurpath = "blurs/"
	files = os.listdir(blurpath)
	for stamp in timestamps:
		# print (stamp)
		if stamp > (len(files) - 5):
			stamp -= 2
		if stamp > 2:
			stamp -= 2
		elif stamp == 2:
			stamp -= 1
		# print(files[(stamp - 1)])
		shutil.copy(blurpath + files[(stamp - 1)],pathout)


def slicer(path):
	slicepath = "cuts/"
	blurpath = "blurs/"
	res = 5000              #The length of each snippet [ms]
	blursize = 6            #The number of snippets in a blur

	sound = pydub.AudioSegment.from_file(path)                              #opens the full recording as the sound variable
	sound = sound[len(sound) % res:]                                    #Removes excess length from the start to limit the files to a multiple of the resolution
	for n in range(1,(len(sound)//res)):
		snippet = sound[(n-1)*res:n*res]
		Nstr = str(n)
		for i in range(0,(len(str(len(sound)//res)))-len(str(n))):
			Nstr = "0"+str(Nstr)
		slice = slicepath+ str(Nstr) + ".wav"
		snippet.export(slice, format = "wav")

	for n in range(1,(len(sound)//res)-(blursize-1)):
		blur = sound[(n-1)*res:(n+(blursize-1))*res]
		Nstr = str(n)
		for i in range(0,(len(str(len(sound)//res)))-len(str(n))):
			Nstr = "0"+str(Nstr)
		blurs = blurpath + str(Nstr) + ".wav"
		blur.export(blurs, format = "wav")


@app.route('/')
def home():
	cuts = 'cuts/'
	for f in os.listdir(cuts):
		if os.path.exists(cuts + f):
  			# os.remove(f)
			x = 0
			# print('exists2')
		# print('exists1')
	blurs = 'blurs/'
	for f in os.listdir(blurs):
		if os.path.exists(f):
  			os.remove(f)
	for f in os.listdir('output/'):
		if os.path.exists(f):
  			os.remove(f)
	print("Cleaned up!")
	return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
	directory = 'cuts/'
	emotionData = []

	for i in range(len(os.listdir(directory))-1):
		i = i+1
		filename = str(0)+str(0)+str(i) +'.wav'
		if(len(filename)>7):
			filename = filename[-7:]
			print(filename)
		print(os.path.join(filename))
		datum = predictEmotion(os.path.join(directory, filename))
		print(os.path.join(directory, filename))
		datum = datum.tolist()
		datum2 = [ '%.3f' % elem for elem in datum[0] ]
		emotionData.append(datum2)
		print(len(emotionData))
		print(len(emotionData[0]))

	result = emotionData[0]
	x = result
	output(analysis(emotionData))


	return render_template('index.html', fAngry=x[0],fCalm=x[1],fFearful=x[2],fHappy=x[3],fSad=x[4],mAngry=x[5],mCalm=x[6],mFearful=x[7],mHappy=x[8],mSad=x[9])

# for file uploading

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename),'uploads/sample.wavd')
			slicer(os.path.join(app.config['UPLOAD_FOLDER'], "sample.wav"))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file type is mp3')
			return redirect(request.url)


@app.route('/results',methods=['POST'])
def results():

	# data = request.get_json(force=True)
	# prediction = model.predict([np.array(list(data.values()))])
	#
	# output = prediction[0]
	# return jsonify(output)
	return

@app.route('/download',methods=['POST'])
def download_file():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	# path = "simple.docx"
	#path = "sample.txt"
	filename = os.listdir('output')[0]
	filepath = os.path.join('output/', filename)

	return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
	app.run(debug=True)
