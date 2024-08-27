def sortDict(unsortedDict):
	sortedDictKeys = []
	for key in unsortedDict.keys():
		valueFound = False
		for i in range(len(sortedDictKeys)):
			name = sortedDictKeys[i]
			if unsortedDict[key] > unsortedDict[name]:
				sortedDictKeys.insert(i, key)
				valueFound = True
				break
		if not valueFound:
			sortedDictKeys.append(key)
			
	sortedDict = {}
	for key in sortedDictKeys:
		sortedDict[key] = unsortedDict[key]

	return sortedDict