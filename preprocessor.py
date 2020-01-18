import os
from bnltk import *

"""
   Normalize a given text by tokenizing the text and removing unnecssary punctuation marks and writing each sentence in a line and returns Normalized text along with total number of sentence, word and character count
"""
def normalize(text):
	sentences = BanglaTokenizer.sentenceTokenize(text)
	normalizedSentenceList = []
	wordCount, characterCount = 0, 0
	for sentence in sentences:
		words = BanglaTokenizer.wordTokenize(sentence)
		wordCount += len(words)
		normalizedSentence = ''
		for word in words:
			characterCount += len(word)
			normalizedSentence += word + ' '
		if(len(normalizedSentence)>0):
			normalizedSentenceList.append(normalizedSentence)
	return (normalizedSentenceList, len(normalizedSentenceList), wordCount, characterCount)
#End of normalize()

"""
Preprocess each text to create desired normal data
"""
def preprocess(readDirectory, writeDirectory):
	directoryList =os.listdir(readDirectory)
	for author in directoryList:
		#If write derectory does not exists create write derectory
		if not os.path.exists(writeDirectory+'/'+author):
			os.makedirs(writeDirectory+'/'+author)
		#List text found in the derectory
		fileList = os.listdir(readDirectory+'/'+author)
		sentenceCount, wordCount, characterCount = 0, 0, 0
		#Normalize each text and write it in write derectory
		for fileName in fileList:
			fr = open(readDirectory+'/'+author+'/'+fileName, 'r', encoding = 'UTF-8')
			fw = open(writeDirectory+'/'+author+'/'+'normal-'+fileName, 'w', encoding = 'UTF-8')
			text = fr.read()
			normalizedText = normalize(text)
			first = True
			for sentence in normalizedText[0]:
				if(not first):
					fw.write('\n')
				first = False
				fw.write(sentence+'।')

			sentenceCount += normalizedText[1]
			wordCount += normalizedText[2]
			characterCount += normalizedText[3]

		print(author+' ('+str(len(fileList))+' texts):')
		print('---------------------------------------')
		print('Mean # Sentences per text: {0:.4f}'.format(sentenceCount/len(fileList)))
		print('Mean # Words per text: {0:.4f}'.format(wordCount/len(fileList)))
		print('Mean # Characters per text: {0:.4f}'.format(characterCount/len(fileList)))
		print()
		#End for
	#End for
#End of preprocess()

#preprocess('Data/tmp', 'Data/Normalized Data')
