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
import metrics_tracker_client

#brokerages defined to be used by the application
brokerages = [
          {'21534': 'Test Data Brokerage'}
          ]

Quovo_base_url = "https://api.quovo.com/v2/"
IP_base_url = "https://investment-portfolio.mybluemix.net/api/v1/"

#Initalize Investment Portfolio Service credentials to find on Bluemix otherwise from .env file
if 'VCAP_SERVICES' in os.environ:
    vcap_servicesData = json.loads(os.environ['VCAP_SERVICES'])

    # Look for the IP service instance.
    IP_W_username=vcap_servicesData['fss-portfolio-service'][0]['credentials']['writer']['userid']
    IP_W_password=vcap_servicesData['fss-portfolio-service'][0]['credentials']['writer']['password']
    IP_R_username=vcap_servicesData['fss-portfolio-service'][0]['credentials']['reader']['userid']
    IP_R_password=vcap_servicesData['fss-portfolio-service'][0]['credentials']['reader']['password']

else:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    IP_W_username=os.environ.get("CRED_PORTFOLIO_USERID_W")
    IP_W_password=os.environ.get("CRED_PORTFOLIO_PWD_W")
    IP_R_username=os.environ.get("CRED_PORTFOLIO_USERID_R")
    IP_R_password=os.environ.get("CRED_PORTFOLIO_PWD_R")


app = Flask(__name__)

def GetQuovoAccessToken(quovo_username, quovo_password):
    """
    Generates and returns access token using Quovo username, password
    """
    #make the request
    BASEURL = Quovo_base_url + "tokens"
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

    #else if token name in use, get token from 'token.json'
    elif data["message"] == "The given name is already in use." and os.path.isfile('token.json'):
        with open('token.json') as data_file:
            token_data = json.load(data_file)
            token = token_data["access_token"]["token"]
    #else print status and message
    else:
        print ("status: " + str(data["status"]))
        print ("message: " + str(data["message"]))
        return None

    print ("token: " + token)
    return token


def CreateGetUser(token, quovo_username):
    """
    Create user with name and email, if user exists, then retrieve the user ID
    """
    #Create/Get user

    #make the request to create user
    BASEURL = Quovo_base_url + "users"
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json"
        }
    data = {
        'username': "main_token",
        'name': quovo_username
        }

    get_data = requests.post(BASEURL, headers=headers, data=json.dumps(data))
    data = get_data.json()
    json_data = json.dumps(data)

    #if user is created, retrieve the User ID
    if 'user' in data:
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
    BASEURL = Quovo_base_url + "users/" + str(user_ID) + "/accounts"
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
        account_ID = data["account"]["id"]

    #else if the account exists, then get accounts
    elif data["id"] == "duplicate_account":
        BASEURL = Quovo_base_url + "accounts"
        headers = {
            'Authorization': "Bearer " + token
            }
        get_account_data = requests.get(BASEURL, headers=headers)
        account_data = get_account_data.json()

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
    BASEURL = Quovo_base_url + "accounts/" + str(account_ID) + "/sync"
    headers = {
        'Authorization': "Bearer " + token
        }
    get_data = requests.post(BASEURL, headers=headers)

    #print json data
    data = get_data.json()


def CheckSync(account_ID, token):
    """
    Check Sync status till "good"
    """
    # Check sync till status: good

    status = ""
    while (status != "good"):
        #make the request
        BASEURL = Quovo_base_url + "accounts/" + str(account_ID) + "/sync"
        headers = {
            'Authorization': "Bearer " + token
            }
        get_data = requests.get(BASEURL, headers=headers)

        #get json data
        data = get_data.json()

        if 'sync' in data:
            if 'status' in data["sync"]:
                if data["sync"]["status"] == "good":
                    status = "good"
                else:
                    time.sleep(3)

def GetPortfolios(account_ID, token):
    """
    Get portfolios for the account, pick first if muliple portfolios
    """
    # Get Portfolios

    #make the request
    BASEURL = Quovo_base_url + "accounts/" + str(account_ID) + "/portfolios"
    headers = {
        'Authorization': "Bearer " + token
        }
    get_data = requests.get(BASEURL, headers=headers)

    #get portfolios json data
    portfolios_data = get_data.json()

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
    BASEURL = Quovo_base_url + "portfolios/" + str(portfolio_ID) + "/positions"
    headers = {
        'Authorization': "Bearer " + token
        }
    get_data = requests.get(BASEURL, headers=headers)

    #get positions json data
    positions_data = get_data.json()    
    return positions_data


def LoadPortfolio(portfolios_data):
    """
    Load portfolio into Investment Portfolio
    """
    #Load Investment Portfolio with brokerage portfolio data

    #create timestamp
    timestamp = '{:%Y-%m-%dT%H:%M:%S.%fZ}'.format(datetime.datetime.now())

    #assign portfolio name and brokerage name
    portfolio_name = portfolios_data["portfolios"][0]['portfolio_name']
    brokerage_name = portfolios_data["portfolios"][0]['brokerage_name']

    #make request for portfolio
    BASEURL = IP_base_url + "portfolios"
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

    #get the status and returned json
    status = get_data.status_code
    if status != 200:
        print(get_data)
        return None
    else:
        return portfolio_name


def LoadHoldings(portfolio_name, positions_data):
    """
    Load portfolio holdings into Investment Portfolio for the portfolio
    """
    #Load holdings into Investment Portfolio for a portfolio

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
    BASEURL = IP_base_url + "portfolios/" + portfolio_name + "/holdings"
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json"
        }
    data = {
        'timestamp': timestamp,
        'holdings': holdings_data,
        }
    get_data = requests.post(BASEURL, auth=(IP_W_username, IP_W_password), headers=headers, data=json.dumps(data))

    #get the status and returned json
    status = get_data.status_code

    if status != 200:
        print(get_data)
    else:
        data = get_data.json()


def GetHoldings(portfolio_name):
    """
    Get portfolio holdings from Investment Portfolio for the portfolio
    """
    #View portfolio and holdings in Investment Portfolio

    #make the request for portfolios
    BASEURL = IP_base_url + "portfolios/"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(BASEURL, auth=(IP_R_username, IP_R_password), headers=headers)

    #get json data
    data = get_data.json()

    #make the request for holdings
    BASEURL = IP_base_url + "portfolios/" + portfolio_name + "/holdings?latest=true"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(BASEURL, auth=(IP_R_username, IP_R_password), headers=headers)

    #get json data
    data = get_data.json()
    return data


@app.route('/')
def run():
    return render_template('index.html')

@app.route('/api/brokeragenames',methods=['GET'])
def api_portfolionames():
    """
    Returns the brokerage names
    """
    return Response(json.dumps(brokerages), mimetype='application/json')


@app.route('/api/analyze', methods =['GET','POST'])
def api_analyze():
    """
    Processes the user inputs
    """

    output = {}

    #retrieve the json from the ajax call
    json_file = ''
    if request.method == 'POST':
        json_file = request.json

    #if json_file successfully posted..
    if json_file != '':

        #check all required arguments are present:
        if not all(arg in json_file for arg in ["brokerageID","brokerageUsername","brokeragePassword","quovoUsername","quovoPassword"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422

        brokerage_ID = json_file["brokerageID"]
        brokerage_username = json_file["brokerageUsername"]
        brokerage_password = json_file["brokeragePassword"]
        quovo_username = json_file["quovoUsername"]
        quovo_password = json_file["quovoPassword"]
        print("retreived data: " + str(brokerage_ID) + " | " + str(brokerage_username) + " | " + str(brokerage_password) + str(quovo_username) + " | " + str(quovo_password))

        #go through steps to load Investment Portfolio service
        token = GetQuovoAccessToken(quovo_username, quovo_password)
        if(token is not None):
            user_ID = CreateGetUser(token, quovo_username)
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
                    return json.dumps({'error': "Unable to retrieve Quovo Account ID"})
            else:
                return json.dumps({'error': "Unable to retrieve Quovo User ID"})
        else:
            return json.dumps({'error': "Unable to retrieve token. Check your Quovo login information"})

        print (output)

    #return Response(json.dumps(output), mimetype='application/json')
    return json.dumps(output)



port = int(os.getenv('VCAP_APP_PORT', 8080))
host='0.0.0.0'
if __name__ == "__main__":
    metrics_tracker_client.track()
	app.run(host='0.0.0.0', port=int(port))
