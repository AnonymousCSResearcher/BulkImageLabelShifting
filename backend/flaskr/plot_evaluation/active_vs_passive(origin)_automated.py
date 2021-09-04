import json
import numpy as np
from scipy.integrate import simps
from matplotlib import pyplot as plt

json_file = '/Users/chilap/BMT/image-sorting-middleware/catalogs/SFS/evaluation/cluster_sort_dict_SFS_evaluation.json'
with open(json_file, "r") as f:
    evaluation_dict = json.load(f)

x1 = []
y1 = []
x2 = []
y2 = []

nr_images = 2754
purities = []

# OPTION HERE!
# Specify evaluation parameters
evaluation_mode = 'completeness_vs_clicked'
# classifier = 'Logistic Regression'
# classifier = 'Decision Tree'
# classifier = 'Logistic Regression'
classifier = 'Multi Layer Perceptron'
uncertainty = 'Shannon Entropy'
# uncertainty = 'Least Confidence'
# uncertainty = 'Margin Sampling'

for datapoint in evaluation_dict[evaluation_mode]:
    x1.append(datapoint[0])
    y1.append(datapoint[1])

    # round markers

if 'completeness_vs_clicked_rounds' in evaluation_dict:
    for datapoint in evaluation_dict[evaluation_mode + '_rounds']:
        x2.append(datapoint[0])
        y2.append(datapoint[1])

# calculate mean purity
for element in evaluation_dict['move_more_statistics']:
    purities.append(element['purity'])

mean_purity = round(np.average(purities) * 100, 2)

# scale x axes
x1 = list(np.divide(x1, nr_images))
x2 = list(np.divide(x2, nr_images))

# compute area
area_passive = 0.5
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

# extend x range
extension = x[-1]
while extension < 1:
    extension += 0.001
    x.append(extension)
    y.append(y[-1])

# plot
plt.style.use('ggplot')
f = plt.figure()

# active learning curve
# s=1 if scatter plot
plt.plot(x, y, label='active learning')
# passive learning curve
# without clustering offset
plt.plot(x, x, label='passive learning')
# rounds
plt.scatter(x2, y2, label='rounds')

# label plot
plt.title('Active vs. passive learning')
plt.xlabel('Clicks / total images')
plt.ylabel('Completeness')
plt.legend()

# area text
# set label coordinates
if classifier == 'Logistic Regression' and uncertainty == 'Shannon Entropy':
    x_active, y_active = [-0.01, 0.95]
    x_passive, y_passive = [0.2, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Logistic Regression' and uncertainty == 'Margin Sampling':
    x_active, y_active = [-0.01, 0.95]
    x_passive, y_passive = [0.2, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Logistic Regression' and uncertainty == 'Least Confidence':
    x_active, y_active = [-0.01, 0.95]
    x_passive, y_passive = [0.2, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Multi Layer Perceptron' and uncertainty == 'Shannon Entropy':
    x_active, y_active = [-0.01, 0.95]
    x_passive, y_passive = [0.2, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Multi Layer Perceptron' and uncertainty == 'Margin Sampling':
    x_active, y_active = [0.1, 0.95]
    x_passive, y_passive = [0.4, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Multi Layer Perceptron' and uncertainty == 'Least Confidence':
    x_active, y_active = [-0.01, 0.95]
    x_passive, y_passive = [0.2, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Decision Tree' and uncertainty == 'Least Confidence':
    x_active, y_active = [0.3, 0.95]
    x_passive, y_passive = [0.4, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Decision Tree' and uncertainty == 'Shannon Entropy':
    x_active, y_active = [0.1, 0.95]
    x_passive, y_passive = [0.3, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]

if classifier == 'Decision Tree' and uncertainty == 'Margin Sampling':
    x_active, y_active = [0.1, 0.95]
    x_passive, y_passive = [0.3, 0.7]
    x_savings, y_savings = [0, 0.4]
    x_classifier, y_classifier = [0.5, 0.40]
    x_uncertainty, y_uncertainty = [0.5, 0.33]
    x_movemorepurity, y_movemorepurity = [0.6, 0.50]
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
f.savefig('tuning/active_vs_passive(origin)_' + classifier + '_' + uncertainty + '.pdf')

print("end")
