from bs4 import BeautifulSoup as bs
import requests
import os
from datetime import date
from datetime import datetime

def remaining_time():
    today = date.today()
    day = today.strftime("%d")
    month = int(today.strftime("%m"))
    tr_months = ["Ocak", "Şubat", "Mart" , "Nisan" , "Mayıs", "Haziran" , "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    tr_month = ""
    for i in range(13):
        if month == i:
            tr_month = tr_months[i-1]
            break
    str_ezan_times = []
    with open("vakitler.txt","r",encoding="utf-8") as file:
        for line in file:
            if day in line and tr_month in line:
                for time in line.split():
                    str_ezan_times.append(time)
    for i in range(4):
        str_ezan_times.pop(0)

    total_min = 1 
    now = datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    minutes_since_midnight = int(seconds_since_midnight /60)
    holder = list()
    for i in range(6):
        checker = False
        for i in str_ezan_times[i].split(":"):
            if checker == False:
                total_min = int(i) * 60
                checker = True
            else:
                total_min += int(i)
        holder.append(total_min)
    
    i = 0
    while (holder[i] < minutes_since_midnight):
        i+=1
        if (i == 6):
            i = 0
            break

    if i == 0:
        remaining_hour = (1440 - minutes_since_midnight + holder[i]) // 60
        remaining_minute = (1440 - minutes_since_midnight + holder[i]) % 60
    else:
        remaining_hour = (holder[i] - minutes_since_midnight) // 60
        remaining_minute = (holder[i] - minutes_since_midnight) % 60

    sentence = "Ezana {} saat {} dakika kaldı".format(remaining_hour,remaining_minute)
    print(sentence)

def pulling_data():
    global page
    page = None
    try:
        page = requests.get("https://namazvakitleri.diyanet.gov.tr/tr-TR/9581/karabuk-icin-namaz-vakti")
    except:
        print("NO INTERNET CONNECTION")
        if "vakitler.txt" in os.listdir():
            print("Kayıtlar kullanılıyor...")

    finally:
        if page:
            soup = bs(page.text,"html.parser")
            table = soup.find(class_="table vakit-table")
            times = table.find_all("td")
            days = []
            vakitler = []
            for i in times:
                if len(i.contents[:][0]) > 5:
                    days.append(i.contents[:][0])
                else:
                    vakitler.append(i.contents[:][0])
            
            with open("vakitler.txt","w",encoding='utf-8') as file:
                a = 0
                for i in days:
                    file.write(i + "\t")
                    j = 0
                    while j<6:
                        file.write(vakitler[a] + " ")
                        j+=1
                        a+=1
                    file.write("\n")
                    


remaining_time()
                



    