#project example 1

from flask import Flask, render_template
import requests
import CPB_Capstone



app = Flask(__name__)



def fetchCompany(ticker):
    CPB_Capstone.print_test()
    
    # GET request to url www.iextrading.com/company_name
    r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(ticker))
    name = r.json()["quote"]["companyName"]
    market_cap = r.json()["quote"]["marketCap"]
    return({
        "name": name,
        "market_cap": market_cap,
        "ticker": ticker
    })

@app.route('/')
def home():
    return render_template('home.html')   #render template takes file from templates folder, then returns it as a string.

@app.route("/<user_ticker>" )
def company(user_ticker):
    import CPB_Capstone

    return render_template("company.html", x=fetchCompany(user_ticker))


# Run the app when the program starts!
if __name__ == '__main__':
    print ("help")
    app.run(debug=True)
    # fetchCompany("goog")


