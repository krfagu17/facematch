from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import face_recognition
import io
import cv2
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

output=""

@app.route("/")
def start():
    return "The MBSA Server is Running"
@app.route('/api/face-match', methods=['POST'])
def face_match():
    try:
        image1data = request.files.get('image1')
        image2data = request.files.get('image2')
        

        # Check if image1 and image2 are present
        

        if image1data is None or image2data is None:
            print('image data no found')
            return jsonify({'error': 'Both image1 and image2 must be provided'}), 400

        # Now you can read the files
        image1_data = image1data.read()
        # print(image1_data)
        image2_data = image2data.read()
     
        nparr1 = np.frombuffer(image1_data, np.uint8)
        nparr2 = np.frombuffer(image2_data, np.uint8)

         # Decode the numpy arrays as images
        img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)

        
        # Load the images
        # image1 = face_recognition.load_image_file(img1[0])
        # image2 = face_recognition.load_image_file(img2[0])

        # Face encoding
        encoding1 = face_recognition.face_encodings(img1)[0]
        encoding2 = face_recognition.face_encodings(img2)[0]

        # Compare faces
        results = face_recognition.compare_faces([encoding1], encoding2)
        if results[0] == True:
            output = "matched"
        else:
            output = "not matched"
        similarity_score = output

        return jsonify({'result': similarity_score})

    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal server error'}), print("this is error:",e)
