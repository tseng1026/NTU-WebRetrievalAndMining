import Parse
import Args
import numpy as np
import math
import jieba
import random
import csv
import operator
from collections import Counter

global N, avdl
global invt		### Format: invt = {QQ}
global qury		### Format: qury = [(query_id, query), ...]
global corp		### Format: corp = [(news_id, url), ...]
global file		### Format: file = {file: size, ...}


def Write(Qury, Accm):
	sort = list(sorted(Accm.items(), key = operator.itemgetter(1), reverse = True))
	Ansr = sort[:300]

	indx = Qury[0]
	text = indx + ","
	for item in Ansr:
		text += file[item[0]][0] + " "
	text += "\n"
	return text


def Score(Vect, Rank):
	scre = {}
	for item in Rank:
		scre[item] = sum([x * y for x, y in zip(Vect, Rank[item])])
	return scre


def FBack(Vect, Rank):
	reln = int(len(Rank) * 0.1)

	### Decide parameters
	a, b, c = 1.2, 0.1, 0.0

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


def Okapi(Qury, k):
	### Add into Term List
	qcnt = Counter()
	term = list(jieba.cut(Qury))
	qcnt.update(term)

	### Format: rank = {file: value, ...}
	indx = 0
	vect = [0] * len(term)
	rank = {}
	for word, time in qcnt.items():
		if word not in invt: continue

		### Parameters
		k1 = 0.75
		k3 = 0.15
		qf = time
		# df = N / math.e**invt[word]['idf']
		# DF = math.log((N - df + 0.5) / (df + 0.5))
		DF = invt[word]['idf']
		QF  = ((k3 + 1) * qf) / (k3 + qf)

		if DF > 900: continue
		if DF < 1: continue

		for item in invt[word]['docs']:
			for name, tf in item.items():
				
				dl = file[name]
				TF = ((k1 + 1) * tf) / (k1 * (0.25 + 0.75 * dl / avdl) + tf)

				### Add into Rank List
				if name not in rank: rank[name] = [0] * len(term)
				rank[name][indx] = float(DF * TF * QF)
		
		### Add into Vect List
		vect[indx] = time
		indx += 1

	return vect, rank


args = Args.Args()

invt       = Parse.ParseInvt(args.i)
qury       = Parse.ParseQury(args.q)
corp       = Parse.ParseCorp(args.c)
file, avdl = Parse.ParseFile(invt)
print("")

N = corp.shape[0] # used for random sample
final_ans = []
for k, temp in qury:
	if k == "q_5": break
	print("query_id: {}".format(k))
	
	vect, rank = Okapi(temp, k)
	if args.r == True:
		vect   = FBack(vect, rank)
	scre       = Score(vect, rank)
	
	# sort the document score pair by the score
	sorted_document_scores = sorted(scre.items(), key=operator.itemgetter(1), reverse=True)
	
	# record the answer of this query to final_ans
	if len(sorted_document_scores) >= 300:
		final_ans.append([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores[:300]])
	else: # if candidate documents less than 300, random sample some documents that are not in candidate list
		documents_set  = set([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores])
		sample_pool = ['news_%06d'%news_id for news_id in range(1, num_corpus+1) if 'news_%06d'%news_id not in documents_set]
		sample_ans = random.sample(sample_pool, 300-count)
		sorted_document_scores.extend(sample_ans)
		final_ans.append([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores])
	
# write answer to csv file
with open(args.o, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	head = ['Query_Index'] + ['Rank_%03d'%i for i in range(1,301)]
	writer.writerow(head)
	for query_id, ans in enumerate(final_ans, 1):
		writer.writerow(['q_%02d'%query_id]+ans)