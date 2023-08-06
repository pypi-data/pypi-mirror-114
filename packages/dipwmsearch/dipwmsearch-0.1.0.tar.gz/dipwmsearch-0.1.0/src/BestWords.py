#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

import math

from .diPwm import diPWM
from .Enumerate import enumerate_words_LAM

def get_first_threshold(diP, number_words_wanted):
	""" Compute a first threshold by using uniforme probability.

	Args:
		diP (diPWM): object diPWM

		number_words_wanted (int): number of words that we want to compute

	Return:
		list of int: list of successive positions (a block)
	"""

	# possibles = diP.alphabet_size^(diP.length + 1)
	possibles = math.pow(diP.alphabet_size, diP.length + 1)
	ratio = number_words_wanted/possibles
	threshold = diP.max - ((diP.max - diP.min)*ratio)
	return threshold

def count_words(diP, threshold, range_count):
	""" Compute the number of words enumerated where it is less or equal than `range_count`. If this number is more than `range_count`, the function returns `range_count + 1`.

	Args:
		diP (diPWM): object diPWM

		threshold (float): threshold given to select the windows

		range_count (int): limit of the number of words that we want to compute

	Return:
		int: number of words enumerate
	"""

	number = 0
	for word, score in enumerate_words_LAM(diP,threshold):
		number += 1
		if number == range_count + 1:
			return number
	return number


def find_threshold_dichotomy(diP, number_words_wanted, range_count, bound_min = None, bound_max = None):
	""" Compute a threshold where the number of words enumerated is between `number_words_wanted` and `range_count`.

	Args:
		diP (diPWM): object diPWM

		number_words_wanted (int): number of words that we want to compute

		range_count (int): limit of the number of words that we want to compute

		bound_min (str, optional): bound minimum for the dichotomy. Defaults to the minimum of diP.

		bound_max (str, optional): bound maximum for the dichotomy. Defaults to the maximum of diP.

	Return:
		int: a threshold where the number of words enumerated is between `number_words_wanted` and `range_count`
	"""

	if bound_min == None:
		bound_min = diP.min
	if bound_max == None:
		bound_max = diP.max
	threshold = (bound_min + bound_max)/2
	number_words = count_words(diP, threshold, range_count)
	while not number_words_wanted <= number_words <= range_count :
		if number_words < number_words_wanted:
			bound_max = threshold
		else:
			bound_min = threshold
		threshold = (bound_min + bound_max)/2
		number_words = count_words(diP, threshold, range_count)
	return threshold

def find_threshold_dichotomy_optimized(diP, number_words_wanted, range_count):
	""" Compute a threshold where the number of words enumerated is between `number_words_wanted` and `range_count`. In this optimized version, we use the function `get_first_threshold` to compute the beginning of the dichotomy.

	Args:
		diP (diPWM): object diPWM

		number_words_wanted (int): number of words that we want to compute

		range_count (int): limit of the number of words that we want to compute

	Return:
		int: a threshold where the number of words enumerated is between `number_words_wanted` and `range_count`
	"""

	threshold = get_first_threshold(diP, number_words_wanted)
	number_words = count_words(diP, threshold, range_count)
	bound_max = diP.max
	bound_min = threshold
	while not number_words > range_count:
		threshold -= (bound_max - bound_min)
		bound_min = threshold
		number_words = count_words(diP, threshold, range_count)
	threshold = find_threshold_dichotomy(diP, number_words_wanted, range_count, bound_min, bound_max)
	return threshold

def find_best_words(diP, number_words_wanted):
	""" Compute the `number_words_wanted` enumerated words by decreasing score.

	Args:
		diP (diPWM): object diPWM

		number_words_wanted (int): number of words that we want to compute

	Return:
		list of tuple: list of the first `number_words_wanted` (enumerated word, score) by decreasing score
	"""

	threshold = find_threshold_dichotomy_optimized(diP, number_words_wanted, number_words_wanted*2)
	li = list(enumerate_words_LAM(diP,threshold))
	li.sort(key=lambda x: x[1], reverse=True)
	return li[:number_words_wanted]
