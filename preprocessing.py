import math
import pickle
import exceptions
import gc

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


def preprocess_train(start):
	"""
	Main Function: reads data and does pre-processing with help of above functions.
	"""
	lines = []

	title_freq_dict = {}
	desc_freq_dict = {}
	# These dictionaries are used to calculate the frequency of words.


	# location_dict = {}
	time_dict = {}
	term_dict = {}
	# company_dict = {}
	category_dict = {}
	source_dict = {}
	# These dictionaries are used to find the list of unique categories of each field.


	filename = 'Training.csv'

	with open(filename, 'rb') as csvfile:
		content = csv.reader(csvfile)
		for line in content:
			lines.append(line)

	T = string.maketrans(string.punctuation, ' ' * (len(string.punctuation)))

	del lines[0]

	M = len(lines)

	i = 0
	for line in lines:
		title_cur_list = clean_str_to_list(line[1], T)
		desc_cur_list = clean_str_to_list(line[2], T)
		lines[i][1] = ' '.join(title_cur_list)
		lines[i][2] = ' '.join(desc_cur_list)
		i += 1
	# for w in title_cur_list:
	# 	title_freq_dict[w] = title_freq_dict.get(w, 0) + 1
	# for w in desc_cur_list:
	# 	desc_freq_dict[w] = desc_freq_dict.get(w, 0) + 1

	# remove_low_freq_words(title_freq_dict)
	# remove_low_freq_words(desc_freq_dict)
	# Low frequency words removed

	# title_freq_list = [(v, k) for k, v in title_freq_dict.iteritems()]
	# desc_freq_list = [(v, k) for k, v in desc_freq_dict.iteritems()]
	# title_freq_list.sort(reverse=True)
	# desc_freq_list.sort(reverse=True)
	# #Sorted by non-increasing frequency of words
	#
	# print "Lists..."
	# print 'title list ', title_freq_list
	# print 'desc list ', desc_freq_list
	#
	# print 'len of title dict ' + str(len(title_freq_dict))
	# print 'len of desc dict ' + str(len(desc_freq_dict))
	#
	# title_idf_dict = compute_idf(lines, title_freq_dict.keys(), 1)
	# desc_idf_dict = compute_idf(lines, desc_freq_dict.keys(), 2)
	#
	# print 'title idf dict' + str(title_idf_dict)
	# print 'desc idf dict' + str(desc_idf_dict)
	#
	# var_file = open('variables', 'w')
	# pickle_list = [title_freq_list, desc_freq_list, title_idf_dict, desc_idf_dict]
	# pickle.dump(pickle_list, var_file)
	# var_file.close()
	#
	# title_freq_file = open('title_freq_dict', 'w') #title_idf_dict
	# pickle.dump(title_idf_dict, title_freq_file)
	# title_freq_file.close()
	#
	# desc_freq_file = open('desc_freq_dict', 'w') #desc_idf_dict
	# pickle.dump(desc_idf_dict, desc_freq_file)
	# desc_freq_file.close()

	for line in lines:
		# location_dict[line[3]] = 1
		time_dict[line[4]] = 1
		term_dict[line[5]] = 1
		# company_dict[line[6]] = 1
		category_dict[line[7]] = 1
		source_dict[line[8]] = 1

	title_idf_dict = {}
	with open('title_idf_dict', 'r') as title_idf_file:
		title_idf_dict = pickle.load(title_idf_file)
		title_list = title_idf_dict.keys()
		title_list.sort()

	desc_idf_dict = {}
	with open('desc_idf_dict', 'r') as desc_idf_file:
		desc_idf_dict = pickle.load(desc_idf_file)
		desc_list = desc_idf_dict.keys()
		desc_list.sort()

	# location_list = location_dict.keys()
	time_list = time_dict.keys()
	term_list = term_dict.keys()
	# company_list = company_dict.keys()
	category_list = category_dict.keys()
	source_list = source_dict.keys()

	# location_list.sort()
	time_list.sort()
	term_list.sort()
	# company_list.sort()
	category_list.sort()
	source_list.sort()

	location_list = []
	company_list = []
	lists_file = open('all_lists', 'w')
	all_list = [title_list, desc_list, location_list, time_list, term_list, company_list, category_list, source_list]
	sum_len = 0
	for i in range(len(all_list)):
		length = len(all_list[i])
		sum_len += length
		print 'length of sublist ' + str(length)
	print 'sum of all lengths  ' + str(sum_len)

	# All these lists have the list of words or categories of that attribute in sorted order.
	pickle.dump(all_list, lists_file)
	lists_file.close()

	title_idf_list = title_idf_dict.items()
	title_idf_list.sort()
	# Sort based on the words
	title_idf_list = [x[1] for x in title_idf_list]
	# Take the idf values

	desc_idf_list = desc_idf_dict.items()
	desc_idf_list.sort()
	# Sort based on the words
	desc_idf_list = [x[1] for x in desc_idf_list]
	# Take the idf values

	line_len = len(lines[0])
	count = 1
	for line in lines:
		if count <= (start - 1) * 10000:
			count += 1
			continue
		if count % 10000 == 1 or count == (start - 1) * 10000 + 1:
			inputs = open('inputs_' + str(1 + count / 10000), 'w')
			targets = open('targets_' + str(1 + count / 10000), 'w')
			print 'file no. ' + str(1 + count / 10000)
			csvwriter_inputs = csv.writer(inputs)
			csvwriter_targets = csv.writer(targets)

		#		print 'line ' + str(count)
		csvwriter_targets.writerow([int(line[-1])])
		new_line = list()

		cur_line_title_dict = dict([(w, line[1].count(w)) for w in line[1].split()])
		cur_line_title_freq_list = [cur_line_title_dict.get(w, 0) for w in title_list]
		max_value = max(cur_line_title_freq_list)
		#		print 'max_value for title is ' + str(max_value)
		if max_value != 0:
			cur_line_title_freq_list = [(x / float(max_value)) if x != 0 else 0 for x in cur_line_title_freq_list]
			assert len(cur_line_title_freq_list) == len(title_idf_list) == 502
			title_tf_idf_list = [cur_line_title_freq_list[i] * title_idf_list[i] if cur_line_title_freq_list[i] != 0
			                     else 0 for i in range(len(title_idf_list))]
		# Both cur_line_title_freq_list and title_idf_list are of same length,
		# they are essentially tf and idf vectors
		else:
			title_tf_idf_list = cur_line_title_freq_list

		new_line.extend(title_tf_idf_list)

		cur_line_desc_dict = dict([(w, line[2].count(w)) for w in line[2].split()])
		cur_line_desc_freq_list = [cur_line_desc_dict.get(w, 0) for w in desc_list]
		max_value = max(cur_line_desc_freq_list)
		#		print 'max_value for desc is ' + str(max_value)
		if max_value != 0:
			cur_line_desc_freq_list = [x / float(max_value) if x != 0 else 0 for x in cur_line_desc_freq_list]
			assert len(cur_line_desc_freq_list) == len(desc_idf_list) == 1003
			desc_tf_idf_list = [cur_line_desc_freq_list[i] * desc_idf_list[i] if cur_line_desc_freq_list[i] != 0
			                    else 0 for i in range(len(desc_idf_list))]
		# Both cur_line_desc_freq_list and desc_idf_list are of same length,
		# they are essentially tf and idf vectors
		else:
			desc_tf_idf_list = cur_line_desc_freq_list

		new_line.extend(desc_tf_idf_list)

		i = 4
		while i < line_len - 1:
			if i == 6:
				i += 1
				continue
			presence_list = [int(w == line[i]) for w in all_list[i - 1]]
			new_line.extend(presence_list)
			# new_line.append(presence_list.index(True) if True in presence_list else -1)
			i += 1
		csvwriter_inputs.writerow(new_line)
		count += 1
		gc.collect()

	if inputs: inputs.close()
	if targets: targets.close()

# return all_list


def num(s):
	try:
		return int(s)
	except exceptions.ValueError:
		return float(s)


def expand_inputs():
	count = 4
	range_list = [2325, 3, 3, 316617, 29, 165]
	lines = []
	while count < 15:
		raw_input('Press enter to process file part_' + str(count) + '  ')
		with open('part_' + str(count), 'r') as input_file:
			content = csv.reader(input_file)
			for line in content:
				new_line = []
				for x in line:
					new_line.append(num(x))
				lines.append(new_line)
		with open('inputs_' + str(count), 'w') as inputs:
			csvwriter = csv.writer(inputs)
			for line in lines:
				new_line = line[:34733]
				for x, y in zip(line[34733:], range_list):
					tmp_list = [0] * y
					tmp_list[x] = 1
					new_line.extend(tmp_list)
				csvwriter.writerow(new_line)
		lines = []
		gc.collect()
		count += 1


def preprocess_train2():
	expand_inputs()


def divide_file_into_parts():
	input_file = open('lines_file', 'r')
	content = csv.reader(input_file)
	i = 1
	part_file = open('part_1', 'w')
	csvwriter = csv.writer(part_file)

	j = 2

	for line in content:
		if i > 10000:
			part_file.close()
			part_file = open('part_' + str(j), 'w')
			j += 1
			csvwriter = csv.writer(part_file)
			i = 1
			gc.collect()
		new_line = []
		for x in line:
			new_line.append(num(x))
		i += 1
		csvwriter.writerow(new_line)
	input_file.close()


def preprocess_test():
	test = 'b.csv'
	lines = []

	title_freq_dict = {}
	desc_freq_dict = {}
	time_dict = {}
	term_dict = {}
	category_dict = {}
	source_dict = {}
	# These dictionaries are used to find the list of unique categories of each field.

	with open(test, 'rb') as test_csvfile:
		content = csv.reader(test_csvfile)
		for line in content:
			lines.append(line)

	T = string.maketrans(string.punctuation, ' ' * (len(string.punctuation)))

	del lines[0]

	M = len(lines)

	i = 0
	for line in lines:
		title_cur_list = clean_str_to_list(line[1], T)
		desc_cur_list = clean_str_to_list(line[2], T)
		lines[i][1] = ' '.join(title_cur_list)
		lines[i][2] = ' '.join(desc_cur_list)
		i += 1
	gc.collect()

	for line in lines:
		time_dict[line[4]] = 1
		term_dict[line[5]] = 1
		category_dict[line[7]] = 1
		source_dict[line[8]] = 1

	title_idf_dict = {}
	with open('title_idf_dict', 'r') as title_idf_file:
		title_idf_dict = pickle.load(title_idf_file)
		title_list = title_idf_dict.keys()
		title_list.sort()

	desc_idf_dict = {}
	with open('desc_idf_dict', 'r') as desc_idf_file:
		desc_idf_dict = pickle.load(desc_idf_file)
		desc_list = desc_idf_dict.keys()
		desc_list.sort()

	time_list = time_dict.keys()
	term_list = term_dict.keys()
	category_list = category_dict.keys()
	source_list = source_dict.keys()

	time_list.sort()
	term_list.sort()
	category_list.sort()
	source_list.sort()

	location_list = []
	company_list = []
	lists_file = open('all_lists', 'r')
	all_list = pickle.load(lists_file)
	# All these lists have the list of words or categories of that attribute in sorted order.
	# [title_list, desc_list, location_list, time_list, term_list, company_list, category_list, source_list] = all_list
	sum_len = 0
	for i in range(len(all_list)):
		length = len(all_list[i])
		sum_len += length
		print 'length of sublist ' + str(length)
	print 'sum of all lengths  ' + str(sum_len)
	lists_file.close()

	title_idf_list = title_idf_dict.items()
	title_idf_list.sort()
	# Sort based on the words
	title_idf_list = [x[1] for x in title_idf_list]
	# Take the idf values

	desc_idf_list = desc_idf_dict.items()
	desc_idf_list.sort()
	# Sort based on the words
	desc_idf_list = [x[1] for x in desc_idf_list]
	# Take the idf values

	gc.collect()
	line_len = len(lines[0])
	count = 1
	for line in lines:
		if count % 10000 == 1 or count == 1:
			inputs = open('test_inputs_' + str(1 + count / 10000), 'w')
			targets = open('test_targets_' + str(1 + count / 10000), 'w')
			print 'file no. ' + str(1 + count / 10000)
			csvwriter_inputs = csv.writer(inputs)
			csvwriter_targets = csv.writer(targets)

		#		print 'line ' + str(count)
		csvwriter_targets.writerow([int(line[-1])])
		new_line = list()

		cur_line_title_dict = dict([(w, line[1].count(w)) for w in line[1].split()])
		cur_line_title_freq_list = [cur_line_title_dict.get(w, 0) for w in title_list]
		max_value = max(cur_line_title_freq_list)
		#		print 'max_value for title is ' + str(max_value)
		if max_value != 0:
			cur_line_title_freq_list = [(x / float(max_value)) if x != 0 else 0 for x in cur_line_title_freq_list]
			assert len(cur_line_title_freq_list) == len(title_idf_list) == 502
			title_tf_idf_list = [cur_line_title_freq_list[i] * title_idf_list[i] if cur_line_title_freq_list[i] != 0
			                     else 0 for i in range(len(title_idf_list))]
		# Both cur_line_title_freq_list and title_idf_list are of same length,
		# they are essentially tf and idf vectors
		else:
			title_tf_idf_list = cur_line_title_freq_list

		new_line.extend(title_tf_idf_list)

		cur_line_desc_dict = dict([(w, line[2].count(w)) for w in line[2].split()])
		cur_line_desc_freq_list = [cur_line_desc_dict.get(w, 0) for w in desc_list]
		max_value = max(cur_line_desc_freq_list)
		#		print 'max_value for desc is ' + str(max_value)
		if max_value != 0:
			cur_line_desc_freq_list = [x / float(max_value) if x != 0 else 0 for x in cur_line_desc_freq_list]
			assert len(cur_line_desc_freq_list) == len(desc_idf_list) == 1003
			desc_tf_idf_list = [cur_line_desc_freq_list[i] * desc_idf_list[i] if cur_line_desc_freq_list[i] != 0
			                    else 0 for i in range(len(desc_idf_list))]
		# Both cur_line_desc_freq_list and desc_idf_list are of same length,
		# they are essentially tf and idf vectors
		else:
			desc_tf_idf_list = cur_line_desc_freq_list

		new_line.extend(desc_tf_idf_list)

		i = 4
		# print all_list[7]
		while i < line_len - 1:
			if i == 6:
				i += 1
				continue
			presence_list = [int(w == line[i]) for w in all_list[i - 1]]
			new_line.extend(presence_list)
			# new_line.append(presence_list.index(True) if True in presence_list else -1)
			i += 1
		csvwriter_inputs.writerow(new_line)
		count += 1
		gc.collect()

	if inputs: inputs.close()
	if targets: targets.close()
