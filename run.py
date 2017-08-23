# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, jsonify, render_template, json, Response, request
from dotenv import load_dotenv
import requests, json, time, datetime
import os

#Initalize Investment Portfolio Service credentials to find on Bluemix otherwise from .env file
if 'VCAP_SERVICES' in os.environ:
    vcap_servicesData = json.loads(os.environ['VCAP_SERVICES'])
    # Log the fact that we successfully found some service information.
    print("Got vcap_servicesData\n")
    # Look for the IP service instance.
    IP_W_username=vcap_servicesData['fss-portfolio-service'][0]['credentials']['writer']['userid']
    IP_W_password=vcap_servicesData['fss-portfolio-service'][0]['credentials']['writer']['password']
    IP_R_username=vcap_servicesData['fss-portfolio-service'][0]['credentials']['reader']['userid']
    IP_R_password=vcap_servicesData['fss-portfolio-service'][0]['credentials']['reader']['password']

    #quovo_username =vcap_servicesData['user-provided'][0]['credentials']['username']
    #quovo_password =vcap_servicesData['user-provided'][0]['credentials']['password']
    
    # Log the fact that we successfully found credentials
    print("Got IP credentials\n")
else:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    IP_W_username=os.environ.get("CRED_PORTFOLIO_USERID_W")
    IP_W_password=os.environ.get("CRED_PORTFOLIO_PWD_W")
    IP_R_username=os.environ.get("CRED_PORTFOLIO_USERID_R")
    IP_R_password=os.environ.get("CRED_PORTFOLIO_PWD_R")


app = Flask(__name__)

#enter Quovo username/password
quovo_username = "raheel.zubairy@gmail.com"
quovo_password = "Shareable!@#123"

#enter name and email of user
quovo_name = "Raheel"
quovo_email = "raheel.zubairy@gmail.com"


#brokerages defined to be used by the application
brokerages = [
          {'21534': 'Test Data Brokerage'}
          ]

def GetQuovoAccessToken():
    """
    Generates and returns access token using Quovo username, password
    """
    #make the request
    print ("Get Quovo Access Token")
    BASEURL = "https://api.quovo.com/v2/tokens"
    headers = {
        'Content-Type': "application/json"
        }
    data = {
        'name': "main_token"
        }
    get_data = requests.post(BASEURL, auth=(quovo_username, quovo_password), headers=headers, data=json.dumps(data))
    data = get_data.json()
    json_data = json.dumps(data)

    #if access token present, create 'token.json' file and assign token variable
    if 'access_token' in data:
        f = open("token.json", "w")
        f.write(json_data)
        f.close()

        token = data["access_token"]["token"]
        print (json.dumps(data, indent=4, sort_keys=True))

    #else print status and message and get token from 'token.json'
    else:
        print ("status: " + str(data["status"]))
        print ("message: " + str(data["message"]))

        if os.path.isfile('token.json'):
            print ("Get token from token.json")
            with open('token.json') as data_file:
                token_data = json.load(data_file)
                token = token_data["access_token"]["token"]

    print ("token: " + token)
    return token


def CreateGetUser(token):
    """
    Create user with name and email, if user exists, then retrieve the user ID
    """
    #Create/Get user

    #make the request to create user
    BASEURL = "https://api.quovo.com/v2/users"
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json"
        }
    data = {
        'username': "main_token",
        'name': quovo_name,
        'email': quovo_email
        }

    get_data = requests.post(BASEURL, headers=headers, data=json.dumps(data))
    data = get_data.json()
    json_data = json.dumps(data)

    #if user is created, retrieve the User ID
    if 'user' in data:
        print ("Create User")
        print (json.dumps(data, indent=4, sort_keys=True))
        user_ID = data["user"]["id"]
        print ("User ID: " + str(user_ID))

    #else get all users, and assign User ID
    else:
        headers = {
            'Authorization': "Bearer " + token
            }
        get_user_data = requests.get(BASEURL, headers=headers)
        user_data = get_user_data.json()
        if 'users' in user_data:
            print ("Get User")
            print (json.dumps(user_data, indent=4, sort_keys=True))
            user_ID = user_data["users"][0]["id"]
            print ("User ID: " + str(user_ID))
        else:
            print ("status: " + str(data["status"]))
            print ("message: " + str(data["message"]))
            return None

    return user_ID


def CreateGetAccount(brokerage_ID, brokerage_username, brokerage_password, user_ID, token):
    """
    Create account, if account exists, then retrieve the account ID
    """
    #Create/Get account

    #make the request to create account
    BASEURL = "https://api.quovo.com/v2/users/" + str(user_ID) + "/accounts"
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json"
        }
    data = {
        'brokerage': brokerage_ID,
        'username': brokerage_username,
        'password': brokerage_password
        }
    get_data = requests.post(BASEURL, headers=headers, data=json.dumps(data))
    data = get_data.json()

    #if account is created, retrieve the Account ID
    if 'account' in data:
        print ("Create account")
        account_ID = data["account"]["id"]
        print (json.dumps(data, indent=4, sort_keys=True))

    #else if the account exists, then get accounts
    elif data["id"] == "duplicate_account":
        print ("Get Account")
        BASEURL = "https://api.quovo.com/v2/accounts"
        headers = {
            'Authorization': "Bearer " + token
            }
        get_account_data = requests.get(BASEURL, headers=headers)
        account_data = get_account_data.json()

        print (json.dumps(account_data, indent=4, sort_keys=True))

        #find the account with the same brokerage and assign Account ID
        for accounts in account_data['accounts']:
            if accounts['brokerage'] ==  brokerage_ID:
                account_ID = accounts["id"]

    #else print the returned status and message
    else:
        print ("status: " + str(data["status"]))
        print ("message: " + str(data["message"]))
        return None

    print ("Account ID: " + str(account_ID))
    return account_ID


def SyncAccount(account_ID, token):
    """
    Sync account
    """
    #Sync account

    #make the request
    print ("Sync account")
    BASEURL = "https://api.quovo.com/v2/accounts/" + str(account_ID) + "/sync"
    headers = {
        'Authorization': "Bearer " + token
        }
    get_data = requests.post(BASEURL, headers=headers)

    #print json data
    data = get_data.json()
    print (json.dumps(data, indent=4, sort_keys=True))


def CheckSync(account_ID, token):
    """
    Check Sync status till "good"
    """
    # Check sync till status: good

    status = ""
    while (status != "good"):
        #make the request
        print ("Check Sync")
        BASEURL = "https://api.quovo.com/v2/accounts/" + str(account_ID) + "/sync"
        headers = {
            'Authorization': "Bearer " + token
            }
        get_data = requests.get(BASEURL, headers=headers)

        #print json data
        data = get_data.json()
        print (json.dumps(data, indent=4, sort_keys=True))

        if 'sync' in data:
            if 'status' in data["sync"]:
                if data["sync"]["status"] == "good":
                    status = "good"
                else:
                    time.sleep(3)
        print ("status: " + status)


def GetPortfolios(account_ID, token):
    """
    Get portfolios for the account, pick first if muliple portfolios
    """
    # Get Portfolios

    print ("Get Portfolios - (Pick first portfolio if multiple portfolios in the account)")

    #make the request
    BASEURL = "https://api.quovo.com/v2/accounts/" + str(account_ID) + "/portfolios"
    headers = {
        'Authorization': "Bearer " + token
        }
    get_data = requests.get(BASEURL, headers=headers)

    #print portfolios json data
    portfolios_data = get_data.json()
    print (json.dumps(portfolios_data, indent=4, sort_keys=True))

    #retrieve Portfolio ID
    portfolio_ID = portfolios_data["portfolios"][0]["id"]
    print ("Portfolio ID: " + str(portfolio_ID))
    return portfolios_data


def GetPortfolioPositions(portfolio_ID, token):
    """
    Get portfolio positions for the portfolio
    """
    #Get Portfolio Positions

    #make the request
    print ("Get Positions of Portfolio")
    BASEURL = "https://api.quovo.com/v2/portfolios/" + str(portfolio_ID) + "/positions"
    headers = {
        'Authorization': "Bearer " + token
        }
    get_data = requests.get(BASEURL, headers=headers)

    #print positions json data
    positions_data = get_data.json()
    print (json.dumps(positions_data, indent=4, sort_keys=True))
    return positions_data


def LoadPortfolio(portfolios_data):
    """
    Load portfolio into Investment Portfolio
    """
    #Load Investment Portfolio with brokerage portfolio data

    print ("Add portfolio to Investment Portfolio service")

    #create timestamp
    timestamp = '{:%Y-%m-%dT%H:%M:%S.%fZ}'.format(datetime.datetime.now())

    #assign portfolio name and brokerage name
    portfolio_name = portfolios_data["portfolios"][0]['portfolio_name']
    brokerage_name = portfolios_data["portfolios"][0]['brokerage_name']

    print ("Investment Portfolio - Name: " + portfolio_name)
    print ("Investment Portfolio - Brokerage: " + brokerage_name)

    #make request for portfolio
    BASEURL = "https://investment-portfolio.mybluemix.net/api/v1/portfolios"
    headers = {
            'Content-Type': "application/json",
            'Accept': "application/json"
            }

    data = {
        'name': portfolio_name,
        'timestamp': timestamp,
        'closed': False,
        'data': { 'brokerage': brokerage_name }
        }
    get_data = requests.post(BASEURL, auth=(IP_W_username, IP_W_password), headers=headers, data=json.dumps(data))

    #print the status and returned json
    status = get_data.status_code
    print("Investment Portfolio status: " + str(status))

    if status != 200:
        print(get_data)
        return None
    else:
        data = get_data.json()
        print (json.dumps(data, indent=4, sort_keys=True))
        return portfolio_name


def LoadHoldings(portfolio_name, positions_data):
    """
    Load portfolio holdings into Investment Portfolio for the portfolio
    """
    #Load holdings into Investment Portfolio for a portfolio

    print ("Load Investment Portfolio Holdings")

    holdings_data = []

    #read asset, quantity andd companyname from positions data and append the holdings array
    for positions in positions_data['positions']:
        position_data = {}

        if 'ticker' in positions:
            position_data["asset"] = positions['ticker']
        if 'quantity' in positions:
            position_data["quantity"] = positions['quantity']
        if 'ticker_name' in positions:
            position_data["companyName"] = positions['ticker_name']

        if 'asset_class' in positions:
            if positions['asset_class'] != 'Cash':
                holdings_data.append(position_data)

    #make the request
    timestamp = '{:%Y-%m-%dT%H:%M:%S.%fZ}'.format(datetime.datetime.now())
    BASEURL = "https://investment-portfolio.mybluemix.net/api/v1/portfolios/" + portfolio_name + "/holdings"
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json"
        }
    data = {
        'timestamp': timestamp,
        'holdings': holdings_data,
        }
    get_data = requests.post(BASEURL, auth=(IP_W_username, IP_W_password), headers=headers, data=json.dumps(data))

    #print the status and returned json
    status = get_data.status_code
    print("Investment Portfolio Holding status: " + str(status))

    if status != 200:
        print(get_data)
    else:
        data = get_data.json()
        print (json.dumps(data, indent=4, sort_keys=True))


def GetHoldings(portfolio_name):
    """
    Get portfolio holdings from Investment Portfolio for the portfolio
    """
    #View portfolio and holdings in Investment Portfolio

    #make the request for portfolios
    print ("Get Portfolios from Investment Portfolio")
    BASEURL = "https://investment-portfolio.mybluemix.net/api/v1/portfolios/"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(BASEURL, auth=(IP_R_username, IP_R_password), headers=headers)
    print("Investment Portfolio status: " + str(get_data.status_code))

    #print json data
    data = get_data.json()
    print (json.dumps(data, indent=4, sort_keys=True))

    #make the request for holdings
    print ("Get Portfolio Holdings for " + portfolio_name)
    BASEURL = "https://investment-portfolio.mybluemix.net/api/v1/portfolios/" + portfolio_name + "/holdings?latest=true"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(BASEURL, auth=(IP_R_username, IP_R_password), headers=headers)
    print("Investment Portfolio - Get Portfolio Holdings status: " + str(get_data.status_code))

    #print json data
    data = get_data.json()
    print (json.dumps(data, indent=4, sort_keys=True))
    return data


@app.route('/')
def run():
    return render_template('index.html')

@app.route('/api/brokeragenames',methods=['GET'])
def api_portfolionames():
    """
    Returns the brokerage names
    """
    print ("Print")
    return Response(json.dumps(brokerages), mimetype='application/json')


@app.route('/api/analyze', methods =['GET','POST'])
def api_analyze():
    """
    Processes the user inputs
    """

    print ("Print Analyze")
    output = {}
    #make the request

    #retrieve the json from the ajax call
    json_file = ''
    print ("request POST")
    if request.method == 'POST':
        print ("make json request")
        json_file = request.json
        print ("post request")

    print ("check GET json")
    #if json_file successfully posted..
    if json_file != '':

        print ("got json file")


        #check all required arguments are present:
        if not all(arg in json_file for arg in ["brokerageID","brokerageUsername", "brokeragePassword"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422

        print ("get brokerage info")

        brokerage_ID = json_file["brokerageID"]
        brokerage_username = json_file["brokerageUsername"]
        brokerage_password = json_file["brokeragePassword"]
        print("retreived data: " + str(brokerage_ID) + " | " + str(brokerage_username) + " | " + str(brokerage_password))

        token = GetQuovoAccessToken()
        user_ID = CreateGetUser(token)

        if(user_ID is not None):
            account_ID = CreateGetAccount(brokerage_ID, brokerage_username, brokerage_password, user_ID, token)
            if (account_ID is not None):
                SyncAccount(account_ID, token)
                CheckSync(account_ID, token)

                #once account is synced, get portfolios
                portfolios_data = GetPortfolios(account_ID, token)

                #get positions for first portfolio if multiple portfolios
                portfolio_ID = portfolios_data["portfolios"][0]["id"]
                positions_data = GetPortfolioPositions(portfolio_ID, token)

                portfolio_name = LoadPortfolio(portfolios_data)
                LoadHoldings(portfolio_name, positions_data)
                holdings_data = GetHoldings(portfolio_name)

                holdings = holdings_data["holdings"][-1]["holdings"]

                #create the output json
                output = {"portfolio_name": portfolio_name, "holdings": holdings}
            else:
                return json.dumps({'error': " Unable to retrieve Quovo Account ID"})
        else:
            return json.dumps({'error': " Unable to retrieve Quovo User ID"})

        print (output)

    #return Response(json.dumps(output), mimetype='application/json')
    return json.dumps(output)



port = int(os.getenv('VCAP_APP_PORT', 8080))
host='0.0.0.0'
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
