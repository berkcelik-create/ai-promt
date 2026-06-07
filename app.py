import streamlit as st
import json
import os

# --- PREMIUM TASARIM & CSS ---
st.set_page_config(page_title="Prompt Engine", layout="wide")
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%); color: #f8fafc; }
    [data-testid="stVerticalBlock"] [data-testid="stContainer"] {
        background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px); border-radius: 20px; padding: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    h1 { color: #38bdf8 !important; text-align: center; }
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
        color: white; border: none; border-radius: 12px; font-weight: 600; padding: 10px 20px; transition: 0.3s;
    }
    .stButton>button:hover { box-shadow: 0 0 20px rgba(14, 165, 233, 0.5); transform: translateY(-2px); }
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
    st.title("⚙️ Dashboard")
    if not st.session_state.giris_yapti:
        secim = st.radio("İşlem:", ["Giriş Yap", "Kayıt Ol"])
        kullanici = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        if secim == "Kayıt Ol" and st.button("Kayıt Ol"):
            if kullanici in st.session_state.kullanicilar: st.error("Kullanıcı mevcut!")
            else:
                st.session_state.kullanicilar[kullanici] = sifre
                veri_kaydet(USER_FILE, st.session_state.kullanicilar)
                st.success("Kayıt başarılı!")
        elif secim == "Giriş Yap" and st.button("Giriş Yap"):
            if st.session_state.kullanicilar.get(kullanici) == sifre:
                st.session_state.giris_yapti = True
                st.session_state.aktif_kullanici = kullanici
                st.rerun()
    else:
        st.write(f"Hoş geldin, **{st.session_state.aktif_kullanici}**")
        if st.button("Çıkış Yap"):
            st.session_state.giris_yapti = False
            st.session_state.admin_id = None
            st.rerun()

    st.divider()
    st.subheader("👑 Admin Paneli")
    admin_id = st.text_input("Admin ID:", key="adm_id")
    admin_pw = st.text_input("Admin Şifre:", type="password", key="adm_pw")
    if admin_id == "admin" and admin_pw == "admin123":
        st.session_state.admin_id = "admin"
        st.warning("Admin Yetkisi Aktif")
        if st.button("Tüm Veriyi Sıfırla"):
            st.session_state.prompt_listesi = []
            veri_kaydet(DATA_FILE, [])
            st.rerun()

# --- ANA EKRAN ---
st.title("🚀 Prompt Engine v2.1")

# İstatistikler (Üye sayısı kaldırıldı, 2 sütunlu düzen)
col1, col2 = st.columns(2)
col1.metric("Toplam İstem", len(st.session_state.prompt_listesi))
col2.metric("Kategori Sayısı", len(set(p.get('kategori') for p in st.session_state.prompt_listesi)))

if st.session_state.giris_yapti:
    with st.expander("➕ Yeni İstem (Prompt) Paylaş"):
        baslik = st.text_input("Başlık")
        kat = st.selectbox("Kategori", ["Yazılım", "Tasarım", "Pazarlama", "Eğitim"])
        prompt = st.text_area("İstem İçeriği")
        if st.button("Sistemde Yayınla"):
            st.session_state.prompt_listesi.append({"yazar": st.session_state.aktif_kullanici, "kategori": kat, "baslik": baslik, "prompt": prompt})
            veri_kaydet(DATA_FILE, st.session_state.prompt_listesi)
            st.rerun()

arama = st.text_input("🔍 İstem ara...")
filtre = st.selectbox("Kategori Seç:", ["Tümü"] + list(set(p.get('kategori', 'Genel') for p in st.session_state.prompt_listesi)))

for i, item in enumerate(st.session_state.prompt_listesi):
    if (filtre == "Tümü" or item.get('kategori') == filtre) and (arama.lower() in item.get('baslik', '').lower()):
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            c1.subheader(item.get('baslik', 'Başlıksız'))
            if c2.button("📋 Kopyala", key=f"kop_{i}"):
                st.toast("İçerik kopyalandı!")
            st.caption(f"Yazar: {item.get('yazar')} | Kategori: {item.get('kategori')}")
            st.code(item.get('prompt', ''))
            if st.session_state.get("admin_id") == "admin":
                if st.button(f"🗑️ Sil", key=f"sil_{i}"):
                    st.session_state.prompt_listesi.pop(i)
                    veri_kaydet(DATA_FILE, st.session_state.prompt_listesi)
                    st.rerun()

st.caption("© 2026 Prompt Engine - Premium AI Platform")
