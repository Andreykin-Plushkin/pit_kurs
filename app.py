import numpy as np 

import io
import base64
import json
from PIL import Image

from flask import Flask, jsonify, Response
from flask import render_template, request

from network import Network


app = Flask(__name__)


network = Network()



def convert_image(user_image):
	image_bytes = base64.b64decode(user_image)
	image = Image.open(io.BytesIO(image_bytes))

	image.save('received_image.png')

	image.close()

	img = Image.open('received_image.png')
	resized_img = img.resize((28, 28))

	return resized_img


@app.route('/')
def index_page():
	return render_template('index.html')

@app.route('/learning')
def learning_page():
	train_info, test_info = network.get_info_about_dataset()
	return render_template('learning.html', train_info=train_info, test_info=test_info)

@app.route('/predict')
def predict_page():
	return render_template('predict.html')

@app.route('/api/predict', methods=['POST'])
def predict():

	answer = ""
	result = ""

	if request.method == 'POST':

		image = convert_image(request.form["image"])
		pix_val = list(image.getdata())
		image.close()

		data = [i[0] for i in pix_val]
		data = np.reshape(data, [-1, 28 * 28]).astype('float32') / 255

		answer = network.predict(data)

	response = Response(
		response=json.dumps({'answer':answer}),
		status=200,
		mimetype='application/json'
	)

	return response

@app.route('/api/learn', methods=['POST'])
def learn():
	
	if request.method == 'POST':
		epochs = request.form['epochs']
		batch_size = request.form['batch_size']

	if epochs is None or batch_size is None or int(epochs) <= 0 or int(batch_size) <= 0:
		return "Error!"
	else:
		network.learn(int(epochs), int(batch_size))


	response = Response(
		response=json.dumps({'status':'done!'}),
		status=200,
		mimetype='application/json'
	)

	return response

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='5000', debug=True)