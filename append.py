from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
def append():
    x=0
    thisdict = {}
    while(x<1000000):
        x+=1
        if(x in '/home/tanavc/mysite/debatedata.csv'):
            continue
        else:
            url = "https://www.tabroom.com/index/results/team_lifetime_record.mhtml?id1=" + "&" + "id2=" + str(x)
            res = urlopen(url)
            thepage = res.read()
            soup = BeautifulSoup(thepage, 'html.parser')
            try:
                teamname = soup.find_all("h4")[5].text
            except:
                continue
            if (soup.find_all("td")[10].text == "/"):
                continue
            else:
                adjustedteamname = teamname.replace('                    ', '')
                thisdict[x] = adjustedteamname.strip()
                print(thisdict[x])
                print(x)
                writeCSV = [x,thisdict[x]]
                f = open("debatedata.csv", "a")
                w = csv.writer(f)
                w.writerow(writeCSV)
                f.close()
append()
