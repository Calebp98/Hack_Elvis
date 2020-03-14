import os
import numpy as np
from flask import Flask, request, jsonify, render_template, flash,redirect
import pickle
from werkzeug.utils import secure_filename
import pandas as pd
import librosa
import glob
import numpy as np
import keras


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)

# for file uploding stuff
app.secret_key = "78929"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# model = pickle.load(open('model.pkl', 'rb'))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def predictEmotion():

    loaded_model = keras.models.load_model('saved_models/Emotion_Voice_Detection_Model.h5')

    # code for tf model
    data, sampling_rate = librosa.load('uploads/sample.mp3')

    X, sample_rate = librosa.load('uploads/sample.mp3', res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
    featurelive = mfccs
    livedf2 = featurelive
    livedf2= pd.DataFrame(data=livedf2)
    twodimNew = livedf2.values
    twodimNew =np.expand_dims(twodimNew, axis=0)
    livepreds = loaded_model.predict(twodimNew, batch_size=32, verbose=1)

    return livepreds

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    result = predictEmotion()
    x = result[0]

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
			os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename),'uploads/sample.mp3')
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

if __name__ == "__main__":
    app.run(debug=True)
