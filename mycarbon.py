import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.set_page_config(page_title="MyCarbon", page_icon="🌿")

dosya = "karbon_verileri.csv"

# --- KATSAYILAR ---
ulasim_katsayi = {
    "Yürüyüş": 0,
    "Toplu Taşıma": 0.05,
    "Özel Araç": 0.21
}

enerji_katsayi = 0.233

beslenme_katsayi = {
    "Sebze Ağırlıklı": 1.5,
    "Karışık": 2.5,
    "Et Ağırlıklı": 3.5
}

# --- AI ÖNERİ ---
def ai_oneri(toplam):
    if toplam < 3:
        return "🌿 Harika! Karbon ayak izin oldukça düşük."
    elif toplam < 6:
        return "👍 İyi gidiyorsun. Enerji tasarrufunu artırabilirsin."
    else:
        return "⚠️ Karbon ayak izin yüksek. Özel araç ve enerji kullanımını azaltmayı deneyebilirsin."

# --- ANA SAYFA ---
st.title("🌿 MyCarbon")

secim = st.radio("Seçim yapınız:", ["👤 Öğrenci Kayıt", "🔐 Yönetici Paneli"])

# ======================================================
# 👤 ÖĞRENCİ KAYIT
# ======================================================
if secim == "👤 Öğrenci Kayıt":

    if "ogrenci_kayit" not in st.session_state:
        st.session_state.ogrenci_kayit = False

    # --- KAYIT EKRANI ---
    if not st.session_state.ogrenci_kayit:
        st.header("👤 Öğrenci Bilgileri")

        isim = st.text_input("İsim")
        soyisim = st.text_input("Soyisim")
        sinif = st.text_input("Sınıf")
        numara = st.text_input("Okul Numarası")

        if st.button("Devam Et"):
            if isim and soyisim and sinif and numara:
                st.session_state.ogrenci_kayit = True
                st.session_state.isim = isim
                st.session_state.soyisim = soyisim
                st.session_state.sinif = sinif
                st.session_state.numara = numara
            else:
                st.error("Tüm alanları doldurun.")

    # --- GÜNLÜK VERİ GİRİŞİ ---
    else:
        st.header("📅 Günlük Karbon Verisi")

        st.write(f"👤 {st.session_state.isim} {st.session_state.soyisim}")

        ulasim = st.selectbox("🚶 Ulaşım Türü", list(ulasim_katsayi.keys()))
        km = 0
        if ulasim != "Yürüyüş":
            km = st.number_input("Günlük kaç km?", min_value=0.0)

        enerji_saat = st.number_input("⚡ Elektrikli cihaz süresi (saat)", min_value=0.0)
        beslenme = st.selectbox("🥗 Beslenme Türü", list(beslenme_katsayi.keys()))

        if st.button("🌍 Hesapla ve Kaydet"):

            ulasim_co2 = km * ulasim_katsayi[ulasim]
            enerji_co2 = enerji_saat * enerji_katsayi
            beslenme_co2 = beslenme_katsayi[beslenme]
            toplam_co2 = ulasim_co2 + enerji_co2 + beslenme_co2

            st.success(f"Toplam: {toplam_co2:.2f} kg CO₂")
            st.info(ai_oneri(toplam_co2))

            # --- GÜNLÜK VERİYİ KAYDET ---
            veri = {
                "Tarih": date.today(),
                "İsim": st.session_state.isim,
                "Soyisim": st.session_state.soyisim,
                "Sınıf": st.session_state.sinif,
                "Numara": st.session_state.numara,
                "Ulaşım_CO2": ulasim_co2,
                "Enerji_CO2": enerji_co2,
                "Beslenme_CO2": beslenme_co2,
                "Toplam_CO2": toplam_co2
            }

            if os.path.exists(dosya):
                df = pd.read_csv(dosya)
                df = pd.concat([df, pd.DataFrame([veri])], ignore_index=True)
            else:
                df = pd.DataFrame([veri])

            df.to_csv(dosya, index=False)

            st.success("📁 Günlük kayıt eklendi!")

            # Grafik
            fig, ax = plt.subplots()
            ax.bar(["Ulaşım", "Enerji", "Beslenme"],
                   [ulasim_co2, enerji_co2, beslenme_co2])
            ax.set_ylabel("kg CO₂")
            st.pyplot(fig)

        if st.button("Çıkış Yap"):
            st.session_state.ogrenci_kayit = False

# ======================================================
# 🔐 YÖNETİCİ PANELİ
# ======================================================
elif secim == "🔐 Yönetici Paneli":

    sifre = st.text_input("Yönetici Şifresi", type="password")

    if sifre == "4380":
        st.success("Giriş başarılı")

        if os.path.exists(dosya):
            df_admin = pd.read_csv(dosya)

            # Günlük kayıtlar olduğu için:
            # Ortalama karbon ayak izi hesaplayıp sıralıyoruz
            ortalama = df_admin.groupby(
                ["İsim", "Soyisim", "Sınıf", "Numara"]
            )["Toplam_CO2"].mean().reset_index()

            ortalama = ortalama.sort_values("Toplam_CO2")

            st.subheader("🏆 Ortalama Karbon Ayak İzi Sıralaması")
            st.dataframe(ortalama)

        else:
            st.warning("Henüz veri yok.")

    elif sifre != "":
        st.error("Şifre yanlış.")








