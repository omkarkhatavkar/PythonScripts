import urllib2
import json
import time

class GoogleFinanceAPI:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="
    
    def get(self,symbol,exchange):
        url = self.prefix+"%s:%s"%(exchange,symbol)
        u = urllib2.urlopen(url)
        content = u.read()
        
        obj = json.loads(content[3:])
        info = obj[0];
	current_trade_price = float(info["l"].replace(',',''))	    	 # current trade price 
   	previous_day_close  = float(info["pcls_fix"].replace(',',''))    # close price (previous trading day)
    	change_percentage   = str(info["cp"])  				 # change percentage
    	time_updated = str(info["lt"])					 # this is time Stamp	
	return (current_trade_price,previous_day_close,change_percentage,time_updated)
        
        
if __name__ == "__main__":
    c = GoogleFinanceAPI()
    
    while 1:
        quote = c.get("NSE","SBIN")
        print "========================================"
	print quote
        time.sleep(2)
