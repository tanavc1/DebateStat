from flask import Flask, request,  redirect, url_for, render_template
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import string
import csv
import webbrowser
import selenium
from urllib.request import urlopen


def commonletter(string1, string2) :
     holder = ""
     firstname1 = string1.split(" ")[0]
     firstname2 = string2.split(" ")[0]
     lastname1 = string1.split(" ")[1]
     lastname2 = string2.split(" ")[1]
     inters=list(set(string1)&set(string2))
     for p in inters :
       holder = holder + p
     if (len(string1) < len(string2)) :
        leftover = len(string1)-len(holder)
     else :
        leftover = len(string2)-len(holder)
     if (leftover <= 1) :
         if (firstname1 == firstname2) :
             return True
         elif (lastname1 == lastname2) :
             return True
         else :
             return False

app = Flask(__name__)
@app.route("/")
def debatesite():
    return render_template("debatesite.html")
@app.route('/ind/')
def individual():
    return render_template("ind.html")
@app.route('/aboutus/')
def aboutus():
    return render_template("aboutus.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['u']
    texttwo = request.form['t']
    with open( 'debatedata.csv' , 'r') as f:
        second_list_1 = []
        url_list_1 = []
        lifetime_list_1 = []
        second_list_2 = []
        url_list_2 = []
        lifetime_list_2 = []
        for line in f.readlines():
            if string.capwords(text) in line:
                firstid = line[0:6]
                second_list_1.append(firstid)
        for x in second_list_1:
            indurl_1 = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=&id2=" + x
            url_list_1.append(indurl_1)
            url_tuple_1 = tuple(url_list_1)
        for y in url_tuple_1 :
            html_1 = urlopen(y)
            wholepage_1 = html_1.read()
            soup_1 = BeautifulSoup(wholepage_1, 'html.parser')
            lifetimerecord_1 = soup_1.find_all("td")[12].text
            locationof_1 = lifetimerecord_1.find("/")
            stringnum_1= lifetimerecord_1[locationof_1+1::]
            finalnum_1 = int(stringnum_1)
            lifetime_list_1.append(finalnum_1)
        lifetime_tuple_1 = tuple(lifetime_list_1)
        highestnumtup_1 = max(lifetime_tuple_1)
        locationmax_1 = lifetime_tuple_1.index(highestnumtup_1)
        idbestlocation_1 = second_list_1[locationmax_1]
        besturlone = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=" + idbestlocation_1
    with open( 'debatedata.csv' , 'r') as f:
        for line in f.readlines():
            if string.capwords(texttwo) in line:
              secondid = line[0:6]
              second_list_2.append(secondid)
        for x in second_list_2:
            indurl_2 = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=&id2=" + x
            url_list_2.append(indurl_2)
            url_tuple_2 = tuple(url_list_2)
        for y in url_tuple_2 :
            html_2 = urlopen(y)
            wholepage_2 = html_2.read()
            soup_2 = BeautifulSoup(wholepage_2, 'html.parser')
            lifetimerecord_2 = soup_2.find_all("td")[12].text
            locationof_2 = lifetimerecord_2.find("/")
            stringnum_2 = lifetimerecord_2[locationof_2+1::]
            finalnum_2 = int(stringnum_2)
            lifetime_list_2.append(finalnum_2)
        lifetime_tuple_2 = tuple(lifetime_list_2)
        highestnumtup_2 = max(lifetime_tuple_2)
        locationmax_2 = lifetime_tuple_2.index(highestnumtup_2)
        idbestlocation_2 = second_list_2[locationmax_2]
        besturltwo = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=" + idbestlocation_2
        totalurl_1 = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=" + idbestlocation_1  + "&id2=" + idbestlocation_2

        html_3 = urlopen(totalurl_1)
        wholepage_3 = html_3.read()
        soup_3 = BeautifulSoup(wholepage_3, 'html.parser')
        lifetimerecord_3 = soup_3.find_all("td")[12].text
        if (lifetimerecord_3 != "-") :
            return redirect(totalurl_1)
        else:
            dupe_dict = {}
            for x in second_list_1:
                for y in second_list_2:
                    totalurl_1 = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=" + x  + "&id2=" + y
                    res = requests.get(totalurl_1)
                    #html_4 = urlopen(totalurl_1)
                    #wholepage_4 = html_4.read()
                    soup_4 = BeautifulSoup(res.content, 'html.parser')
                    lifetimerecord_4 = soup_4.find_all("td")[12].text
                    if(lifetimerecord_4 == "-") :
                        continue
                    locationof_4 = lifetimerecord_4.find("-")
                    stringnum_4 = lifetimerecord_4[locationof_4+1::]
                    finalnum_4 = int(stringnum_4)
                    dupe_dict[finalnum_4] = totalurl_1
            maximum = 0
            for i in dupe_dict.keys():
                if i>maximum:
                    maximum = i
            return redirect(dupe_dict[maximum])

@app.route('/ind/', methods=['POST']) ## Individual
def ind_version():
    indtext = request.form['secone']
    with open('debatedata.csv', 'r') as files:
        second_list = []
        url_list = []
        lifetime_list = []
        event_list = []
        for line in files.readlines():
            if string.capwords(indtext) in line:
                indsecond = line[0:6]
                second_list.append(indsecond)
        if (second_list == []) :
            files.seek(0)
            if indtext.count(" ") == 0 :
                    return "Try again. You may have misspelled a name or your entry does not exist."
            for line in files.readlines():
                if line.split(",")[1].count(" ") == 0 :
                    continue
                elif commonletter(indtext,line.split(",")[1]) == True :
                    redirect("https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=&id2=" + line[0:6])
        if (second_list == []) :
            return "Try again. You may have misspelled a name or your entry does not exist."
        for x in second_list:
            indurl = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=&id2=" + x
            url_list.append(indurl)
            url_tuple = tuple(url_list)
        for y in url_tuple :
            html = urlopen(y)
            wholepage = html.read()
            soup = BeautifulSoup(wholepage, 'html.parser')
            debateevent = soup.find(class_='fifth semibold bluetext rightalign padtop').text
            if debateevent.count("Public Forum") > 0 :
                debateevent = "PF"
            elif debateevent.count("Lincoln") > 0 :
                debateevent = "LD"
            elif debateevent.count("LD") > 0 :
                debateevent = "LD"
            elif debateevent.count("Policy") > 0 :
                debateevent = "Policy"
            elif debateevent.count("PF") > 0 :
                debateevent = "PF"
            elif debateevent.count("Parliamentary") > 0 :
                debateevent = "Parli"
            elif debateevent.count("Parli") > 0 :
                debateevent = "Parli"
            event_list.append(debateevent)
            lifetimerecord = soup.find_all("td")[12].text
            locationof = lifetimerecord.find("/")
            stringnum = lifetimerecord[locationof+1::]
            finalnum = int(stringnum)
            lifetime_list.append(finalnum)
        event_tuple = tuple(event_list)
        lifetime_tuple = tuple(lifetime_list)
        highestnumtup = max(lifetime_tuple)
        locationmax = lifetime_tuple.index(highestnumtup)
        urlbestlocation = url_tuple[locationmax]
        lifeurldic = dict(zip(lifetime_tuple,url_tuple))
        urlwithevent = dict(zip(lifetime_tuple,event_tuple))
        if len(second_list) <= 6 :
            second_list = []
            return redirect(urlbestlocation)
        else :
            second_list = []
            return render_template("ind.html" , url_tuple = url_tuple, lifetime_tuple = lifetime_tuple, lifeurldic = lifeurldic, urlwithevent = urlwithevent )
#@app.route('/aboutus/', methods=['POST'])
    #randomstuff = ("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in url_dictlist.items()) + "}")
    #return render_template("ind.html" , theurl = urlbestlocation )
    # lifetimerecord = highestnumtup
   # res = requests.get(indurl)
   # soup = BeautifulSoup(res.content, 'html.parser')
  #  lifetimerecord = soup.find_all("td")[12].text
   # lifetimepercent = soup.find_all("td")[13].text
   # lifetimeelim = soup.find_all("td")[14].text
  #  lifetimeelimpercent = soup.find_all("td")[14].text
  #  if (lifetimeelim == "/"):
  #      lifetimeelim = "N/A"
  #  if (lifetimeelimpercent == "/"):
  #      lifetimeelimpercent = "N/A"
  #  tourneyone = soup.find_all("h5")[1].text.strip()
  # , len = len(url_tuple), url_tuple = urlbestlocation

  #  return render_template("ind.html" , theurl = indurl, lifetimetotal = "Lifetime Prelim Record: "+ lifetimerecord, lifetimepe =  "Lifetime Prelim Percent: " + lifetimepercent , lifetimeelim = "Lifetime Elim Record: " + lifetimeelim , lifetimeelimpe = "Lifetime Elim Record: " + lifetimeelimpercent)
if __name__ == "__main__" :
  app.run()

  #debug=True

  #res = requests.get(totalurl)
  #soup = BeautifulSoup(res.content, 'html.parser')
  #lifetimestat = soup.find_all("td")[9].text
  #return lifetimestat
  #, methods=['POST']

  # totalurlfirst = urlopen(totalurl_1)
  #  totalurlpage = totalurlfirst.read()
  #  totalurlhtmlparse = BeautifulSoup(totalurlpage, 'html.parser')
 #   totalurllifetime = totalurlhtmlparse.find_all("td")[12].text
 #   if totalurllifetime != "-" :
 #       totalurl_1 = totalurl_1
 #   else :
 #       q =-1
 #       while totalurllifetime == "-" :
 #for line in files.readlines():
 #               if commonletter(indtext,line) == True :
  #                  close_names.append(line)
 #           cnames_tuple = tuple(close_names)
   #         return render_template("ind.html" , cnames_tuple = cnames_tuple )
  #         q+=1
          #changingurl = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=" + second_list_1[q]  + "&id2=" + idbestlocation_2
   #        totalurl_1 = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=" + idbestlocation_1   + "&id2=" + second_list_2[q]


