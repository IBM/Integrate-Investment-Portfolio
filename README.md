![Bluemix Deployments](https://metrics-tracker.mybluemix.net/stats/afef6278be1bd0007fded450dc3ae2c7/badge.svg)

# Integrate an Investment Portfolio

In this developer journey, we will integrate a user's brokerage portfolio (e.g. e*Trade, charles schwab, Fidelity) with IBM's Investment Portfolio service.  The integration will use Quovo's Aggregation API to aggregate user's portfolio account and post it to the Investment Portfolio service. The steps to perform the integration will be done using Jupyter Notebook with Python scripts. The IBM Watson Studio provides a great place to work with notebooks, in addition to other data analytical tools and services.  In this journey, we will use IBM Watson Studio for walking through steps in our notebook.  In addition, the steps have been put together to create a web application that performs the integration of user's brokerage portfolio data with Investment Portfolio service.

When the reader has completed this journey, they will understand how to:

* Retrieve portfolio information and positions from a brokerage account using Quovo
* Load Investment Portfolio service with portfolio and holdings
* Use IBM Watson Studio to open and run cells in notebook


# Architecture Flow

<p align="center">
  <img width="650" height="400" src="images\arch_flow.png">
</p>

1. The user logs into IBM Watson Studio
2. The user creates a project and opens the notebook
3. The initial steps walk through retrieving brokerage portfolio account info using Quovo Aggregation API
4. The next steps loads the portfolio and associated holdings into the Investment Portfolio service


## Included Components
+ [Bluemix Investment Portfolio](https://console.bluemix.net/apidocs/751-investment-portfolio)
+ [Quovo's Aggregation API service](https://api.quovo.com/docs/agg/)
+ [IBM Watson Studio](https://www.ibm.com/bs-en/marketplace/data-science-experience)


## Featured technologies
+ [Jupyter Notebook](http://jupyter.org/)
+ [Python](https://www.python.org/downloads/)


# Running the Application
Follow these steps to setup and run this developer journey. The steps are described in detail below.

## Steps
1. [Create Quovo account](#1-create-quovo-account)
2. [Create Investment Portfolio service](#2-create-investment-portfolio-service)
3. [Sign up for the Watson Studio](#3-sign-up-for-the-data-science-experience)
4. [Open the SetupPortfolio Notebook](#4-open-the-setupportfolio-notebook)
5. [Add Credentials](#5-add-credentials)
6. [Walk through steps to integrate portfolio with Investment Portfolio](#6-walk-through-steps-to-integrate-portfolio-with-investment-portfolio)
7. [Explore the App](#6-explore-the-app)

## 1. Create Quovo account

Create a [Quovo account](https://www.quovo.com/pricing/).  A Sandbox account can be used to integrate the portfolio for this journey.

<p align="left">
  <img width="650" src="images\quovo_signIn_scrnshot.png">
</p>

## 2. Create Investment Portfolio service

Create the following service:

* [**Investment Portfolio**](https://console.ng.bluemix.net/catalog/services/investment-portfolio)

## 3. Sign up for the Watson Studio

Sign up for [IBM's Watson Studio](https://datascience.ibm.com/).

<p align="left">
  <img width="1000"  src="images\ibm_dsx_signup_scrnshot.png">
</p>


## 4. Open the SetupPortfolio Notebook

Once you have completed the steps outlined above, you are ready to open and walk through the Notebook.  Go ahead and sign into the IBM Data Science experience and create a Project

__Create a Project:__
* Click on ``Get Started`` in the top right corner, and then ``New Project``.

<p align="left">
  <img width="1000" src="images\get_started_scrnshot.png">
</p>

* In the 'Create new project' window, enter a ``Name`` and, optionally, a ``Description``. By signing up for the IBM Watson Studio, an Apache Spark service and an Object Storage will be created in your Bluemix account. These services can be integrated with Notebook or Rstudio for data analysis using IBM Watson Studio. Here, choose the default ``Spark Service`` and ``Storage Type``.
<p align="left">
  <img width="600" src="images\create_project_scrnshot.png">
</p>

* Click ``Create``.


__Create Notebook:__
* After your project opens, click ``add notebooks``.
<p align="left">
  <img width="1000"  src="images\add_notebook_scrnshot.png">
</p>

* With IBM Watson Studio, you can start with a ``Blank`` notebook or open ``From File``. We will import the notebook from github, so will use ``From URL``.  Click the tab for ``From URL``. Enter a ``Name`` and an optional ``Description``.
* In the ``Notebook URL`` box put:
`` https://github.com/IBM/Integrate-Investment-Portfolio/blob/master/notebooks/SetupPortfolio.ipynb``

<p align="left">
  <img width="500"  src="images\create_notebook_scrnshot.png">
</p>

* Click ``Create Notebook``. This should open the notebook in your IBM Watson Studio.

<p align="left">
  <img width="1000"  src="images\open_notebook_scrnshot.png">
</p>

## 5. Add Credentials

Once the notebook opens, you will need to add: credentials for the Investment Portfolio service, your Quovo login information and your brokerage info.  

In the 'Enter Credentials' cell, enter your:
  * Quovo account information
  * Brokerage ID - the Brokerage ID for a financial institute can be found in 'brokerage.json'
  * Username and password associated with the brokerage account
  * Investment Portfolio credentials

<p align="left">
  <img width="850"  src="images\enter_credentials_scrnshot.png">
</p>

Once your credentials are entered, go ahead and run the cell.

## 6. Walk through steps to integrate portfolio with Investment Portfolio

You are now ready to integrate your portfolio data with Investment Portfolio. Each step provides a description of the step and what actions the script will perform. Walk through steps by running each cell in order, as the script may be dependent on information retrieved in the previous step.

<p align="left">
  <img width="1000"  src="images\notebook_step_scrnshot.png">
</p>

The initial steps use Quovo's Aggregation API to retrieve portfolio data from your brokerage account. Once the portfolio and its associated positions are retrieved, we load the portfolio data and associated positions as holdings into Investment Portfolio.

## 7. Explore the App

You can run a web application using the steps from the notebook to capture portfolio data from user's brokerage account into Investment Portfolio service by deploying directly to Bluemix or run it locally.

### Deploy to Bluemix

Deploy the web application. This will create an Investment Portfolio service for you.

[![Deploy to Bluemix](https://metrics-tracker.mybluemix.net/stats/afef6278be1bd0007fded450dc3ae2c7/button.svg)](https://bluemix.net/deploy?repository=https://github.com/IBM/Integrate-Investment-Portfolio)

### Run it locally

#### Clone the repo

Clone the Integrate-Investment-Portfolio code locally. In a terminal, run:

```none
git clone https://github.com/IBM/Integrate-Investment-Portfolio.git
```

#### Configure .env file

You can run it locally by providing your Investment Portfolio credentials in a `.env file`. Copy the sample `.env.example` file using the following command:

  ```none
  cp .env.example .env
  ```

and fill in your Investment Portfolio credentials.

  ```none
  #INVESTMENT PORTFOLIO

  CRED_PORTFOLIO_USERID_W=
  CRED_PORTFOLIO_PWD_W=
  CRED_PORTFOLIO_USERID_R=
  CRED_PORTFOLIO_PWD_R=
  URL_GET_PORTFOLIO_HOLDINGS=https://investment-portfolio.mybluemix.net/api/v1/portfolios/
  ```

#### Run application

In your project directory:

+ Run `pip install -r requirements.txt` to install the app's dependencies
+ Run `python run.py`
+ Access the running app in a browser at <http://0.0.0.0:8080/>

<p align="left">
  <img width="1000"  src="images\web_ui_scrnshot.png">
</p>


Go ahead and integrate your portfolio with IBM's Investment Portfolio!

## Privacy Notice

If using the Jupyter Notebook or the application, some metrics are tracked. The following information is sent to a [Deployment Tracker](https://github.com/IBM/metrics-collector-service) service on each deployment on Bluemix:

* Python package version
* Python repository URL
* Application Name (`application_name`)
* Application GUID (`application_id`)
* Application instance index number (`instance_index`)
* Space ID (`space_id`) or OS username
* Application Version (`application_version`)
* Application URIs (`application_uris`)
* Cloud Foundry API (`cf_api`)
* Labels of bound services
* Number of instances for each bound service and associated plan information
* Metadata in the repository.yaml file

This data is collected from the `setup.py` and `repository.yaml` file in the sample application and the `VCAP_APPLICATION` and `VCAP_SERVICES` environment variables in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix to measure the usefulness of our examples, so that we can continuously improve the content we offer to you. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

## Disabling Deployment Tracking

To disable tracking on the Jypyter Notebook, simply remove the last 3 lines of code in the secode cell from the **SetupPortfolio.ipynb** file in the **notebooks** directory.

To disable tracking on the application, simply remove `metrics_tracker_client.track()` from the run.py file in the top level directory.

# License

[Apache 2.0](LICENSE)
