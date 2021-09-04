import flaskr.file_system
import flaskr.evaluation
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
import numpy as np
import math
import json
from flask import jsonify
import base64
from flaskr.setup import root
import pickle
from os.path import isfile


def get_labels(catalogname, dict_name):
    with open("catalogs/" + catalogname + "/img_pkl/img_files_" + catalogname + ".pkl", "rb") as f:
        files = pickle.load(f)
    with open("catalogs/" + catalogname + "/sort_dict/" + dict_name, "r") as f:
        sort_dict = json.load(f)

    labs_new = []

    for file in files:
        for item in sort_dict.items():
            for image in item[1]:
                if image == file:
                    labs_new.append(item[0])

                    # TODO save classification dict -> function

    with open("catalogs/" + catalogname + "/img_pkl/img_labs_" + catalogname + ".pkl", 'wb') as f:
        pickle.dump(labs_new, f)


def get_foldernames(catalog_name, dict_name):
    json_file = "catalogs/" + catalog_name + "/sort_dict/" + dict_name
    if isfile(json_file):
        with open(json_file, "r") as f:
            sort_dict = json.load(f)
            alphabetic_list = sorted(list(sort_dict.keys()))
        return alphabetic_list
    else:
        return None


def classify_uncertainty(catalogname, dict_name):
    print("Start...")
    # set classification algorithm

    # load pickle
    data, files, labs = flaskr.file_system.load_data_files_labs(catalogname)
    X = data
    Y = labs

    # fit model
    classifier = LogisticRegression(multi_class='multinomial', solver='lbfgs').fit(X, Y)
    # classifier = LogisticRegression().fit(X, Y)
    # predict labels and calculate uncertainty
    # predictions = classifier.predict(X)
    probabilities = list(classifier.predict_proba(X))
    classes = classifier.classes_

    # calculate completeness of sorting/classification
    completeness = 0
    # predicted labels
    predictions = list(classifier.predict(X))
    # actual labels
    # labels = []
    # for file in files:
    #    labels.append(get_manual_label_string(catalogname, file))
    # completeness
    # for idx in range(0, len(files)):
    #    if predictions[idx] == labels[idx]:
    #        completeness += 1
    # completeness = np.divide(completeness, len(files))

    # get candidates and uncertainty measures
    nr_candidates = 10 # for recommendations
    candidates = []
    distances = []
    entropies = []

    # each row in probabilities corresponds to one image
    for row in probabilities:

        # get predictions
        tmp_list = list(row)
        idx_list = [tmp_list.index(x) for x in sorted(tmp_list, reverse=True)]
        preds = []
        for idx in idx_list:
            preds.append(classes[idx])
        candidates.append(preds)

        # get distance 1st to 2nd (ranking measure 1)
        tmp_list = list(row)
        idx_list = [tmp_list.index(x) for x in sorted(tmp_list, reverse=True)[:2]]
        proxs = []
        for idx in idx_list:
            proxs.append(classes[idx])
        # distance from 1st to 2nd ranked predicted class
        distances.append(tmp_list[idx_list[0]] - tmp_list[idx_list[1]])

        # get entropy (ranking measure 2)
        entr = 0
        for prob in row:
            entr += np.multiply(prob, math.log(prob, 2))
        entropies.append(-entr)
    # plt.plot(entropies)
    # plt.ylabel('Entropy')
    # plt.xlabel('img_index')
    # plt.show()

    # calculate accuracy
    accuracy = cross_val_score(classifier, X, Y, cv=3)
    accuracy = np.mean(accuracy)
    # accuracy = cross_val_score(clf1, X1, Y1, cv=3)

    # create classification dictionary for response
    classification_dict = {}
    file_probs = []
    # iterate over image file
    for idx in range(0, len(files)):
        file_attr = {}

        file_attr['idx'] = idx
        file_attr['file'] = files[idx]
        file_attr['act_lab'] = flaskr.file_system.get_manual_label(catalogname, files[idx])
        file_attr['curr_lab'] = labs[idx]
        file_attr['pred_labs'] = candidates[idx][:nr_candidates]
        file_attr['rest_labs'] = sorted(
            list(set(get_foldernames(catalogname, dict_name)) - set(file_attr['pred_labs'])))
        file_attr['distance'] = distances[idx]
        file_attr['entropy'] = entropies[idx]

        with open(root + '/' + catalogname + '/unsorted/' + files[idx], "rb") as f:
            base64_bytes = base64.b64encode(f.read())
            base64_string = base64_bytes.decode('utf-8')
            file_attr['data'] = base64_string

        file_probs.append(file_attr)

    def get_distance(file_prob):
        return file_prob['distance']

    def get_entropy(file_prob):
        return file_prob['entropy']

    # rank image files by distance 1st to 2nd ranked predicted class (ranking measure 1)
    # file_probs.sort(key=get_distance, reverse=False)
    # rank image files by entropy (ranking measure 2)
    file_probs.sort(key=get_entropy, reverse=True)

    # check for already seen images and remove from candidates

    evaluation_dict = flaskr.evaluation.getEvaluationDict(catalogname, dict_name)
    if 'seenImages' in evaluation_dict:
        seen_images = evaluation_dict['seenImages']
    else:
        seen_images = []

    nr_shown_images = 250
    shown_candidates = []

    for image in file_probs:
        if len(shown_candidates) == nr_shown_images:
            break
        else:
            if image['file'] not in seen_images:
                shown_candidates.append(image)

    classification_dict['candidates'] = shown_candidates
    classification_dict['accuracy'] = np.round(accuracy, 2)
    # classification_dict['completeness'] = np.round(completeness, 2)

    # update learning curves
    if 'seenImages' in evaluation_dict:
        nr_seen_images = len(evaluation_dict['seenImages'])
    else:
        nr_seen_images = 0
    if 'shiftCounter' in evaluation_dict:
        nr_shifted_images = evaluation_dict['shiftCounter']
    else:
        nr_shifted_images = 0
    if 'clickCounter' in evaluation_dict:
        nr_clicks = evaluation_dict['clickCounter']
    else:
        nr_clicks = 0

    evaluation_dict = flaskr.file_system.append_element_to_dict_list(evaluation_dict, 'accuracy_vs_seen',
                                                                     [nr_seen_images, accuracy])
    evaluation_dict = flaskr.file_system.append_element_to_dict_list(evaluation_dict, 'accuracy_vs_shifted',
                                                                     [nr_shifted_images, accuracy])
    evaluation_dict = flaskr.file_system.append_element_to_dict_list(evaluation_dict, 'accuracy_vs_clicked',
                                                                     [nr_clicks, accuracy])

    # increase round number
    if 'round_number' in evaluation_dict:
        evaluation_dict['round_number'] = int(evaluation_dict['round_number']) + 1
    else:
        evaluation_dict['round_number'] = 1
    flaskr.evaluation.saveEvaluationDict(catalogname, dict_name, evaluation_dict)
    with open("catalogs/" + catalogname + "/classification/candidates_" + dict_name, "w") as f:
        json.dump(classification_dict, f)
    return jsonify(classification_dict)


def classify_comittee(catalogname, dict_name):
    print("Start...")
    # set classification algorithm

    print("Load pickle...")
    with open("catalogs/" + catalogname + "/img_pkl/img_data_" + catalogname + ".pkl", "rb") as f:
        data = pickle.load(f)
    with open("catalogs/" + catalogname + "/img_pkl/img_files_" + catalogname + ".pkl", "rb") as f:
        files = pickle.load(f)
    with open("catalogs/" + catalogname + "/img_pkl/img_labs_" + catalogname + ".pkl", "rb") as f:
        labs = pickle.load(f)

    X = data
    Y = labs

    # split with overlap
    # split_idx = int(np.divide(len(labs),2))
    # overlap = np.multiply(0.25, len(labs))
    # X1 = X[:split_idx+overlap]
    # X2 = X[split_idx-overlap+1:-1]
    # Y1 = Y[:split_idx+overlap]
    # Y2 = Y[split_idx-overlap+1:-1]

    # split with margin
    margin = int(np.multiply(0.01, len(labs)))
    X1 = X[margin:-1]
    X2 = X[0:-1 - margin]
    Y1 = Y[margin:-1]
    Y2 = Y[0:-1 - margin]

    clf1 = LogisticRegression().fit(X1, Y1)
    clf2 = LogisticRegression().fit(X2, Y2)

    preds1 = list(clf2.predict(X))
    preds2 = list(clf1.predict(X))

    disagreements = []

    for idx1, pred1 in enumerate(preds1):
        for idx2, pred2 in enumerate(preds2):
            if idx1 == idx2 and pred1 != pred2:
                disagreements.append(idx1)

    # prob1 = list(clf2.predict_proba(X1))
    # prob2 = list(clf1.predict_proba(X2))

    # fit model
    # classifier = LogisticRegression().fit(X,Y)
    # predict labels and calculate uncertainty
    # predictions = classifier.predict(X)
    # probabilities = list(classifier.predict_proba(X))
    # classes = classifier.classes_

    # get unique labs as class names
    # lookup = set()
    # unique_labs = [x for x in labs if x not in lookup and lookup.add(x) is None]

    # find neighbors and distances
    # neighbors = []
    # distances = []
    # for row in probabilities:
    #     tmp_list = list(row)
    #     idx_list = [tmp_list.index(x) for x in sorted(tmp_list, reverse=True)[:4]]
    #     proxs = []
    #     for idx in idx_list:
    #         proxs.append(classes[idx])
    #     neighbors.append(proxs)
    #     # distance from first to second ranked predicted class
    #     distances.append(tmp_list[idx_list[0]] - tmp_list[idx_list[1]])

    # calculate accuracy
    # accuracy = cross_val_score(classifier, X, Y, cv=3)
    # accuracy = cross_val_score(clf1, X1, Y1, cv=3)

    # create classification dictionary for response
    classification_dict = {}
    file_probs = []
    for idx in disagreements:
        file_attr = {}

        file_attr['idx'] = idx
        file_attr['file'] = files[idx]

        file_attr['curr_lab'] = labs[idx]
        file_attr['next_labs'] = [preds1[idx], preds2[idx]]
        file_attr['distance'] = "N/A"

        with open(root + '/' + catalogname + '/unsorted/' + files[idx], "rb") as f:
            base64_bytes = base64.b64encode(f.read())
            base64_string = base64_bytes.decode('utf-8')
            file_attr['data'] = base64_string

        file_probs.append(file_attr)

    def get_distance(file_prob):
        return file_prob['distance']

    file_probs.sort(key=get_distance, reverse=False)

    classification_dict['candidates'] = file_probs
    classification_dict['accuracy'] = "N/A"

    with open("catalogs/" + catalogname + "/classification/candidates_" + dict_name, "w") as f:
        json.dump(classification_dict, f)

    return jsonify(classification_dict)

# TODO evaluation file versioning
# TODO 1 json file pro version (candidates_dict,sort_dict,evaluation_dict)
