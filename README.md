# AnalyticsCal-Classroom


In this branch I have added 2 things
1. analyticsCal : 
   i. a flask project which has API to communicate with frontend 
      - Open this project in eclipse as flask project and go through code
      - Then all modules prepared by each team can be imported and called as function inside this file
   ii. Frontend code itself, it is readily available demo application build in ORACLE JET
      - cd to analyticsCal/webServer/FixItFast/  and start local http-server 
      - go to browser and enter localhost:<serverport>/index.html

2. load_and_filter_data.py
   - This loads data into DB, currently it does not do anything else and logic is hardcoded for dataset filename given in file
   - Web server code can import this as package and call filter functino to load data into db and perform data cleaning operation
