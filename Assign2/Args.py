import argparse

def Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", action="store_true", default=False)
	parser.add_argument("-i", default="inverted_file.json", type=str)
	parser.add_argument("-q", default="QS_1.csv", type=str)
	parser.add_argument("-c", default="NC_1.csv", type=str)
	parser.add_argument("-o", default="answer.csv", type=str)

	args = parser.parse_args()
	return args