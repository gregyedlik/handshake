import pandas

df = pandas.read_csv('list4.csv', header=None)
df.columns = ['ID', 'data', 'timestamp']

arbIDs = set(df.ID)
dataframes = {arbID: df[df.ID == arbID] for arbID in arbIDs}

#Checking if the stats are the same for each arbID
# for arbID, dataframe in dataframes.items():
#     print("For " + arbID + ":")
#     print(str(len(dataframes[arbID].index)) + " valid recordings")
#     histogram = dataframe.data.value_counts()
#     print(str(len(histogram)) + " unique data values for")
#     repeating_at_least_once = len(histogram[histogram > 1])
#     print(str(repeating_at_least_once) + " repeating data values")
#     ratio = repeating_at_least_once / len(histogram)
#     print(f'{ratio*100:.2f}% there!')

# Evaluating how quickly the hit ratio increases:
df72 = dataframes['0x72']
points = range(5000, 40000, 10000)
for limit in points:
    dataframe = df72[:limit]
    histogram = dataframe.data.value_counts()
    repeating_at_least_once = len(histogram[histogram > 1])
    ratio = repeating_at_least_once / len(histogram)
    print(f'{ratio*100:.2f}% @ ' + str(limit))

# Todo:
# Can we estimate the time needed to capture everything?
# How could we systematically notice patterns in the data?
    # Some bytes have limited range?
# Could I use machine learning to pick it up?!
# Could I collect data faster by bombarding a battery with 72/73?
