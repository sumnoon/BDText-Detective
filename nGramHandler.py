import os
from bnltk import *
from util import *
import pandas as pd
from termcolor import *

"""
	Returns a gramDictionary for a particualr text
"""
def nGram(n, text):
	dictionary = dict()
	sentences = BanglaTokenizer.sentenceTokenize(text)
	#Last sentence is alwawys empty string
	sentences.pop()
	#print('No of sentences:', len(sentences))
	for sentence in sentences:
		words = BanglaTokenizer.wordTokenize(sentence)
		#print(len(words))
		for i in range(len(words)-n+1):
			gram = words[i]
			for j in range(n-1):
				gram += ' ' + words[i+j+1]
			if gram in dictionary.keys():
				dictionary[gram] += 1
			else:
				dictionary[gram] = 1
	return dictionary
#End of nGram()

"""
Returns gram dictionary for a particualr directory
"""
def getGramDictionary(n, directory):
	directoryList = os.listdir(directory)
	gramDictionary = dict()
	totalAuthor, totalProcessedFile = len(directoryList), 0
	#Search for each of the author
	for author in directoryList:
		fileList = os.listdir(directory + '/' + author)
		totalProcessedFile += len(fileList)
		#Search for each of the particualr text of each of the author
		for fileName in fileList:
			fr = open(directory + '/' + author + '/' + fileName, 'r', encoding = 'UTF-8')
			#print('Author:', author, 'File Name:', fileName)
			dictionary = nGram(n, fr.read())
			#Marge each file's dictionary for same author to authorDictionary
			for key in dictionary.keys():
				if key in gramDictionary.keys():
					gramDictionary[key] = max(gramDictionary[key], dictionary[key])
				else:
					gramDictionary[key] = dictionary[key]

	#print('Total no. of author:', totalAuthor)
	#print('Total no. of processed file:', totalProcessedFile)
	return gramDictionary
#End getGram()

"""Selects n-gram with a minimum frequency of minFrequency"""
def getnGramListWithMinFrequency(gramDictionary, minFrequency):
	reducedGramDictionary = dict((key, value) for key, value in gramDictionary.items() if value>=minFrequency)
	return list(reducedGramDictionary.keys())
#End of func()

def getGramFeature(gramList, gramDictionary):
	fileData = []
	for gram in gramList:
		if gram in gramDictionary.keys():
			fileData.append(gramDictionary[gram])
		else:
			fileData.append(0)
	return fileData
#End of getGramFeature()

"""
Take a gram-list as input and returns gram-list with information gain more than or eaual to thresholdIG
"""
def getGramListWithMinIG(n, minFrequency, thresholdIG):
	gramDictionary = getGramDictionary(n, 'Data/Normalized Data')
	print('Total no. of gram:', colored(len(gramDictionary), 'red'))
	gramList = getnGramListWithMinFrequency(gramDictionary, minFrequency)
	print('Total no. of gram after reducing by frequency:', colored(len(gramList), 'cyan'))
	labels = [gram for gram in gramList]
	labels.append('AuthorName')
	temporaryData = []
	authorList = os.listdir('Data/Normalized Data')
	for author in authorList:
		fileList = os.listdir('Data/Normalized Data/' + author)
		#print(author+' has',len(fileList),'files.')
		for fileName in fileList:
			fr = open('Data/Normalized Data/' + author + '/' + fileName, 'r', encoding = 'UTF-8')
			gramDictionary = nGram(n, fr.read())
			fileData = getGramFeature(gramList, gramDictionary)
			fileData.append(author)
			temporaryData.append(fileData)
		#End for fileName
	#End for author

	dataSet = pd.DataFrame.from_records(temporaryData, columns = labels)
	return getFeatureDictionaryWithMinIG(dataSet, thresholdIG)
#End of getGramListWithMinIG()
