# python 3
import Parse
import Args
import numpy as np
import math
import types
import operator
import sys

global N, avdl
global vocb		### Format: vocb = [vocb, ...]
global file		### Format: file = [(file, size), ...]
global invt		### Format: invt = {(word[0], word[1]): [fileNumb, (fileIndex, fileTime), ...], ...}
global qury		### Format: qury = [[number, title, question, narrative, concept], ...]

def Write(Qury, Accm):
	sort = list(sorted(Accm.items(), key = operator.itemgetter(1), reverse = True))
	Ansr = sort[:100]

	indx = Qury[0]
	text = indx + ","
	for item in Ansr:
		text += file[item[0]][0] + " "
	text += "\n"
	return text


def Accum(Scr1, Scr2):
	accm = {}
	for item in Scr1: 
		if item in accm:     accm[item] += Scr1[item]
		if item not in accm: accm[item]  = Scr1[item]

	for item in Scr2:
		if item in accm:     accm[item] += Scr2[item]
		if item not in accm: accm[item]  = Scr2[item]

	return accm


def Score(Vect, Rank):
	scre = {}
	for item in Rank:
		scre[item] = sum([x * y for x, y in zip(Vect, Rank[item])])
	return scre


def FBack(Vect, Rank, Labl):
	reln = int(len(Rank) * 0.15)

	### Decide parameters
	# a, b, c = 0.9, 0.3, 0.2
	if Labl == 1: a, b, c = 0.1, 0.0, 0.0
	if Labl == 2: a, b, c = 0.7, 0.1, 0.0
	if Labl == 3: a, b, c = 0.4, 0.1, 0.1
	if Labl == 4: a, b, c = 0.9, 0.5, 0.0

	scre = {}
	for item in Rank:
		scre[item] = sum(Rank[item])
	sort = list(sorted(scre.items(), key = operator.itemgetter(1), reverse = True))
	
	### Compute original
	Original = np.array(Vect)

	### Compute related
	Related = np.array([0] * len(Vect))
	for item in sort[:reln]:
		Related = Related + np.array(Rank[item[0]])
	Related = np.array(Related)

	### Compute irrelated
	IrRelated = np.array([0] * len(Vect))
	for item in sort[-reln:]:
		IrRelated = IrRelated + np.array(Rank[item[0]])
	IrRelated = np.array(IrRelated)

	vect = a * Original + b * Related / reln - c * IrRelated / reln
	return vect


def Ngram(Qury, Labl):
	temp = Qury[Labl]
	
	### Format: term = {(word[0], word[1]): quryTime, ...}
	term = {}
	for char in range(len(temp) - 1):
		### Skip the punctuation
		if temp[char] == u'、' or temp[char + 1] == u'、': continue 
		if temp[char] == u'，' or temp[char + 1] == u'，': continue 
		if temp[char] == u'。' or temp[char + 1] == u'。': continue 
		if temp[char] == u'（' or temp[char + 1] == u'（': continue 
		if temp[char] == u'）' or temp[char + 1] == u'）': continue 
		if temp[char] == u'「' or temp[char + 1] == u'「': continue 
		if temp[char] == u'」' or temp[char + 1] == u'」': continue 

		### Find the word
		word = (vocb.index(temp[char]), vocb.index(temp[char + 1]))
		if word not in invt: continue

		### Add into Term List
		if word not in term: term[word] = 0
		term[word] += 1

	### Format: rank = {file: [value, value, ...], ...}
	indx = 0
	vect = []
	rank = {}
	for word, time in term.items():
		k1 = 2.0
		k3 = 0.2
		qf = time
		df = invt[word][0]
		DF = math.log((N - df + 0.5) / (df + 0.5))
		QF  = ((k3 + 1) * qf) / (k3 + qf)

		for item in invt[word]:
			if type(item) != type((0, 0)): continue

			tf = item[1]
			dl = file[item[0]][1]
			TF = ((k1 + 1) * tf) / (k1 * (0.25 + 0.75 * dl / avdl) + tf)
			
			### Add into Rank List
			if item[0] not in rank: rank[item[0]] = [0] * len(term)
			rank[item[0]][indx] = float(DF * TF * QF)

		### Add into Vect List
		vect.append(time)
		indx += 1
	
	return vect, rank

args = Args.Args()

vocb       = Parse.ParseVocb(args.m)
file, avdl = Parse.ParseFile(args.m, args.d)
invt       = Parse.ParseInvt(args.m)
qury       = Parse.ParseQury(args.i)
print("")

N = len(file)
text = "query_id,retrieved_docs\n"
for temp in qury:
	
	accm = {}
	
	### Consider label k
	for k in range(1, 5):
		vect, rank = Ngram(temp, k)
		if args.r == True:
			vect   = FBack(vect, rank, k)
		scre       = Score(vect, rank)
		accm       = Accum(accm, scre)
		print("[Done] Analyzing \"label\"", k)

	### Write the file
	text      += Write(temp, accm)

data = open(args.o, "w")
data.write(text)
print("[Done] Writing the output file!")