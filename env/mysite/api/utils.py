import base64
import numpy as np
from PIL import Image
from io import BytesIO
from django.conf import settings
from tensorflow.keras.models import model_from_json,load_model
import logging
import os
# Configure logger
logger = logging.getLogger('mylogger')

def process_image(base64_image):
    try:
        model = load_model('C:/Users/huawei/Desktop/ปี  4  เทอม  1/Project/price_of_astrophytum_be/env/mysite/api/models/model4.h5')
        model.summary()
        if base64_image.startswith('data:image'):
            base64_image = base64_image.split(',')[1]
        image_data = base64.b64decode(base64_image)
        logger.info(f"image_data: {image_data}")
        try:
            image = Image.open(BytesIO(image_data)).convert('RGB')
        except Exception as e:
            logger.error(f"Error opening image: {e}")
            return []
        image = image.resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        predictions = model.predict(image)
        predicted_classes = np.argmax(predictions, axis=1)
        class_labels = ['normal', 'special']
        listpredicted = [class_labels[i] for i in predicted_classes]
        logger.info(f"listpredicted {listpredicted}", exc_info=True)
        if len(listpredicted) > 0:
            logger.info(f"listpredicted true", exc_info=True)
            if listpredicted[0] == "normal":
                logger.info(f"listpredicted normal", exc_info=True)
                return [1]
            elif(listpredicted[0] == "special"):
                logger.info(f"listpredicted special", exc_info=True)
                return [2]
        else :
            logger.info(f"listpredicted false", exc_info=True)
            return []

    except Exception as e:
        logger.error(f"Error processing image: {e}", exc_info=True)
        return []
