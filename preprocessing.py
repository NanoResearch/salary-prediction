import math
import pickle

__author__ = 'saimanoj'

import csv
import string

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
             'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
             'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
             'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
             'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
             'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
             'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
             'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
             'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
             'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should',
             'now']

log_dict = {}


def clean_str_to_list(dirty_str, T):
	"""
	Given string contains unicode characters like \x92, \xe2 etc for things like curved quote character.
	So, the string is stripped of all those characters which are not ASCII. Then all punctuation characters are
	replaced with spaces, then the string is converted to lowercase and split() on whitespace(space, tab, newline etc.)
	Stopwords are removed from the list obtained.
	:param dirty_str: The string to be cleaned.
	:param T: The translate table created by preprocess_train() for translating punctuation to space.
	:return: cleaned list with just words(may have digits).
	"""
	word_list = ((string.translate(str(unicode(dirty_str, 'ascii', 'ignore')), T)).lower()).split()
	neat_list = [w for w in word_list if w not in stopwords and len(w) > 3]
	return neat_list


def remove_low_freq_words(words_dict, k=4):
	"""
	Removes words with low freq. from the given dictionary-- IN PLACE
	:param words_dict:  Dictionary with words and frequencies
	:param k: words with freq below k are removed.
	"""
	keys_to_be_deleted = []
	for word, frequency in words_dict.iteritems():
		if frequency < k:
			keys_to_be_deleted.append(word)
	for word in keys_to_be_deleted:
		del words_dict[word]


def compute_idf(lines, words_list, i):
	"""
	Computes idf -- Inverse document frequency of each word in words_list.
	:param lines: a list of lists, each sub-list containing a record in the given data-set(which is clean).
	:param words_list: list containing all the words for which idf should be computed.
	:param i: index(column) of the attribute in the record. Here, for title it is 1 and for description it is 2.
	:rtype : dict
	"""
	M = len(lines)
	print 'M ' + str(M)
	idf_dict = {}
	for word in words_list:
		count = 1 # To avoid division by zero problem.
		for line in lines:
			if word in line[i]:
				count += 1
		if count not in log_dict:
			log_dict[count] = math.log(M / float(count))
		idf_dict[word] = log_dict[count]

	return idf_dict


def preprocess_train():
	"""
	Main Function: reads data and does pre-processing with help of above functions.
	"""
	lines = []
	filename = 'a.csv'

	with open(filename, 'rb') as csvfile:
		content = csv.reader(csvfile)
		for line in content:
			lines.append(line)

	T = string.maketrans(string.punctuation, ' ' * (len(string.punctuation)))

	del lines[0]

	M = len(lines)

	title_dict = {}
	desc_dict = {}

	i = 0
	for line in lines:
		title_cur_list = clean_str_to_list(line[1], T)
		desc_cur_list = clean_str_to_list(line[2], T)
		lines[i][1] = ' '.join(title_cur_list)
		lines[i][2] = ' '.join(desc_cur_list)
		i += 1
		for w in title_cur_list:
			title_dict[w] = title_dict.get(w, 0) + 1
		for w in desc_cur_list:
			desc_dict[w] = desc_dict.get(w, 0) + 1

	remove_low_freq_words(title_dict)
	remove_low_freq_words(desc_dict)
	# Low frequency words removed

	title_freq_list = [(v, k) for k, v in title_dict.iteritems()]
	desc_freq_list = [(v, k) for k, v in desc_dict.iteritems()]
	title_freq_list.sort(reverse=True)
	desc_freq_list.sort(reverse=True)
	#Sorted by non-increasing frequency of words

	print "Lists..."
	print 'title list ', title_freq_list
	print 'desc list ', desc_freq_list

	print 'len of title dict ' + str(len(title_dict))
	print 'len of desc dict ' + str(len(desc_dict))

	title_idf_dict = compute_idf(lines, title_dict.keys(), 1)
	desc_idf_dict = compute_idf(lines, desc_dict.keys(), 2)

	print 'title idf dict' + str(title_idf_dict)
	print 'desc idf dict' + str(desc_idf_dict)

	file = open('variables', 'w')
	pickle_list = [title_freq_list, desc_freq_list, title_idf_dict, desc_idf_dict]
	pickle.dump(pickle_list, file)
	file.close()

	file = open('dict_title', 'w')
	pickle.dump(title_idf_dict, file)
	file.close()

	file = open('dict_desc', 'w')
	pickle.dump(desc_idf_dict, file)
	file.close()


def preprocess_test():
	pass
