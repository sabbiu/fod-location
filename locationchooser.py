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
    27.691839671753126,
    85.30750751495361
  ],
  [
    27.692143669834316,
    85.30935287475586
  ],
  [
    27.691877671559567,
    85.31068325042725
  ],
  [
    27.692143669834316,
    85.31252861022949
  ],
  [
    27.691725672254414,
    85.31587600708008
  ],
  [
    27.691041672762378,
    85.31999588012695
  ],
  [
    27.69119367301984,
    85.32411575317383
  ],
  [
    27.69119367301984,
    85.32780647277832
  ],
  [
    27.69077567180258,
    85.30561923980713
  ],
  [
    27.690737671612563,
    85.3077220916748
  ],
  [
    27.690623670963152,
    85.30982494354248
  ],
  [
    27.690623670963152,
    85.31162738800049
  ],
  [
    27.690205667563497,
    85.31415939331055
  ],
  [
    27.69024366793867,
    85.31647682189941
  ],
  [
    27.68982566308413,
    85.3221845626831
  ],
  [
    27.689787662563436,
    85.32557487487793
  ],
  [
    27.68670957646487,
    85.32527446746826
  ],
  [
    27.68758360973416,
    85.32209873199463
  ],
  [
    27.688077625443746,
    85.31802177429199
  ],
  [
    27.688191628751646,
    85.31639099121094
  ],
  [
    27.688837645247894,
    85.3157901763916
  ],
  [
    27.690281668300646,
    85.31162738800049
  ],
  [
    27.68974966202954,
    85.30905246734619
  ],
  [
    27.689901664085795,
    85.3057050704956
  ],
  [
    27.687469605791446,
    85.30656337738037
  ],
  [
    27.688267630890756,
    85.30866622924805
  ],
  [
    27.68784961847092,
    85.31167030334473
  ],
  [
    27.68731760034935,
    85.31373023986816
  ],
  [
    27.68716559469563,
    85.3148889541626
  ],
  [
    27.686671574859663,
    85.31720638275146
  ],
  [
    27.68632955981777,
    85.31866550445557
  ],
  [
    27.686139550998284,
    85.32235622406006
  ],
  [
    27.684771477737907,
    85.3242015838623
  ],
  [
    27.68602554554789,
    85.31832218170166
  ],
  [
    27.68545551651053,
    85.31935214996338
  ],
  [
    27.68169325023781,
    85.32338619232178
  ],
  [
    27.683935424530283,
    85.31819343566895
  ],
  [
    27.685303508264685,
    85.31420230865479
  ],
  [
    27.686253556329646,
    85.31330108642578
  ],
  [
    27.68777361604083,
    85.30982494354248
  ],
  [
    27.686747578056828,
    85.30699253082275
  ],
  [
    27.68450546150249,
    85.31076908111572
  ],
  [
    27.680097098117574,
    85.31355857849121
  ],
  [
    27.676676693601085,
    85.30729293823242
  ],
  [
    27.674054310941543,
    85.30596256256104
  ],
  [
    27.672039974270085,
    85.30823707580566
  ],
  [
    27.67117650608259,
    85.31325817108154
  ],
  [
    27.67117650608259,
    85.31325817108154
  ],
  [
    27.67112780959914,
    85.3143310546875
  ],
  [
    27.671925954102655,
    85.3123140335083
  ],
  [
    27.67276209923398,
    85.31278610229492
  ],
  [
    27.674320352631145,
    85.31102657318115
  ],
  [
    27.6733048775205,
    85.31068325042725
  ],
  [
    27.675308501806295,
    85.31712055206299
  ],
  [
    27.672496053749928,
    85.30978202819824
  ],
  [
    27.67261007332242,
    85.31334400177002
  ],
  [
    27.672382034058433,
    85.31965255737305
  ],
  [
    27.676600683395378,
    85.32754898071289
  ],
  [
    27.677968859006334,
    85.33707618713379
  ],
  [
    27.688229629827816,
    85.33969402313232
  ],
  [
    27.682757338692124,
    85.29845237731934
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










