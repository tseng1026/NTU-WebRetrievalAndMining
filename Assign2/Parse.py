# python 3
import os
import json
import pandas
import numpy as np

def ParseInvt(Dir):
	with open(Dir) as f:
		invt = json.load(f)
	print("[Done] Parsing \"inverted_file.json\"!")
	return invt


def ParseQury(Dir):
	### Format: qury = [(query_id, query), ...]
	qury = np.array(pandas.read_csv(Dir))
	print("[Done] Parsing \"QS_1.csv\"!")
	return qury


def ParseCorp(Dir):
	### Format: corp = [(news_id, url), ...]
	corp = np.array(pandas.read_csv(Dir))
	print("[Done] Parsing \"NC_1.csv\"!")
	return corp 


def ParseFile(Invt):
	### Format: file = {file: length, ...}
	avdl = 0
	file = {}
	for word in Invt:
		for item in Invt[word]['docs']:
			for name, tf in item.items():
				temp = tf * len(word)

				if name not in file: file[name] = 0
				file[name] += temp
				avdl += temp

	print("[Done] Parsing \"FileLength\"!")
	return file, avdl / len(file)