#project example 1

from flask import Flask, render_template
import requests
import csv

app = Flask(__name__)


held = {
        'dis' : 87.76,
        'nvda' : 19.62,
        'kopn' : 3.32,
        'calm' : 41.61,
        'cor' : 103.67,
        'grub' : 131.76,
        'kbr' : 20.79,
        'pcar' : 68.17,
        'shop' : 146.7,
        'swir' : 27.16,
        'ttwo' : 124.56,
        'xyl' : 67.25
        }

watch = {
        'chrw' : 85.00,
        'ddd' : 10.50,
        'rop' : 288.50,
        'mtch' : 45.75
        }

sold = {
        'ba' : [20.78, "April 2, 2018"],
        'x' : [33.94, "April 23, 2018"],
        'rgnx' : [70.45, "August 1, 2018"],
        'hpq' : [25.77, "September 1, 2018"],
        }



class StockCalcs:

    def __init__(self, ticker):
        self.tic = ticker

    def held_return(self, current_price):
        stock_return = (current_price / held[self.tic]) - 1
        return stock_return

    def watch_distance(self, current_price):
        above_target = (current_price / watch[self.tic]) - 1
        return above_target

    def change_since_sale(self, current_price):
        post_sale_perf = (current_price / sold[self.tic]) - 1
        return post_sale_perf

def fetchHeld(ticker):
    # GET request to url www.iextrading.com/company_name
    r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(ticker))
    name = r.json()["quote"]["companyName"]
    market_cap = '${:,.2f}'.format(r.json()["quote"]["marketCap"])
    sector = r.json()["quote"]["sector"]
    current_price = '{:,.2f}'.format(r.json()["quote"]["latestPrice"])
    prev_close = '${:,.2f}'.format(r.json()["quote"]["previousClose"])
    purchase_price = '${:,.2f}'.format(held[ticker])
    if r.json()["quote"]["peRatio"] is None:
        pe_ratio = "null"
    else:
        pe_ratio = '{:,.2f}'.format(r.json()["quote"]["peRatio"])
    volume = '{:,.0f}'.format(r.json()["quote"]["latestVolume"])
    avg_volume = '{:,.0f}'.format(r.json()["quote"]["avgTotalVolume"])
    percent_change = '{:,.2%}'.format(r.json()["quote"]["changePercent"])
    x = StockCalcs(ticker)
    stock_return = '{:,.2%}'.format(x.held_return(float(current_price)))
    return({
        "name": name,
        "market_cap": market_cap,
        "ticker": ticker,
        "sector": sector,
        "current_price": current_price,
        "prev_close": prev_close,
        "purchase_price": purchase_price,
        "pe_ratio": pe_ratio,
        "volume": volume,
        "avg_volume": avg_volume,
        "stock_return" : stock_return,
        "percent_change" : percent_change
        })

def fetchWatch(ticker):
    r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(ticker))
    name = r.json()["quote"]["companyName"]
    market_cap = r.json()["quote"]["marketCap"]
    sector = r.json()["quote"]["sector"]
    current_price = r.json()["quote"]["latestPrice"]
    prev_close = r.json()["quote"]["previousClose"]
    target_price = watch[ticker]
    x = StockCalcs(ticker)
    above_target = x.watch_distance(current_price)
    return({
        "name": name,
        "market_cap": market_cap,
        "ticker": ticker,
        "sector": sector,
        "current_price": current_price,
        "prev_close": prev_close,
        "target_price": target_price,
        "above_target" : above_target
        })

def fetchSold(ticker):
    r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(ticker))
    name = r.json()["quote"]["companyName"]
    market_cap = r.json()["quote"]["marketCap"]
    sector = r.json()["quote"]["sector"]
    current_price = r.json()["quote"]["latestPrice"]
    prev_close = r.json()["quote"]["previousClose"]
    price_sold = sold[ticker][0]
    date_sold = sold[ticker][1]
    x = StockCalcs(ticker)
    post_sale_performance = x.change_since_sale(current_price)
    return({
        "name": name,
        "market_cap": market_cap,
        "ticker": ticker,
        "sector": sector,
        "current_price": current_price,
        "prev_close": prev_close,
        "target_price": target_price,
        "above_target" : above_target
        })

    # parse request into databse

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def home():
    return render_template('home.html')   #render template takes file from templates folder, then returns it as a string.

@app.route("/<user_ticker>" )
def company(user_ticker):
    if user_ticker in held:
        return render_template("held.html", x=fetchHeld(user_ticker))
    elif user_ticker in watch:
        return render_template("watch.html", x=fetchWatch(user_ticker))
    elif user_ticker in sold:
        return render_template("sold.html", x=fetchSold(user_ticker))

# @app.route("/<user_ticker>" )
# def company(user_ticker):
#     return render_template("watch.html", x=fetchwWatch(user_ticker))






#
# with open('stocks_dis.csv', 'a', newline='') as csvfile:
#   # These are the header row values at the top.
#   fieldnames = ['purchase','target', 'current', 'date_time', 'change']
#   # This opens the `DictWriter`.
#   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#   # Write out the header row (this only needs to be done once!).
#   writer.writeheader()
#   # Write as many rows as you want!
#   for i in employees:
#     writer.writerow(i)

# fieldnames = ['purchase','target', 'current', 'date_time', 'change']
# with open('stocks_dis.csv','a',newline='') as f:
#     writer=csv.writer(f)
#     y = fetchCompany("dis")
#     writer.writerow([0,0,y["current_price"],0,0])

# with open('mycsvfile.csv') as f:
#     print(f.read())




# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=True)
    # fetchCompany("goog")


# with open('stocks_dis.csv','a',newline='') as f:
#     writer=csv.writer(f)
#     y = fetchCompany("dis")
#     writer.writerow([0,0,y["current_price"],0,0])
#
# r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format("kopn"))
# print(r.json()["quote"]["peRatio"])
