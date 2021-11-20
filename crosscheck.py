import pandas

# The goal here is to see if the handshake looks the same or not when using a different battery.
# I shall have a list of all the 0x72s in the scott recordings, and the same for the other. Each should be a set.
# Then I shall see how many elements are there in their intersection.


def getdata(filename):
    df = pandas.read_csv(filename, header=None)
    df.columns = ['ID', 'data', 'timestamp']
    df['Int'] = [int(proba.replace(' ', ''), 16) for proba in df.data]
    return df


def get72s(filename):
    df = getdata(filename)
    arbIDs = set(df.ID)
    dataframes = {arbID: df[df.ID == arbID] for arbID in arbIDs}

    df72 = dataframes['0x72'].copy()
    return set(df72.Int)


values_scott = get72s('list_scott.csv')
values_badconnector = get72s('list_badconnector.csv')
intersection = values_scott.intersection(values_badconnector)
print(str(len(intersection)) + " 0x72s have appeared identical in both datasets.")

# Now the question is - do the handshakes completely match, or only the 0x72s?
# I could go through the intersection, and select each handshake from both datasets and compare them.

df = getdata('list_scott.csv')
#df = df[:20000]
timestamps = set(df.timestamp)
handshakes = [df[df.timestamp == ts] for ts in timestamps]
handshakes_intersecting = []
for hs in handshakes:
    hs72 = hs[hs.ID == '0x72']
    if hs72.Int.values[0] in intersection:
        handshakes_intersecting.append(hs)

handshakesdict = {
    df.timestamp.values[0]:
        {
            0x72: df[df.ID == '0x72'].Int.values[0],
            0x73: df[df.ID == '0x73'].Int.values[0],
            0x80: df[df.ID == '0x80'].Int.values[0],
            0x81: df[df.ID == '0x81'].Int.values[0]
        }
    for df in handshakes_intersecting
}

handshakes_scott = pandas.DataFrame(handshakesdict)
scott = handshakes_scott.transpose()
