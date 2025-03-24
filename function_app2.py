import logging
import binascii
import cv2
import numpy as np
from flask import Flask, request, Response

app = Flask(_name_)

@app.route('/create_thumbnail', methods=['POST'])
def create_thumbnail():
    try:
        # Get the image data from the request body
        image_data = request.get_data()
        if not image_data:
            return Response("No image provided", status=400)
        
        # Log first 32 bytes of the image data
        logging.info(f"Received image data (first 32 bytes): {binascii.hexlify(image_data[:32])}")

        # Decode into a numpy array
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            logging.error("cv2.imdecode failed to decode the image")
            return Response("Invalid image", status=400)

        # Log the shape of the image
        logging.info(f"Image shape: {image.shape}")

        # Resize the image to 100x100
        thumbnail = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)

        # Encode the resized image back to jpg
        _, encoded_image = cv2.imencode('.jpg', thumbnail)

        # Log first 32 bytes of the encoded image
        logging.info(f"Encoded image (first 32 bytes): {binascii.hexlify(encoded_image[:32])}")

        # Return as a binary response
        return Response(encoded_image.tobytes(), mimetype="image/jpeg")

    except Exception as e:
        logging.exception("Error during thumbnail creation:")
        return Response(f"Error: {str(e)}", status=500)


if _name_ == '_main_':
    # Important for Knative: listen on port 8080 and 0.0.0.0
    app.run(host='0.0.0.0', port=8080)
