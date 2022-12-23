import GrammaTools as gt
from Gramma import Gramma

test_G = Gramma({'A','B','C'},{'','a'},
			{'A' : ['BC'],
			 'B' : ['CA', "a", ""],
			 'C' : ['AB', ""]},
			 'A')

test_G.printGramma()
test_G = gt.remove_lambda_rules(test_G)

test_G.printGramma()