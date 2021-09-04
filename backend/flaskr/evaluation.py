import flaskr.file_system
import json, jsonify
import numpy as np
from flask import jsonify
from os.path import isfile


def getEvaluationDict(catalog_name, dict_name):
    json_file = "catalogs/" + catalog_name + "/evaluation/" + dict_name.strip(".json") + "_evaluation.json"
    if isfile(json_file):
        with open(json_file, "r") as f:
            evaluation_dict = json.load(f)
    else:
        evaluation_dict = {}

    return evaluation_dict


def saveEvaluationDict(catalog_name, dict_name, evaluation_dict):
    json_file = "catalogs/" + catalog_name + "/evaluation/" + dict_name.strip(".json") + "_evaluation.json"
    with open(json_file, "w") as f:
        json.dump(evaluation_dict, f)


def saveSeenImages(catalog_name, dict_name, image_filename, shifted):
    evaluation_dict = getEvaluationDict(catalog_name, dict_name)

    # add to seen images
    if 'seenImages' in evaluation_dict:
        evaluation_dict['seenImages'].append(image_filename)
    else:
        evaluation_dict['seenImages'] = []
        evaluation_dict['seenImages'].append(image_filename)

    # update shift counter
    try:
        shiftCounter = int(evaluation_dict['shiftCounter'])
    except:
        shiftCounter = 0
    if shifted:
        shiftCounter += 1
    evaluation_dict['shiftCounter'] = shiftCounter

    saveEvaluationDict(catalog_name, dict_name, evaluation_dict)


def get_round_number(catalog_name, dict_name):
    evaluation_dict = getEvaluationDict(catalog_name, dict_name)
    if 'round_number' in evaluation_dict:
        round_number = evaluation_dict['round_number']
    else:
        round_number = 0

    return jsonify({'round_number': round_number})


def calculate_completeness(catalog_name, dict_name):
    manual_dict = flaskr.file_system.loadManualSorting(catalog_name)
    sort_dict = flaskr.file_system.loadSortDict(catalog_name, dict_name)
    completeness = 0
    total = 0
    for category in sort_dict.keys():
        total += len(sort_dict[category])
        # get number of matching images in current and manual sorting
        completeness += len(set(manual_dict[category]).intersection(set(sort_dict[category])))

    completeness = np.divide(completeness, total)
    return completeness


def update_completeness_statistics(catalog_name, dict_name):
    completeness = calculate_completeness(catalog_name, dict_name)

    # save statistics to evaluation dict
    evaluation_dict = getEvaluationDict(catalog_name, dict_name)

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

    evaluation_dict = flaskr.file_system.append_element_to_dict_list(evaluation_dict, 'completeness_vs_seen',
                                                                     [nr_seen_images, completeness])
    evaluation_dict = flaskr.file_system.append_element_to_dict_list(evaluation_dict, 'completeness_vs_shifted',
                                                                     [nr_shifted_images, completeness])
    evaluation_dict = flaskr.file_system.append_element_to_dict_list(evaluation_dict, 'completeness_vs_clicked',
                                                                     [nr_clicks, completeness])
    saveEvaluationDict(catalog_name, dict_name, evaluation_dict)


def get_completeness(catalog_name, dict_name):
    completeness = calculate_completeness(catalog_name, dict_name)

    return jsonify({'completeness': np.round(completeness, 3)})


def evaluate_more_move(catalog_name, dict_name, destination_folder_key, more_images_list):
    # count correct move more recommendations and purity
    counter = 0
    for image in more_images_list:
        if image['act_lab'] == destination_folder_key:
            counter += 1

    move_more_statistics = {}
    move_more_statistics['correct'] = counter
    move_more_statistics['purity'] = np.divide(counter, len(more_images_list))

    # save to evaluation dict
    evaluation_dict = getEvaluationDict(catalog_name, dict_name)
    if 'move_more_statistics' in evaluation_dict:
        evaluation_dict['move_more_statistics'].append(move_more_statistics)
    else:
        evaluation_dict['move_more_statistics'] = []
        evaluation_dict['move_more_statistics'].append(move_more_statistics)

    saveEvaluationDict(catalog_name, dict_name, evaluation_dict)
    return jsonify({'success': 'successfully requested'})


def increment_click_counter(catlog_name, dict_name):
    evaluation_dict = getEvaluationDict(catlog_name, dict_name)
    # update click counter
    if 'clickCounter' in evaluation_dict:
        clickCounter = int(evaluation_dict['clickCounter'])
        clickCounter += 1
    else:
        clickCounter = 1
    evaluation_dict['clickCounter'] = clickCounter
    saveEvaluationDict(catlog_name, dict_name, evaluation_dict)
    return jsonify({'success': 'click counter incremented'})
