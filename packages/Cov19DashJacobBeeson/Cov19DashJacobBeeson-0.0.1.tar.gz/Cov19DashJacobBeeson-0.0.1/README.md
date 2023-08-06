# Coronavirus dashboard application README

A simple dashboard to help being kept up to date with the local and national infection rates and news on government guidelines. The user can schedule repeated or single updates to news and/or covid data displayed. The user can also cancel updates these updates and remove news articles or click on a link to read more.

## Installation Notes:

Python version 3.9.7 was used for development.

Please make sure the following modules are installed along with python3. And that your own API key is set in the config file.

- json
- logging
- time
- datetime
- flask
- uk\_covid19
- csv
- sched
- requests
- pytest

## Getting started tutorial:

Ensure the python code is running on your machine. Navigate to http://127.0.0.1:5000/index on a web browser and the interface should be displayed.

The dashboard is split into three columns. The left column is where all scheduled updates are displayed. The middle column displays local and national coronavirus statistics and at the bottom the form to submit new updates. The form will only allow an update to be scheduled if a label is entered and will only execute if a time is specified. The right column displays news articles containing covid keywords in the headline. There is also a hyper link to click to carry on reading the full article. The &#39;x&#39; in the top right-hand corner will close the news article and it will not be re-displayed. Clicking this &#39;x&#39; in the scheduled updates will consequently cancel that update.

Testing – How to test the code:

There is a log file which is automatically generated when the code is run. The log file will contain any errors and events that happend when the application is running. There is a &#39;tests&#39; folder which contains three test files, one for each module. To run these tests, make sure pytest is installed then using comand prompt in the directory python package is type &#39;python -m pytest&#39; and this will run the tests.

## Developer notes:

There are three modules: application.py, covid\_data\_handler, covid\_news\_handling. Covid data and news articles are stored in two json files &#39;covid\_data&#39; and &#39;news\_data&#39;. If these json files are deleted or do not exist simply run update\_covid() in the covid\_data\_handler module and update\_news() in the covid\_news\_handling module to avoid errors trying to read from a file that doesn&#39;t exist. In the config file the national and local locations, language can also be adjusted. The html for the interface is stored in the templates folder and in the static folder the image and favicon are stored in the images and favicons folder respectively.