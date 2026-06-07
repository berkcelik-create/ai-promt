import streamlit as st
import json
import os

DATA_FILE = "promptlar.json"
USER_FILE = "kullanicilar.json"

def veri_yukle(dosya):
    if os.path.exists(dosya):
        with open(dosya, "r", encoding="utf-8") as f: return json.load(f)
    return {} if dosya == USER_FILE else []

def veri_kaydet(dosya, data):
    with open(dosya, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

if 'prompt_listesi' not in st.session_state: st.session_state.prompt_listesi = veri_yukle(DATA_FILE)
if 'kullanicilar' not in st.session_state: st.session_state.kullanicilar = veri_yukle(USER_FILE)
if 'giris_yapti' not in st.session_state: st.session_state.giris_yapti = False

# --- YAN PANEL: GİRİŞ/KAYIT ---
with st.sidebar:
    st.header("🔑 Hesap İşlemleri")
    if not st.session_state.giris_yapti:
        secim = st.radio("İşlem:", ["Giriş Yap", "Kayıt Ol"])
        kullanici = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        
        if secim == "Kayıt Ol":
            if st.button("Kayıt Ol"):
                if kullanici in st.session_state.kullanicilar: st.error("Bu kullanıcı zaten var!")
                else:
                    st.session_state.kullanicilar[kullanici] = sifre
                    veri_kaydet(USER_FILE, st.session_state.kullanicilar)
                    st.success("Kayıt başarılı! Şimdi giriş yapabilirsin.")
        else:
            if st.button("Giriş Yap"):
                if st.session_state.kullanicilar.get(kullanici) == sifre:
                    st.session_state.giris_yapti = True
                    st.session_state.aktif_kullanici = kullanici
                    st.rerun()
                else: st.error("Hatalı bilgiler!")
    else:
        st.write(f"Hoş geldin, **{st.session_state.aktif_kullanici}**")
        if st.button("Çıkış Yap"):
            st.session_state.giris_yapti = False
            st.rerun()

# --- İÇERİK PAYLAŞIM ---
if st.session_state.giris_yapti:
    with st.expander("➕ Yeni Prompt Paylaş"):
        baslik = st.text_input("Başlık")
        kat = st.selectbox("Kategori", ["Yazılım", "Tasarım", "Pazarlama", "Eğitim"])
        prompt = st.text_area("İçerik")
        if st.button("Yayınla"):
            st.session_state.prompt_listesi.append({"yazar": st.session_state.aktif_kullanici, "kategori": kat, "baslik": baslik, "prompt": prompt})
            veri_kaydet(DATA_FILE, st.session_state.prompt_listesi)
            st.rerun()

# --- LİSTELEME ---
st.title("🚀 Yapay Zeka Destekli Kütüphane")
for item in st.session_state.prompt_listesi:
    with st.container(border=True):
        st.subheader(item.get('baslik', 'Başlıksız'))
        st.caption(f"Yazar: {item.get('yazar')} | Kategori: {item.get('kategori')}")
        st.code(item.get('prompt', ''))
