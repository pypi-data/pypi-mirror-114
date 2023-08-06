# googlewrapper

[![PyPI Latest Release](https://img.shields.io/pypi/v/googlewrapper.svg)](https://pypi.org/project/googlewrapper/)

General Connector Classes for Google Products 

__Current Wrappers Available__

 - <a href=https://github.com/jaceiverson/google-wrapper#google-analytics>Google Analytics</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-search-console>Google Search Console</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-calendar>Google Calendar</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-big-query>Google Big Query</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-page-speed-insights>Google PageSpeed API</a>
 - <a href=https://github.com/jaceiverson/google-wrapper#google-sheets>Google Sheets</a>

_Wrappers In the Pipeline_
 - <a href=https://github.com/jaceiverson/google-wrapper#google-maps>Google Maps</a>  
 - <a href=https://github.com/jaceiverson/google-wrapper#gmail>Gmail</a>


# STEPS
 1) <a href=https://github.com/jaceiverson/google-wrapper#Acquire-Google-Credentials-from-API-Console>Acquire Google Credentials from API Console</a>
 2) <a href=https://github.com/jaceiverson/google-wrapper#installation>Install this package</a>
 3) <a href=https://github.com/jaceiverson/google-wrapper#establish-your-connection>Create Connection in Python</a>
 4) <a href=https://github.com/jaceiverson/google-wrapper#product-specific-methods>Use wrapper to make API calls</a>


## Acquire Google Credentials from API Console

First we will need to get our own Google Project set up so we can get our credentials. If you don't have experience, you can do so here <a href=https://console.cloud.google.com/apis/dashboard>Google API Console</a>

After you have your project set up, oAuth configured, and the optional service account (only for Google Big Query connections), you are good to install this package.

Make sure to download your oAuth credentials and save them to your working directory as 'client_secret.json'.

## Installation
It is recommended to create a virtualenv using the <a href="https://pypi.org/project/virtualenv/" target="_blank">virtualenv library</a>. Once created, I recommend installing googlewrapper with the following command:
```
pip install googlewrapper
```
OR
```
python -m pip install googlewrapper
```

## Establish your Connection
### Option 1 - Assign Connection Variable
Use the Connection class found in connect.py to assign credentials. It is recomended to do this, if you want to use credentials to authenticate with other libraries. 

'client_secret.json' should be in the working directory, if not, please declare the path while initializing the class. See the example below for both versions.
```py
from googlewrapper.connect import Connection

#in working directory
google_connection = Connection()

#declare path in class
google_connection = Connection("file/path/to/client_secret.json")
```

Once we have our connection object, we will need to declare the scope of our access. You can do this by accessing the following class methods:

| Google Service       | Module     | Authentication Type | Credential File |
| :------------- | :----------: | :----------: | :----------: |
|  Analytics | .ga()   | oAuth | client_secret.json | 
| Search Console   | .gsc() | oAuth |  client_secret.json | 
| Calendar   | .cal() | oAuth | client_secret.json | 
| Big Query   | .gbq() | Service Account | gbq-sa.json |
| PageSpeed  | n/a | API Key | n/a | 
| Gmail   | .gmail() | oAuth | client_secret.json | 
| Sheets   | .gs() | oAuth | client_secret.json | 

Note, you can change the file path for authenticating Google Big Query by passing in the Service Account json in the gbq method

```py
gbq_connection = Connection().gbq("file/path/to/service_account.json")
```

### Option 2 - Default Connection (One Line Connect)
It is possible to just use one line when connecting. It is recommended to do this if you will not need your authentication object, and will just be using the wrapper class.  

This can be done by initializing the wrapper classes, without any arguments. By default, each class will authenticate with the default method found in the connect class. 

__IMPORTANT__: To do this, we must have 'client_secret.json' in our working directory. -- for GBQ your 'gbq-sa.json' must be in the working directory

See below
```py
from googlewrapper.gsc import GoogleSearchConsole

gsc = GoogleSearchConsole()
```

After authentication has taken place (via either option), a folder will be created in your cwd named _credentials_. The respective authentication scopes will be stored there so you don't have to authenticate every time. Each token is stored with the Google property name as a .dat file.


# Product Specific Methods
Now that we have our credential object, we are ready to call the api. We will walk through examples for the different products
## Google Analytics
### Initialize 
```py
from googlewrapper.ga import GoogleAnalytics

ga = GoogleAnalytics()
```
### Methods
### Examples

## Google Search Console

Domain properties need to have 'sc-domain:' prefixed to the front of the url to pull the domain property.
### Initialize 
```py
from googlewrapper.gsc import GoogleSearchConsole

gsc = GoogleSearchConsole()
```
### Methods

#### Assigning Dates
The following all accept a datetime variable. There are 2 options for setting the date.

##### Option 1 - assign both start and end dates
> Use this option if you would like a range of dates
> 
>You need to call both these methods to assign start and end dates

```py
.set_start_date(start_date)
```
```py
.set_end_date(end_date)
```
##### Option 2 - assign one date
> Use this option if you only want to see one day worth of data
> 
> You only need to call the method below to make it work
```py
.set_date(date)
```
#### Other GSC API Parameters
```py
.set_filters()
```
 - sets the dimension filters, format them as a list of dictionaries. <a href=https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics/query#request-body target=_blank>See Google's Docs</a>
 - metric filters are not assigned prior to the pull, filter data after the api pull
```py
.set_dimensions()
```
 - Options:
   - "page"
   - "query"
   - "date"
   - "country"
   - "device"
   - "searchAppearance"
 - Default values: ["page","date"] 
```py
.set_sites(sites_list)
```
 - Assigns the list of sites we want to pull
---
#### Pulling Data
```py
.all_sites(site_filter)
```
 - Optional param
 - site_filter: type: list of strings
 - will filter your sites to sites including the strings in the list
 - **Returns**: list of all verified sites in the GSC profile

```py
.get_data()
```
 - After assigning all the parameters, run this method to make the api request
 - Assigns the value gsc.output (required for .ctr())
 - **Returns**: dictionary
   - Keys: Site URLs from the site_list
   - Values: pd.DataFrame of GSC data 

```py
.ctr()
```
 - Calculates custom Click Through Rates based our our GSC data we pulled
 - For accurate results, make sure that you: 
   - have "query" in the dimension lis
   - have set branded queries using .set_branded()
 - **Returns**: dictionary
   - Keys: ["all","branded","non-branded"]
   - Values: pd.DataFrame with index as Position and columns ["Clicks","Impressions","CTR"] 

### Examples
#### Pull one day's worth of data
```py
# initialize our class
from googlewrapper import GoogleSearchConsole
gsc = GoogleSearchConsole()

# assign variables to our GSC object
gsc.set_sites(sites_list)
gsc.set_date(dt.date.today())
gsc.set_dimensions(dim_list)

# call the api to get the data
data = gsc.get_data()
```
#### Find Custom CTR for last 12 months
```py
# initialize our class
from googlewrapper import GoogleSearchConsole
gsc = GoogleSearchConsole()

#declare all the parameters
gsc.set_start_date(dt.date.today()-dt.timedelta(days=365))
gsc.set_end_date(dt.date.today())
gsc.set_dimensions(['query'])
gsc.set_branded(branded_dict)
gsc.set_sites(sites_list)

data = gsc.get_data()
ctr = gsc.ctr()
```
## Google Calendar
### Initialize 
```py
from googlewrapper.cal import GoogleCalendar

cal = GoogleCalendar()
```
### Methods
```py
.set_default(cal_id)
```
 - Assigns which calendar will be used to create and find events
---
```py
.find_event(str)
```
   - Searches for an event in your calendar by name 
   - Returns <a href=https://developers.google.com/calendar/v3/reference/events/list#response>events list response object</a>
---
```py
.get_event(eventId)
```
Returns the <a href=https://developers.google.com/calendar/v3/reference/events#resource>event object</a> of the eventId you passed in

---
```py
.all_events(num_events,min_date)
```
   - Params
     - num_events
       - Is the number of events you'd like to return
       - defaults to 250
     - min_date
       - the starting point will only search forward in time from this date
       - defaults to the current date and time 
   - Returns
     - <a href=https://developers.google.com/calendar/v3/reference/events/list#response>events list response object</a>
---
```py
.update_event(new_event,send_updates)
```
Params
  - new_event
    - event formatted json to update
  - send_updates: str
    - if you want to send the updates
    - see <a href=https://developers.google.com/calendar/v3/reference/events/update#parameters>Google's Docs</a> for more info
    - defaults to 'all'

Returns 
 - <a href=https://developers.google.com/calendar/v3/reference/events#resource>updated event object</a>


### Examples 
```py
my_event = cal.find_event('Team Meeting')
```

## Google Big Query
### Initialize 
```py
from googlewrapper.gbq import GoogleBigQuery

gbq = GoogleBigQuery()
```
Remember that Google Big Query authenticates from a service account, be sure to include the gbq-sa.json file in your path, or pass in the pass to the .gbq() method.
### Methods
### Examples 

## Google PageSpeed Insights
### Initialize 
```py
from googlewrapper.pagespeed import PageSpeed

page_speed = PageSpeed(API_KEY)
```
### Methods
### Examples 

## Gmail
### Initialize 
```py
from googlewrapper.gmail import Gmail

mail = Gmail()
```
### Methods
### Examples 

## Google Sheets
To initialize, you need to pass in the URL of the sheet you wish to use. By default the first sheet is set to the active sheet, but that can be changed by calling 
`.set_sheet(new_sheet_name)`
### Initialize 
```py
from googlewrapper.gs import GoogleSheets

gs = GoogleSheets(YOUR_URL_HERE)
```
### Methods
```py
.set_sheet(sheet_name)
```
Assign which sheet (tab) we will be pulling from. This must be called to make the other methods work properly.

Params
- sheet_name
    - the name of the tabe we want to pull from
---
```
.df(start='a1',index=1)
```
pulls the google sheet and returns it as a pd.DF

Params
 - start (optional)
    -  where we want the top left (including headers) of our table to start
    - defaults to 'a1'
- index (optional)
    - which column will be the index when pulled
    - defaults to the first column
---
```py
.save(df,start = 'a1',index=True,header=True,extend=True))
```
Saves a pd.DF to our assigned GoogleSheet

Params
- df
    - pd.DF of data we want to save
- start (optional)
    - type: string
    - where we want to start saving the data
    - default: 'a1'
- index (option)
    - type: bool
    - include the pd.DF index in the sheet
    - default: True
- header (optional)
    - type: bool
    - include the headers in the sheet?
    - default: True
- extend (optional)
    - type: bool
    - if rows/columns would be cut off, create those rows/columns and place the data
    - default: True
---
```
.clear(start,end)
```
Removes any data from the selected range of cells. Does not remove formatting

Params
- start
    - type: string formatted as cell reference
    - top left cell to start clearing
- end
    - type: string formatted as cell reference
    - bottom right cell to end clearing
---

```
.row(row_number)
```
Returns an entire row of data.

Params
- row_number
    - type: int
    - which row number you want to pull
---

```
.col(col)
```
Returns an entire column of data.

Params
- col_number
    - type: int
    - which column number you want to pull
---
```
.add_sheet(sheet,data=None)
```
Creates a new sheet/tab in your spreadsheet. Assigns that sheet as the active sheet - _self.set_sheet()_. If you pass in data (a pd.DF), it will also write that data starting in 'a1' of your new tab. 

Params
- sheet
    - type: string
    - the name of the new tab to be created
- data
    - type: pd.DF
    - data that you want filled in to 'a1' on the new tab
---
```
.delete_sheet(sheet)
```
Deletes the sheet/tab whose name you pass in.
Params
- sheet
    - type: string
    - which tab you would like to delete
---
```
.share(email_list,role = 'reader')
```
Shares your spreadsheet with all emails in the list. Can assign different permissions. 

Params
- email_list
    - type: list
    - all the emails you'd like to share this with
- role
    - type: string
    - which permissions to grant this email list
    - options: 'reader','commenter','editor'

### Examples 

## Combining Products Examples
### Example 1
> Take a list of URLs from Sheets, grab Search Console Data, and import it into Big Query.

```py
from googlewrapper.sheets import GoogleSheets
from googlewrapper.gsc import GoogleSearchConsole
from googlewrapper.gbq import GoogleBigQuery
import datetime as dt

# init our objects
sheets = GoogleSheets(YOUR_URL_HERE)
gsc = GoogleSearchConsole()
gbq = GoogleBigQuery()

# get our urls we want to pull
# remember that sheet1 is default
sites = sheets.get_column(1)

'''
this one is a bit more technical
we can pull our column Branded Words right 
from sheets then assign it to a dictionary to use
in our GSC object.

Make sure that your url column is the index for 
your df. This will happen by default if the urls
are in the first column in google sheets
'''
branded_list = sheets.df()['Branded Words'].to_dict()

# assign those sheets to GSC
gsc.set_sites(sites)
# assign other GSC variables
gsc.set_date(dt.date(2021,1,1))
gsc.set_dims(['page','date','query'])

# get our data
gsc_data = gsc.get_data()

# print the total clicks/impressions and avg position
# for all the sites we just pulled data for
# send them to Big Query
for site in gsc_data:
  print(f"{site}'s Data\n"\
      f"Clicks: {gsc_data[site]['Clicks'].sum()}\n"\
      f"Impressions: {gsc_data[site]['Impressions'].sum()}\n"\
      f"Avg Position: {gsc_data[site]['Position'].mean()}\n\n")
  # now we will send our data into our GBQ tables for storage
  # we will assign the dataset name to be our url
  # we will assign table to be gsc
  gbq.set_dataset(site)
  gbq.set_table('gsc')
  # send the data to GBQ
  gbq.send(gsc_data[site])
```

## Thanks for using my code
<p align="center">
If you found this library useful, I'd appreciate a coffee. 
<br>
<br>
<a href="https://www.buymeacoffee.com/jaceiverson" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
</p>
