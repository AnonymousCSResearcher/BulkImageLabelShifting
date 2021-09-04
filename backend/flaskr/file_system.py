from flaskr.evaluation import saveSeenImages, update_completeness_statistics
import json
import base64
from flask import jsonify
from flaskr.setup import root
from os.path import isdir
from os import listdir
from os.path import isfile, join
from flask import Response
import pickle
import time
import shutil


##############  FILEPATH    ###############
def get_file_paths():
    directory_arr = []
    dir_path = root
    directory = listdir(dir_path)
    for f in directory:
        if not f.startswith('.'):
            data = {}
            data['catalog_name'] = f
            data['path'] = dir_path + '/' + f
            directory_arr.append(data)
    return jsonify({'path_array': directory_arr})


def get_file_path(path):
    dir_path = root
    directory = listdir(dir_path)
    for f in directory:
        print(path, f)
        if not f.startswith('.') and path == f:
            print(path, f)
    return jsonify({'pathName': path, 'path': dir_path + '/' + path})


##############  DICTIONARY    ###############
# load sorting dictionary
def loadSortDict(catalog_name, dict_name):
    json_file = "catalogs/" + catalog_name + "/sort_dict/" + dict_name
    if isfile(json_file):

        with open(json_file, "r") as f:
            sort_dict = json.load(f)
        return sort_dict
    else:
        return Response("{'error': 'no files found'}", 404)


def get_all_sortdict(catalog_name):
    sort_dict = "catalogs/" + catalog_name + '/sort_dict/'
    sort_dict_list = [f for f in listdir(sort_dict) if isfile(join(sort_dict, f))]
    return jsonify({"sort_dict": sort_dict_list})


##############  TIMESTAMP    ###############
# save the sorting dictionary
def saveSortDict(sort_dict, catalog_name, dict_name):
    json_file = "catalogs/" + catalog_name + "/sort_dict/" + dict_name
    with open(json_file, "w") as f:
        json.dump(sort_dict, f)


# save dictionary version from cache
def saveDictVers(catalog_name, dict_name, round):
    dict_name = dict_name.replace('.json', '')
    timestr = time.strftime("%Y%m%d-%H%M%S")

    json_file = "catalogs/" + catalog_name + "/sort_dict/" + dict_name + '.json'
    saved_file = "catalogs/" + catalog_name + "/sort_dict/" + dict_name.replace('.json',
                                                                                '') + '/' + dict_name + '_' + str(
        timestr) + 'round_' + round + ".json"
    if isfile(json_file):
        shutil.copy(json_file, saved_file)
        return jsonify({'success': 'saved dictionary as: ' + dict_name + "_" + str(
            timestr) + ".json"})
    else:
        return Response("{'error': 'Error while saving dict}", 400)


# load dictionary version in cache
def loadDictVers(catalog_name, version_dict, cache_dict):
    version_file = "catalogs/" + catalog_name + "/sort_dict/" + cache_dict.replace('.json', '') + '/' + version_dict
    cache_file = "catalogs/" + catalog_name + "/sort_dict/" + cache_dict
    if isfile(version_file):
        shutil.copy(version_file, cache_file)
        return jsonify({'success': 'saved dictionary as: ' + cache_file})
    else:
        return Response("{'error': 'Error while saving dict}", 400)


# get all timestamped dictionaries
def getTmpDicts(catalog_name, dict_name):
    sort_dict = "catalogs/" + catalog_name + '/sort_dict/' + dict_name.replace('.json', '')
    timeStamp = listdir(sort_dict)
    return jsonify({"timeStamp": timeStamp})


##############  FOLDER    ###############
# get folder names of version dictionary
def getFolderNamesOfDict(catalog_name, version_dict, cache_dict):
    json_file = "catalogs/" + catalog_name + "/sort_dict/" + cache_dict.replace('.json', '') + '/' + version_dict
    if isfile(json_file):
        with open(json_file, "r") as f:
            sort_dict = json.load(f)
            alphabetic_list = sorted(list(sort_dict.keys()))
        return jsonify({'folderNames': alphabetic_list})
    else:
        return Response("{'error': 'File not found'}", 404)


# get folder names of cached catalog
def getFolderNames(catalog_name, dict_name):
    json_file = "catalogs/" + catalog_name + "/sort_dict/" + dict_name
    if isfile(json_file):
        with open(json_file, "r") as f:
            sort_dict = json.load(f)
            alphabetic_list = sorted(list(sort_dict.keys()))
        return jsonify({'folderNames': alphabetic_list})
    else:
        return Response("{'error': 'File not found'}", 404)


# create a folder
def createFolder(catalog_name, folder_key, dict_name):
    sort_dict = loadSortDict(catalog_name, dict_name)
    sort_dict[folder_key] = []
    saveSortDict(sort_dict, catalog_name, dict_name)

    return jsonify({'success': 'created folder ' + folder_key})


# delete a folder
def deleteFolder(catalog_name, folder_key, dict_name):
    sort_dict = loadSortDict(catalog_name, dict_name)

    # delete only if empty
    if len(sort_dict[folder_key]) == 0:
        del sort_dict[folder_key]
        saveSortDict(sort_dict, catalog_name, dict_name)
        return jsonify({'success': 'deleted folder ' + folder_key})
    else:
        return Response({'folder contains images'}, 400)


# renames a folder
def renameFolder(catalog_name, old_folder_key, new_folder_key, dict_name):
    sort_dict = loadSortDict(catalog_name, dict_name)

    if new_folder_key not in sort_dict:
        sort_dict[new_folder_key] = sort_dict.pop(old_folder_key)

    else:
        sort_dict[new_folder_key].extend(sort_dict.pop(old_folder_key))

    saveSortDict(sort_dict, catalog_name, dict_name)

    return jsonify({'success': 'renamed from ' + old_folder_key + ' to ' + new_folder_key})


##############  IMAGES    ###############

# get all folders and its content of a catalog
def getFolderImages(catalog_name, folder_key, dict_name):
    json_file = "catalogs/" + catalog_name + '/sort_dict/' + dict_name

    if isfile(json_file):
        with open(json_file, "r") as f:
            sort_dict = json.load(f)

        images = {}
        img_files = sort_dict[folder_key]
        img_data = []
        for img in img_files:
            # second: base64 encode read data
            # result: bytes (again)
            with open(root + '/' + catalog_name + '/unsorted/' + img, "rb") as f:
                # second: base64 encode read data
                # result: bytes (again)
                base64_bytes = base64.b64encode(f.read())
                # third: decode these bytes to text
                # result: string (in utf-8)
                base64_string = base64_bytes.decode('utf-8')
                img_data.append(base64_string)

        images["files"] = img_files
        images["data"] = img_data
        return jsonify(images)

    else:
        return Response("{'error': 'no dictionary created'}", 404)


# get all folders and its content of a catalog
def getUnsortedImages(catalog_name):
    path = root + '/' + catalog_name + '/unsorted'
    if isdir(path):

        images = {}
        img_files = listdir(path)
        img_data = []

        for img in img_files:
            # second: base64 encode read data
            # result: bytes (again)
            with open(root + '/' + catalog_name + '/unsorted/' + img, "rb") as f:
                # second: base64 encode read data
                # result: bytes (again)
                base64_bytes = base64.b64encode(f.read())
                # third: decode these bytes to text
                # result: string (in utf-8)
                base64_string = base64_bytes.decode('utf-8')
                img_data.append(base64_string)

        images["files"] = img_files
        images["data"] = img_data

        return jsonify(images)

    else:
        return Response("{'error': 'no files found'}", 404)


# moves an image from source folder to a destination folder

def shiftImage(catalog_name, source_folder_key, source_file_index, destination_folder_key, dict_name, candidateIndex):
    if candidateIndex != 'undefined':
        filename = "catalogs/" + catalog_name + "/classification/candidates_" + dict_name
        # load dict
        with open(filename, "r") as f:
            classification_dict = json.load(f)

        for idx, candidate in enumerate(classification_dict['candidates']):
            if candidate['idx'] == int(candidateIndex):
                del classification_dict['candidates'][idx]

        # del classification_dict['candidates'][int(classificationIndex)]

        # save candidates dict
        with open(filename, "w") as f:
            json.dump(classification_dict, f)

        #       # get images filename
        source_file_index = int(source_file_index)
        sort_dict = loadSortDict(catalog_name, dict_name)
        image_filename = sort_dict[source_folder_key][source_file_index]

        # shift in sort dict
        shifted = False
        if source_folder_key != destination_folder_key:
            sort_dict[destination_folder_key].append(image_filename)
            del sort_dict[source_folder_key][source_file_index]

            saveSortDict(sort_dict, catalog_name, dict_name)

            update_completeness_statistics(catalog_name, dict_name)

            shifted = True  # for saveSeenImages

        # add images to seen images list
        saveSeenImages(catalog_name, dict_name, image_filename, shifted)

        return jsonify(classification_dict)

    else:
        source_file_index = int(source_file_index)
        sort_dict = loadSortDict(catalog_name, dict_name)

        sort_dict[destination_folder_key].append(sort_dict[source_folder_key][source_file_index])
        del sort_dict[source_folder_key][source_file_index]
        saveSortDict(sort_dict, catalog_name, dict_name)
        return jsonify({
            'success': 'image from ' + catalog_name + ' moved from ' + source_folder_key + ' to ' + destination_folder_key})


def get_classification_dict(catalogname, dict_name):
    filename = "catalogs/" + catalogname + "/classification/candidates_" + dict_name
    if isfile(filename):
        with open(filename, "r") as f:
            results = json.load(f)
        return jsonify(results)
    else:
        return Response("{'error': 'file not found'}", 404)


def acceptImage(catalogname, idx, dict_name):
    filename = "catalogs/" + catalogname + "/classification/candidates_" + dict_name
    if isfile(filename):
        with open(filename, "r") as f:
            classification_dict = json.load(f)

        del classification_dict['candidates'][int(idx)]

        with open(filename, "w") as f:
            json.dump(classification_dict, f)

        image_filename = classification_dict['candidates'][int(idx)]['file']

        shifted = False

        saveSeenImages(catalogname, dict_name, image_filename, shifted)

        return jsonify(classification_dict)

    else:
        return Response("{'error': 'file not found'}", 404)


#########################################
def load_data_files_labs(catalogname):
    print("Load pickle...")
    with open("catalogs/" + catalogname + "/img_pkl/img_data_" + catalogname + ".pkl", "rb") as f:
        data = pickle.load(f)
    with open("catalogs/" + catalogname + "/img_pkl/img_files_" + catalogname + ".pkl", "rb") as f:
        files = pickle.load(f)
    with open("catalogs/" + catalogname + "/img_pkl/img_labs_" + catalogname + ".pkl", "rb") as f:
        labs = pickle.load(f)
    return data, files, labs


# get file index for filename from sort dict list
def getFileIndex(catalog_name, filename, folder_key, dict_name):
    sort_dict = loadSortDict(catalog_name, dict_name)
    for idx in range(0, len(sort_dict[folder_key])):
        if sort_dict[folder_key][idx] == filename:
            return jsonify({'index': idx})
    return Response({'no file found'}, 404)


# def getFileIndex(catalog_name, filename, folder_key, dict_name):
#     sort_dict = loadSortDict(catalog_name, dict_name)
#     for idx in range(0, len(sort_dict[folder_key])):
#         if sort_dict[folder_key][idx] == filename:
#             return idx

def loadManualSorting(catalog_name):
    json_file = "catalogs/" + catalog_name + "/sort_dict/cluster_sort_dict_" + catalog_name + "/manual_sort_dict_" + catalog_name + ".json"
    if isfile(json_file):
        with open(json_file, "r") as f:
            sort_dict = json.load(f)
    return sort_dict


def get_manual_label(catalog_name, filename):
    manual_dict = loadManualSorting(catalog_name)

    for label in manual_dict.items():
        for imagename in label[1]:
            if imagename == filename:
                return label[0]

    return None


def get_manual_label_string(catalog_name, filename):
    manual_dict = loadManualSorting(catalog_name)

    for label in manual_dict.items():
        for imagename in label[1]:
            if imagename == filename:
                return label[0]

    return 0


def append_element_to_dict_list(dict, key, element):
    if key in dict:
        dict[key].append(element)
    else:
        dict[key] = []
        dict[key].append(element)

    return dict

    # TODO CRUD round number
    # TODO Candidates per version
