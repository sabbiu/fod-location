import math
from matplotlib import path

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
			if minmax[hotel]['max'][0] < latlng[0]:
				minmax[hotel]['max'][0] = latlng[0]
			if minmax[hotel]['min'][1] > latlng[1]:
				minmax[hotel]['min'][1] = latlng[1]
			if minmax[hotel]['max'][1] < latlng[1]:
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

	# Step 5: 'Polygon for all the hotels'
	polygons = {}
	for hotel in converted:
		p = None
		p = path.Path(converted[hotel])
		polygons[hotel] = p

	# Final model
	model = {
		'data': converted,
		'polygons': polygons,
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
	# print(lat, lng)
	selected = ''
	if lat > model['latMean']:
		latdiff = abs(model['latMean'] - lat)

		if lng > model['lngMean']:
			lngdiff = abs(model['lngMean'] - lng)
			if latdiff > lngdiff:
				selected = 'lngRight'
			else:
				selected = 'latRight'
		else:
			lngdiff = abs(model['lngMean'] - lng)
			if latdiff > lngdiff:
				selected = 'lngLeft'
			else:
				selected = 'latRight'
		# print(latdiff, lngdiff)
	else:
		latdiff = abs(model['latMean'] - lat)
		if lng > model['lngMean']:
			lngdiff = abs(model['lngMean'] - lng)
			if latdiff > lngdiff:
				selected = 'lngRight'
			else:
				selected = 'latLeft'
		else:
			lngdiff = abs(model['lngMean'] - lng)
			if latdiff > lngdiff:
				selected = 'lngLeft'
			else:
				selected = 'latLeft'
		# print(latdiff, lngdiff)

	if selected == 'latLeft' or selected == 'lngLeft':
		if selected == 'latLeft':
			value = lat
		if selected == 'lngLeft':
			value = lng
		low = 0
		high = len(model[selected]) -1
		while low != high:
			mid = math.ceil((low + high)/2)
			# print (mid)
			if model[selected][mid][0] > value:
				high = mid - 1
			else:
				low = mid
		index = low + 1 # plus one because of slicing in next step

	if selected == 'latRight' or selected == 'lngRight':
		if selected == 'latRight':
			value = lat
		if selected == 'lngRight':
			value = lng
		low = 0
		high = len(model[selected]) - 1
		while low != high:
			mid = (low + high)//2 # forcing integer value
			# print (mid)
			if model[selected][mid][0] < value:
				low = mid+1
			else:
				high = mid
		index = low

	print(selected)
	# print (index)
	# print (model[selected])
	filtered_hotels = []
	if selected == 'latRight':
		for item in model[selected][index:]:
			# print ( item[1] )
			# print ( model['minmax'][item[1]]['min'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )	
			# print ( model['minmax'][item[1]]['max'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )

			if model['minmax'][item[1]]['min'][0] <= lat and model['minmax'][item[1]]['min'][1] <= lng and model['minmax'][item[1]]['max'][1] >= lng:
				filtered_hotels.append(item[1])
	if selected == 'latLeft':
		for item in model[selected][:index]:
			# print ( item[1] )
			# print ( model['minmax'][item[1]]['min'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )	
			# print ( model['minmax'][item[1]]['max'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )

			if model['minmax'][item[1]]['max'][0] >= lat and model['minmax'][item[1]]['min'][0] <= lng and model['minmax'][item[1]]['max'][1] >= lng:
				filtered_hotels.append(item[1])

	if selected == 'lngLeft':
		for item in model[selected][:index]:
			# print ( item[1] )
			# print ( model['minmax'][item[1]]['min'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )	
			# print ( model['minmax'][item[1]]['max'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )

			if model['minmax'][item[1]]['min'][0] <= lat and model['minmax'][item[1]]['max'][0] >= lat and model['minmax'][item[1]]['max'][1] >= lng:
				filtered_hotels.append(item[1])

	if selected == 'lngRight':
		for item in model[selected][index:]:
			# print ( item[1] )
			# print ( model['minmax'][item[1]]['min'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )	
			# print ( model['minmax'][item[1]]['max'][0] )	
			# print ( model['minmax'][item[1]]['min'][1] )

			if model['minmax'][item[1]]['min'][0] <= lat and model['minmax'][item[1]]['max'][0] >= lat and model['minmax'][item[1]]['min'][1] <= lng:
				filtered_hotels.append(item[1])

	for hotel in filtered_hotels:
		if model['polygons'][hotel].contains_point((lat, lng)):
			selected_hotels.append(hotel)

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
location = [27.672785, 85.311146]
location = [27.690083, 85.312722]
location = [27.6728001056788, 85.31089782714844]
for i,location in enumerate([
  [
    27.679551384508493,
    85.32400846481323
  ],
  [
    27.68686692672062,
    85.3258752822876
  ],
  [
    27.688576982801756,
    85.3172492980957
  ],
  [
    27.68622089856461,
    85.31235694885254
  ],
  [
    27.684890828561496,
    85.31521081924438
  ],
  [
    27.68652491229059,
    85.31677722930908
  ],
  [
    27.687759959348572,
    85.31759262084961
  ],
  [
    27.68663891721963,
    85.3187084197998
  ],
  [
    27.68441579963428,
    85.3204894065857
  ],
  [
    27.68502383629082,
    85.3179144859314
  ],
  [
    27.686182896789326,
    85.31748533248901
  ],
  [
    27.686239899447273,
    85.31855821609497
  ],
  [
    27.685270850215502,
    85.31941652297974
  ],
  [
    27.68585988116562,
    85.31834363937378
  ],
  [
    27.68597388678899,
    85.31851530075073
  ],
  [
    27.688481980388758,
    85.30821561813354
  ],
  [
    27.69190201517862,
    85.31059741973877
  ],
  [
    27.68916599591736,
    85.31609058380127
  ],
  [
    27.688576982801756,
    85.31641244888306
  ],
  [
    27.687626954951984,
    85.31688451766968
  ],
  [
    27.685365855422372,
    85.3149962425232
  ],
  [
    27.686391906389623,
    85.3126573562622
  ],
  [
    27.688177972111657,
    85.31632661819458
  ],
  [
    27.68646790978144,
    85.3144383430481
  ],
  [
    27.686790923606527,
    85.3142237663269
  ],
  [
    27.686752922029637,
    85.31227111816406
  ],
  [
    27.687474949728912,
    85.31418085098267
  ],
  [
    27.68850098087798,
    85.31162738800049
  ],
  [
    27.68910899478699,
    85.31167030334473
  ]
]):
	selected_hotels = location_in(model, location)
	print ('********************** ',i+3,selected_hotels)



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










