import streamlit as st
import json
import os

# --- AYARLAR ---
DATA_FILE = "promptlar.json"
DATA_DIR = "data"

if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

def veri_yukle():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def veri_kaydet(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if 'prompt_listesi' not in st.session_state:
    st.session_state.prompt_listesi = veri_yukle()

# --- ADMIN PANELİ ---
with st.sidebar:
    st.header("⚙️ Admin Paneli")
    if st.text_input("Şifre:", type="password") == "admin123":
        st.subheader("Yeni Prompt Ekle")
        yeni_baslik = st.text_input("Başlık")
        yeni_kategori = st.selectbox("Kategori", ["Yazılım", "Tasarım", "Pazarlama", "Eğitim"])
        yeni_prompt = st.text_area("Prompt İçeriği")
        
        if st.button("Kaydet"):
            st.session_state.prompt_listesi.append({
                "baslik": yeni_baslik, "kategori": yeni_kategori, "prompt": yeni_prompt
            })
            veri_kaydet(st.session_state.prompt_listesi)
            st.success("Kaydedildi!")

# --- ANA EKRAN ---
st.title("🚀 AI Prompt Kütüphanesi")

# Kategori Filtresi
kategoriler = ["Tümü"] + list(set(p['kategori'] for p in st.session_state.prompt_listesi))
secilen_filtre = st.selectbox("Kategoriye Göre Filtrele:", kategoriler)

# Gösterim
for item in st.session_state.prompt_listesi:
    if secilen_filtre == "Tümü" or item["kategori"] == secilen_filtre:
        with st.container(border=True):
            st.markdown(f"**{item['baslik']}** | *{item['kategori']}*")
            st.code(item["prompt"])
