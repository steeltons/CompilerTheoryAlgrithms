from Gramma import *
import GrammaTools as gt
import pytest

def test_itmo():
	test_G = Gramma({'S','A','B','C'}, {'d','a','c',''},
					{'S' : ['ABCd'],
					 'A' :['a',''],
					 'C' : ['c',''],
					 'B' : ['AC']},
					 'S')
	good_G = Gramma({'S','A','B','C'}, {'d','a','c'},
					{'S' : ['Ad','ABd','ACd','ABCd','Bd','BCd','Cd','d'],
					 'A' :['a'],
					 'C' : ['c'],
					 'B' : ['AC','A','C']},
					 'S')
	test_G = gt.remove_lambda_rules(test_G)
	assert test_G.equals(good_G)

def test1():
	test_G = Gramma({'S'},{'a','b',''},
				    {'S' : ['aSbS','bSaS','']},
					'S')
	good_G = Gramma({'S','S_new'},{'a','b'},
					{'S_new' : ['S',''],
					 'S' : ['ab','abS','aSbS','aSb','bSaS','ba','baS','bSa']},
					 'S_new')
	test_G = gt.remove_lambda_rules(test_G)
	assert test_G.equals(good_G)

def test2():
	test_G = Gramma({'S','K','N','A','B','M'}, {'a','b',''},
					{'S' : ['KNM'],
					 'K' : ['ab'],
					 'N' : ['Ab'],
					 'M' : ['AB'],
					 'A' : [''],
					 'B' : ['']},
					 'S')
	good_G = Gramma({'S','K','N'}, {'a','b'},
					{'S' : ['KN'],
					 'K' : ['ab'],
					 'N' : ['b']},
					 'S')
	test_G = gt.remove_lambda_rules(test_G)
	test_G.equals(good_G)

def test_no_lambda():
	test_G = good_G = Gramma({'S','A'}, {'a','b',''},
					{'S' : ['aAb',''],
					 'A' : ['b']},
					 'S')
	test_G = gt.remove_lambda_rules(test_G)
	test_G.equals(good_G)

def test3():
	test_G = Gramma({'S','N','K','M','B','A'},{'a','b','c','d',''},
					{'S' : ['KNM'],
					 'K' : ['ab'],
					 'N' : ['Ab'],
					 'M' : ['AB'],
					 'A' : ['c',''],
					 'B' : ['d','']},
					 'S')
	good_G = Gramma({'S','N','K','M','B','A'},{'a','b','c','d'},
					{'S' : ['KNM', 'KN'],
					 'N' : ['Ab', 'b'],
					 'M' : ['AB','A','B'],
					 'K' : ['ab'],
					 'A' : ['c'],
					 'B' : ['d']},
					 'S')
	test_G = gt.remove_lambda_rules(test_G)
	test_G.equals(good_G)

def test6():
	test_G = Gramma({'A','B','C'},{},
			{'A' : ['BC'],
			 'B' : [''],
			 'C' : ['']},
			 'A')