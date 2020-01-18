import math
from termcolor import *
import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def uploadFile(filetype, titleText, initialDirectory):
    rootDirectory = os.path.dirname(os.path.abspath(__file__))
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filePath = askopenfilename(filetypes = filetype, title=titleText, initialdir=rootDirectory+'/'+initialDirectory) # show an "Open" dialog box and return the path to the selected file
    return filePath
#End of uploadFile()

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = colored('#', 'blue')):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()
#End of printProgressBar()

def clearCache():
	directoryList = os.listdir('Data/Normalized Data')
	for directory in directoryList:
		shutil.rmtree('Data/Normalized Data/' + directory)
	directoryList = os.listdir('Data/train')
	for directory in directoryList:
		shutil.rmtree('Data/train/' + directory)
	if os.path.exists('Data/Meta Data/normalizedTestText.txt'):
		os.remove('Data/Meta Data/normalizedTestText.txt')
#End of clearCache()

"""
Take feature columns and prediction columns as input and
returns information gain of the given feature column
"""
def calculateEntropy(distributionSet):
	entropy = 0
	total = sum(distributionSet)
	for element in distributionSet:
		p = element/total
		if(p):
			entropy -= p*math.log(p, 2)

	return entropy
#End of calculateEntropy()

def calculateIG(featureValues, predictionCalssValues):
	#Calculate initial entropy
	initialEntropy = 0
	predictionCalssNames = dict.fromkeys(set(predictionCalssValues), 0)
	distributionSet = []
	for name in predictionCalssNames.keys():
		predictionCalssNames[name] = predictionCalssValues.count(name)
		distributionSet.append(predictionCalssNames[name])

	initialEntropy = calculateEntropy(distributionSet)

	distinctFeatureValues = dict.fromkeys(set(featureValues), 0)
	for key in distinctFeatureValues.keys():
		distinctFeatureValues[key] = featureValues.count(key)

	finalEntropy = 0
	for key in distinctFeatureValues.keys():
		tempEntropy = 0
		distributionSet2 = []
		for name in predictionCalssNames.keys():
			cnt = 0
			for i in range(len(featureValues)):
				if(featureValues[i] == key and predictionCalssValues[i] == name):
					cnt += 1
			distributionSet2.append(cnt)
		p = distinctFeatureValues[key]/len(featureValues)
		finalEntropy += p*calculateEntropy(distributionSet2)
	#End of for key
	#print('Initial Entropy:',initialEntropy)
	#print('Final Entropy:',finalEntropy)
	#print('Information Gain:',abs(initialEntropy - finalEntropy))
	return abs(initialEntropy - finalEntropy)
#End of calculateIG()

"""
Take a data set, calculate information gain for each feature in the data set
and returns a dictionary of features which has information gain at list uqual to a threshold
along with its information gain value
"""
def getFeatureDictionaryWithMinIG(dataSet, thresholdIG):
	#print('\nShape of Dataset: ',dataSet.shape)
	featureColumnNames = list(dataSet.head(0))
	#Get last column name from featureColumnName
	predictionClasssName = featureColumnNames[-1]
	#Remove the last column from featureColumnNames as it is the predictionClasssName
	featureColumnNames.pop()
	#Get prediction class values in y
	y = dataSet[predictionClasssName].values
	#For every feature in featureColumnNames find Information gain
	featureDictionary = dict()
	# Initial call to print 0% progress
	l = len(featureColumnNames)
	printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	for i in range(len(featureColumnNames)):
		#print(i, 'th Feature Name:', featureColumnNames[i])
		featureDictionary[featureColumnNames[i]] = calculateIG(list(dataSet[featureColumnNames[i]].values), list(y))
		printProgressBar(i+1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	#Reduce featureDictionary with feature wich has minimum at least information gain equal to thresholdIG
	featureDictionary = {key:featureDictionary[key] for key in featureDictionary.keys() if featureDictionary[key]>=thresholdIG}

	return featureDictionary
#End of getFeatureListWithMinIG()


#print(calculateEntropy([9, 5]))
#print(calculateEntropy([4, 0]))
#print(calculateIG([1, 1, 2, 3, 3 ,3, 2, 1, 1, 3, 1, 2, 2, 3], ['No', 'No', 'Yes','Yes','Yes','No', 'Yes','No', 'Yes','Yes','Yes','Yes','Yes','No']))
