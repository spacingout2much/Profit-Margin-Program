import json
import urllib.request


# API will be used to grab prices of deals to use as selling price

meh_json = urllib.request.urlopen('https://api.meh.com/1/current.json?apikey=yourapikeygoeshere').read()
# Converts encoded json data from meh.com api into string.
json_string = str(meh_json,'utf-8')
# Parse's json string to make it an accesible dictionary.
parsed_json = json.loads(json_string)
#acceses the value associated with the 'deal' key in the dictionary.
item_specifics = parsed_json['deal']
#accesses the 'item' list within the 'deal' dictionary.
c_item = item_specifics['items']
# the 'items' list contains a single dictionary within it and is accessed here.
attributes_item = c_item[0]
#within this dictionary is a key of 'price' that unlocks the actual price of the item
#as an integer without shipping.
meh_price = attributes_item['price']
#converts the 'price' value from integer into a float.
meh_flprice = float(meh_price)
#Prints the title of the item and its price on the meh.com website
mehitem = item_specifics['title']
print (item_specifics['title'], "from meh.com is selling at", "%.2f" % meh_flprice, "dollars")
#variable that represents the shipping charge that meh.com charges from any transaction unless you are a vmp member.
meh_shipfee = 5.00
#Change the PM_condition variable to change your profit margin if desired here in percents***********************************
PM_condition = 15
#****************************************************************************************************************************
PM_pertodec = PM_condition / 100
#This is the standard paypal fee anytime you recieve payments to your paypal account.    
def paypal_fee(sellingprice):
    fee = (sellingprice * 0.029)+ 0.30
    return fee

#The ebay fee is 10% of whatever you sell including shipping you charge the buyer that is charged at the end of the month.
def ebay_fee(sellingprice):
    e_fee = sellingprice * 0.10
    return e_fee
#calculate a twenty percent profit margin starting from meh price 
def twentypercent(item_cost):
    #set the sell price to the cost of item to purchase without shipping.
    sellprice = item_cost
    
    profit = sellprice - (item_cost + meh_shipfee + paypal_fee(sellprice) + ebay_fee(sellprice))
    #calculates profit margin after all costs assuming you charge ebay buyer the shipping costs.
    profitmargin = profit / sellprice
    
    while profitmargin < PM_pertodec:
        #iterates until profit margin is no longer less than PM_condition above 
        profit = sellprice - (item_cost + meh_shipfee + paypal_fee(sellprice) + ebay_fee(sellprice))
        profitmargin = profit / sellprice
        #sellprice is increased by a cent until the profit margin reaches PM_condition percent
        sellprice = sellprice + 0.01
        
    else:       
        return sellprice

#This displays the selling price you should sell item on ebay to make a 20% profit margin 
print ("The selling price to make more than a", "%2.0f" % PM_condition, "% profit margin on Ebay is", "%.2f" % twentypercent(meh_flprice), "dollars, including shipping charges to buyer.")

print ("The money made is ", "%.2f" % (twentypercent(meh_flprice) - (meh_flprice + meh_shipfee + paypal_fee(twentypercent(meh_flprice)) + ebay_fee(twentypercent(meh_flprice)) )), "dollars if above conditions are fulfilled.")
