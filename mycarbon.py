import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.set_page_config(page_title="MyCarbon", page_icon="🌿")

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

dosya = "karbon_verileri.csv"

# --- AI ÖNERİ SİSTEMİ ---
def ai_oneri(toplam, ulasim, enerji, beslenme):
    if toplam < 3:
        return "Harika! 🌿 Karbon ayak izin oldukça düşük. Böyle devam et!"
    elif toplam < 6:
        return "İyi gidiyorsun 👍 Toplu taşıma ve enerji tasarrufu artırılabilir."
    else:
        return "Karbon ayak izin yüksek ⚠️ Özel araç kullanımını azaltabilir, enerji tasarrufuna dikkat edebilirsin."

# --- ANA SAYFA ---
st.title("🌿 MyCarbon")

secim = st.radio("Lütfen bir seçenek seçiniz:", 
                 ["👤 Öğrenci Kayıt", "🔐 Yönetici Paneli"])

# ======================================================
# 👤 ÖĞRENCİ KAYIT BÖLÜMÜ
# ======================================================
if secim == "👤 Öğrenci Kayıt":

    if "kayit_tamam" not in st.session_state:
        st.session_state.kayit_tamam = False

    if not st.session_state.kayit_tamam:
        st.header("👤 Öğrenci Bilgileri")

        isim = st.text_input("İsim")
        soyisim = st.text_input("Soyisim")
        sinif = st.text_input("Sınıf")
        numara = st.text_input("Okul Numarası")

        if st.button("Devam Et"):
            if isim and soyisim and sinif and numara:
                st.session_state.kayit_tamam = True
                st.session_state.isim = isim
                st.session_state.soyisim = soyisim
                st.session_state.sinif = sinif
                st.session_state.numara = numara
            else:
                st.error("Lütfen tüm alanları doldurun.")

    else:
        st.header("📥 Günlük Veri Girişi")

        ulasim = st.selectbox("🚶 Ulaşım Türü", list(ulasim_katsayi.keys()))
        km = 0
        if ulasim != "Yürüyüş":
            km = st.number_input("Günlük kaç km?", min_value=0.0)

        enerji_saat = st.number_input("⚡ Elektrikli cihaz kullanım süresi (saat)", min_value=0.0)
        beslenme = st.selectbox("🥗 Beslenme Türü", list(beslenme_katsayi.keys()))

        if st.button("🌍 Karbon Ayak İzini Hesapla"):

            ulasim_co2 = km * ulasim_katsayi[ulasim]
            enerji_co2 = enerji_saat * enerji_katsayi
            beslenme_co2 = beslenme_katsayi[beslenme]
            toplam_co2 = ulasim_co2 + enerji_co2 + beslenme_co2

            st.success(f"Toplam Karbon Ayak İzin: {toplam_co2:.2f} kg CO₂")

            # AI ÖNERİ
            st.info(ai_oneri(toplam_co2, ulasim_co2, enerji_co2, beslenme_co2))

            veri = {
                "Tarih": date.today(),
                "İsim": st.session_state.isim,
                "Soyisim": st.session_state.soyisim,
                "Sınıf": st.session_state.sinif,
                "Numara": st.session_state.numara,
                "Toplam_CO2": toplam_co2
            }

            if os.path.exists(dosya):
                df = pd.read_csv(dosya)
                df = pd.concat([df, pd.DataFrame([veri])], ignore_index=True)
            else:
                df = pd.DataFrame([veri])

            df.to_csv(dosya, index=False)

            # Grafik
            fig, ax = plt.subplots()
            ax.bar(["Ulaşım", "Enerji", "Beslenme"],
                   [ulasim_co2, enerji_co2, beslenme_co2])
            ax.set_ylabel("kg CO₂")
            st.pyplot(fig)

# ======================================================
# 🔐 YÖNETİCİ PANELİ
# ======================================================
elif secim == "🔐 Yönetici Paneli":

    sifre = st.text_input("Yönetici Şifresi", type="password")

    if sifre == "4380":

        st.success("Giriş Başarılı")

        if os.path.exists(dosya):
            df_admin = pd.read_csv(dosya)

            # SIRALAMA (En düşük karbon ayak izi üstte)
            df_admin = df_admin.sort_values("Toplam_CO2")

            st.subheader("🏆 Karbon Ayak İzi Sıralaması (En Düşük → En Yüksek)")
            st.dataframe(df_admin)

        else:
            st.warning("Henüz veri yok.")

    elif sifre != "":
        st.error("Şifre yanlış.")







