import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.set_page_config(page_title="GreenMetric", page_icon="🌿")

st.title("🌿 GreenMetric – Akıllı Karbon Analiz Sistemi")

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

# --- KİŞİYE ÖZEL AI ÖNERİ ---
def ai_kisisel_oneri(ulasim, enerji, beslenme):
    en_yuksek = max({
        "Ulaşım": ulasim,
        "Enerji": enerji,
        "Beslenme": beslenme
    }, key=lambda x: {
        "Ulaşım": ulasim,
        "Enerji": enerji,
        "Beslenme": beslenme
    }[x])

    if en_yuksek == "Ulaşım":
        return "🚶 Ulaşım karbon oranınız yüksek. Toplu taşıma veya yürüyüşü artırabilirsiniz."
    elif en_yuksek == "Enerji":
        return "⚡ Enerji tüketiminiz yüksek. Cihaz kullanım süresini azaltabilirsiniz."
    else:
        return "🥗 Beslenme kaynaklı karbon oranı yüksek. Sebze ağırlıklı beslenme tercih edilebilir."

# --- ANA SAYFA ---
secim = st.radio("Seçim Yap:", ["👤 Öğrenci Girişi", "🔐 Yönetici Paneli"])

# ======================================================
# 👤 ÖĞRENCİ GİRİŞİ
# ======================================================
if secim == "👤 Öğrenci Girişi":

    isim = st.text_input("İsim")
    soyisim = st.text_input("Soyisim")
    sinif = st.text_input("Sınıf")
    numara = st.text_input("Numara")

    if isim and soyisim and sinif and numara:

        st.header("📅 Günlük Veri Girişi")

        ulasim = st.selectbox("Ulaşım", list(ulasim_katsayi.keys()))
        km = 0
        if ulasim != "Yürüyüş":
            km = st.number_input("Km", min_value=0.0)

        enerji_saat = st.number_input("Enerji (saat)", min_value=0.0)
        beslenme = st.selectbox("Beslenme", list(beslenme_katsayi.keys()))

        if st.button("Hesapla ve Kaydet"):

            ulasim_co2 = km * ulasim_katsayi[ulasim]
            enerji_co2 = enerji_saat * enerji_katsayi
            beslenme_co2 = beslenme_katsayi[beslenme]
            toplam = ulasim_co2 + enerji_co2 + beslenme_co2

            st.success(f"Toplam: {toplam:.2f} kg CO₂")
            st.info(ai_kisisel_oneri(ulasim_co2, enerji_co2, beslenme_co2))

            veri = {
                "Tarih": date.today(),
                "İsim": isim,
                "Soyisim": soyisim,
                "Sınıf": sinif,
                "Numara": numara,
                "Ulaşım": ulasim_co2,
                "Enerji": enerji_co2,
                "Beslenme": beslenme_co2,
                "Toplam": toplam
            }

            if os.path.exists(dosya):
                df = pd.read_csv(dosya)
                df = pd.concat([df, pd.DataFrame([veri])], ignore_index=True)
            else:
                df = pd.DataFrame([veri])

            df.to_csv(dosya, index=False)

            # --- ZAMAN İÇİNDE DÜŞÜŞ ANALİZİ ---
            ogrenci_df = df[
                (df["İsim"] == isim) &
                (df["Soyisim"] == soyisim) &
                (df["Numara"] == numara)
            ]

            ogrenci_df = ogrenci_df.sort_values("Tarih")

            st.subheader("📉 Zaman İçindeki Değişim")

            fig, ax = plt.subplots()
            ax.plot(ogrenci_df["Tarih"], ogrenci_df["Toplam"])
            ax.set_ylabel("kg CO₂")
            ax.set_xticklabels(ogrenci_df["Tarih"], rotation=45)
            st.pyplot(fig)

# ======================================================
# 🔐 YÖNETİCİ PANELİ
# ======================================================
elif secim == "🔐 Yönetici Paneli":

    sifre = st.text_input("Şifre", type="password")

    if sifre == "4380":

        if os.path.exists(dosya):

            df = pd.read_csv(dosya)

            st.subheader("🏫 Okul Genel Sıralaması")

            okul = df.groupby(
                ["İsim", "Soyisim", "Sınıf", "Numara"]
            )["Toplam"].mean().reset_index()

            okul = okul.sort_values("Toplam")

            st.dataframe(okul)

            st.subheader("📊 Sınıf Ortalamaları")

            sinif_ort = df.groupby("Sınıf")["Toplam"].mean().reset_index()
            st.dataframe(sinif_ort)

        else:
            st.warning("Veri bulunamadı.")








