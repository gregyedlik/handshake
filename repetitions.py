import pandas
import matplotlib.pyplot as plt

df = pandas.read_csv('list_scott.csv', header=None)
df.columns = ['ID', 'data', 'timestamp']
df['Int'] = [int(proba.replace(' ', ''), 16) for proba in df.data]

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
df72 = dataframes['0x72'].copy()
points = range(2000, len(df72.index), 2000)
diagram = {}
for limit in points:
    dataframe = df72[:limit]
    histogram = dataframe.data.value_counts()
    repeating_at_least_once = len(histogram[histogram > 1])
    ratio = repeating_at_least_once / len(histogram)
    diagram[limit] = ratio*100
    print(f'{ratio*100:.2f}% @ ' + str(limit))

fig, ax = plt.subplots()
ax.plot(diagram.keys(), diagram.values())
ax.set_xlabel('Number of recorded handshakes')
ax.set_ylabel('Reoccurance rate [%]')
ax.set_title('Learning progress')
plt.show()

# Seeing if there is any gap in the numbers covering the range they have available:
# fig, ax = plt.subplots(2, 2)
# ax[0, 0].hist(dataframes['0x72'].Int, bins=1000)
# ax[0, 0].set_xlabel('Data as 64bit unsigned int, 0x72')
# ax[0, 1].hist(dataframes['0x73'].Int, bins=1000)
# ax[0, 1].set_xlabel('Data as 64bit unsigned int, 0x73')
# ax[1, 0].hist(dataframes['0x80'].Int, bins=1000)
# ax[1, 0].set_xlabel('Data as 64bit unsigned int, 0x80')
# ax[1, 1].hist(dataframes['0x81'].Int, bins=1000)
# ax[1, 1].set_xlabel('Data as 64bit unsigned int, 0x81')
# plt.show()

# This has only really proved that the first byte has full range. Let's bitbang a bit!
# interesting = '0x81'
# fig, ax = plt.subplots(4, 2)
# filtered = [(i & int('0xFF00000000000000', 16)) >> 56 for i in dataframes[interesting].Int]
# ax[0, 0].hist(filtered, bins=256)
# ax[0, 0].set_xlabel(interesting + ', MSB')
# filtered = [(i & int('0x00FF000000000000', 16)) >> 48 for i in dataframes[interesting].Int]
# ax[0, 1].hist(filtered, bins=256)
# filtered = [(i & int('0x0000FF0000000000', 16)) >> 40 for i in dataframes[interesting].Int]
# ax[1, 0].hist(filtered, bins=256)
# filtered = [(i & int('0x000000FF00000000', 16)) >> 32 for i in dataframes[interesting].Int]
# ax[1, 1].hist(filtered, bins=256)
# filtered = [(i & int('0x00000000FF000000', 16)) >> 24 for i in dataframes[interesting].Int]
# ax[2, 0].hist(filtered, bins=256)
# filtered = [(i & int('0x0000000000FF0000', 16)) >> 16 for i in dataframes[interesting].Int]
# ax[2, 1].hist(filtered, bins=256)
# filtered = [(i & int('0x000000000000FF00', 16)) >> 8 for i in dataframes[interesting].Int]
# ax[3, 0].hist(filtered, bins=256)
# filtered = [i & int('0x00000000000000FF', 16) for i in dataframes[interesting].Int]
# ax[3, 1].hist(filtered, bins=256)
# ax[3, 1].set_xlabel(interesting + ', LSB')
# plt.show()

# They look all the same, and all flat.. all bits take all values.




# Todo:
# Can we estimate the time needed to capture everything?
# How could we systematically notice patterns in the data?
# Could I use machine learning to pick it up?!
# Could I collect data faster by bombarding a battery with 72/73?
