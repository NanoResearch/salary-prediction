__author__ = 'saimanoj'

import preprocessing
import sys

def main(arg):
	preprocessing.preprocess_train(arg)
	# preprocessing.preprocess_train2()


if __name__ == "__main__":
	main(int(sys.argv[1]))
