#load alerts-processed.json file on panda
alerts = pd.read_json('/Users/marsescobin/Downloads/alerts-processed.json')
jams = pd.read_json('/Users/marsescobin/Downloads/jams-processed.json')

#examine how big data set is 
alerts.shape
jams.shape
#examine if there are missing data points in the dataset
alerts.isna().sum()
#get a feel of the data 
alerts.describe()
#convert pubMillis into human readable date and time format
alerts['date_time'] = alerts['pubMillis'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000, tz= pytz.timezone('Asia/Hong_Kong')))

jams['date_time'] = jams['pubMillis'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000, tz= pytz.timezone('Asia/Hong_Kong')))


#breakdown of alert types
alerts.type.value_counts()

#breakdown of alert subtypes 
alerts_subtype = alerts.subtype.value_counts()
alerts_subtype.plot(kind = 'bar')

#breakdown thumbsup based on Report Rating
alerts.groupby('reportRating').nThumbsUp.count()

#breakdown of alerts based on Report Rating 
alerts.groupby('reportRating').pubMillis.count()

#breakdown of alerts based on reliability
alerts.groupby('reliability').pubMillis.count()

#breakdown of alerts based on confidence 
alerts.groupby('confidence').pubMillis.count()

#get alerts vs date 
alerts['date'] = alerts['date_time'].dt.date
alerts['time'] = alerts['date_time'].dt.time
alerts.groupby('date').pubMillis.count()

#get jams vs date
jams['date'] = jams['date_time'].dt.date
jams['time'] = jams['date_time'].dt.time

#get alerts vs hour
alerts['date_hour'] = alerts['date_time'].dt.floor('h')
alerts['hour'] = alerts['date_hour'].dt.time

#get jams vs hour
jams['date_hour'] = jams['date_time'].dt.floor('h')
jams['hour'] = jams['date_hour'].dt.time

#breakdown alerts by subtype vs hour 
alerts.groupby(['hour', 'subtype']).pubMillis.count()


#Most jammed streets vs hours of the day
pd.set_option("display.max_columns", 999)
unpivoted_jams = jams.groupby(['hour', 'street']).pubMillis.count().reset_index()
unpivoted_jams.pivot(columns = 'hour', index = 'street', values = 'pubMillis')

#Average delay per hour on most jammed streets
unpivoted_delays = jams.groupby(['hour', 'street']).delay.mean().reset_index()
unpivoted_delays.pivot(columns = 'hour', index = 'street', values = 'delay')


#Average congestion level per hour on most jammed streets
unpivoted_level = jams.groupby(['hour', 'level']).pubMillis.count().reset_index()
unpivoted_level.pivot(columns = 'hour', index = 'level', values = 'pubMillis')
