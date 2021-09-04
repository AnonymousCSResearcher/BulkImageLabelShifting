import json
import numpy as np
from matplotlib import pyplot as plt

json_file = '/Users/chilap/BMT/image-sorting-middleware/catalogs/SFS/evaluation/cluster_sort_dict_SFS_evaluation.json'
with open(json_file, "r") as f:
    evaluation_dict = json.load(f)

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
#classifier = 'Multi Layer Perceptron'
#uncertainty = 'Shannon Entropy'
# uncertainty = 'Least Confidence'
uncertainty = 'Margin Sampling'

offset = evaluation_dict[evaluation_mode][0][1]

# active and passive learning curves
for datapoint in evaluation_dict[evaluation_mode]:
    x1.append(datapoint[0])
    # active learning curve
    y1.append(datapoint[1])
    # passive learning curve
    y2.append(np.divide(datapoint[0], nr_images) + offset)

# round markers
for datapoint in evaluation_dict[evaluation_mode + '_rounds']:
    x2.append(datapoint[0])
    y3.append(datapoint[1])

for element in evaluation_dict['move_more_statistics']:
    purities.append(element['purity'])

mean_purity = round(np.average(purities) * 100, 2)

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

# over and under sum
# print(area_active_over)
# print(area_active_under)
# print(area_active_trapez)

area_active = np.round(area_active_trapez, 3)
if y[-1] < 0.99:
    area_active += np.inf
savings = 1 - np.divide(area_active, area_passive)
print('active: ', area_active)
print('passive: ', area_passive)
print('savings: ', savings)

# trapezoidal sum
# area_active_trapez = np.trapz(y, dx=float(np.mean(dys)))
# print(area_active_trapez)

# simpson's rule
# area_active_simpson = simps(y, dx=float(np.mean(dys)))
# print(area_active_simpson)
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

# set label coordinates
if classifier == 'Logistic Regression' and uncertainty == 'Shannon Entropy':
    x_active, y_active = [0.1, 0.975]
    x_passive, y_passive = [0.17, 0.9]
    x_savings, y_savings = [0, 0.8]
    x_classifier, y_classifier = [0.1, 0.72]
    x_uncertainty, y_uncertainty = [0.1, 0.70]
    x_movemorepurity, y_movemorepurity = [0.13, 0.75]

if classifier == 'Logistic Regression' and uncertainty == 'Margin Sampling':
    x_active, y_active = [0.27, 0.85]
    x_passive, y_passive = [0.15, 0.93]
    x_savings, y_savings = [0, 0.8]
    x_classifier, y_classifier = [0.1, 0.72]
    x_uncertainty, y_uncertainty = [0.1, 0.70]
    x_movemorepurity, y_movemorepurity = [0.15, 0.75]

if classifier == 'Logistic Regression' and uncertainty == 'Least Confidence':
    x_active, y_active = [0.1, 0.975]
    x_passive, y_passive = [0.17, 0.9]
    x_savings, y_savings = [0, 0.8]
    x_classifier, y_classifier = [0.1, 0.72]
    x_uncertainty, y_uncertainty = [0.1, 0.70]
    x_movemorepurity, y_movemorepurity = [0.13, 0.75]
# set label coordinates
if classifier == 'Multi Layer Perceptron' and uncertainty == 'Shannon Entropy':
    x_active, y_active = [0.1, 0.9]
    x_passive, y_passive = [0.22, 0.94]
    x_savings, y_savings = [0, 0.8]
    x_classifier, y_classifier = [0.1, 0.72]
    x_uncertainty, y_uncertainty = [0.1, 0.70]
    x_movemorepurity, y_movemorepurity = [0.15, 0.75]

if classifier == 'Multi Layer Perceptron' and uncertainty == 'Margin Sampling':
    x_active, y_active = [0.278, 0.939]
    x_passive, y_passive = [0.15, 0.95]
    x_savings, y_savings = [0, 0.8]
    x_classifier, y_classifier = [0.1, 0.72]
    x_uncertainty, y_uncertainty = [0.1, 0.70]
    x_movemorepurity, y_movemorepurity = [0.15, 0.75]

if classifier == 'Multi Layer Perceptron' and uncertainty == 'Least Confidence':
    x_active, y_active = [0.13, 0.95]
    x_passive, y_passive = [0.25, 0.9]
    x_savings, y_savings = [0, 0.8]
    x_classifier, y_classifier = [0.1, 0.72]
    x_uncertainty, y_uncertainty = [0.1, 0.70]
    x_movemorepurity, y_movemorepurity = [0.15, 0.75]

if classifier == 'Decision Tree' and uncertainty == 'Least Confidence':
    x_active, y_active = [0.25, 0.9]
    x_passive, y_passive = [0.18, 0.98]
    x_savings, y_savings = [0, 0.85]
    x_classifier, y_classifier = [0.2, 0.72]
    x_uncertainty, y_uncertainty = [0.2, 0.70]
    x_movemorepurity, y_movemorepurity = [0.2, 0.75]

if classifier == 'Decision Tree' and uncertainty == 'Shannon Entropy':
    x_active, y_active = [0.33, 0.98]
    x_passive, y_passive = [0.15, 0.92]
    x_savings, y_savings = [0, 0.85]
    x_classifier, y_classifier = [0.2, 0.72]
    x_uncertainty, y_uncertainty = [0.2, 0.70]
    x_movemorepurity, y_movemorepurity = [0.2, 0.75]

if classifier == 'Decision Tree' and uncertainty == 'Margin Sampling':
    x_active, y_active = [0.32, 0.98]
    x_passive, y_passive = [0.15, 0.92]
    x_savings, y_savings = [0, 0.85]
    x_classifier, y_classifier = [0.2, 0.72]
    x_uncertainty, y_uncertainty = [0.2, 0.70]
    x_movemorepurity, y_movemorepurity = [0.2, 0.75]
# colors as legends
if area_active != -np.inf:
    plt.text(x_active, y_active, 'area = ' + str(np.round(area_active, 3)), color='#d2553e')
    plt.text(x_passive, y_passive, 'area = ' + str(np.round(area_passive, 3)), color='#3977AF')
    plt.text(x_savings, y_savings, 'savings = ' + str(np.round(np.multiply(savings, 100), 2)) + "%", color='darkgreen')
plt.text(x_classifier, y_classifier, 'classifier= ' + classifier, color='grey')
plt.text(x_uncertainty, y_uncertainty, 'uncertainty= ' + uncertainty, color='#e3aa02')
plt.text(x_movemorepurity, y_movemorepurity, 'move more purity= ' + str(mean_purity) + '%', color='purple')

# show and save
plt.show()
f.savefig('tuning/active_vs_passive(offset)_' + classifier + '_' + uncertainty + '.pdf')

print("end")
