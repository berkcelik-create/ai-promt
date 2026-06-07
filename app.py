import streamlit as st
import json
import os

# --- AYARLAR ---
DATA_FILE = "promptlar.json"

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

# --- ÜYE / ADMIN PANELİ ---
with st.sidebar:
    st.header("👤 Üye Girişi / Paylaşım")
    kullanici = st.text_input("Kullanıcı Adı:")
    sifre = st.text_input("Şifre:", type="password")
    
    if sifre == "uye123": # Basit üyelik şifresi
        st.success(f"Hoş geldin, {kullanici}!")
        st.subheader("Prompt Paylaş")
        yeni_baslik = st.text_input("Prompt Başlığı")
        yeni_kat = st.selectbox("Kategori", ["Yazılım", "Tasarım", "Pazarlama", "Eğitim"])
        yeni_prompt = st.text_area("İçerik")
        
        if st.button("Sitede Yayınla"):
            st.session_state.prompt_listesi.append({
                "yazar": kullanici, "baslik": yeni_baslik, "kategori": yeni_kat, "prompt": yeni_prompt
            })
            veri_kaydet(st.session_state.prompt_listesi)
            st.rerun()
    else:
        st.info("İçerik paylaşmak için giriş yap.")

# --- ANA EKRAN ---
st.title("🚀 Topluluk Prompt Kütüphanesi")
# Arama Çubuğu
arama = st.text_input("🔍 Prompt ara...")

# Kategori Filtreleme
katlar = ["Tümü"] + list(set(p['kategori'] for p in st.session_state.prompt_listesi))
filtre = st.selectbox("Kategori Seç:", katlar)

for item in st.session_state.prompt_listesi:
    # Arama ve Filtreleme Mantığı
    if (filtre == "Tümü" or item["kategori"] == filtre) and (arama.lower() in item["baslik"].lower()):
        with st.container(border=True):
            st.subheader(item["baslik"])
            st.caption(f"Yazar: {item['yazar']} | Kategori: {item['kategori']}")
            st.code(item["prompt"])
