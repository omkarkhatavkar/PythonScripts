import csv
from getStock import *
import json
import time
import random

class SortedDisplayDict(dict):
	def __str__(self):
       		return "{" + ", ".join("%r: %r" % (key, self[key]) for key in sorted(self)) + "}"

class GetStockUpdate:

	def getPageUpdate(self):
		with open('/opt/RND/CSV/stock.csv') as f:
			clusterName = dict(filter(None, csv.reader(f)))
		clusterName = SortedDisplayDict(clusterName)
		print clusterName
		f = open('/var/www/html/getStockUpdate.html','w')
		message = """<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content="5"><script src="sorttable.js" type="text/javascript"></script>
</head>
<body>
<table class="sortable" border=5 style="width:75" CELLPADDING="4" CELLSPACING="3">
  <tr style="background-color:Aqua ;">
        <th>Stock Name</th>
        <th>Stock Quote</th>
	<th> LTP </th>
        <th>1 Minute Change</th>
        <th>2 Minute Change</th>
        <th>3 Minute Change</th>
        <th>4 Minute Change</th>
        <th>Today's Change</th>
	<th>CHART<th>
  </tr>
"""
		current = {};
		one_minute = {};
		two_minute = {};
		for key in sorted(clusterName):
 #       		print clusterName[key];
        		Stock_Exchange = "NSE"
        		c = GoogleFinanceAPI()
  		        lp,pp,cp,tp = c.get(Stock_Exchange,clusterName[key].strip(' \t\n\r'))
     	   		current[clusterName[key]] = lp;
			Link_URL = '''<td><a href="https://www.google.com/finance?q=NSE:{0}" target="_blank">LINK</a></td>"'''.format(clusterName[key]);
			#print Link_URL
        		if '-' not in str(cp):
               	 		cp+= "<td style='background-color:LightGreen'>{0}%</td>".format(cp);
        		else:
                		cp+= "<td style='background-color:Red'>{0}%</td>".format(cp);
        		message+= "<tr><td>{1}</td><td>{0}</td><td>{3}</td><td></td><td></td><td></td><td></td>{2}{4}tr>".format( clusterName[key], key,cp, lp, Link_URL)
#		print message
		f.write(message)
		f.close()
		return current
	
	
	def getPageUpdate1(self, one_minute, two_minute ):	
		with open('/opt/RND/CSV/stock.csv') as f:
			clusterName = dict(filter(None, csv.reader(f)))
		clusterName = SortedDisplayDict(clusterName)
#		print clusterName
		f = open('/var/www/html/getStockUpdate.html','w')
		message = """<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content="5"><script src="sorttable.js" type="text/javascript"></script>
</head>
<body><b>Updated On ==>  timestamp</b><br>
<table class="sortable" border=4 style="width:85" CELLPADDING="4" CELLSPACING="3">
  <tr style="background-color:Aqua ;">
        <th>Stock Name</th>
        <th>Stock Quote</th>
	<th> LTP </th>
        <th>1 Minute Change</th>
        <th>2 Minute Change</th>
        <th>3 Minute Change</th>
        <th>4 Minute Change</th>
        <th>Today's Change</th>
	<th> CHART <th>
  </tr>
"""
	
		current = {};
		percentage = 0.0;
		for key in sorted(clusterName):
        	#	print clusterName[key];
        		Stock_Exchange = "NSE"
        		c = GoogleFinanceAPI()
        		lp,pp,cp,tp = c.get(Stock_Exchange,clusterName[key].strip(' \t\n\r'))
        		current[clusterName[key]] = lp;
			Link_URL = '''<td><a href="https://www.google.com/finance?q=NSE:{0}" target="_blank">LINK</a></td>"'''.format(clusterName[key]);
	
			if two_minute[clusterName[key]] < current[clusterName[key]]:
                                percentage2 = (current[clusterName[key]]-two_minute[clusterName[key]])/current[clusterName[key]];
                                percentage2 = percentage2 * 100;
                        else:
                                percentage2 = (two_minute[clusterName[key]]-current[clusterName[key]])/two_minute[clusterName[key]];
                                percentage2 = percentage2 * -100;

			if '-' not in str(percentage2):
                                percentage2 = "<td style='background-color:LightGreen'>{0}%</td>".format(percentage2);
                        else:
                                percentage2 = "<td style='background-color:Red'>{0}%</td>".format(percentage2);



			if one_minute[clusterName[key]] < current[clusterName[key]]:
				percentage = (current[clusterName[key]]-one_minute[clusterName[key]])/current[clusterName[key]];
				percentage = percentage * 100;
			else: 
				percentage = (one_minute[clusterName[key]]-current[clusterName[key]])/one_minute[clusterName[key]];
				percentage = percentage * -100;
        		if '-' not in str(percentage):
				percentage = "<td style='background-color:LightGreen'>{0}%</td>".format(percentage);
			else:
				percentage = "<td style='background-color:Red'>{0}%</td>".format(percentage);

			if '-' not in str(cp):
               			cp= "<td style='background-color:LightGreen'>{0}%</td>".format(cp);
        		else:
                		cp= "<td style='background-color:Red'>{0}%</td>".format(cp);
        		message+= "<tr><td>{1}</td><td>{0}</td><td>{5}</td>{3}{4}<td></td><td></td>{2}{6}</tr>".format(clusterName[key], key, str(cp), str(percentage), str(percentage2), lp,Link_URL);		
			message=message.replace('timestamp',tp)
		f.write(message)
		f.close()
		return (current,one_minute)
	
if __name__ == "__main__":
	test = GetStockUpdate();
	one_minute = test.getPageUpdate();
	time.sleep(2);
	two_minute = one_minute;
	while 1:
		one_minute,two_minute = test.getPageUpdate1(one_minute,two_minute);
		time.sleep(47);
  
                        


                                                                   
