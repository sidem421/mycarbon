import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.set_page_config(page_title="MyCarbon", page_icon="🌿")

st.title("🌿 MyCarbon – Karbon Ayak İzi Hesaplayıcı")
st.write("Bu uygulama eğitim ve farkındalık amaçlıdır.")

# --- KATSAYILAR ---
ulasim_katsayi = {
    "Yürüyüş": 0,
    "Toplu Taşıma": 0.05,
    "Özel Araç": 0.21
}

enerji_katsayi = 0.233  # kg CO2 / saat

beslenme_katsayi = {
    "Sebze Ağırlıklı": 1.5,
    "Karışık": 2.5,
    "Et Ağırlıklı": 3.5
}

# --- KULLANICI GİRİŞLERİ ---
st.header("📥 Günlük Bilgileri Gir")

ulasim = st.selectbox("🚶 Ulaşım Türü", list(ulasim_katsayi.keys()))
km = 0
if ulasim != "Yürüyüş":
    km = st.number_input("Günlük kaç km?", min_value=0.0)

enerji_saat = st.number_input("⚡ Elektrikli cihaz kullanım süresi (saat)", min_value=0.0)
beslenme = st.selectbox("🥗 Beslenme Türü", list(beslenme_katsayi.keys()))

# --- HESAPLAMA ---
ulasim_co2 = km * ulasim_katsayi[ulasim]
enerji_co2 = enerji_saat * enerji_katsayi
beslenme_co2 = beslenme_katsayi[beslenme]
toplam_co2 = ulasim_co2 + enerji_co2 + beslenme_co2

# --- BUTON ---
if st.button("🌍 Karbon Ayak İzini Hesapla"):
    st.subheader("📊 Sonuçlar")
    st.write(f"🚶 Ulaşım: **{ulasim_co2:.2f} kg CO₂**")
    st.write(f"⚡ Enerji: **{enerji_co2:.2f} kg CO₂**")
    st.write(f"🥗 Beslenme: **{beslenme_co2:.2f} kg CO₂**")
    st.success(f"🌿 Toplam Karbon Ayak İzin: **{toplam_co2:.2f} kg CO₂**")

    # --- VERİYİ KAYDET ---
    veri = {
        "Tarih": date.today(),
        "Ulaşım_CO2": ulasim_co2,
        "Enerji_CO2": enerji_co2,
        "Beslenme_CO2": beslenme_co2,
        "Toplam_CO2": toplam_co2
    }

    dosya = "karbon_verileri.csv"

    if os.path.exists(dosya):
        df = pd.read_csv(dosya)
        df = pd.concat([df, pd.DataFrame([veri])], ignore_index=True)
    else:
        df = pd.DataFrame([veri])

    df.to_csv(dosya, index=False)

    st.info("📁 Günlük veri kaydedildi.")

    # --- GRAFİK ---
    st.subheader("📈 Karbon Dağılım Grafiği")

    fig, ax = plt.subplots()
    ax.bar(
        ["Ulaşım", "Enerji", "Beslenme"],
        [ulasim_co2, enerji_co2, beslenme_co2]
    )
    ax.set_ylabel("kg CO₂")
    ax.set_title("Günlük Karbon Ayak İzi Dağılımı")

    st.pyplot(fig)

# --- KAYITLI VERİLER ---
if os.path.exists("karbon_verileri.csv"):
    st.subheader("🗂️ Önceki Günler")
    st.dataframe(pd.read_csv("karbon_verileri.csv"))





