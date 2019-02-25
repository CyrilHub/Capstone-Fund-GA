#project example 1

from flask import Flask, render_template
import requests
import CVS


app = Flask(__name__)



#given a csv, load into dictionary called database
def loadDictionary(filename):
    database = {}

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line=0
        for row in csv_reader:
            if line == 0:
                pass
            else:
                username = row[0]
                ticker = row[1]
                if username in database.keys():
                    database[username]["tickers"].append(ticker)
                else:
                    database[username] = {
                        "tickers": [ticker]
                    }



def fetchCompany(ticker):
    # GET request to url www.iextrading.com/company_name
    r = requests.get("https://api.iextrading.com/1.0/stock/{}/book".format(ticker))
    # if r.json() == {}:
    #     name = "COMPANY NOT FOUND"
    #     market_cap = "?"
    #     return ({"name": name, "market_cap":market_cap, "ticker":ticker})
    name = r.json()["quote"]["companyName"]
    market_cap = r.json()["quote"]["marketCap"]
    return({
        "name": name,
        "market_cap": market_cap,
        "ticker": ticker
    })

    # parse request into databse

@app.route('/')
def home():
    return render_template('home.html')   #render template takes file from templates folder, then returns it as a string.

@app.route("/<user_ticker>" )
def company(user_ticker):

    return render_template("company.html", x=fetchCompany(user_ticker))


# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=True)
    # fetchCompany("goog")




# Creating CVS files
with open('stock.csv', 'w', newline='') as csvfile:
  # These are the header row values at the top.
  fieldnames = ['Current_Price' ]
  # This opens the `DictWriter`. 
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  # Write out the header row (this only needs to be done once!). 
  writer.writeheader()
  # NOT Being used Write as many rows as you want!
    #for i in employees:
    #writer.writerow(i)


# Append row
with open('mycsvfile.csv','a',newline='') as f:
    writer=csv.writer(f)
    writer.writerow([0])
   

with open('mycsvfile.csv') as f:
    print(f.read())