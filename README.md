# Integrate an Investment Portfolio

In this developer journey, we will integrate Investment Portfolio service with a user's brokerage portfolio.  The integration will use Quovo to aggregate user's portfolio account and post it to the Bluemix Investment Portfolio service. The steps to perform the integration will be done using Jupyter Notebook.  The IBM Data Science Experience can be used to run the Jupyter Notebook.

When the reader has completed this journey, they will understand how to:

* Retrieve portfolio information and positions from a user's brokerage account using Quovo API calls
* Load Investment Portfolio service with portfolio and holdings
* Use Jupyter Notebook to run Python scripts for making the API calls


## Included Components
+ [Bluemix Investment Portfolio](https://console.bluemix.net/apidocs/751-investment-portfolio)
+ [Quovo's Aggregation API service](https://api.quovo.com/docs/agg/)
+ [IBM Data Science Experience](https://www.ibm.com/bs-en/marketplace/data-science-experience)


## Featured technologies
+ [Jupyter Notebooks](http://jupyter.org/)
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

Create a [Quovo account](https://www.quovo.com/pricing/).  A Sandbox account can be used to integrate potfolio for this journey.


## 2. Create Bluemix Investment Portfolio service

Create the following service:

* [**Investment Portfolio**](https://console.ng.bluemix.net/catalog/services/investment-portfolio)


## 3. Sign up for the Data Science Experience

Sign up for [IBM's Data Science Experience](https://datascience.ibm.com/).

## 4. Load the SetupPortfolio Notebook

Once you have completed the steps outlined above, you are ready to open and walk through the Notebook.  Go ahead and sign into the IBM Data Science experience and create a Project

Create a Project:
* Click on ``+ Create Project`` or ``+ New Project`` under Recently updated projects.
* Choose a ``Name`` and, optionally, a ``Description``. Accept the default settings for other options.
* Click ``Create``.

Create Notebook:
* In your project, click ``add notebooks``.
* Click the tab for ``From URL`` and enter a ``Name`` and optional ``Description``.
* In the ``Notebook URL`` box put:
`` https://github.com/IBM/Integrate-Investment-Portfolio/blob/master/notebooks/SetupPortfolio.ipynb``
* Click ``Create Notebook``.


## 5. Follow steps in the SetupPortfolio Notebook

Once you have the ``SetupPortfolio`` notebook open, follow the steps listed to load your Investment Portfolio service.

Be sure to run the code cell one at a time, and providing the required information to the script listed under __Before Running__.  This information will include Quovo account information, Bluemix service credentials and IDs that may have been created in a previous step.


## 6. Check Investment Portfolio

After you have completed all the steps in ``SetupPortfolio`` notebook, open ``CheckInvestmentPortfolio`` notebook. Use the url: ``https://github.com/IBM/Integrate-Investment-Portfolio/blob/master/notebooks/CheckInvestmentPortfolio.ipynb``

Follow the instructions to re-enter your Bluemix credentials to view your portfolio in the Investment Portfolio service and enter the Portfolio name in the next cell to view your holdings.


# License

[Apache 2.0](LICENSE)
