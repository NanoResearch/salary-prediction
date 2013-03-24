__author__ = 'saimanoj'

import preprocessing
import sys

def main(arg):
	# preprocessing.preprocess_train()
	preprocessing.divide_file_into_parts()


if __name__ == "__main__":
	main(sys.argv[1])
