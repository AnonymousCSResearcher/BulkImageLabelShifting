import flaskr.file_system
import flaskr.classification
import flaskr.evaluation
from os.path import isfile
import json
import shutil
from flask import Flask
import numpy as np
import time

app = Flask(__name__)
with app.app_context():
    time1 = time.time()
    print('start time:', time1)
    catalog_name = 'SFS'
    dict_name = 'cluster_sort_dict_SFS.json'
    version_dict = 'cluster_sort_dict_SFS_foldernames.json'

    # CLEAN FILES
    # load foldernames in sort dict
    version_file = "../catalogs/" + catalog_name + "/sort_dict/" + dict_name.replace('.json', '') + '/' + version_dict
    cache_file = "../catalogs/" + catalog_name + "/sort_dict/" + dict_name
    if isfile(version_file):
        shutil.copy(version_file, cache_file)
    # load candidates foldername in candidate dict
    version_file = "../catalogs/" + catalog_name + "/classification/candidates_cluster_sort_dict_SFS_foldernames.json"
    cache_file = "../catalogs/" + catalog_name + "/classification/candidates_cluster_sort_dict_SFS.json"
    if isfile(version_file):
        shutil.copy(version_file, cache_file)
    # delete evaluation dict
    empty_dict = {}
    with open("../catalogs/" + catalog_name + "/evaluation/cluster_sort_dict_SFS_evaluation.json", "w") as f:
        json.dump(empty_dict, f)

    print("Start evaluation...")


    def get_candidate_properties(candidate):
        file_name = candidate['file']
        candidate_index = candidate['idx']
        source_folder_key = candidate['curr_lab']
        destination_folder_key = candidate['act_lab']
        file_index = flaskr.file_system.getFileIndex(catalog_name, file_name, source_folder_key, dict_name)
        return file_name, candidate_index, source_folder_key, destination_folder_key, file_index


    # start rounds
    round = 0
    while flaskr.evaluation.calculate_completeness(catalog_name, dict_name) < 0.99:  # and round < 2:
        completeness = flaskr.evaluation.calculate_completeness(catalog_name, dict_name)
        print("Completeness: ", completeness)
        round += 1
        print("Starting round " + str(round))

        # save round marker data points
        flaskr.evaluation.save_round_marker(catalog_name, dict_name)

        # CLASSIFICATION
        print("Get labels from sort_dict and write to img_pkl")
        flaskr.classification.get_labels(catalog_name, dict_name)
        print("Classify images...")
        class_dict = flaskr.classification.classify_uncertainty(catalog_name, dict_name)

        # CANDIDATES
        print("Get classification dict")
        filename = "../catalogs/" + catalog_name + "/classification/candidates_" + dict_name
        if isfile(filename):
            with open(filename, "r") as f:
                candidates = json.load(f)

        # SORTING
        # shift images
        seen_candidates = []
        candidate_counter = 0
        for candidate in list(candidates['candidates']):

            candidate_counter += 1
            progress = np.round(np.multiply(np.divide(candidate_counter, len(candidates['candidates'])), 100), 2)
            print("Candidate progress: " + str(progress) + "%")
            # check if already seen
            if candidate not in seen_candidates:
                # look for other candidates for move more
                more_moved = False
                more_images_list = []
                for more_candidate in candidates['candidates']:
                    # check if both have same actual label
                    if more_candidate != candidate and more_candidate not in seen_candidates:
                        # check if actual label at same position in rest_labs for both
                        for i, lab in enumerate(candidate['pred_labs']):
                            if lab == candidate['act_lab']:
                                if candidate['pred_labs'][i] == more_candidate['pred_labs'][i]:

                                    # shift other move more candidate
                                    file_name, candidate_index, source_folder_key, destination_folder_key, file_index = get_candidate_properties(
                                        more_candidate)
                                    flaskr.file_system.shiftImage(catalog_name, source_folder_key, file_index,
                                                                  destination_folder_key,
                                                                  dict_name,
                                                                  candidate_index)
                                    # print("shift from " + source_folder_key + " to " + destination_folder_key)

                                    # click if not shifted to bulk destination folder (in rest labs)
                                    if more_candidate['act_lab'] != candidate['act_lab']:
                                        flaskr.evaluation.increment_click_counter(catalog_name, dict_name)
                                        # print("clack")
                                    # there are some candidates left for bulk shift
                                    else:
                                        more_moved = True

                                    more_images_list.append(more_candidate)

                                    # add to seen candidates
                                    seen_candidates.append(more_candidate)

                if more_moved:
                    # print("done bulk shift to " + candidate['act_lab'])
                    # one click for move more button
                    flaskr.evaluation.increment_click_counter(catalog_name, dict_name)
                    # print("cluck")
                    # evaluate move more
                    more_images_list.append(candidate)
                    # get destination folder key for purity evaluation
                    file_name, candidate_index, source_folder_key, destination_folder_key, file_index = get_candidate_properties(
                        candidate)
                    flaskr.evaluation.evaluate_more_move(catalog_name, dict_name, destination_folder_key,
                                                         more_images_list)

                # shift candidate
                file_name, candidate_index, source_folder_key, destination_folder_key, file_index = get_candidate_properties(
                    candidate)
                flaskr.file_system.shiftImage(catalog_name, source_folder_key, file_index, destination_folder_key,
                                              dict_name,
                                              candidate_index)
                # print("shift from " + source_folder_key + " to " + destination_folder_key)
                # print("not a bulk shift")
                # one click for move
                flaskr.evaluation.increment_click_counter(catalog_name, dict_name)
                # print("cleck")

                # add to seen candidates
                seen_candidates.append(candidate)

    # save round marker data points
    flaskr.evaluation.save_round_marker(catalog_name, dict_name)

    evaluation_dict = flaskr.evaluation.getEvaluationDict(catalog_name, dict_name)
    time2 = time.time()
    evaluation_dict['runtime'] = time2 - time1
    flaskr.evaluation.saveEvaluationDict(catalog_name,dict_name,evaluation_dict)
    print(time2 - time1)
print('end')
