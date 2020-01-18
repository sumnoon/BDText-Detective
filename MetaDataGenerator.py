import os
from nGramHandler import *
from bnltk import *
import pickle
import re
from util import printProgressBar

def getMetaData(featureVector, n, text):
	data = []
	gramDictionary  = nGram(n, text)
	for feature in featureVector:
		if feature in gramDictionary.keys():
			data.append(gramDictionary[feature])
		else:
			data.append(0)
	#print(data)
	return data
#End of getnGramMetaData()

def getLables(featureSet):
	labels = []
	for featureList in featureSet:
		labels.extend(featureList)

	labels.append('meanWordLength')
	labels.append('meanSenetnceLength')
	labels.append('noOfWords')
	labels.append('noOfSentences')
	return labels
#End of getLables

def getFeatureValues(featureSet, text):
	featureValues = []
	#print(len(featureSet[0]),len(featureSet[1]),len(featureSet[2]),len(featureSet[3]),len(featureSet[4]),len(featureSet[5]))
	featureValues.extend(getMetaData(featureSet[0], 1, text))
	featureValues.extend(getMetaData(featureSet[1], 2, text))
	featureValues.extend(getMetaData(featureSet[2], 3, text))
	featureValues.extend(getMetaData(featureSet[3], 1, text))
	featureValues.extend(getMetaData(featureSet[4], 1, text))
	featureValues.extend(getMetaData(featureSet[5], 1, text))
	featureValues.extend(getMetaData(featureSet[6], 1, text))
	featureValues.extend(getMetaData(featureSet[7], 1, text))
	featureValues.extend(getMetaData(featureSet[8], 1, text))
	featureValues.extend(getMetaData(featureSet[9], 1, text))
	meanWordLength = 0
	meanSenetnceLength = 0
	noOfWords = 0
	noOfSentences = 0
	sentences = BanglaTokenizer.sentenceTokenize(text)
	sentences.pop()
	noOfSentences = len(sentences)
	#Last sentence is alwawys empty string
	for sentence in sentences:
		meanSenetnceLength += len(sentence)
		words = BanglaTokenizer.wordTokenize(sentence)
		noOfWords += len(words)
		for word in words:
			meanWordLength += len(word)

	#print('Total words:',noOfWords)
	#print('Total sentences:',noOfSentences)
	#if noOfWords == 0 :
	#	print(fileName)
	meanWordLength = meanWordLength/noOfWords
	meanSenetnceLength = meanSenetnceLength/noOfSentences

	featureValues.append(meanWordLength)
	featureValues.append(meanSenetnceLength)
	featureValues.append(noOfWords)
	featureValues.append(noOfSentences)
	return featureValues
#End of getFeatureValue()

def writeToFile(data, f, seperator):
	firstWord = True
	for value in data:
		if(not firstWord):
			f.write(seperator)
		f.write(str(value))
		firstWord = False
	f.write('\n')
#End of fileWriter

def loadFeatureSet(pathToFeatureSet):
	fr = open(pathToFeatureSet, 'rb')
	featureSet = pickle.load(fr)
	return featureSet
#End of loadFeatureSet()

def generateMetaData(pathToFeatureSet, fileName, saveDirectory, readDirectory = 'Data/Normalized Data'):
	#Generate label for meta data
	featureSet = loadFeatureSet(pathToFeatureSet)
	labels = getLables(featureSet)
	labels.append('AuthorName')
	#print(len(labels))
	fw = open(saveDirectory + '/' + fileName + '.tsv', 'w', encoding = 'UTF-8')
	writeToFile(labels, fw, '	')
	#For each of the Normalized Text get required feature value
	i, l = 0, 0
	authorList = os.listdir(readDirectory)
	for author in authorList:
		fileList = os.listdir(readDirectory + '/' + author)
		l += len(fileList)
	printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	for author in authorList:
		fileList = os.listdir(readDirectory + '/' + author)
		for fileName in fileList:
			fr = open(readDirectory + '/' + author + '/' + fileName, 'r', encoding = 'UTF-8')
			text = fr.read()
			#print('Author Name:', author, 'File Name:', fileName)
			featureValues = getFeatureValues(featureSet, text)
			featureValues.append(author)
			writeToFile(featureValues, fw, '	')
			printProgressBar(i+1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
			i += 1
#End of metaDataGenerator()

#generateMetaData('Data/feature set/feat_check.tsv', 'metadata_check.tsv', 'Data/Meta Data')
