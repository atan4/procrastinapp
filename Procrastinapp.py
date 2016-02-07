# Anne Schwartz, Adrianna Tan, Maja Svanberg
# ProcrastinApp.py
# Hack @ Smith
# 2o16-o2-o6

import sqlite3
import pandas.io.sql as sql
from pandas import *
import datetime
import classify
import matplotlib.pyplot as plt
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

          
app = Flask(__name__)

def fromTextToPickle(email,filename):
    
    # translating the .txt file
    history = sqlite3.connect(filename)
    
    # connects sqlite into a dataframe
    h = history.cursor()

    # goes through and gets the url table from database
    table = sql.read_sql('select * from urls["url"]',history)

    # reduces table into two columns, time of visit, url
    timeStamps = table[['last_visit_time','url','visit_count']]

    # adds 'email' column to table
    timeDF = DataFrame(data = timeStamps, columns = ['last_visit_time','url','visit_count','email'])
    # sets email to input email
    timeDF['email'] = email

    # stores table as file
    timeDF.to_pickle(email.split('@')[0] + '_pickle.pkl')
    
    #converts unix time to readable times
    timeDF['last_visit_time'] = timeDF['last_visit_time'].apply(dateTimeConversion)
    
    # reduces URL to main webpage url
    def splitIt(url):
        if url.split('/')[0] == 'http:' or url.split('/')[0] == 'https:':
            return '/'.join(url.split('/')[:3]) + '/'
        else:
            return None
    
    timeDF['url'] = timeDF['url'].apply(splitIt)

    # sorts by visit count
    timeDF = timeDF.sort(['visit_count'],ascending = False)
    # returns dataframe
    return timeDF


def dateTimeConversion(unixtime):
    #converts 17 digit time stamp
    time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=unixtime) 
    # formats it into calendar format
    convertedTime = time.isoformat()
    return convertedTime

def addCategories(df):
    '''takes a dataframe and changes it, adds category'''
    df['category'] = df['url'].apply(classify.getType)

#makes a dictionary with 24 spaces (one for each hour of the day)
def fillDict(): 
    count = 1
    twentyFour = {}
    while count <= 24:
        twentyFour[count] = 0
        count += 1
    return twentyFour

#fills the dictionary values with the number of sites visited in that hour (key)      
def mostCommonTimes(email,filename):
    dayDict = fillDict()
    for entry in fromTextToPickle(email,filename)['last_visit_time']:
        for key in dayDict:
            #splits the timestamp so only the hour 
            if key == int(entry.split('T')[1].split('.')[0].split(':')[0]):
                dayDict[key] += 1
    return dayDict
    
def top5websites(df):
    '''takes a datafram and returns the 10 most used websites'''
    # take the dataframe, group it by url and summarize
    grouped = df['visit_count'].groupby(df['url']).sum()
    # sort visit_count
    grouped['visit_count'] = grouped.sort(['visit_count'], ascending = False)
    # put the series into a dataframe for further analysis
    df = DataFrame({'url':grouped.index, 'visit_count':grouped.values})
    # write to textfile
    text_file = open("figure2.txt", "w")
    text_file.write(str(df.head()))
    text_file.close()
    # return head of data frame
    return df.head()
    
def top3categories(df):
    '''takes a dataframe and changes it, adds category'''
    # get the categories based on the urls
    df['category'] = df['url'].apply(classify.getType)
    # group visit counts by category and summarize
    grouped = df['visit_count'].groupby(df['category']).sum()
    # make dataframe from series
    df = DataFrame({'category':grouped.index, 'visit_count':grouped.values})

    #fixes missing parameter error from classify
    def errorFix(string):
        if len(string) >= 30:
            string = 'Other'
        return string
    # make sure error enters 'other'
    df['category'] = df['category'].apply(errorFix)
    
    # write to text file
    text_file = open("figure3.txt", "w")
    text_file.write(str(df))
    text_file.close()
    
    # return data frame
    return df
    
def findValue(string):
    '''returns value based on which category. the results are from
    a survey conducted online in a wellesley college community. 'other' 
    is categories as a 3, neutral on a scale'''
    if string == 'Arts':
        return 2.58
    elif string == 'Business & Economy':
        return 2.36
    elif string == 'News':
        return 1.96
    elif string == 'Computers & Technology':
        return 2.12
    elif string == 'Home & Domestic Life':
        return 3.2
    elif string == 'Health':
        return 2.08
    elif string == 'Reference & Education':
        return 1.76
    elif string == 'Recreation & Activities':
        return 2.68
    elif string == 'Science':
        return 1.8
    elif string == 'Shopping':
        return 3.76
    elif string == 'Society':
        return 3.08
    elif string == 'Sports':
        return 3.44
    else:
        return 3
    
def procrastinationValue(df):
    '''takes a data frame category/visit_count and returns to 
    a string and stores in a file a sentence describing the users
    procrastination rate'''
    # transform categoy into value
    df['category'] = df['category'].apply(findValue)
    # calculate provalue as categoryvalue * visit_count
    df['provalue'] = df['category']*df['visit_count']
    # store provalue as sum of provalues over sum of visit counts
    provalue = df['provalue'].sum()/df['visit_count'].sum()
    string = 'Your procrastination rate is: ' + str(provalue-1) + \
        ', on a scale from 0-4.'
    # saves string in .txt
    text_file = open("figure4.txt", "w")
    text_file.write(string)
    text_file.close()
    # returns string
    return string 
    
#makes a line plot of the daily activity (number of sites visited at different hours)
def dailyPlot(email, filename):
    # define most common times
    gg = mostCommonTimes(email, filename)
    # define x list and y list
    xlist = gg.keys() 
    ylist = gg.values()
    # initialize figure
    fig = plt.figure()
    # plot the thing
    plt.title('Daily Online Activity')
    plt.ylabel('number of sites visited')
    plt.xlabel('Time (24 Hour GMT)')
    # on a scale from 0 to 23 (24 in total), and 0 to max+200
    plt.axis([0,max(xlist)-2,0,max(ylist)+200])
    plt.plot(xlist)
    plt.plot(ylist)
    # display plot in kernel
    plt.show()
    # save figure
    fig.savefig('figure1.png')

@app.route('/')
def main():

    gg = dailyPlot('msvanberg@wellesley.edu', 'History.txt')
    df = top5websites(fromTextToPickle('msvanberg@wellesley.edu', 'History.txt'))
    print df
    top = top3categories(df)
    print top
    value = procrastinationValue(top)
    print value


if __name__=='__main__':
    #app.run()
    main()