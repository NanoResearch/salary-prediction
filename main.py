__author__ = 'saimanoj'

import preprocessing
import sys

def main(arg):
	# preprocessing.preprocess_train()
	preprocessing.preprocess_train2(int(arg))


if __name__ == "__main__":
	main(sys.argv[1])
