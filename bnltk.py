import re

class BanglaTokenizer:
	#Tokenize a text and returns a list of senetences
	def sentenceTokenize(text):
		sentences = re.split('\?|!|।', text)
		return sentences
		
	#Tokenize a sentence and returns a list of words
	def wordTokenize(sentence):
		words = re.findall(r'[\w|ি|া|ী|ু|ূ|ৃ|ে|ৈ|ো|ৌ|্|ঃ|ঁ|়|ঽ|ৄ|ৗ|ৠ|ৡ|ৢ|ৣ|্য|্র|ক্ষ|ঙ্ক|ঙ্গ|জ্ঞ|ঞ্চ|ঞ্ছ|ঞ্জ|ত্ত|ষ্ণ|হ্ম|ণ্ড|।|৳|ৰ|ৱ|৲|৴|৵|৶|৷|৸|৹|৺]+', sentence)
		return words
#End of BanglaTokenizer
