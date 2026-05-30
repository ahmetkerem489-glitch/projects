def secim_yap(liste, baslik):
    print(f"---Lütfen bir {baslik} seçin---")
    for i, eleman in enumerate(liste, 1):
        print(f"{i}.{eleman}")

    while True:
        try:
            secim = int(input(f"Seçiminiz (1-{len(liste)})\n"))
            if 1 <= secim <= len(liste):
                secilen_eleman = liste[secim - 1]
                print(f"-> Seçilen {baslik}: {secilen_eleman}\n")
                return secilen_eleman
            else:
                print("Lütfen listedeki sayılardan birini giriniz!")
        except ValueError:
            print("Lütfen bir sayı giriniz!\n")


def giris_ekrani():
    print("=" * 25 + "\nHASTANE RANDEVU SİSTEMİ\n" + "=" * 25)
    secim = secim_yap(yetkiler, "Yetki")
    return secim.upper()


def randevu_al():
    while True:
        ad = input("Adınızı giriniz:\n")
        polikinik = secim_yap(polikinikler, "Polikinik")
        gun = secim_yap(gunler, "Gün")
        saat = int(input("Saat kaça randevu almak istersiniz(08:00 - 17:00):\n"))
        randevu1 = {"polikinik": polikinik, "gun": gun, "saat": saat}
        if ad not in ran_listesi:
            ran_listesi[ad] = []
        ran_listesi[ad].append(randevu1)
        ran_istek = input("İkinci bir randevu almak ister misiniz(E/H):").upper()
        if ran_istek == "E":
            while True:
                polikinik2 = secim_yap(polikinikler, "Polikinik")
                gun2 = secim_yap(gunler, "Gün")
                saat2 = int(input("Saat kaça randevu almak istersiniz(08:00 - 17:00):"))
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
            break
    print(f"{ad} adına randevular başarı ile alındı.")
    return ran_listesi


def randevu_iptal():
    if not ran_listesi:
        print("Sistemde kayıtlı randevu bulunmamaktadır.")
        return
    ad = input("Randevusunu iptal etmek istediğiniz kişinin adını giriniz:")
    if ad not in ran_listesi:
        print(f"'{ad}' adına kayıtlı randevu bulunamadı")
        return
    randevular = ran_listesi[ad]
    print(f"\n{ad} adına kayıtlı randevular\n:")
    for i, r in enumerate(randevular):
        print(f"{i + 1}.Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}")

    if len(randevular) == 1:
        while True:                                          
            onay = input("\nBu randevuyu iptal etmek ister misiniz(E/H):\n").upper()
            if onay == "E":
                del ran_listesi[ad]
                print("Randevunuz başarıyla iptal edilmiştir.")
                break                                       
            elif onay == "H":
                print("İptal işleminden vazgeçildi.")
                break
            else:
                print("\nE veya H giriniz!!\n")
    else:
        secim = input("Hangi randevuyu iptal etmek istersiniz(numara giriniz/Tümü için T):").upper()
        if secim == "T":
            del ran_listesi[ad]
            print("Tüm randevular başarıyla iptal edildi")
        else:
            try:
                secim = int(secim) - 1
                if 0 <= secim < len(randevular):
                    iptal_edilen = randevular.pop(secim)
                    print(f"{iptal_edilen['polikinik']} - {iptal_edilen['gun']} - {iptal_edilen['saat']} randevusu iptal edilmiştir!")
                    if not ran_listesi[ad]:
                        del ran_listesi[ad]
                else:
                    print("!!Geçersiz Numara!!")
            except ValueError:
                print("Lütfen geçerli bir numara giriniz.")


def sekreter_menusu():
    if not ran_listesi:
        print("Sistemde kayıtlı randevu bulunmamaktadır.")
        return
    print("-" * 5, "RANDEVU LİSTESİ", "-" * 5)
    for ad, randevular in ran_listesi.items():               
        print(f"\nHasta: {ad}")
        for i, r in enumerate(randevular, 1):               
            print(f"  {i}. Polikinik: {r['polikinik']} | Gün: {r['gun']} | Saat: {r['saat']}")

    islem_sekreter = secim_yap(["Randevu İptal", "Randevu Düzenle"], "İşlem")

    if islem_sekreter == "Randevu İptal":
        randevu_iptal()

    elif islem_sekreter == "Randevu Düzenle":
        duzenle_ad = input("Randevusunu düzenlemek istediğiniz hastanın adını yazınız:\n")
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
            secim = int(input("Hangi randevuyu düzenlemek istersiniz(numara giriniz): ")) - 1
            yeni_polikinik = secim_yap(polikinikler, "Polikinik")
            yeni_gun = secim_yap(gunler, "Gün")
            yeni_saat = int(input("08:00 ila 17:00 arasında bir saat seçin: "))
            duzenlenecek_ran[secim] = {"polikinik": yeni_polikinik, "gun": yeni_gun, "saat": yeni_saat}  
        print(f"{duzenle_ad} adına randevu başarıyla güncellendi.")



yetkiler = ["HASTA", "RANDEVU SEKRETERİ"]
ran_listesi = {}
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
polikinikler = ["Dahiliye", "Kardiyoloji", "Dermatoloji", "Nöroloji", "Göğüs Hastalıkları",
                "Fizik Tedavi ve Rehabilitasyon", "Genel Cerrahi", "Ortopedi ve Travmatoloji",
                "Kadın Hastalıkları ve Doğum", "Çocuk Sağlığı ve Hastalıkları", "Kulak Burun Boğaz",
                "Beyin ve Sinir Cerrahisi", "Ağız ve Diş Sağlığı", "Psikiyatri", "Göz Hastalıkları",
                "Anesteziyoloji ve Reanimasyon"]


while True:
    yetki = giris_ekrani()
    if yetki == "HASTA":
        islem=secim_yap(["Randevu Al", "Randevu İptal"], "İşlem")
        if islem=="Randevu Al":
            randevu_al()
        elif islem=="Randevu İptal":
            randevu_iptal()
    elif yetki=="RANDEVU SEKRETERİ":
        sekreter_menusu()
        
        
        
        
        
        
        
        