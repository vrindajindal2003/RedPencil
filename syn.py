from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import json
import urllib.request as urllib2
import requests

def getSynonyms(wordBefore, word, wordAfter):
	api_url = 'https://api.datamuse.com/words?ml='
	api_url = api_url + word
	if (wordBefore!="" and pos_tag([wordBefore])[0][1]!='.'):
		api_url = api_url + '&lc=' + wordBefore
	if (wordAfter!="" and pos_tag([wordAfter])[0][1]!='.'):
		api_url = api_url + '&rc=' + wordAfter
	api_url = api_url + '&max=5'
	#print(api_url)
	data = json.load(urllib2.urlopen(api_url))
	data_format = json.dumps(data, indent=4, sort_keys=True)
	res = []
	for i in data:
		wd = i['word']
		if (pos_tag([wd])[0][1]==pos_tag([word])[0][1]):
			trigram = []
			if (wordBefore!="" and pos_tag([wordBefore])[0][1]!='.'):
				trigram.append(wordBefore)# trigram = [trigram wordBefore]
			trigram.append(wd)# trigram = [trigram wd]
			if (wordAfter!="" and pos_tag([wordAfter])[0][1]!='.'):
				trigram.append(wordAfter)# trigram = [trigram wordAfter]
			f = phraseFreqFinder("%20".join(trigram))
			if (f>10000):
				res.append((f,wd))
	return res

def tag(sentence):
	words = word_tokenize(sentence)
	words = pos_tag(words)
	return words

def paraphraseable(tag):
	l = ['JJ','NN','NNS','NNP','NNPS','RB','VB','VBD','VBG','VBN','VBP','VBZ']
	if tag in l:
		return True
	else:
		return False

def phraseFreqFinder(phrase):
	#phrase = "%20".join([wordBefore,word,wordAfter]).lower()
	#print(trigram)
	api_url = 'https://api.phrasefinder.io/search?corpus=eng-us&topk=1&format=tsv&query=' + phrase
	response = requests.get(api_url)
	# data = response.json()
	# data_format = json.dumps(data, indent=4, sort_keys=True)
	data = response.text
	#print(data.split('\t'))
	try:
		x = data.split('\t')[1]
	# lines = data.split("\n")
	# for l in lines:
	# 	print(l.split('\t')[1])
	# 	x = l.split('\t')[1]
		return int(x)
	except:
		return 0

sentence = input()
words = tag(sentence)
#print(words)

for i in range(len(words)):

	if (i==0):
		wb = ""
	else:
		(wb,tb) = words[i-1]

	(w,t) = words[i]

	if (i==len(words)-1):
		wa = ""
	else:
		(wa,ta) = words[i+1]

	if (paraphraseable(t)):
		syns = getSynonyms(wb,w,wa)
		syns.sort(reverse=True)
		if (len(syns)!=0):
			print(w,[ x[1] for x in syns ])	