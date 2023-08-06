#About The Auto Optimizer Package

Machine Learning algorithm optimizer for sklearn.
AutoOptimizer provides tools to automatically optimize machine learning model for a dataset with very little user intervention.

It refers to techniques that allow semi-sophisticated machine learning practitioners and non-experts 
to discover a good predictive model pipeline for their machine learning algorithm task quickly,
with very little intervention other than providing a dataset.

#Prerequisites:
	jupyterlab(contains all sub packages except mlxtend) or:
	sklearn
	matplotlib
	mlxtend
	numpy

#Installation
	Github:
		https://github.com/mrb987/autooptimizer.git
	Install package:
		pip install autooptimizer

#Usage
scikit learn supervised and unsupervised learning models using python.
{DBSCAN, KMeans, MeanShift,  LogisticRegression, KNeighborsClassifier, SupportVectorClassifier, DecisionTree}
Support more models in future versions.

#Running:
>>from autooptimizer.dbscan import dbscan
>>from autooptimizer.kmeans import kmeans
>>from autooptimizer.meanshift import meanshift
>>from autooptimizer.logreg import logreg
>>from autooptimizer.knn import knn
>>from autooptimizer.svc import svc
>>from autooptimizer.decisiontree import decisiontree
>>dbscan(x)
>>kmeans(x)
>>meanshift(x)
>>logreg(x,y)
>>knn(x,y)
>>svc(x,y)
>>decisiontree(x,y)

'x' should be your independent variable or feature's values and 'y' is target variable or dependent variable.
The output of the program is the maximum possible accuracy with the appropriate parameters to use in model.


#Contact and Contributing
Please share your good ideas with us. 
Simply letting us know how we can improve the programm to serve you better.
Thanks for contributing with the programm.

>>>https://github.com/mrb987/autooptimizer
>>>info@genesiscube.ir