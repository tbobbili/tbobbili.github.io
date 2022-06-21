from hashlib import new
from os import times
import string
from xml.dom import minicompat
from bs4 import BeautifulSoup
import requests
import statistics
#from selenium import Select
#import pandas as pd


#get the website for a specific school 
def grab_time_link(link):
    link = (link.partition(' ')[2])
    link = (link.partition(' ')[2])
    link = (link.partition(' ')[0])
    link = (link.partition('"')[2])
    link = (link.partition('"')[0])
    new_link = 'https://swimcloud.com' + link
    return new_link



def get_event(par_list, link):
    while True: 
        event = input(par_list)
        if event in par_list:
            break
        else:
            print()
            print(event, "not in list. Is your event capitalized?TRY AGAIN")
    for option in link.find_all('option'):
        if event == (option.text):
            event_val = str(option['value'])
    return event_val



def get_times(link):
    times = []
    table_rows = link.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if len(row) != 0:
            time = row[-2]
            #print(time)
            if ':' in str(time):
                min = int(time.partition(':')[0])
                fin_time = min*60 + float(time.partition(':')[2])
                times.append(fin_time)
            else:
                times.append(float(time))
    return times


def min_times(time):
    min = int(time) // 60
    sec = round(time - min*60, 2)
    if sec < 10:
        return str(str(min) + ':0' + str(sec))
    return str(str(min) + ':' + str(sec))


def main():
    base_url = 'https://www.swimcloud.com/team/105/'
    soup = BeautifulSoup(requests.get(base_url).text, 'lxml')
    #print(soup.body.div.nav.a)
    block = soup.find('nav', class_ = 'c-nav c-nav--inline c-nav--responsive')
    for button in block:
        if 'Times' in str(button):
            time_link = str(button)
    spec_link = grab_time_link(time_link)
    ###function to grab time data (paramter should be event)
    soup2 = BeautifulSoup(requests.get(spec_link).text, 'lxml')
    selection = soup2.find_all('option')
    new_select = []
    for i in selection:
        x = str(i).partition('>')[2]
        x = x.partition('<')[0]
        new_select.append(x)
    new_select = new_select[:26]
    print("Please select the event you want data for")
    event_link = spec_link + '?page=1&gender=M&event=' + get_event(new_select, soup2) +'&course=Y&season=25'
    soup3 = BeautifulSoup(requests.get(event_link).text, 'lxml')
    time_list = get_times(soup3)
    new_quant = []
    quant = statistics.quantiles(time_list)
    if int(time_list[-1]) > 60:
        print()
        print("The mean time is" , min_times(statistics.mean(time_list)))
        print("The fastest time is", min_times(min(time_list)))
        for i in quant:
            new_quant.append(round(min_times(i),2))
        print("The quartiles are", new_quant)
    else:
        print()
        print("The mean time is" , round(statistics.mean(time_list), 2))
        print("The fastest time is", min_times(min(time_list)))
        for i in quant:
            new_quant.append(round(i,2))
        print("The quartiles are", new_quant)
    
    
    

if __name__ == "__main__":
  main()



