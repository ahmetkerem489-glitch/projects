#Hastane Randevu Sistemi

#Kullanıcı ve randevu sekreteri olmak üzere iki yetki olacak. kullanıcı randevu günü, randevu saati, 
#randevu alacağı polikliniği seçebilecek. her kullanıcının ayrı bir randevu listesi olacaktır. 
#randevu alma sınırı olacaktır. sekreter ise randevuları iptal edebilir gününü ve saatini değiştirebilir.
#kullanıcılar da randevu iptal edebilir. bir kullanıcı randevu iptal ettikten 
#sonra bir daha randevu alamaz

#str ve int (E/H) T VEYA numara seç değerleri birbirleri yerine almasını engellemek için 
def veri_al(tip,mesaj,min_val=None,max_val=None,gecerli_degerler=None):
    while True:
        ham_veri=input(mesaj).strip()
        if tip =="str":
            if not ham_veri:
                print("\Bu alan boş bırakılamaz, lütfen bir değer giriniz\n")
                continue
            if not ham_veri.replace(" ","").isalpha():
                print("Lütfen sadece harf giriniz!")
                continue
            return ham_veri
        elif tip=="int":
            try:
                deger=int(ham_veri)
            except ValueError:
                print("\nLütfen bir sayı giriniz! '{ham_veri}' sayı değil.\n")
                continue
            if min_val is not None and deger < min_val:
                print(f"\nGirilen değer çok küçük. Minimum: {min_val}\n")
                continue
            if max_val is not None and deger>max_val:
                print(f"\nGirilen değer çok büyük. Maksimum: {max_val}")
                continue
            if gecerli_degerler is not None and deger not in gecerli_degerler:
                print(f"\nGeçersiz değer. Kabul edilen değerler: {gecerli_degerler}")
                continue
            return deger
        elif tip=="eh":
            deger=ham_veri.upper()
            if deger not in("E","H"):
                print("\nLütfen yalnızca E veya H giriniz\n")
                continue
            return deger
        elif tip=="int_veya_T":
            deger=ham_veri.upper()
            if deger=="T":
                return "T"
            try:
                deger=int(ham_veri)
            except ValueError:
                print(f"\nLütfen bir numara veya 'T' giriniz. '{ham_veri}' geçerli değil\n")
                continue
            if min_val is not None and deger<min_val:
                print(f"\nGirilen değer çok küçük. Minimum: {min_val}\n")
                continue
            if max_val is not None and deger>max_val:
                print(f"\nGirilen değer çok büyük. Maksimum: {max_val}")
                continue
            return deger
        else:
            raise TypeError(f"Tanımsız tip: '{tip}'.Geçerli Tipler: str|int|eh|int_veya_T")
                
#polikinik yetki veya gün seçerken tüm seçenekleri göstermesi için     
def secim_yap(liste, baslik):
    print(f"---Lütfen bir {baslik} seçin---")
    for i, eleman in enumerate(liste, 1):
        print(f"{i}.{eleman}")

    while True:
        try:
            secim = int(input(f"Seçiminiz (1-{len(liste)})\n"))
            if 1 <= secim <= len(liste):
                secilen_eleman = liste[secim - 1]
                print(f"\nSeçilen {baslik}: {secilen_eleman}\n")
                return secilen_eleman
            else:
                print("Lütfen listedeki sayılardan birini giriniz!")
        except ValueError:
            print("Lütfen bir sayı giriniz!\n")

#bunu fonksiyon olarak yazmaya gerek yoktu ama böyle daha havalı oluyor
def giris_ekrani():
    print("\n\n"+"=" * 25 + "\nHASTANE RANDEVU SİSTEMİ\n" + "=" * 25+"\n")
    secim = secim_yap(yetkiler, "Yetki")
    return secim.upper()


def randevu_al():
    ad = veri_al("str","Adınızı giriniz:\n")
    if ad in iptal_listesi:
        #bura nedense çalışmıyor. çözemedim
        print("\n!!Bu hasta daha önce ranevu iptal ettiği için bir daha randevu alamaz!!\n")
        return
    if ad not in ran_listesi:
        ran_listesi[ad] = []
    
    if ad in ran_listesi:
        if len(ran_listesi[ad])>=2:
            print("\n2'den fazla randevu alamazsınız!\n")
            return
    polikinik = secim_yap(polikinikler, "Polikinik")
    gun = secim_yap(gunler, "Gün")
    
    while True:
        try:
            saat = veri_al("int","Saat kaça randevu almak istersiniz(08:00 - 17:00):\n", min_val=8, max_val=17)
            if saat < 8 or saat > 17:
                print("\nLütfen 8 ile 17 arasında bir saat giriniz!")
            else:
                break  
    
        except ValueError:
            print("\nLütfen sadece sayı giriniz!")

    randevu1 = {"polikinik": polikinik, "gun": gun, "saat": saat}
    ran_listesi[ad].append(randevu1)
    ran_istek = input("İkinci bir randevu almak ister misiniz(E/H):").upper()
    if ran_istek == "E":
        if len(ran_listesi[ad])>=2:
            print("\n2'den fazla randevu alamazsınız!\n")
            return ran_istek
        while True:
            polikinik2 = secim_yap(polikinikler, "Polikinik")
            gun2 = secim_yap(gunler, "Gün")
            saat2 = veri_al("int","Saat kaça randevu almak istersiniz(08:00 - 17:00):", min_val=8,max_val=17)
            if gun == gun2 and saat == saat2:
                print("Farklı bir gün ve saat belirleyin!!\n")
                continue
            elif polikinik == polikinik2:
                print("Farklı bir polikinik seçin!!\n")
                continue
            else:
                randevu2 = {"polikinik": polikinik2, "gun": gun2, "saat": saat2}
                ran_listesi[ad].append(randevu2)
                break
    elif ran_istek == "H":
        print(f"{ad} adına randevular başarı ile alındı.")
    randevular=ran_listesi[ad]
    for i, r in enumerate(randevular):
        print(f"\n{i + 1}.Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}")
    return ran_listesi

# randevu iptal eden yetkiye göre hastayı randevu almasını engellemek için
def randevu_iptal(yetkili=None):
    if not ran_listesi:
        print("Sistemde kayıtlı randevu bulunmamaktadır.")
        return
    ad = veri_al("str","Randevusunu iptal etmek istediğiniz kişinin adını giriniz:\n")
    if ad not in ran_listesi:
        print(f"'{ad}' adına kayıtlı randevu bulunamadı")
        return
    randevular = ran_listesi[ad]
    print(f"\n{ad} adına kayıtlı randevular:\n")
    for i, r in enumerate(randevular):
        print(f"{i+1}.Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}\n")

    if len(randevular) == 1:
        while True:                                          
            onay = input("\nBu randevuyu iptal etmek ister misiniz(E/H):\n").upper()
            if onay == "E":
                del ran_listesi[ad]
                if yetkili == "HASTA":
                    iptal_listesi.add(ad) 
                print("Randevunuz başarıyla iptal edilmiştir.")
                break                                       
            elif onay == "H":
                print("İptal işleminden vazgeçildi.")
                break
            else:
                print("\nE veya H giriniz!!\n")
    else:
        secim = veri_al("int_veya_T","Hangi randevuyu iptal etmek istersiniz(numara giriniz/Tümü için T):", min_val=1, max_val=len(randevular))
        if secim == "T":
            del ran_listesi[ad]
            iptal_listesi.add(ad)
            print("Tüm randevular başarıyla iptal edildi")
        else:
            try:
                secim = int(secim) - 1
                if 0 <= secim < len(randevular):
                    iptal_edilen = randevular.pop(secim)
                    print(f"{iptal_edilen['polikinik']} - {iptal_edilen['gun']} - {iptal_edilen['saat']} randevusu iptal edilmiştir!")
                    if not ran_listesi[ad]:
                        iptal_listesi.add(ad)
                        del ran_listesi[ad]
                else:
                    print("!!Geçersiz Numara!!")
            except ValueError:
                print("Lütfen geçerli bir numara giriniz.")

#bunun gibi hasta menüsü yapmak yerine hasta menüsünü ana koda yazdım
def sekreter_menusu():
    if not ran_listesi:
        print("Sistemde kayıtlı randevu bulunmamaktadır.")
        return
    print("-" * 5, "RANDEVU LİSTESİ", "-" * 5)
    for ad, randevular in ran_listesi.items():               
        print(f"\nHasta: {ad}")
        for i, r in enumerate(randevular, 1):               
            print(f"  {i}. Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}")

    islem_sekreter = secim_yap(["Randevu İptal", "Randevu Düzenle","Ana Menü"], "İşlem")

    if islem_sekreter == "Randevu İptal":
        randevu_iptal()
        #Boş çünkü randevu sekreteri iptal ediyor o yüzden hasta gene randevu alabilir
    elif islem_sekreter == "Randevu Düzenle":
        for i, r in enumerate(randevular):
            print(f"{i + 1}.Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}")
        duzenle_ad = veri_al("str","Randevusunu düzenlemek istediğiniz hastanın adını yazınız:\n")
        if duzenle_ad not in ran_listesi:
            print("Bu isimde bir hasta randevu almamış.")
            return
        duzenlenecek_ran = ran_listesi[duzenle_ad]
        if len(duzenlenecek_ran) == 1:
            r = duzenlenecek_ran[0]                          
            print(f"1. Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}")
            yeni_polikinik = secim_yap(polikinikler, "Polikinik")
            yeni_gun = secim_yap(gunler, "Gün")
            yeni_saat = int(input("08:00 ila 17:00 arasında bir saat seçin: "))
            duzenlenecek_ran[0] = {"polikinik": yeni_polikinik, "gun": yeni_gun, "saat": yeni_saat}  
        else:
            for i, r in enumerate(duzenlenecek_ran, 1):     
                print(f"{i}. Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}")
            secim = int(input("Hangi randevuyu düzenlemek istersiniz(numara giriniz):")) - 1
            yeni_polikinik = secim_yap(polikinikler, "Polikinik")
            yeni_gun = secim_yap(gunler, "Gün")
            yeni_saat = veri_al("int","08:00 ila 17:00 arasında bir saat seçin:", min_val=8,max_val=17)
            duzenlenecek_ran[secim] = {"polikinik": yeni_polikinik, "gun": yeni_gun, "saat": yeni_saat}  
        print(f"\n{duzenle_ad} adına randevu başarıyla güncellendi.")
    
    elif islem_sekreter == "Ana Menü":
        giris_ekrani()


yetkiler = ["HASTA", "RANDEVU SEKRETERİ"]
ran_listesi = {}
iptal_listesi = set()
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
polikinikler = ["Dahiliye", "Kardiyoloji", "Dermatoloji", "Nöroloji", "Göğüs Hastalıkları",
                "Fizik Tedavi ve Rehabilitasyon", "Genel Cerrahi", "Ortopedi ve Travmatoloji",
                "Kadın Hastalıkları ve Doğum", "Çocuk Sağlığı ve Hastalıkları", "Kulak Burun Boğaz",
                "Beyin ve Sinir Cerrahisi", "Ağız ve Diş Sağlığı", "Psikiyatri", "Göz Hastalıkları",
                "Anesteziyoloji ve Reanimasyon"]


while True:
    yetki = giris_ekrani()
    if yetki == "HASTA":
        islem=secim_yap(["Randevu Al", "Randevu İptal","Ana Menü"], "İşlem")
        if islem=="Randevu Al":
            randevu_al()
        elif islem=="Randevu İptal":
            randevu_iptal(yetkili="HASTA")
        elif islem=="Ana Mneü":
            giris_ekrani()
    elif yetki=="RANDEVU SEKRETERİ":
        sekreter_menusu()
        
