
from bs4 import BeautifulSoup as bs
import requests
import os
from datetime import date
from datetime import datetime

path = "C:\ezan_project"

def open_file():
    today = date.today()
    day = today.strftime("%d")
    month = int(today.strftime("%m"))
    tr_months = ["Ocak", "Şubat", "Mart" , "Nisan" , "Mayıs", "Haziran" , "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    tr_month = ""
    for i in range(13):
        if month == i:
            tr_month = tr_months[i-1]
            break
    str_ezan_times = list()
    complete_path = os.path.join(path,"vakitler.txt")
    with open(complete_path,"r",encoding="utf-8") as file:
        checker = False
        for line in file:
            if day in line and tr_month in line:
                checker = True
                for time in line.split():
                    str_ezan_times.append(time)
        if checker == False:
            return False

    return str_ezan_times
    
def correct():
    if "vakitler.txt" not in os.listdir(path):
        print("Vakitler yükleniyor...")
        pulling_data()
    value = open_file()
    if value == False:
        print("Vakitler güncelleniyor...")
        pulling_data()
    liste = open_file()
    return liste

def remaining_time():
    str_ezan_times = correct()
    for i in range(4):
        str_ezan_times.pop(0)

    total_min = 1 
    now = datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    minutes_since_midnight = int(seconds_since_midnight /60)
    holder = list()
    for j in str_ezan_times:
        checker = False
        for i in j.split(":"):
            if checker == False:
                total_min = int(i) * 60
                checker = True
            else:
                total_min += int(i)
        holder.append(total_min)
    
    i = 0
    if len(holder) == 0:
        print("HOLDER BOŞŞŞŞ")
    while (holder[i] < minutes_since_midnight):
        if (i > 5):
            i = 0
            break
        i+=1

    if i == 0:
        remaining_hour = (1440 - minutes_since_midnight + holder[i]) // 60
        remaining_minute = (1440 - minutes_since_midnight + holder[i]) % 60
    else:
        remaining_hour = (holder[i] - minutes_since_midnight) // 60
        remaining_minute = (holder[i] - minutes_since_midnight) % 60
    
    next_time = ["Sabaha", "Güneşe", "Öğlene", "İkindiye", "Akşama", "Yatsıya"]
    if(remaining_hour != 0):
        sentence = "{} {} saat {} dakika kaldı".format(next_time[i],remaining_hour,remaining_minute)
    else:
        sentence = "{} {} dakika kaldı".format(next_time[i],remaining_minute)
        if (remaining_minute <= 45 and next_time[i] == "Akşama"):
            print("Yine kerahat vaktine kaldın kardeşşşş")

    print(sentence)

def pulling_data():
    global page
    page = None
    try:
        page = requests.get("https://namazvakitleri.diyanet.gov.tr/tr-TR/9581/karabuk-icin-namaz-vakti")
    except:
        print("NO INTERNET CONNECTION")
        if "vakitler.txt" in os.listdir(path):
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
            
            complete_path = os.path.join(path,"vakitler.txt")
            with open(complete_path,"w",encoding='utf-8') as file:
                a = 0
                for i in days:
                    file.write(i + "\t")
                    j = 0
                    while j<6:
                        file.write(vakitler[a] + " ")
                        j+=1
                        a+=1
                    file.write("\n")
                    
if __name__ == "__main__":
    remaining_time()
                



    
