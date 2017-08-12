import math
def model_creation(data):
	'''
	This stuff helps in creating model for checking latitude and longitude
	'''
	# Step 1: Convert lat-lng to array
	converted = {}
	for hotel in data:
		converted[hotel] = [[float(loc) for loc in latlng.split(',')] for latlng in data[hotel]]
		# converted[hotel] = [[int(float(loc)*10**10) for loc in latlng.split(',')] for latlng in data[hotel]]
	print ('Step 1: lat-lng converted to array')
	# print (converted)

	# Step 2: Create min-max latlng array
	minmax = {}
	for hotel in converted:
		minmax[hotel] = {
			'min': converted[hotel][0][:],
			'max': converted[hotel][0][:]
		}
		for latlng in converted[hotel][1:]:
			if minmax[hotel]['min'][0] > latlng[0]:
				minmax[hotel]['min'][0] = latlng[0]
			else:
				minmax[hotel]['max'][0] = latlng[0]
			if minmax[hotel]['min'][1] > latlng[1]:
				minmax[hotel]['min'][1] = latlng[1]
			else:
				minmax[hotel]['max'][1] = latlng[1]
	print ('Step 2: minmax array')
	# print (minmax)

	# Step 3: Sort lat min to max -> latLeft and max to min -> latRight,
	#			   lng min to max -> lngLeft and max to min -> lngRight
	latLeft = sorted((minmax[hotel]['min'][0], hotel) for hotel in minmax)
	latRight = sorted((minmax[hotel]['max'][0], hotel) for hotel in minmax)
	lngLeft = sorted((minmax[hotel]['min'][1], hotel) for hotel in minmax)
	lngRight = sorted((minmax[hotel]['max'][1], hotel) for hotel in minmax)
	print ('Step 3: sorting')
	# print (latLeft, '\n', latRight, '\n', lngLeft, '\n', lngRight)

	# Step 4: 'Mean'
	print ('Step 4: Mean')
	latMean = (latLeft[len(latLeft)//2 - 1][0] + latRight[len(latRight)//2 - 1][0])/2
	# print(latMean)
	lngMean = (lngLeft[len(lngLeft)//2 - 1][0] + lngRight[len(lngRight)//2 - 1][0])/2
	# print(lngMean)


	# Final model
	model = {
		'data': data,
		'minmax': minmax,
		'latLeft': latLeft,
		'latRight': latRight,
		'lngLeft': lngLeft,
		'lngRight': lngRight,
		'latMean': latMean,
		'lngMean': lngMean
	}

	return model


def location_in(model, location):
	'''
	Using created model and given lat-lng, it states which hotel is the location close to
	'''
	selected_hotels = []
	lat = location[0]
	lng = location[1]

	selected = ''
	if lat > model['latMean']:
		latdiff = abs(model['latRight'][len(model['latRight'])-1][0] - lat)
		if lng > model['lngMean']:
			lngdiff = abs(model['lngRight'][len(model['lngRight'])-1][0] - lng)
			if latdiff > lngdiff:
				selected = 'lngRight'
			else:
				selected = 'latRight'
		else:
			lngdiff = abs(model['lngLeft'][len(model['lngLeft'])-1][0] - lng)
			if latdiff > lngdiff:
				selected = 'lngLeft'
			else:
				selected = 'latRight'
		print(latdiff, lngdiff)
	else:
		latdiff = abs(model['latLeft'][len(model['latLeft'])-1][0] - lat)
		if lng > model['lngMean']:
			lngdiff = abs(model['lngRight'][len(model['lngRight'])-1][0] - lng)
			if latdiff > lngdiff:
				selected = 'lngRight'
			else:
				selected = 'latLeft'
		else:
			lngdiff = abs(model['lngLeft'][len(model['lngLeft'])-1][0] - lng)
			if latdiff > lngdiff:
				selected = 'lngLeft'
			else:
				selected = 'latLeft'
		print(latdiff, lngdiff)
	print(selected)

	if selected == 'latLeft' or selected == 'lngLeft':
		if selected == 'latLeft':
			value = lat
		if selected == 'lngLeft':
			value = lng
		low = 0
		high = len(model[selected]) -1
		while low != high:
			mid = math.ceil((low + high)/2)
			print (mid)
			if model[selected][mid][0] > lat:
				high = mid - 1
			else:
				low = mid
		index = low

	if selected == 'latRight' or selected == 'lngRight':
		if selected == 'latRight':
			value = lat
		if selected == 'lngRight':
			value = lng
		low = 0
		high = len(model[selected]) - 1
		while low != high:
			mid = (low + high)//2 # forcing integer value
			print (mid)
			if model[selected][mid][0] < value:
				low = mid+1
			else:
				high = mid
		index = low

	print (index)
	print (model[selected])

	

	

	return selected_hotels




# function calls
data = {
	'acem': ['27.6892487, 85.31624458', '27.69209872, 85.31055829', '27.68848868, 85.30789754', '27.68504954, 85.31508586', '27.68744365, 85.3171458'],
	'himalayanhotel': ['27.68875469, 85.31723163', '27.6862656, 85.31218908', '27.67934906, 85.32411954', '27.68694963, 85.32605073'],
	'bhatti': ['27.6862276, 85.31708142', '27.68634161, 85.31862638', '27.68485953, 85.3200855'],
	'zoo': ['27.67155793, 85.30712507', '27.67532055, 85.31068704', '27.67304019, 85.31407735', '27.67026569,85.3119745']
}
model = model_creation(data)
location = [27.6848595,85.3200855]
selected_hotels = location_in(model, location)
print (selected_hotels)



# '''
# tests
# '''
# a = [1,2,3,4]
# a = [1,2,3,4, 5]
# val = 8
# val = 0
# val = 3.5

# # lefty
# low = 0
# high = len(a) -1
# while low != high:
# 	mid = math.ceil((low + high)/2) # forcing integer value
# 	print (mid)
# 	if a[mid] > val:
# 		high = mid -1
# 	else:
# 		low = mid
# print(low,high)

# # righty
# low = 0
# high = len(a) - 1
# while low != high:
# 	mid = (low + high)//2 # forcing integer value
# 	print (mid)
# 	if a[mid] < val:
# 		low = mid+1
# 	else:
# 		high = mid
# print(low,high)


# '''
# models algorithms
# '''
# for x in ['latLeft']:
# 	low = 0
# 	high = len(model[x]) -1
# 	while low != high:
# 		mid = math.ceil((low + high)/2) # forcing integer value
# 		print (mid)
# 		if model[x][mid][0] > lat:
# 			high = mid - 1
# 		else:
# 			low = mid
# 	print (x, '===>', low, high, '\n---------\n', model[x])

# for x in ['latRight']:
# 	low = 0
# 	high = len(model[x]) - 1
# 	while low != high:
# 		mid = (low + high)//2 # forcing integer value
# 		print (mid)
# 		if model[x][mid][0] < lat:
# 			low = mid+1
# 		else:
# 			high = mid
# 	print (x, '===>', low, high, '\n---------\n', model[x])

# for x in ['lngLeft']:
# 	low = 0
# 	high = len(model[x]) -1
# 	while low != high:
# 		mid = math.ceil((low + high)/2) # forcing integer value
# 		print (mid)
# 		if model[x][mid][0] > lng:
# 			high = mid -1
# 		else:
# 			low = mid
# 	print (x, '===>', low, high, '\n---------\n', model[x])

# for x in ['lngRight']:
# 	low = 0
# 	high = len(model[x]) - 1
# 	while low != high:
# 		mid = (low + high)//2 # forcing integer value
# 		print (mid)
# 		if model[x][mid][0] < lng:
# 			low = mid+1
# 		else:
# 			high = mid
# 	print (x, '===>', low, high, '\n---------\n', model[x])










