from keras.preprocessing import image

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

import numpy as np
from flaskr.setup import root
import pickle
import os
from flask import Response


def get_feature_vectors(catalogname):
    image_path = root + '/' + catalogname + '/unsorted'
    if len(os.listdir(image_path)) == 0:
        return Response("{'error':'no images in folder'}", 404)
    # load model
    else:
        model = VGG16(weights='imagenet', include_top=False)
        model.summary()
        # load dataset
        data = []
        files = []

        for file in os.listdir(image_path):
            print(file)
            if file.endswith(".jpg") or file.endswith(".png"):
                print(file)
                img = image.load_img(os.path.join(image_path, file), target_size=(224, 224))

                # preprocess image
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis=0)
                img = preprocess_input(img)

                # generate features
                features = model.predict(img)
                features = np.array(features).flatten()

                # append data and filename
                data.append(features)
                files.append(image_path + "/" + file)

        # convert to numpy array
        data = np.array(data)

    # save data and labels
    with open("catalogs/"+catalogname + "/img_data_" + catalogname + ".pkl", "wb") as f:
        pickle.dump(data, f)
    with open("catalogs/"+catalogname + "/img_files_" + catalogname + ".pkl", "wb") as f:
        pickle.dump(files, f)
    return Response("{'success':'feature vector created'}", 200)
