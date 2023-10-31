from prettytable import PrettyTable
import os
import pwinput
import time
import json

# ==============================================
#                      Data
# ==============================================
jam = time.asctime(time.localtime(time.time()))
os.system("cls" if os.name == "nt" else "clear")


pathJsonPengguna = "PA\datapengguna.json"
with open(pathJsonPengguna, "r") as jsonPengguna:
    dataPengguna = json.loads(jsonPengguna.read())

def updatePengguna():
    with open(pathJsonPengguna, "w") as sn:
        json.dump(dataPengguna, sn, indent=4)

pathJsonFilm = "PA\datafilm.json"
with open(pathJsonFilm, "r") as jsonFilm:
    dataFilm = json.loads(jsonFilm.read())

def updateFilm():
    with open(pathJsonFilm, "w") as sn:
        json.dump(dataFilm, sn, indent=4)

akunAdmin = "a"
pwAdmin = "1"
failsleft = 3

def back():
    input("\nTekan Enter untuk kembali...")

def error(a = ""):
    print(f"============================================================")
    print(f" Inputan {(a)} yang Anda masukkan salah silahkan ulangi   ")
    print(f"============================================================")
    back()        

def cekinput(input):
    return input.isalnum()

def login_berhasil():
    clear()
    print("\t\t\t  Login Successful..." )
    time.sleep(2)

def login_gagal():
    global failsleft
    time.sleep(0.5)
    print("==============================================")
    print("|   PASSWORD SALAH MOHON DIINGAT KEMBALI!!   |")
    print("==============================================")
    failsleft = failsleft - 1 
    print("Kamu  memiliki " + str(failsleft) + " kesempatan ⚠️")
    print("--"*20)
    input("Tekan enter untuk melanjutkan.....")
    if failsleft == 0:
        clear()
        print("=======================================================================")
        print("|                 UPS!, ANDA SALAH SEBANYAK TIGA KALI                 |")
        print("|               Maaf anda telah terlogout dari program                |")
        print("=======================================================================")
        print()
        quit()
    

def loading_transaksi():
    clear()
    print("\t\t\t  Loading Transaksi..." )
    time.sleep(2)

def tabelFilm():
    tabelDataFilm = PrettyTable()
    tabelDataFilm.clear_rows()
    tabelDataFilm.title = "Data Film"
    tabelDataFilm.field_names = ["Nomor", "Nama", "Harga"]
    for nomor, (nama, harga) in enumerate(dataFilm.items(), start=1):
        tabelDataFilm.add_row([nomor, nama, f'Rp.{harga["Harga Tiket"]}'])
    print(tabelDataFilm)

def tabelJadwal():
    tabelJadwalFilm = PrettyTable()
    tabelJadwalFilm.clear_rows()
    tabelJadwalFilm.title = filmTerpilih
    tabelJadwalFilm.field_names = ["Nomor", "Jadwal"]
    for nomorJadwal, jadwal in enumerate(dataFilm[filmTerpilih]["Jam Tayang"], start= 1):
        tabelJadwalFilm.add_row([nomorJadwal, jadwal])
    print(tabelJadwalFilm)


# Buat bersih-bersih
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Menu utama
def menuUtama():
    while True:
        clear()
        print("+====================================================================+")
        print("|                           SELAMAT DATANG                           |")
        print("|                           Di SISFOR.FLIX                           |")
        print("+====================================================================+")
        print("|                        Silahkan Pilih Menu                         |")
        print("+====================================================================+")
        print("| [1]. Pesan Tiket                                                   |")
        print("| [2]. Saldo                                                         |")
        print("| [3]. Kembali                                                       |")
        print("+====================================================================+")
        try:
            pilihMenu = int(input("Pilih menu: "))
            if pilihMenu == 1:
                pesanTiket()
            elif pilihMenu == 2:
                saldo()
            elif pilihMenu == 3:
                break
            else:
                error(pilihMenu)
        except ValueError:
            clear()
            error()
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def pesanTiket():
    try:
        clear()
        tabelFilm()            
        pilihFilm = int(input("Pilih Film: "))
        daftarFilm = list(dataFilm.keys())
        global filmTerpilih
        filmTerpilih = daftarFilm[pilihFilm - 1]
        if filmTerpilih in dataFilm:
            tabelJadwal()
            pilihJadwal = int(input("Piih jadwal film: "))
            global jadwalTerpilih
            jadwalTerpilih = dataFilm[filmTerpilih]["Jam Tayang"][pilihJadwal - 1]
            global jumlahTiket
            jumlahTiket = int(input("Masukkan Jumlah Tiket: "))
            if jumlahTiket >0:
                global harga
                harga = dataFilm[filmTerpilih]["Harga Tiket"]
                global hargaTotal
                hargaTotal = harga * jumlahTiket
                saldo = dataPengguna["Saldo"][index]
                if hargaTotal <= saldo:
                    sisaTiket = dataFilm[filmTerpilih]["Jumlah Tiket"] - jumlahTiket
                    dataFilm[filmTerpilih]["Jumlah Tiket"] = sisaTiket
                    updateFilm()
                    clear()
                    loading_transaksi()
                    clear()
                    global sisaSaldo
                    sisaSaldo = saldo - hargaTotal
                    dataPengguna["Saldo"][index] = sisaSaldo
                    updatePengguna()
                    print("======================================")
                    print("|         TRANSAKSI BERHASIL!!       |")
                    print("======================================")
                    input("Tekan enter untuk memunculkan bukti pemesanan.....")
                    invoicePembelian()
                else:
                    print("======================================")
                    print("|          TRANSAKSI GAGAL!!         |")
                    print("-------------------------------------|")
                    print("|        Saldo Tidak Mencukupi!      |")
                    print("======================================")
                    input("Tekan enter untuk melanjutkan.....")
            else:
                print("=========================================")
                print("|    Tiket tidak boleh minus atau 0!    |")
                print("=========================================")
                input("Tekan enter untuk melanjutkan.....")
        else:
            print("======================================")
            print("|       FILM TIDAK ADA DI DATA!!     |")
            print("======================================")
            input("Tekan enter untuk melanjutkan.....")
    except ValueError:
        clear()
        error()
    except KeyboardInterrupt:
        print("========================================================")
        print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
        print("========================================================")
        input("Tekan enter untuk melanjutkan.....")
    except IndexError:
        print("====================================================")
        print("|    Tolong masukkan angka sesuai dengan tabel!    |")
        print("====================================================")
        input("Tekan enter untuk melanjutkan.....")

def invoicePembelian():
    clear()
    print("============= BUKTI PEMESANAN =============")
    print(f"Judul Film: {filmTerpilih}")
    print(f"Jam Tayang: {jadwalTerpilih}")
    print(f"Harga Tiket: Rp.{harga}")
    print(f"Jumlah Tiket: {jumlahTiket}")
    print("\n")
    print(f"Waktu pemesanan: {jam}")
    print(f"Total harga: Rp.{hargaTotal}")
    print("Status: Lunas")
    print(f"Sisa saldo: Rp.{sisaSaldo}")
    print("===========================================")
    time.sleep(4)  
    clear()  

def saldo():
    while True:
        clear()
        print("+====================================================================+")
        print("|                        Silahkan Pilih Menu                         |")
        print("+====================================================================+")
        print("| [1]. Tampilkan Saldo                                               |")
        print("| [2]. Isi Saldo                                                     |")
        print("| [3]. Kembali                                                       |")
        print("+====================================================================+")
        try:
            saldo = dataPengguna["Saldo"][index]
            pilihMenu = int(input("Pilih menu: "))
            if pilihMenu == 1:
                clear()
                print("======================================")
                print(f" Saldo anda Rp.{saldo}   ")
                print("======================================")
                input("Tekan enter untuk melajutkan.....")
            elif pilihMenu == 2:
                saldoTambahan = int(input("Masukkan nominal saldo tambahan: "))
                if len(str(saldoTambahan)) <= 8:
                    if saldoTambahan >= 0:
                        saldo += saldoTambahan
                        if len(str(saldo)) <= 8:
                            dataPengguna["Saldo"][index] = saldo
                            updatePengguna()
                            print(f"Saldo berhasil ditambah, sekarang saldo anda adalah Rp.{saldo}")
                            input("Tekan enter untuk melanjutkan.....")
                        else:
                            print("Total saldo tidak boleh lebih dari 8 digit.")
                            input("Tekan enter untuk melanjutkan.....")
                    elif saldoTambahan < 0:
                        print("Saldo tidak boleh kurang dari 0")
                        input("Tekan enter untuk melanjutkan.....")
                else:
                    print("Saldo tidak boleh lebih dari 8 digit.")
                    input("Tekan enter untuk melanjutkan.....")
            elif pilihMenu == 3:
                return True
            else:
                error(pilihMenu)     
        except ValueError:
            clear()
            error()
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def menuAdmin():
    while True:
        clear()
        print("+====================================================================+")
        print("|                            Selamat Datang Admin                    |")
        print("+====================================================================+")
        print("| [1]. Menambahkan Film                                              |")
        print("| [2]. Lihat Film                                                    |")
        print("| [3]. Edit Film                                                     |")
        print("| [4]. Hapus Film                                                    |")
        print("| [5]. Kembali                                                       |")
        print("+====================================================================+")
        try:
            pilihMenu = int(input("Pilih menu: "))
            if pilihMenu == 1:
                tambahFilm()
            elif pilihMenu == 2:
                lihatFilm()
            elif pilihMenu == 3:
                editFilm()
            elif pilihMenu == 4:
                hapusFilm()
            elif pilihMenu == 5:
                return True
            else:
                error(pilihMenu)
        except ValueError:
            clear()
            error()
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def tambahWaktu():
    global daftarWaktu
    daftarWaktu = []
    while True:
        clear()
        print("=========================================================================")
        print("|  Masukkan dalam format JJ:MM, jika ingin mengakhiri ketik 'selesai.'  |")
        print("=========================================================================")
        print(f"Daftar Waktu = {daftarWaktu}")
        jamTayang = input("Masukkan jam tayang: ")
        if jamTayang.lower() == "selesai":
            if daftarWaktu == []:
                clear()
                print("====================================")
                print("|     Waktu tidak boleh kosong     |")
                print("====================================")
                input("Tekan enter untuk melanjutkan.....")
            else:
                clear()
                print(f"Daftar waktu = {daftarWaktu}")
                return True
        else:
            try:
                cekJam = time.strptime(jamTayang,"%H:%M")
                if 0 <= cekJam.tm_hour <= 23 and 0 <= cekJam.tm_min <= 59:
                    daftarWaktu.append(jamTayang)
                    clear()
                    print("===================================")
                    print("|     Waktu berhasil ditambah     |")
                    print("===================================")
                    input("Tekan enter untuk melanjutkan.....")
                else:
                    clear()
                    print("===============================================================")
                    print("|  Jam dan waktu tidak valid. Tolong masukkan waktu yang benar.")
                    print("===============================================================")
                    input("Tekan enter untuk melanjutkan.....")

            except ValueError:
                clear()
                print("==================================")
                print("|    Format waktu tidak valid    |")
                print("==================================")
                input("Tekan enter untuk melanjutkan.....")

def tambahFilm():
    global daftarWaktu
    while True:
        clear()
        print("+====================================================================+")
        print("|                            MENAMBAHKAN FILM                        |")
        print("+====================================================================+")
        daftarFilm = list(dataFilm.keys())
        try:
            namaFilm = str(input("Masukkan nama film: "))
            if namaFilm in daftarFilm:
                print("======================================")
                print("|        FILM SUDAH TERDAFTAR!!      |")
                print("======================================")
            else:
                if len(namaFilm) <= 100:
                    tambahWaktu()
                    hargaTiket = int(input("Masukkan harga tiket: "))
                    if len(str(hargaTiket)) <= 7:
                        jumlahTiket = int(input("Masukkan jumlah tiket: "))
                        if jumlahTiket <= 100:
                            dataFilm.update({namaFilm: {
                                "Jam Tayang": daftarWaktu,
                                "Harga Tiket": hargaTiket,
                                "Jumlah Tiket": jumlahTiket,
                                }})
                            del daftarWaktu
                            updateFilm()
                            print(f"Data film {namaFilm} berhasil ditambahkan!")
                            input("Tekan enter untuk melanjutkan.....")
                            return True 
                        else: 
                            print("Jumlah tiket tidak boleh lebih dari 100")
                            input("Tekan enter untuk melanjutkan.....")
                    else:
                        print("Harga tidak boleh lebih dari 7 digit")
                        input("Tekan enter untuk melanjutkan.....")
                else:
                    print("Nama tidak boleh lebih dari 100 digit.")
                    input("Tekan enter untuk melanjutkan.....")
        except ValueError:
            error()
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def lihatFilm():
    while True:
        clear()
        print("+====================================================================+")
        print("|                              LIHAT FILM                            |")
        print("+====================================================================+")
        print("|        Pilih film untuk melihat jam tayang film tersebut!          |")
        print("+====================================================================+")
        tabelFilm()
        try:
            pilihFilm = int(input("Pilih Film: "))
            daftarFilm = list(dataFilm.keys())
            global filmTerpilih
            filmTerpilih = daftarFilm[pilihFilm - 1]
            if filmTerpilih in dataFilm:
                tabelJadwal()
                ulang = str(input("Lagi? (y/t): "))
                if ulang == "y" or ulang =="Y":
                    print()
                elif ulang == "t" or ulang =="T":
                    break
                else:
                    error()
                    break
            else:
                print(f"Tidak ada film dengan nomor {pilihFilm}")
                input("Tekan enter untuk melanjutkan......")
        except ValueError:
            error()
        except IndexError:
            print(f"Tidak ada film dengan nomor {pilihFilm}")
            input("Tekan enter untuk melanjutkan......")
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def editFilm():
    while True:
        clear()
        print("+====================================================================+")
        print("|                                EDIT FILM                           |")
        print("+====================================================================+")
        print("| [1]. Nama Film                                                     |")
        print("| [2]. Jam Tayang                                                    |")
        print("| [3]. Harga Tiket                                                   |")
        print("| [4]. Jumlah Tiket                                                  |")
        print("| [5]. Kembali                                                       |")
        print("+====================================================================+")
        try:
            pilihMenu = int(input("Pilih menu: "))
            if pilihMenu == 1:
                tabelFilm()
                pilihFilm = int(input("Pilih Film: "))
                daftarFilm = list(dataFilm.keys())
                filmTerpilih = daftarFilm[pilihFilm - 1]
                if filmTerpilih in dataFilm:
                    namaBaru = str(input("Masukkan nama baru: "))
                    if len(namaBaru) <= 100:
                        dataFilm[namaBaru] = dataFilm.pop(filmTerpilih)
                        updateFilm()
                        print(f"Film {filmTerpilih} telah diubah menjadi{namaBaru}")
                        tabelFilm()
                    else:
                        print("Nama tidak boleh lebih dari 100 digit.")
                        input("Tekan enter untuk melanjutkan.....")
                else:
                    print("======================================")
                    print("|       FILM TIDAK ADA DI DATA!!     |")
                    print("======================================")
                    input("Tekan enter untuk melanjutkan......")
            elif pilihMenu == 2:
                global daftarWaktu
                tabelFilm()
                pilihFilm = int(input("Pilih Film: "))
                daftarFilm = list(dataFilm.keys())
                filmTerpilih = daftarFilm[pilihFilm - 1]
                if filmTerpilih in dataFilm:
                    tambahWaktu()
                    dataFilm[filmTerpilih]["Jam Tayang"] = daftarWaktu
                    updateFilm()
                    del daftarWaktu
                else:
                    print("======================================")
                    print("|       FILM TIDAK ADA DI DATA!!     |")
                    print("======================================")
                    input("Tekan enter untuk melanjutkan.....")
            elif pilihMenu == 3:
                tabelFilm()
                pilihFilm = int(input("Pilih Film: "))
                daftarFilm = list(dataFilm.keys())
                filmTerpilih = daftarFilm[pilihFilm - 1]
                if filmTerpilih in dataFilm:
                    hargaTiketBaru = int(input("Masukkan harga tiket baru: "))
                    if len(str(hargaTiketBaru)) <= 7:
                        dataFilm[filmTerpilih]["Harga Tiket"] = hargaTiketBaru
                        updateFilm()
                        print(f"Harga tiket film {filmTerpilih} telah diubah menjadi Rp.{hargaTiketBaru}")
                        input("Tekan enter untuk melanjutkan......")
                    else:
                        print("Harga tidak boleh lebih dari 7 digit")
                        input("Tekan enter untuk melanjutkan.....")
                else:
                    print("======================================")
                    print("|       FILM TIDAK ADA DI DATA!!     |")
                    print("======================================")
                    input("Tekan enter untuk melanjutkan.....")
            elif pilihMenu == 4:
                tabelFilm()
                pilihFilm = int(input("Pilih Film: "))
                daftarFilm = list(dataFilm.keys())
                filmTerpilih = daftarFilm[pilihFilm - 1]
                if filmTerpilih in dataFilm:
                    jumlahTiketBaru = int(input("Masukkan jumlah tiket baru: "))
                    if jumlahTiketBaru <= 100:
                        dataFilm[filmTerpilih]["Jumlah Tiket"] = jumlahTiketBaru
                        updateFilm()
                        print(f"Jumlah tiket film {filmTerpilih} telah diubah menjadi {jumlahTiketBaru}")
                        input("Tekan enter untuk melanjutkan......")
                    else:
                        print("Jumlah tiket tidak boleh lebih dari 100")
                        input("Tekan enter untuk melanjutkan.....")
                else:
                    print("======================================")
                    print("|       FILM TIDAK ADA DI DATA!!     |")
                    print("======================================")
                    input("Tekan enter untuk melanjutkan.....")
            elif pilihMenu == 5:
                return True
            else:
                error(pilihMenu)
        except ValueError:
            error()
        except IndexError:
            print(f"Tidak ada film dengan nomor {pilihFilm}")
            input("Tekan enter untuk melanjutkan.....")
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def hapusFilm():
    while True:
        clear()
        tabelFilm()
        try:
            pilihFilm = int(input("Pilih Film: "))
            daftarFilm = list(dataFilm.keys())
            filmTerpilih = daftarFilm[pilihFilm - 1]
            if filmTerpilih in dataFilm:
                del dataFilm[filmTerpilih]
                updateFilm()
                tabelFilm()
                ulang = str(input("Lagi? (y/t): "))
                if ulang == "t":
                    return True
                elif ulang == "y":
                    print("")
                else:
                    print(f"Kembali ke menu data film dikarenakan tidak ada untuk {ulang}")
                    input("Tekan enter untuk melanjutkan.....")
                    return True
            else:
                print("======================================")
                print("|       FILM TIDAK ADA DI DATA!!     |")
                print("======================================")
                input("Tekan enter untuk melanjutkan.....")
        except ValueError:
            error()
        except IndexError:
            print("========================================================")
            print(f"|       Tidak ada film dengan nomor {pilihFilm}       |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def login():
    while True:
        clear()
        print("======================================================================")
        print("|                           Silahkan Login                           |")
        print("======================================================================")
        global namaUser
        try:
            namaUser = str(input("Masukkan nama akun: "))
            if cekinput(namaUser):
                if namaUser in dataPengguna["Nama"]:
                    global index
                    index = dataPengguna["Nama"].index(namaUser)
                    pwUser = pwinput.pwinput(prompt='Masukkan password: ')
                    if cekinput(pwUser):
                        if pwUser == dataPengguna["Password"][index]:
                            login_berhasil()
                            menuUtama()
                            break
                        else:
                            login_gagal()
                    else:
                        print("Input hanya menerima huruf dan angka")
                        input("Tekan enter untuk melanjutkan.....")
                elif namaUser == akunAdmin:
                    pwUser = pwinput.pwinput(prompt='Masukkan password: ')
                    if cekinput(pwUser):
                        if pwUser == pwAdmin:
                            menuAdmin()
                            break
                        else:
                            login_gagal()
                    else:
                        print("Input hanya menerima huruf dan angka")
                        input("Tekan enter untuk melanjutkan.....")
                else:
                    print
                    print("======================================")
                    print("|         AKUN TIDAK TERDAFTAR       |")
                    print("|      SILAHKAN MENDAFTARKAN AKUN    |")
                    print("======================================")
                    daftarMenu = str(input("Apakah anda ingin daftar dulu? [y/t]: "))
                    if daftarMenu == "y" or daftarMenu == "Y":
                        daftar()
                        break
                    elif daftarMenu == "t" or daftarMenu == "T":
                        break
                    else:
                        clear()
                        error()
                        break
            else:
                print("Input hanya menerima huruf dan angka")
                input("Tekan enter untuk melanjutkan.....")
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

def daftar():
    while True:
        clear()
        print("======================================================================")
        print("|                           Silahkan Daftar                          |")
        print("======================================================================")
        try:
            namaUser = str(input("Masukkan nama: "))
            if cekinput(namaUser):
                if len(namaUser) <= 20:
                    if namaUser in dataPengguna["Nama"]:
                        print(f"Nama {namaUser} tersebut sudah ada di database!")
                        input("Tekan enter untuk melanjutkan.....")
                    else:
                        pwUser = pwinput.pwinput(prompt='Masukkan password: ')
                        if cekinput(pwUser):
                            if len(pwUser) <= 20:
                                saldoAwal = int(input("Masukkan saldo awal: "))
                                if len(str(saldoAwal)) <= 8:
                                    if saldoAwal >= 0 :
                                        dataPengguna["Nama"].append(namaUser)
                                        dataPengguna["Password"].append(pwUser)
                                        dataPengguna["Saldo"].append(saldoAwal)
                                        updatePengguna()
                                        print(f"Nama {namaUser} dengan saldo Rp.{saldoAwal} sudah di daftar di data")
                                        input("Tekan enter untuk melanjutkan.....")
                                    elif saldoAwal < 0:
                                        print("Saldo tidak boleh kurang dari 0, silahkan masukkan ulang.")
                                        input("Tekan enter untuk melanjutkan.....")
                                    return True
                                else:
                                    print("Saldo tidak boleh lebih dari 8 digit")
                                    input("Tekan enter untuk melanjutkan.....")
                            else:
                                print("Batas karakter untuk password adalah 20!")
                                input("Tekan enter untuk melanjutkan.....")
                        else:
                            print("Input hanya menerima huruf dan angka")
                            input("Tekan enter untuk melanjutkan.....")
                else:
                    print("Batas karakter untuk nama adalah 20!")
                    input("Tekan enter untuk melanjutkan.....")
            else:
                print("Input hanya menerima huruf dan angka")
                input("Tekan enter untuk melanjutkan.....")
        except ValueError:
            print("======================================")
            print("|           SALDO WAJIB ANGKA!!      |")
            print("======================================")
            input("Tekan enter untuk melanjutkan.....")
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")
            
def menuAwal():
    while True:
        clear()
        print("+====================================================================+")
        print("|                           SELAMAT DATANG                           |")
        print("|                               (◍•ᴗ•◍)                              |")
        print("|                           Di SISFOR.FLIX                           |")
        print("|    OLEH : KELOMPOK 11 - SISTEM INFORMASI - UNIVERSITAS MULAWARMAN  |")
        print("+====================================================================+")
        print("| [1] Login                                                          |")
        print("| [2] Daftar Akun                                                    |")
        print("| [0] Keluar Program                                                 |")
        print("+====================================================================+")
        try:
            pilihMenu = int(input("Pilih menu: "))
            if pilihMenu == 1:
                login()
            elif pilihMenu == 2:
                daftar()
            elif pilihMenu == 0:
                clear()
                print("✦======================================================================✦")
                print("|                        PROGRAM TELAH SELESAI                         |")
                print("✦======================================================================✦")
                print("|           TERIMAKASIH TELAH MENGGUNAKAN PROGRAM SEDERHANA            |")
                print("|                     YANG DISUSUN OLEH KELOMPOK 11                    |")
                print("|                         SISTEM INFORMASI A'23                        |")
                print("|                                  |||                                 |")
                print("|                         UNIVERSITAS MULAWARMAN                       |")
                print("✦======================================================================✦")
                break
            else:
                clear()
                error(pilihMenu)
        except ValueError:
            error()
        except KeyboardInterrupt:
            print("========================================================")
            print("|  Tolong jangan menekan ctrl dan c secara bersamaan!  |")
            print("========================================================")
            input("Tekan enter untuk melanjutkan.....")

menuAwal()