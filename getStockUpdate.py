import csv
from getStock import *
import json

class SortedDisplayDict(dict):
   def __str__(self):
       return "{" + ", ".join("%r: %r" % (key, self[key]) for key in sorted(self)) + "}"

with open('/opt/RND/CSV/stock.csv') as f:
    clusterName = dict(filter(None, csv.reader(f)))
clusterName = SortedDisplayDict(clusterName) 
print clusterName

f = open('/var/www/html/getStockUpdate.html','w')
message = """<!DOCTYPE html>
<html>
<head>
</head>
<body>
<table border=5 style="width:75" CELLPADDING="4" CELLSPACING="3">
  <tr style="background-color:Aqua ;">
	<th>Stock Name</th>
	<th>Stock Quote</th>
	<th>2 Minute Change</th>
	<th>3 Minute Change</th>
	<th>4 Minute Change</th>
	<th>5 Minute Change</th>
	<th>Today's Change</th>
  </tr>
"""
current = {};
one_minute = {};
two_minute = {};


for key in sorted(clusterName):
	print clusterName[key];
	Stock_Exchange = "NSE"
	c = GoogleFinanceAPI()
	lp,pp,cp,tp = c.get(Stock_Exchange,clusterName[key].strip(' \t\n\r'))
	current[clusterName[key]] = lp;
	if '-' not in str(cp):
		cp+= "<td style='background-color:LightGreen'>{0}%</td>".format(cp);
	else:
		cp+= "<td style='background-color:Red'>{0}%</td>".format(cp);
	message+= "<tr><td>{1}</td><td>{0}</td><td></td><td></td><td></td><td></td>{2}</tr>".format( clusterName[key], key,cp)
print message
print current
f.write(message)
f.close()

