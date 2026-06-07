import streamlit as st
import json
import os

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

# --- PANEL SİSTEMİ ---
with st.sidebar:
    st.header("🔐 Giriş Panelleri")
    
    # Üye Paneli
    with st.expander("👤 Üye Girişi (İçerik Paylaş)"):
        u_kullanici = st.text_input("Üye Adı:")
        u_sifre = st.text_input("Üye Şifre:", type="password")
        if u_sifre == "uye123":
            y_baslik = st.text_input("Başlık")
            y_kat = st.selectbox("Kategori", ["Yazılım", "Tasarım", "Pazarlama", "Eğitim"])
            y_prompt = st.text_area("Prompt İçeriği")
            if st.button("Paylaş"):
                st.session_state.prompt_listesi.append({
                    "yazar": u_kullanici, "kategori": y_kat, "baslik": y_baslik, "prompt": y_prompt
                })
                veri_kaydet(st.session_state.prompt_listesi)
                st.rerun()

    # Admin Paneli
    with st.expander("⚙️ Admin Girişi (Tüm Yetki)"):
        a_sifre = st.text_input("Admin Şifre:", type="password")
        if a_sifre == "admin123":
            st.warning("Admin modundasın.")
            if st.button("Tüm Veriyi Sıfırla"):
                st.session_state.prompt_listesi = []
                veri_kaydet([])
                st.rerun()

# --- ANA EKRAN ---
st.title("🚀 Yapay Zeka Destekli Kütüphane")
arama = st.text_input("🔍 Prompt ara...")
kategoriler = ["Tümü"] + list(set(p.get('kategori', 'Genel') for p in st.session_state.prompt_listesi))
filtre = st.selectbox("Kategori Seç:", kategoriler)

for item in st.session_state.prompt_listesi:
    # Hata almamak için .get() metodu kullanıldı
    yazar = item.get('yazar', 'Anonim')
    kat = item.get('kategori', 'Genel')
    baslik = item.get('baslik', 'Başlıksız')
    prompt = item.get('prompt', '')
    
    if (filtre == "Tümü" or kat == filtre) and (arama.lower() in baslik.lower()):
        with st.container(border=True):
            st.subheader(baslik)
            st.caption(f"Yazar: {yazar} | Kategori: {kat}")
            st.code(prompt)
