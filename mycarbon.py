import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="MyCarbon | Karbon Ayak İzi", layout="wide")

st.title("🌍 MyCarbon – Kişisel Karbon Ayak İzi Analizi")
st.write("Bu uygulama bireylerin karbon ayak izini hesaplar ve azaltmaya yönelik **akıllı öneriler** sunar.")

st.divider()

# --- KULLANICI GİRDİLERİ ---
st.header("📥 Günlük Alışkanlıklarını Gir")

km = st.slider("🚗 Günlük araçla gidilen mesafe (km)", 0, 100, 10)
electricity = st.slider("⚡ Aylık elektrik tüketimi (kWh)", 50, 500, 200)
meat_days = st.slider("🍖 Haftada kaç gün kırmızı et tüketiyorsun?", 0, 7, 3)

# --- HESAPLAMA (EMİSYON FAKTÖRLERİ) ---
transport_emission = km * 0.21        # kg CO2 / gün
electricity_emission = electricity * 0.42 / 30
meat_emission = meat_days * 2.5 / 7

total_emission = transport_emission + electricity_emission + meat_emission

st.divider()

# --- SONUÇ ---
st.header("📊 Günlük Karbon Ayak İzin")
st.metric(label="Toplam (kg CO₂ / gün)", value=round(total_emission, 2))

# --- GRAFİK ---
labels = ["Ulaşım", "Elektrik", "Beslenme"]
values = [transport_emission, electricity_emission, meat_emission]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_ylabel("kg CO₂")
ax.set_title("Karbon Ayak İzi Dağılımı")

st.pyplot(fig)

st.divider()

# --- AKILLI ÖNERİ SİSTEMİ ---
st.header("🤖 Kişisel Karbon Azaltma Önerileri")

recommendations = []

if km > 20:
    recommendations.append(
        "🚲 Ulaşım kaynaklı emisyonun yüksek. Haftada 2 gün toplu taşıma veya bisiklet kullanarak %15–20 azaltabilirsin."
    )

if electricity > 250:
    recommendations.append(
        "💡 Elektrik tüketimin fazla. LED ampuller ve prizden çekme alışkanlığıyla aylık %10 tasarruf mümkün."
    )

if meat_days >= 4:
    recommendations.append(
        "🥗 Kırmızı et tüketimin yüksek. Haftada 1 gün azaltmak karbon ayak izini ciddi düşürür."
    )

if not recommendations:
    st.success("👏 Harika! Karbon ayak izin zaten düşük. Bu alışkanlıkları sürdür.")
else:
    for rec in recommendations:
        st.write("- " + rec)

st.divider()

# --- SENARYO ANALİZİ ---
st.header("🔮 Senaryo Analizi")

reduced_emission = (km * 0.15) + electricity_emission + meat_emission
difference = total_emission - reduced_emission

st.write(
    f"Eğer araç kullanımını azaltırsan günlük karbon ayak izin yaklaşık **{round(difference,2)} kg CO₂** azalır."
)

st.caption("📚 Emisyon katsayıları IPCC ve EPA verilerine dayalıdır.")


