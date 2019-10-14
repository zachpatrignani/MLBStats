import requests
from bs4 import BeautifulSoup
import re
import numpy
import pandas as pd
import datetime

#Discription
# This application uses Beautiful Soup to scrape MLB stats from ESPN.
# The user inputs desired category and year, which is inserted into a url
# where the HTML is parsed and stored in a pandas dataframe.
# The statistics are then exported from pandas to a csv file.


#Current year
currentYear = datetime.datetime.now()

#Prompts user to choose batting or pitching stats and converts category to lowercase.
category = input("Please enter category of the stats you would like to see (Batting or Pitching): ")
category = category.lower()

#Validation loop for category
while(category != "pitching" and category != "batting"):
    print("ERROR: Invalid category entered.")

    category = input("Please enter category of the stats you would like to see (Batting or Pitching): ")
    category = category.lower()

#Prompts user to choose year they want the stats of.
year = input("Please enter the year of the MLB season you would like to see "
"(1876 - Present): ")

#Validation loop for year
while (int(year) < 1876 or int(year) > currentYear.year):
    print("ERROR: Invalid year entered.")

    year = input("Please enter the year of the MLB season you would like to see "
    "(1876 - Present): ")


#if else statement depending on category chosen.
if category == "batting":

    #for loop to loop through the number of players that year in increments of 50.
    for x in range(1, 331, 50):

        # Takes the source code for the website hitting stats.
        urlBATTING = "http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/{}".format(year)+\
         "/start/{}".format(x)

        #opens the ESPN page
        pageBATTING = requests.get(urlBATTING)

        #Parses the page in HTML
        soupBATTING = BeautifulSoup(pageBATTING.text, 'html.parser')

        #Arguments that will be passed into our .find and .find_all
        attrs = {'attribute1Name': 'attribute1Value', 'attribute2Name': 'attribute2Value'}

        #Takes the five column headers. Only need to find it once
        #since it appears five times on the ESPN page.
        headers = soupBATTING.find('tr', attrs={'class': 'colhead'})

        columns = [col.get_text() for col in headers.find_all('td')]

        #Using pandas to create an empty data frame to store player stats
        final_df = pd.DataFrame(columns=columns)

        #Use re's compile function to scrape all player data
        players = soupBATTING.find_all('tr', attrs={'class':re.compile('row player-10-')})

        for player in players:
            #Gets player's stats
            stats = [stat.get_text() for stat in player.find_all('td')]

            #Temporary dataframe for a single player's stats
            temp_df = pd.DataFrame(stats).transpose()
            temp_df.columns = columns

            #Put player stats in the final dataframe
            final_df = pd.concat([final_df, temp_df], ignore_index=True)
        print(final_df)

        # Export to csv file displaying all 331 batters and their stats
        final_df.to_csv(r"C:\Users\Zach Patrignani\Desktop\mlb_stats.csv", index = False,
        header= True, sep=',', encoding='utf-8',mode='a')

else:

    # for loop to loop through the number of players that year in increments of 50.
    for x in range(1,151,50):
        urlPITCHING = "http://www.espn.com/mlb/history/leaders/_/type/pitching/breakdown/season/year/{}".format(year) + \
        "/start/{}".format(x)

        # opens the ESPN page
        pagePITCHING = requests.get(urlPITCHING)

        # Parses the page in HTML
        soupPITCHING = BeautifulSoup(pagePITCHING.text, 'html.parser')

        # Arguments that will be passed into our .find and .find_all
        attrs = {'attribute1Name': 'attribute1Value', 'attribute2Name': 'attribute2Value'}

        # Takes the five column headers. Only need to find it once
        # since it appears five times on the ESPN page.
        headers = soupPITCHING.find('tr', attrs={'class': 'colhead'})

        columns = [col.get_text() for col in headers.find_all('td')]

        # Using pandas to create an empty data frame to store player stats
        final_df = pd.DataFrame(columns=columns)

        # Use re's compile function to scrape all player data
        players = soupPITCHING.find_all('tr', attrs={'class': re.compile('row player-10-')})

        for player in players:
            # Gets player's stats
            stats = [stat.get_text() for stat in player.find_all('td')]

            # Temporary dataframe for a single player's stats
            temp_df = pd.DataFrame(stats).transpose()
            temp_df.columns = columns

            # Put player stats in the final dataframe
            final_df = pd.concat([final_df, temp_df], ignore_index=True)
        print(final_df)

        # Export to csv file displaying all 331 batters and their stats
        final_df.to_csv(r"C:\Users\Zach Patrignani\Desktop\mlb_stats.csv", index=False,
        header=True, sep=',', encoding='utf-8', mode='a')