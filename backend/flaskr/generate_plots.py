import flaskr.evaluation
import numpy as np
import jsonify
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from flask import jsonify

def generate_plot(catalog_name, dict_name):
    evaluation_dict = flaskr.evaluation.getEvaluationDict(catalog_name, dict_name)

    x1 = []
    x2 = []
    y1 = []
    y2 = []
    y3 = []

    nr_images = 2754
    purities = []

    # OPTION HERE!
    # Specify evaluation parameters
    evaluation_mode = 'completeness_vs_clicked'
    # classifier = 'Logistic Regression'
    # classifier = 'Decision Tree'
    classifier = 'Logistic Regression'
    # classifier = 'Multi Layer Perceptron'
    # uncertainty = 'Shannon Entropy'
    # uncertainty = 'Least Confidence'
    uncertainty = 'Shannon Entropy'

    offset = evaluation_dict[evaluation_mode][0][1]

    # active and passive learning curves
    for datapoint in evaluation_dict[evaluation_mode]:
        x1.append(datapoint[0])
        # active learning curve
        y1.append(datapoint[1])
        # passive learning curve
        y2.append(np.divide(datapoint[0], nr_images) + offset)

    if 'completeness_vs_clicked_rounds' in evaluation_dict:
        for datapoint in evaluation_dict[evaluation_mode + '_rounds']:
            x2.append(datapoint[0])
            y3.append(datapoint[1])

    for element in evaluation_dict['move_more_statistics']:
        purities.append(element['purity'])

    # scale x axes
    x1 = list(np.divide(x1, nr_images))
    x2 = list(np.divide(x2, nr_images))

    # compute area
    area_passive = np.multiply(np.multiply((1 - offset), (1 - offset)), 0.5)

    area_active_over = 0
    area_active_under = 0
    area_active_trapez = 0
    # for trapez dx
    x = x1
    y = y1
    dys = []
    # get dAs
    for i in range(0, len(y) - 1):
        area_active_over += np.multiply(y[i + 1] - y[i], x[i + 1])
        area_active_under += np.multiply(y[i + 1] - y[i], x[i])
        area_active_trapez += np.divide(np.multiply(y[i + 1] - y[i], x[i] + x[i + 1]), 2)
        dys.append(y[i + 1] - y[i])
    area_active = np.round(area_active_trapez, 3)
    if y[-1] < 0.99:
        area_active += np.inf
    savings = 1 - np.divide(area_active, area_passive)

    plt.style.use('ggplot')
    # plot
    f = plt.figure()

    # active learning curve
    # s=1 if scatter plot
    plt.plot(x1, y1, label='active learning')
    # passive learning curve
    # with clustering offset
    plt.plot(x1, y2, label='passive learning')
    # rounds
    plt.scatter(x2, y3, label='rounds')
    # set y-range
    plt.ylim(offset, 1.01)

    # label plot

    plt.title('Active vs. passive learning')
    plt.xlabel('Clicks / total images')
    plt.ylabel('Completeness')
    plt.legend()

    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)
    my_base64_jpgData = base64.b64encode(image.getvalue())
    return jsonify({'learning_curve': my_base64_jpgData.decode('utf-8')})
