import os
import re
import pickle
import pandas as pd
from bnltk import BanglaTokenizer
from preprocessor import normalize
from MetaDataGenerator import getMetaData, writeToFile, getLables, getFeatureValues, loadFeatureSet

def dataLoader(filePath):
	dataSet = pd.read_csv(filePath)
	#dataset = dataset.iloc[np.random.permutation(len(dataset))]
	return dataSet
#end of dataLoader()

def predict(model, featureVector):
	predictedClass = model.predict(featureVector)
	return predictedClass
#End of predict()

def test1(pathToModel, Text):
	#generate Normalized text from given raw text
	fr = Text
	fw = open('normalizedTestText.txt', 'w', encoding = 'UTF-8')
	normalizedText = normalize(fr)
	#print(len(normalizedText[0]))
	first = True
	for sentence in normalizedText[0]:
		if(not first):
			fw.write('\n')
		first = False
		fw.write(sentence+'।')
	fw.close()
	#Generate feature values for the given text for testing
	directory = os.path.dirname(pathToModel) + '/Required/'
	featureSet = loadFeatureSet(directory+'featureSet')
	labels = getLables(featureSet)
	fr = open('normalizedTestText.txt', 'r', encoding = 'UTF-8')
	featureValues = getFeatureValues(featureSet, fr.read())
	#load the model from disk
	model = pickle.load(open(pathToModel, 'rb'))
	featureVector = [featureValues]

	#Generate pandas dataSet for testing the model
	dataSet = pd.DataFrame.from_records(featureVector, columns = labels)
	x = dataSet[labels].values

	#get predicted result
	result = predict(model, x)

	#get class name map for getting actual name of the predicted class
	classNameMap = pickle.load(open(directory+'classNameMap', 'rb'))
	"""
	In testing module, after classNameMap loading and before returning do this,
	"""
	pred_prob = model.predict_proba(featureVector)
	proba_list = []
	proba_list.append(classNameMap[result[0]])
	for i in range(0, len(classNameMap)):
		proba_list.append(str(pred_prob[0][i]) + " " + str(classNameMap[i]))
	return proba_list
#End of test

#print('Predicted Class Value:',test1('250/250.sav', "    বহুকোটি লোক প্রায় একটি সমগ্র জাতি মৎস-মাংস-আহার  একেবারে  পরিত্যাগ  করেছে  হেসে অস্থির হত তাই ওদের সামনে কিছু করি নে  আমাদের প্রাণ আমাদের প্রতিভা  আমাদের চণ্ডীমণ্ডপ  হইতে  বিলাতি  কারখানাঘরের  প্রভূত ডাক পড়িল  উদ্‌বেলিতহৃদয়ে রতন গৃহের  মধ্যে   প্রবেশ  করিয়া  বলিল   দাদাবাবু  আমাকে এই পর্যবেক্ষণের পক্ষে অত্যন্ত বাধাজনক  বিশেষত বায়ুর  নিম্নস্তরগুলি  সর্বাপেক্ষা  অস্বচ্ছ     পৃথিবীর সমস্ত মাধ্যাকর্ষণশক্তি সবলে বালককে নীচের দিকে টানিতে লাগিল কিন্তু  ক্ষুদ্র    কোশল    সেই লোভেই তো এসেছি  যিনি দেখা দেন না তাঁর জন্যে  আমার  বিশেষ  ঔৎসুক্য                             প্রসন্ন সরল হাসি হোথা পুষ্পবনে    বিশেষত  কথাগুলা  তাহার  স্বামীর   উপর   লক্ষ্য   করিয়া   বলা    এবং   স্বামী মিস্টার জ এর যে এক পিতৃব্য বোন মিস ই অস্ট্রেলিয়ায় আছেন তাঁর কাপ্তেন  ব এর  সঙ্গে থাকে না কিন্তু বসন্তনিশীথে যখন প্রেয়সী     ইন্দু  ঐ দেখো-না তোমাদের বন্ধ দরজার খড়্‌খড়ে খুলে গেছে  বিনোদিনীর সহিত বিহারীর চিঠিপত্র দ্বারা এই মিলন ঘটিয়াছে ইহাতে তাহার  আর  সন্দেহ    কেবল তাহাই নহে  আমাদের ইন্দ্রিয়শক্তি সীমাবদ্ধ এইজন্য ইন্দ্রিয় দ্বারা  আমরা  কোনো বাঁকা  পথ  নীরব মিনতির  মতো  পাহাড়কে   জড়িয়ে   ধরে   আর   ছোটো   ছোটো   ঝরনা বন্ধন শিথিল করিয়া অবশেষে আনন্দের সহিত মৃত্যুকে  মোক্ষের  নামান্তররূপে  গ্রহণ  করিবে  ওটা হয় না মন যদি হল তো আবার শরীর বাদী হয় একদিন যদি  হল  তো  আবার  আর-একদিন দিতে যাইব না  তবে বল্‌ দেখি আর কাহার সহিত খেলা করিবি                    বিবাহ সথগিত রবে কিছুকাল এর"))
