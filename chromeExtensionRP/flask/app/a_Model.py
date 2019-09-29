def ModelIt(event):
	# result = title.upper()
	import numpy as np
	import pandas as pd
	import datetime as dt
	import pickle


	# define an empty list
	columns = []

	# open file and read the content in a list
	with open('./app/columns.txt', 'r') as filehandle:
	    for line in filehandle:
	        # remove linebreak which is the last character of the string
	        current_col = line[:-1]

	        # add item to the list
	        columns.append(current_col)

	# initiate data series
	a = np.zeros(shape=(1,len(columns)))
	event_data = pd.DataFrame(a,columns=columns)

	created_dt = pd.Timestamp.now()
	published_dt = pd.Timestamp.now() + dt.timedelta(minutes=5)

	start_utc_dt = pd.to_datetime(event['eventStart'])
	start_local_dt = pd.to_datetime(event['eventStart'])
	end_utc_dt = pd.to_datetime(event['eventEnd'])
	end_local_dt = pd.to_datetime(event['eventEnd'])

	event_data['start_DOY'] = start_local_dt.dayofyear
	event_data['end_DOY'] = end_local_dt.dayofyear

	event_data['start_hour_' + str(start_local_dt.hour)] = start_local_dt.hour
	event_data['start_DOW_' + str(start_local_dt.dayofweek)] = start_local_dt.dayofweek
	event_data['start_DOM_' + str(start_local_dt.day)] = start_local_dt.day
	event_data['start_MOY_' + str(start_local_dt.month)] = start_local_dt.month
	event_data['start_year_' + str(start_local_dt.year)] = start_local_dt.year

	event_data['end_hour_' + str(end_local_dt.hour)] = end_local_dt.hour
	event_data['end_DOW_' + str(end_local_dt.dayofweek)] = end_local_dt.dayofweek
	event_data['end_DOM_' + str(end_local_dt.day)] = end_local_dt.day
	event_data['end_MOY_' + str(end_local_dt.month)] = end_local_dt.month
	event_data['end_year_' + str(end_local_dt.year)] = end_local_dt.year


	event_data['created_to_publish'] = (published_dt - created_dt).total_seconds()//60
	event_data['publish_to_start'] = (start_utc_dt - published_dt).total_seconds()//60
	event_data['start_to_end'] = (end_utc_dt - start_utc_dt).total_seconds()//60



	event_data['start_tz_' + event['timeZone']] = 1




	first_two_zip_digits = event['zip'][:2]
	event_data['postal_region_'+first_two_zip_digits] = first_two_zip_digits

	if event['format'] == '':
	    event_data['format_id_-999.0'] = 1
	else:
	    event_data['format_id_' + event['format'] + '.0'] = event['format']
	    
	if event['category'] == '':
	    event_data['category_id_-999.0'] = 1
	else:
	    event_data['category_id_' + event['category'] + '.0'] = event['category']

	if event['subcategory'] == '':
	    event_data['subcategory_id_-999.0'] = 1
	else:
	    event_data['subcategory_id_' + event['subcategory'] + '.0'] = event['subcategory']

	if (event['city'] == '') & (event['state'] == '') & (event['zip'] == ''):
	    event_data['online_event_0.0'] = 0
	else:
	    event_data['online_event_0.0'] = 1


	# Impute some values
	event_data['is_paid_0.0'] = 0
	event_data['shareable_0.0'] = 0
	event_data['free_0.0'] = 0
	event_data['donation_0.0'] = 0
	event_data['on_sale_status_SOLD_OUT'] = 1


	pkl_filename = './app/RightPrice_model.pkl'

	with open(pkl_filename, 'rb') as file:
	    pickle_model = pickle.load(file)

	Ypredict = pickle_model.predict(event_data)
	# print("Suggested price: $%.2f" % float(Ypredict))

	return Ypredict
		# return result