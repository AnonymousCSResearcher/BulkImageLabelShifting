# Accelerating Active Learning Image Labeling Through Bulk Shift Recommendations

We present a web-based active learning framework that helps to accelerate the labeling process. After manually labeling some images, the user gets recommendations of further candidates that could potentially be labeled equally (bulk image folder shift). We aim to explore the most efficient 'uncertainty' measure to improve the quality of the recommendations such that all images are sorted with a minimum number of user interactions (clicks).

## Evaluation and Results

We conducted experiments using a manually labeled reference dataset to evaluate different combinations of classifiers and uncertainty measures.

To demonstrate our approach, we plot the completeness (fraction of labeled instances in the dataset) vs. the number of clicks normalized by the total number of images.
Benefiting from an unsupervised pre-clustering, we already start with a completeness of 0.668. This means that 67% of the images were already grouped correctly by the unsupervised clustering. The user only has to label the cluster folders (which we do not count as click). Further, the positive effect of bulk moves (counted as a single click) are visible in the plot as vertical jumps.

As a measure for the performance, one could use the fraction of clicks needed to reach a completeness of 100%. However, this would not discriminate how this point is reached. Inspired by the ROC-analysis, we use the area under the learning curve AUC as a more complete measure for the performance. A perfect curve reaching 100% completeness with one click would have an AUC of 1.0. In contrast, an almost perfect curve reaching 99% with one click but needing many more clicks afterwards to finally reach 100% would also have an AUC close to 1.

![Completeness vs. clicks learning curves](https://user-images.githubusercontent.com/85504774/132089958-56b2e364-e44d-4ae0-977d-db6376402d26.png)

To get the (active vs. passive) learning curves, we employ an automated simulation of the process:
```
backend/flaskr/automated_evaluation.py
```
Using the image vectores stored in
```
dataset/img_data.pkl
```
to be extracted from
```
dataset/img_data.zip
```
the output is a respective
```
sort_dict.json
```
that can be used to generate the plots.

Having executed the simulation for different sampling settings (classifier uncertainty combinations), plot figures can be generated from the output data either starting with or without an offset (origin) at the completeness obtained by the pre-clustering.
The results can be reproduced by running
```
backend/flaskr/generate_plots.py
```
for a combined plot or
```
backend/flaskr/plot_evaluation/active_vs_passive(offset)_automated.py
```
or
```
backend/flaskr/plot_evaluation/active_vs_passive(origin)_automated.py
```
respectively.

Beforhand, image vectors need to be generated using a VGG16 network pretrained on the ImageNET dataset, and provided in Keras from
https://keras.io/api/applications/#vgg16
using
```
backend/flaskr/feature_vector.py
```

The pre-clustering can then be carried out via
```
backend/flaskr/clustering.py
```
**All data necessary to reproduce the results is provided in the 'dataset' folder.**
**If something is missing or does not work, please contact anonymousCSresearcher@outlook.com**

The following table summarizes the Area AUC under the active learning curves comparing different sampling strategies, which correlates with the click-savings of the process. The green/red cell color indicates minimum/maximum values.

![AUC area under the active learning curves](https://user-images.githubusercontent.com/85504774/132089680-73cfe223-a754-4c8a-a06d-bf35bb43677a.png)

The results reveal that the logistic regression classifier with either shannon entropy or least confidence as uncertainty measure are the most efficient combinations in terms of AUC (0.963) and also more efficient than the multi layer perceptron and the decision tree. Logistic regression with shannon entropy or least confidence are also the best combinations for reducing the number of clicks until reaching full completeness. Labeling approximately 22% of the image dataset is already sufficient to have all images sorted.

Comparing the runtimes of the classifiers (table below), one can see that the decision tree is by far the fastest algorithm on average, only taking half as long as the other classification models. Multi layer perceptron requires 61% more runtime compared to decision tree. Furthermore, margin sampling provides the highest average number of recommended bulk moves and a maximum mean purity of nearly 92%, whereas least confidence performs worst in both test-metrics.

![Runtime comparison of sampling strategies](https://user-images.githubusercontent.com/85504774/132089938-d314a97c-ffd2-4ba7-8afb-744befa2e7bf.png)

Overall, the results clearly show the effectiveness of an uncertainty sampling with bulk image shift recommendations (our novel method), which can reduce the number of required clicks to only around 20% compared to manual labeling.

The frontend can be installed as specified in
```
frontend/README.md
```
