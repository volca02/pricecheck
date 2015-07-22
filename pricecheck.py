#!/usr/bin/python2
import urllib, json, pickle

API_KEY = open("api_key", "r").readline()

interactive=False

def notify(pricestr):
    if interactive:
        print(pricestr)
    from pushbullet import Pushbullet
    pb = Pushbullet(API_KEY)
    pb.push_note("New lowest price", pricestr)

def pricecheck(itemName):
    enc = urllib.quote(itemName)
    url = "http://steamcommunity.com/market/priceoverview/?appid=440&currency=3&market_hash_name=%s" % (enc)
    response = urllib.urlopen(url);
    data = json.loads(response.read())

    # convert to number. If it is lower use pushbullet to inform
    low = data["lowest_price"].split("&")[0]
    low = low.replace(",", ".")
    pc = float(low)

    if interactive:
        print(u"Current lowest prize '%s': %3.2f\u20ac" % (itemName, pc))

    # lowest price persistent storage
    pickleFile = "lowest."+enc+".p"

    # load previous lowest
    lowest = None
    try:
        lowest = pickle.load(open(pickleFile, "rb"))
    except:
        pass

    if lowest:
        if pc != lowest:
	    if pc < lowest:
                notify(u"Lowered price '%s': %3.2f\u20ac (from %3.2f\u20ac)" % (itemName, pc, lowest))
            pickle.dump(pc, open(pickleFile, "wb"))
    else:
        pickle.dump(pc, open(pickleFile, "wb"))


items = [line.rstrip('\n') for line in open('items.txt')]
for item in items:
    pricecheck(item)