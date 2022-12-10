from Gramma import Gramma

# Компаратор для приземления лямбда правил в самый низ списка
def __comparator(pair):
	for key in pair:
		if pair[key] == "":
			return True
	return False

# Метод-проверка правила на то, состоит ли правило полностью из лямбда-терминалов
# Возвращает True - если в правиле есть нетерминалЮ который переходит в терминал, или это сам терминал
# Возвращает False - если правило полностью состоит из лябда-терминалов
def __is_rule_contains_lambda(rule, lamba_rules_set):
	for symbol in rule:
		if symbol not in lamba_rules_set:
			return False
	return True

# Метод, который отсеивает нетерминалы на лямбда-нетерминалы и нетерминалы, из которых можно вывести терминальную цепочку
# Возвращает два множества - лямбда-нетерминалы и нормальные нетерминалы
def __create_lambda_and_normal_rules_sets(rules, terminals):
	lambda_rules_set = set() #лямбда-нетерминалы
	normal_rules_set = set() # нормальные нетерминалы
	for pair in rules:
		for key in pair:
			if (pair[key] == "") or __is_rule_contains_lambda(pair[key], lambda_rules_set):
				lambda_rules_set = lambda_rules_set | {key}
			elif (set(pair[key]) & terminals) != set():
					normal_rules_set = normal_rules_set | {key}
	for pair in rules: # Вторая прогонка, чтобы полностью покрыть нетерминалы
		key = [key for key in pair][0]
		if (set(pair[key]) & normal_rules_set) != set():
			normal_rules_set = normal_rules_set | {key}
	return lambda_rules_set, normal_rules_set

# Метод, который ищет те правила, в правых частях которых есть символы из лямбда-терминалов
# Возвращает множество правил, которые нужно исправить
def __find_all_bad_rules(rules, lambda_rules):
	P_bad = list()
	for pair in rules:
		key = [key for key in pair][0]
		if (set(pair[key]) & lambda_rules) != set():
			P_bad.append(pair)
	return P_bad

# Метод, который исправляет все плохие правила на нормальные
# Возвращает множество исправленных правил
# pair - пара вида <Нетерминал : вывод>
def __repair_bad_rules(P_bad, lambda_rules, normal_rules):
	P_new = {}
	for pair in P_bad:
		key = [key for key in pair][0]
		new_rules = {pair[key]} # Добавляем вывод 
		rule_symbols = set(pair[key]) # Разбиваем правило на символы

		# Итерируем множестов символов, принадлежащих как лямбда-правилам, так и нормальным
		for symbol in rule_symbols & lambda_rules & normal_rules: 
			# Получаем все индексы для нашего символа
			symbol_indexes = [i for i, c in enumerate(pair[key]) if c == symbol]
			for index in symbol_indexes:
				# Добавляем к выводу новую вариацию вывода по типу S -> aSbS|abS|aSb|ab
				new_rules = new_rules | {pair[key][:index]+pair[key][index+1:]}
			for rule in new_rules: # Убираем лябда терминал из всех существующих правил
				tt = rule.replace(symbol, '')
				if tt != '':
					new_rules = new_rules | {tt}

		# Итерируем множестов символов, принадлежащих только лямбда-нетерминалам
		for symbol in rule_symbols & lambda_rules - normal_rules:
				temp_new_rules = set()
				# Убираем лябда-терминал из всех новых выводов
				while new_rules != set():
					rule = new_rules.pop().replace(symbol,'')
					if rule != '':
						temp_new_rules = temp_new_rules | {rule}
				new_rules = temp_new_rules

		if new_rules != set() and new_rules != set({''}): # Отсеиваем все пустые выводы
			if key in P_new:
				P_new[key] = P_new[key] + list(new_rules)
			else:
				P_new[key] = list(new_rules)
				
	return P_new

def remove_unnatainable_symbols(gramma):
		prev_V = set({gramma.S}) # Первый шаг алгоритма, инициализация начального множества
		set_of_checked_nonterminals = set() 
		# Множество терминалов и нетерминалов
		terminals_and_nonterminals = sorted(gramma.N.union(gramma.T), reverse=True, key=len) 
		while True:
			current_V = set() 
			for x in prev_V - set_of_checked_nonterminals - gramma.T:
				if x in gramma.P:
					set_of_checked_nonterminals = set_of_checked_nonterminals.union({x})
					copy_P = list(gramma.P[x]) # Копия вывода чтобы не изменять исходный массив
					for term in terminals_and_nonterminals:
						for production in copy_P:
							if term in production:	
								production.replace(term, '')
								current_V = current_V.union({term})
			current_V = current_V.union(prev_V)

			if prev_V == current_V: # Проверка на равенство множеств
				break
			else:
				prev_V = current_V
		
		P_new = {}
		for key in gramma.N & prev_V:
			if key in gramma.P:
				P_new[key] = gramma.P[key]
		return Gramma(gramma.N & prev_V, gramma.T & prev_V, P_new, gramma.S)

def remove_lambda_rules(gramma):
	all_rules = [] # список правил вывода
	for key in gramma.P: # Переводим все правила вывода из словаря в пары вида <нетерминал : вывод>
		for rule in gramma.P[key]:
			all_rules.append({key : rule})
	all_rules.sort(key=__comparator, reverse=True) # Поднимаем все лямбда-выводы в самый верх
	lamda_rules, normal_rules = __create_lambda_and_normal_rules_sets(all_rules, gramma.T) # Формируем лямбда-нетерминалы и непустые терминалы
	P_bad = __find_all_bad_rules(all_rules, lamda_rules)
	P_new = __repair_bad_rules(P_bad, lamda_rules, normal_rules)
	all_rules = [rule for rule in all_rules if rule not in P_bad] # Убираем те правила, которые уже исправили
	for pair in all_rules: # Добавляем недостающие правила, которые оканчиваются терминалом
		key = [key for key in pair][0]
		if key in normal_rules and pair[key] != '':
			if key not in P_new:
				P_new[key] = list()
			if pair[key] not in P_new[key]:
				P_new[key].append(pair[key])
	if(gramma.S in lamda_rules): # Проверяем на необходимость изменения аксиомы
		new_N = gramma.N | {'S_new'}
		normal_rules = normal_rules | {'S_new'}
		P_new['S_new'] = ['',gramma.S]
		new_S = 'S_new'
		return Gramma(new_N & normal_rules, gramma.T - {''}, P_new, new_S)
	else: 
		return Gramma(gramma.N & normal_rules, gramma.T - {''}, P_new, gramma.S)

	