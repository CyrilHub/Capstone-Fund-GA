from flask import Flask, render_template, request
import requests
from flask import Flask, render_template, request


app = Flask(__name__)

#separate dictionaries for stock that are held vs stocks that are potential buys
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


class StockCalcs:

    def __init__(self, ticker):   #Class inializer function
        self.tic = ticker

    def held_return(self, current_price):
        #Function calculates the return of stocks that are held
        stock_return = (current_price / held[self.tic]) - 1
        return stock_return

    def watch_distance(self, current_price):
        #Function calculates how far away the current price of a stock on watch is from its target price
        above_target = (current_price / watch[self.tic]) - 1
        return above_target

    def confirm_ticker(self):
        #Function confirms a ticker exists, and if it does returns values from the iextrading.com API.
        api = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(self.tic))
        result = api.json()
        if "quote" in result.keys():
            current_price = '{:,.2f}'.format(api.json()["quote"]["latestPrice"])
            ticker = self.tic
            name = api.json()["quote"]["companyName"]
            return {
                "current_price": current_price,
                "ticker": ticker.upper(),
                "name": name
            }
        else:
            return None


def fetchHeld(ticker):
    #Function scrapes data for stocks in the "held" dictionary.
    #Formating was done here instead of the html pages in order to make it easier to pass values.
    r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(ticker))
    name = r.json()["quote"]["companyName"]
    market_cap = '${:,.2f}'.format(r.json()["quote"]["marketCap"])
    sector = r.json()["quote"]["sector"]
    current_price = '{:,.2f}'.format(r.json()["quote"]["latestPrice"])
    prev_close = '${:,.2f}'.format(r.json()["quote"]["previousClose"])
    purchase_price = '${:,.2f}'.format(held[ticker])
    #This if/else statement is needed because some stocks pass "null" for the PE Ratio instead of a float value
    if r.json()["quote"]["peRatio"] is None:
        pe_ratio = "null"
    else:
        pe_ratio = '{:,.2f}'.format(r.json()["quote"]["peRatio"])
    volume = '{:,.0f}'.format(r.json()["quote"]["latestVolume"])
    avg_volume = '{:,.0f}'.format(r.json()["quote"]["avgTotalVolume"])
    percent_change = '{:,.2%}'.format(r.json()["quote"]["changePercent"])
    x = StockCalcs(ticker=ticker)  #This declares "x" as a StockCalcs object type, allowing the next line of code to use a StockCalcs method
    stock_return = '{:,.2%}'.format(x.held_return(float(current_price)))
    #The return statement passes the values above as a dictionary straight a single variable on the render_template line in @app.route("/<user_ticker>" )
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


# Gets all the data iexTrading has on ticker in the held dictionary and
# returns specific key from that list as dictionary.
# The current market values will be compared to hardcoded value of interest
def fetchWatch(ticker):
    # Gets all the data iexTrading has on ticker which comes is a json
    r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(ticker))
    name = r.json()["quote"]["companyName"]
    # {:,.2f} determines the data's precision, in case 2
    market_cap = '${:,.2f}'.format(r.json()["quote"]["marketCap"])
    sector = r.json()["quote"]["sector"]
    current_price = '{:,.2f}'.format(r.json()["quote"]["latestPrice"])
    prev_close = '${:,.2f}'.format(r.json()["quote"]["previousClose"])
    target_price = watch[ticker]
    #This if/else statement is needed because some stocks pass "null" for the PE Ratio instead of a float value
    if r.json()["quote"]["peRatio"] is None:
        pe_ratio = "null"
    else:
        pe_ratio = '{:,.2f}'.format(r.json()["quote"]["peRatio"])
    volume = '{:,.0f}'.format(r.json()["quote"]["latestVolume"])
    avg_volume = '{:,.0f}'.format(r.json()["quote"]["avgTotalVolume"])
    percent_change = '{:,.2%}'.format(r.json()["quote"]["changePercent"])
    x = StockCalcs(ticker=ticker)   #This declares "x" as a StockCalcs object type, allowing the next line of code to use a StockCalcs method
    above_target = '{:,.2%}'.format(x.watch_distance(float(current_price)))
    #The return statement passes the values above as a dictionary straight a single variable on the render_template line in @app.route("/<user_ticker>" )
    return({
        "name": name,
        "market_cap": market_cap,
        "ticker": ticker,
        "sector": sector,
        "current_price": current_price,
        "prev_close": prev_close,
        "target_price": target_price,
        "above_target" : above_target,
        "pe_ratio": pe_ratio,
        "volume": volume,
        "avg_volume": avg_volume,
        "percent_change" : percent_change
        })


def plotticker(ticker):    
    pass



#The function under @app.after_request prevent formats from being cached.
#We had issues were we updated html files but they didn't

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


@app.route('/', methods = ['GET', 'POST'])
def home():
    #The TRY command allows the site to "exist" if a new ticker has not yet been entered
    try:
        new_ticker = (request.form["input_ticker"])
        ticker_dict = StockCalcs(new_ticker)
        return render_template('home.html', results=ticker_dict.confirm_ticker())   #render template takes file from templates folder, then returns it as a string.
    except:
        return render_template('home.html')


@app.route("/<user_ticker>" )
def company(user_ticker):
    #The if/elif series of commands exists to call different templates depending on the status of each stock (hled vs watch)
    if user_ticker in held:
        return render_template("held.html", x=fetchHeld(user_ticker))
    elif user_ticker in watch:
        return render_template("watch.html", x=fetchWatch(user_ticker))


# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=True)
