import argparse

def Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", action="store_true", default=False)
	parser.add_argument("-b", action="store_true", default=False)
	parser.add_argument("-i", default="../Query/query-test.xml", type=str)
	parser.add_argument("-o", default="answer.csv", type=str)
	parser.add_argument("-m", default="../Model/", type=str)
	parser.add_argument("-d", default="../CIRB010/", type=str)

	args = parser.parse_args()
	return args