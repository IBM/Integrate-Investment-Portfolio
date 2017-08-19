# Integrate an Investment Portfolio

In this developer journey, we will integrate a user's brokerage portfolio (e.g. e*Trade, charles schwab, Fidelity) with the Investment Portfolio service.  The integration will use Quovo's Aggregation API to aggregate user's portfolio account and post it to the Bluemix Investment Portfolio service. The steps to perform the integration will be done using Jupyter Notebook with Python scripts. The IBM Data Science Experience provides a great place to work with notebooks, in addition to other data analytical tools and services.  In this journey, we will use IBM Data Science Experience for loading notebooks.

When the reader has completed this journey, they will understand how to:

* Retrieve portfolio information and positions from a brokerage account using Quovo
* Load Bluemix Investment Portfolio service with portfolio and holdings
* Use IBM Data Science Experience to open and run cells in notebook


# Architecture Flow

<p align="center">
  <img width="650" height="400" src="images\arch_flow.png">
</p>

1. The user logs into IBM Data Science Experience
2. The user creates a project and opens the notebook
3. The initial steps walk through retrieving brokerage portfolio account info using Quovo Aggregation API
4. The next steps loads the portfolio and associated holdings into the Investment Portfolio service


## Included Components
+ [Bluemix Investment Portfolio](https://console.bluemix.net/apidocs/751-investment-portfolio)
+ [Quovo's Aggregation API service](https://api.quovo.com/docs/agg/)
+ [IBM Data Science Experience](https://www.ibm.com/bs-en/marketplace/data-science-experience)


## Featured technologies
+ [Jupyter Notebook](http://jupyter.org/)
+ [Python](https://www.python.org/downloads/)


# Running the Application
Follow these steps to setup and run this developer journey. The steps are described in detail below.

## Steps
1. [Create Quovo account](#1-create-quovo-account)
2. [Create Bluemix Investment Portfolio service](#2-create-bluemix-investment-portfolio-service)
3. [Sign up for the Data Science Experience](#3-sign-up-for-the-data-science-experience)
4. [Load the SetupPortfolio Notebook](#4-load-the-setupportfolio-notebook)
5. [Follow steps in the SetupPortfolio Notebook](#5-follow-steps-in-the-setupportfolio-notebook)
6. [Check Investment Portfolio](#6-check-investment-portfolio)

## 1. Create Quovo account

Create a [Quovo account](https://www.quovo.com/pricing/).  A Sandbox account can be used to integrate the portfolio for this journey.

<p align="left">
  <img width="600" height="400" src="images\quovo_signIn_scrnshot.png">
</p>

## 2. Create Bluemix Investment Portfolio service

Create the following service:
* [**Investment Portfolio**](https://console.ng.bluemix.net/catalog/services/investment-portfolio)

[Deploy to Bluemix]

## 3. Sign up for the Data Science Experience

Sign up for [IBM's Data Science Experience](https://datascience.ibm.com/).

<p align="left">
  <img width="600" height="400" src="images\ibm_dsx_signup_scrnshot.png">
</p>


## 4. Load the SetupPortfolio Notebook

Once you have completed the steps outlined above, you are ready to open and walk through the Notebook.  Go ahead and sign into the IBM Data Science experience and create a Project

__Create a Project:__
* Click on ``Get Started`` in the top right corner, and then ``New Project``.

<p align="left">
  <img width="800" height="300" src="images\get_started_scrnshot.png">
</p>

* In the 'Create new project' window, enter a ``Name`` and, optionally, a ``Description``.
<p align="left">
  <img width="600" height="550" src="images\create_project_scrnshot.png">
</p>

* Click ``Create``.


__Create Notebook:__
* In your project, click ``add notebooks``.
<p align="left">
  <img width="800" height="300" src="images\add_notebook_scrnshot.png">
</p>

* Click the tab for ``From URL`` and enter a ``Name`` and optional ``Description``.
* In the ``Notebook URL`` box put:
`` https://github.com/IBM/Integrate-Investment-Portfolio/blob/master/notebooks/SetupPortfolio.ipynb``

<p align="left">
  <img width="500" height="550" src="images\create_notebook_scrnshot.png">
</p>

* Click ``Create Notebook``. This should open the notebook in your IBM Data Science Experience.

<p align="left">
  <img width="600" height="400" src="images\open_notebook_scrnshot.png">
</p>

## 5. Add Credentials

Once the notebook opens, you will need to add: credentials for the Investment Portfolio service, your Quovo login information and your brokerage info.  

In the 'Enter Credentials' cell, enter your:
  * Quovo account information
  * Brokerage ID - the Brokerage ID for a financial institute can be found in 'brokerage.json'
  * Username and password associated with the brokerage account
  * Investment Portfolio credentials

<p align="left">
  <img width="500" height="300" src="images\enter_credentials_scrnshot.png">
</p>

Once your credentials are entered, go ahead and run the cell.

## 6. Walk through steps to integrate portfolio with Investment Portfolio steps

You are now ready to integrate your portfolio data with Investment Portfolio.  Each step provides a description of the step and what actions the script will perform. Walk through steps by running each cell in order as it may be dependent on information retrieved in the previous step.

<p align="left">
  <img width="500" height="300" src="images\notebook_step_scrnshot.png">
</p>

The initial steps walk through steps using Quovo's Aggregation API to retrieve portfolio data from your brokerage account. Once the portfolio and its associated positions are retrieved, we load the portfolio data and associated positions as holdings into Investment Portfolio.



Go ahead and integrate your portfolio with IBM's Investment Portfolio.

# License

[Apache 2.0](LICENSE)
