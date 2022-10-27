#bu python dosyası, trendyol ve n11 sitelerinden veri kazıma işlemi için yazılmıştır.

#kütüphanelerin import edilmesi
import requests, re, json
from bs4 import BeautifulSoup
import psycopg2
import time

#kodun toplam çalışma süresini çıkarmak amaçlı timer başlatılması
start_time = time.time()

print('\nBu program Trendyol ve n11 üzerinden veri kazıma işlemi yapmaktadır.\n')
print('İşlem internet ve işlemci hızına göre değişkenlik göstermekle birlikte yaklaşık olarak 500 saniye sürmektedir. \n')

#veritabanı bağlantısının gerçekleştirilmesi
def dbConn():
    global connection, cursor
    connection = psycopg2.connect(
        user = "btbecirgkryyve",
        password = "23bebea366f5c8b8ce063c9b68d987a321bb979dee22aad3d975f7398dd4e652",
        host = "ec2-23-20-140-229.compute-1.amazonaws.com",
        port = "5432",
        database = "d7i1hcukm4nttn"
    )
    cursor = connection.cursor()
    print('Veri tabanı bağlantısı gerçekleştiriliyor....\n')

#trendyol veri kazıma fonksiyonu
def getTrendyolData():
    dbConn()
    main_url = "https://www.trendyol.com/laptop-x-c103108"
    print('Trendyol veri kazıma işlemi başladı.')
    
    #sayfa geçişleri için for döngüsü kurulması
    for a in range(1,10):
        print('Veri kazıma işlemi devam ediyor.')
        if a == 5:
            print("Kazıma işleminin %25'i tamamlandı")
            print("(X----)")
        elif a == 9:
            print("Kazıma işleminin %50'si tamamlandı")
            print("(XXx--)")
        
        url = main_url+'?pi={}'.format(a)
        page = requests.get(url) #html request
        soup = BeautifulSoup(page.content, "html.parser") #sayfa içeriğinin parse edilmesi
        tags = soup.find("div", {'class':"prdct-cntnr-wrppr"}).find_all('a') #sayfadaki tüm ürün linklerinin alınması

        #ürün linklerinin içindeki bilgileri almak için for döngüsü kurulması
        for tag in tags:
            tag = tag['href']
            r = requests.get('https://www.trendyol.com'+tag)
            soup2 = BeautifulSoup(r.content, "html.parser")

            #ürün görsel linklerinin alınması
            for item in soup2.find_all('img'):
                if str(item).find('mnresize') > 0:
                    item['src'] = item['src'].replace('/mnresize','')
                    start = item['src'].index('com')+3
                    end = item['src'].index('ty')-2
                    if len(item['src'])>end:
                        photo = item['src'][0: start:] + item['src'][end + 1::]
                        break

            r = r.text

            #verilerin json formatında çekilmesi
            matches1 = re.search(r"window.__PRODUCT_DETAIL_APP_INITIAL_STATE__=({.*}});window", r)
            matches2 = re.search(r"window.__PRODUCT_DETAIL_APP_INITIAL_STATE__\s=\s({.*}})", r)
            if matches1 is not None:
                matches = matches1
            elif matches2 is not None:
                matches = matches2
            else:
                print('Lütfen regex ifadelerini veya json data kaynaklarını kontrol edin.')
            if matches is not None:
                json_data = json.loads(matches.group(1))
                global brand, model_name, model_no, price, point, website, os, cpu, cpu_gen, ram, ssd_size, hdd_size,screen_size
                brand, model_name, model_no, price, point, website, os, cpu, cpu_gen, ram, disk_capacity, screen_size = "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok"
                brand = (json_data['product']['brand']['name']).upper() #marka adı
                model_name = (json_data['product']['name'].upper()) #model adı
                model_no = (json_data['product']['productCode'].upper()) #model no
                price =  (json_data['product']['price']['discountedPrice']['value']) #ürün fiyatı
                point =  (json_data['product']['ratingScore']['averageRating']) #ürün puanı
                website = 'trendyol'
                #ürünler bilgilerine id detayından ulaşılması
                for i in json_data['product']['attributes']:
                    attr_check = list(list(i.values())[0].values())[1]
                    if attr_check == 28:
                        os = list(list(i.values())[1].values())[0].upper()
                    elif attr_check == 168:
                        cpu = list(list(i.values())[1].values())[0].upper()
                    elif attr_check == 320:
                        cpu_gen = list(list(i.values())[1].values())[0].upper()
                    elif attr_check == 232:
                        ram = list(list(i.values())[1].values())[0].upper()
                    elif attr_check == 249:
                        ssd_size = list(list(i.values())[1].values())[0].upper()
                    elif attr_check == 467:
                        disk_capacity = list(list(i.values())[1].values())[0].upper()
                    elif attr_check == 23:
                        screen_size = list(list(i.values())[1].values())[0].upper()

                        #near duplicate kontrolü yapılması
                        duplicate_check = """select url from brand where url='"""+tag+"""'"""
                        cursor.execute(duplicate_check)
                        try:
                            global record
                            record = cursor.fetchall()[0][0]
                        except:
                            record = " "

                        #veritabanına kayıt için string veritipine dönüşüm.
                        point = str(point)
                        price = str(price)
                        
                        #near duplicate kontrolüne devam ediliyor.
                        if record == tag:
                            print('aynı kayıt olduğu için kaydedilmedi.', tag)
                            print('-------')
                            price_check = """SELECT price FROM brand WHERE url = '"""+tag+"""'"""
                            point_check = """SELECT product_point FROM brand WHERE url = '"""+tag+"""'"""
                            cursor.execute(price_check)
                            price_record = cursor.fetchall()[0][0]
                            cursor.execute(point_check)
                            point_record = cursor.fetchall()[0][0]
                            
                            #çekilen verideki price veya point değerleri veritabanındakinden farklıysa update işlemi yapılıyor.
                            if price != price_record:
                                print('fiyat güncelleniyor!')
                                new_price = price
                                price_update = """UPDATE brand SET price ='"""+new_price+"""' WHERE url = '"""+tag+"""'"""
                                cursor.execute(price_update)
                                connection.commit()
                            if point != point_record:
                                print('puan güncelleniyor')
                                new_point = point
                                point_update = """UPDATE brand SET product_point ='"""+new_point+"""' WHERE url ='"""+tag+"""'"""
                                cursor.execute(point_update)
                                connection.commit()
                        else:
                            brand_insert = """INSERT INTO brand VALUES ('"""+tag+"""', '"""+brand+"""', '"""+model_name+"""', '"""+model_no+"""', '"""+photo+"""', '"""+point+"""', '"""+price+"""', '"""+website+"""', '"""+os+"""', '"""+cpu+"""', '"""+cpu_gen+"""', '"""+ram+"""', '"""+disk_capacity+"""', '"""+screen_size+"""');"""
                            type_change = """ALTER TABLE brand ALTER COLUMN price type float USING PRICE::FLOAT;"""
                            cursor.execute(brand_insert)
                            cursor.execute(type_change)
                            connection.commit()
                            print(brand, model_no, 'pc kaydedildi.')
                            print('------')

#n11 veri kazıma fonksiyonu
def getn11Data():
    dbConn()
    main_url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar"
    print('n11 veri kazıma işlemi başladı.')
    #sayfa geçişleri için for döngüsünün kurulması
    for a in range(1,10):
        print('Veri kazıma işlemi devam ediyor.')
        if a == 5:
            print("Kazıma işleminin %60'ı tamamlandı")
            print("(XXXx-)")
        elif a == 9:
            print("Kazıma işleminin %75'i tamamlandı")
            print("(XXXXX)")
        url = main_url+'?pg={}'.format(a)
        page = requests.get(url) #html request
        soup = BeautifulSoup(page.content, "html.parser") #sayfa içeriğinin parse edilmesi
        tags = soup.find("div", {'class':"catalogView"}).find_all('a') #ürün linklerinin çekilmesi

        #ürün linklerinin içindeki bilgileri almak için for döngüsü kurulması
        for tag in tags:
            tag = tag['href']
            r = requests.get(tag)
            soup2 = BeautifulSoup(r.content, "html.parser")

            #n11 veri alınması engellemek için link forwardlama yapmakta.
            #link forwardlama kontrolü yapılması.
            fw_check = soup2.find('div', {'class': 'filterArea'})
            if fw_check is not None:
                print('n11 link forwardlayarak önlem almakta. Bu sebeple veri çekilemiyor.')
            else:
                data = soup2.find('div', {'class': 'unf-prop-context'}).find('ul').find_all('p', {'class': 'unf-prop-list-title'})
                data = list(data)
                key_data = []
                for i in data:
                    i = i.text
                    key_data.append(i)

                value_data = []
                data2 = soup2.find('div', {'class': 'unf-prop-context'}).find('ul').find_all('p', {'class': 'unf-prop-list-prop'})
                data2 = list(data2)
                for k in data2:
                    k = k.text
                    value_data.append(k)

                #elde edilen verilerin dictionary formatına dönüştürülmesi.
                #ürün özelliklerinin çekilmesi
                dictionary = dict(zip(key_data, value_data))
                brand_n11 = (dictionary['Marka'][1:]).upper()
                model_name_n11 = soup2.find('h1', {'class': 'proName'}) #model adı
                if model_name_n11 is None:
                    model_name_n11 = "Bilgi yok"
                else:
                    model_name_n11 = model_name_n11.text
                photo_n11 = soup2.find('div', {'class': 'imgObj'}).find('a')['href'] #ürün görseli
                if photo_n11 is None:
                    photo_n11 = "Bilgi yok"
                model_name_n11 = " ".join(model_name_n11.split()).upper() #model adı
                model_no_n11 = dictionary['Model'][1:].upper() #model numarası
                os_n11 = dictionary['İşletim Sistemi'][1:].upper() #işletim sistemi
                cpu_n11 = dictionary['İşlemci'][1:].upper() #cpu
                cpu_gen_n11 = dictionary['İşlemci Modeli'][1:].upper() #cpu nesli
                ram_n11 = dictionary['Bellek Kapasitesi'][1:].upper() #ram
                disk_capacity_n11 = dictionary['Disk Kapasitesi'][1:].upper() #disk kapasitesi
                screen_size_n11 = dictionary['Ekran Boyutu'][1:].upper() #ekran ölçüsü
                point_n11 = soup2.find('strong', {'class': 'ratingScore r100'}) #ürün puanı
                if point_n11 is None:
                    point_n11 = "Bilgi yok"
                    point_n11 = str(point_n11)
                else:
                    point_n11 = point_n11.text
                    point_n11 = str(point_n11)
                price_n11 = soup2.find('div', {'class': 'unf-p-summary-price'}) #ürün fiyatı
                if price_n11 is None:
                    price_n11 = "Bilgi yok"
                    price_n11 = str(price_n11)
                    price_n11 = price_n11.replace(".", "")
                    price_n11 = price_n11.replace(",", ".")
                else:
                    price_n11 = price_n11.text
                    price_n11 = str(price_n11)
                    price_n11 = price_n11.replace(".", "")
                    price_n11 = price_n11.replace(",", ".")
                website_n11 = 'n11'

                if brand_n11 is None:
                    brand_n11 = "Bilgi yok"
                elif model_name_n11 is None:
                    model_name_n11 = "Bilgi yok"
                elif model_no_n11 is None:
                    model_no_n11 = "Bilgi yok"
                elif os_n11 is None:
                    os_n11 = "Bilgi yok"
                elif cpu_n11 is None:
                    cpu_n11 = "Bilgi yok"
                elif cpu_gen_n11 is None:
                    cpu_gen_n11 = "Bilgi yok"
                elif ram_n11 is None:
                    ram_n11 = "Bilgi yok"
                elif disk_capacity_n11 is None:
                    disk_capacity_n11 = "Bilgi yok"
                elif screen_size_n11 is None:
                    screen_size_n11 = "Bilgi yok"

                #near duplicate kontrolü
                duplicate_check2 = """select url from brand where url='"""+tag+"""'"""
                cursor.execute(duplicate_check2)
                try:
                    global record2
                    record2 = cursor.fetchall()[0][0]
                except:
                    record2 = " "
                
                if record2 == tag:
                    print('aynı kayıt olduğu için kaydedilmedi.', tag)
                    print('-------')
                    price_check = """SELECT price FROM brand WHERE url = '"""+tag+"""'"""
                    point_check = """SELECT product_point FROM brand WHERE url = '"""+tag+"""'"""
                    cursor.execute(price_check)
                    price_record = cursor.fetchall()[0][0]
                    cursor.execute(point_check)
                    point_record = cursor.fetchall()[0][0]

                    #çekilen verideki price veya point değerleri veritabanındakinden farklıysa update işlemi yapılıyor.
                    if price_n11 != price_record:
                        print('fiyat güncelleniyor!')
                        new_price = price_n11
                        price_update = """UPDATE brand SET price ='"""+new_price+"""' WHERE url = '"""+tag+"""'"""
                        cursor.execute(price_update)
                        connection.commit()
                    if point_n11 != point_record:
                        print('puan güncelleniyor')
                        new_point = point_n11
                        point_update = """UPDATE brand SET product_point ='"""+new_point+"""' WHERE url ='"""+tag+"""'"""
                        cursor.execute(point_update)
                        connection.commit()
                else:
                    brand_insert2 = """INSERT INTO brand VALUES ('"""+tag+"""', '"""+brand_n11+"""', '"""+model_name_n11+"""', '"""+model_no_n11+"""', '"""+photo_n11+"""', '"""+point_n11+"""', '"""+price_n11+"""', '"""+website_n11+"""', '"""+os_n11+"""', '"""+cpu_n11+"""', '"""+cpu_gen_n11+"""', '"""+ram_n11+"""', '"""+disk_capacity_n11+"""', '"""+screen_size_n11+"""');"""
                    type_change2 = """ALTER TABLE brand ALTER COLUMN price type float USING PRICE::FLOAT;"""
                    cursor.execute(brand_insert2)
                    cursor.execute(type_change2)
                    connection.commit()
                    print(brand_n11, model_no_n11, 'pc kaydedildi.')
                    print('---------')

#veri kazıma fonksiyonlarının çalıştırılması
getTrendyolData()
print('Trendyol kazıma işlemi tamamlandı.')
getn11Data()
print('n11 kazıma işlemi tamamlandı.')

#veritabanı bağlantısının kapatılması
cursor.close()
connection.close()

#sayacın durdurulması
stop_time = time.time()
print("The time of the run:", stop_time - start_time)