import GrammaTools as gt
from Gramma import Gramma

G = Gramma({"S", "A","B","C"},
		   {"a","c","d",""},
		   {"S" : ["ABCd"],
		    "A" : ["a",""],
			"B" : ["AC"],
			"C" : ["c",""]},
		   "S")

G.printGramma()
G_new = gt.remove_lambda_rules(G)
G_new.printGramma()