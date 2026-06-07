import streamlit as st
import json
import os

# --- PREMIUM TASARIM & CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #3a3a5a 100%);
        color: white;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        border: none;
    }
    .css-1r6slb0 { background-color: #2e2e48; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
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

# --- YAN PANEL ---
with st.sidebar:
    st.header("🔑 Hesap Paneli")
    if not st.session_state.giris_yapti:
        secim = st.radio("İşlem:", ["Giriş Yap", "Kayıt Ol"], key="radio_giris")
        kullanici = st.text_input("Kullanıcı Adı", key="u_ad")
        sifre = st.text_input("Şifre", type="password", key="u_sifre")
        
        if secim == "Kayıt Ol" and st.button("Kayıt Ol", key="btn_kayit"):
            if kullanici in st.session_state.kullanicilar: st.error("Zaten var!")
            else:
                st.session_state.kullanicilar[kullanici] = sifre
                veri_kaydet(USER_FILE, st.session_state.kullanicilar)
                st.success("Kayıt başarılı!")
        elif secim == "Giriş Yap" and st.button("Giriş Yap", key="btn_giris"):
            if st.session_state.kullanicilar.get(kullanici) == sifre:
                st.session_state.giris_yapti = True
                st.session_state.aktif_kullanici = kullanici
                st.rerun()
            else: st.error("Hatalı bilgiler!")
    else:
        st.write(f"Hoş geldin, **{st.session_state.aktif_kullanici}**")
        if st.button("Çıkış Yap", key="btn_cikis"):
            st.session_state.giris_yapti = False
            st.rerun()

    st.divider()
    st.header("👑 Admin")
    admin_id = st.text_input("Admin ID:", key="adm_id")
    admin_pw = st.text_input("Admin Şifre:", type="password", key="adm_pw")
    if admin_id == "admin" and admin_pw == "admin123":
        st.session_state.admin_id = "admin"
        st.warning("Admin Modu Aktif")
        if st.button("Tüm Veriyi Sıfırla", key="btn_reset"):
            st.session_state.prompt_listesi = []
            veri_kaydet(DATA_FILE, [])
            st.rerun()

# --- ANA EKRAN ---
st.title("🚀 Yapay Zeka Destekli Kütüphane")

if st.session_state.giris_yapti:
    with st.expander("➕ Yeni Prompt Paylaş"):
        baslik = st.text_input("Başlık", key="y_baslik")
        kat = st.selectbox("Kategori", ["Yazılım", "Tasarım", "Pazarlama", "Eğitim"], key="y_kat")
        prompt = st.text_area("İçerik", key="y_prompt")
        if st.button("Yayınla", key="btn_yayinla"):
            st.session_state.prompt_listesi.append({"yazar": st.session_state.aktif_kullanici, "kategori": kat, "baslik": baslik, "prompt": prompt})
            veri_kaydet(DATA_FILE, st.session_state.prompt_listesi)
            st.rerun()

arama = st.text_input("🔍 Prompt ara...", key="ana_arama")
kategoriler = ["Tümü"] + list(set(p.get('kategori', 'Genel') for p in st.session_state.prompt_listesi))
filtre = st.selectbox("Kategori Seç:", kategoriler, key="ana_filtre")

for i, item in enumerate(st.session_state.prompt_listesi):
    if (filtre == "Tümü" or item.get('kategori') == filtre) and (arama.lower() in item.get('baslik', '').lower()):
        with st.container(border=True):
            st.subheader(item.get('baslik', 'Başlıksız'))
            st.caption(f"Yazar: {item.get('yazar')} | Kategori: {item.get('kategori')}")
            st.code(item.get('prompt', ''))
            if st.session_state.get("admin_id") == "admin":
                if st.button(f"🗑️ Sil: {item.get('baslik')}", key=f"sil_{i}"):
                    st.session_state.prompt_listesi.pop(i)
                    veri_kaydet(DATA_FILE, st.session_state.prompt_listesi)
                    st.rerun()
