import streamlit as st
import pandas as pd
import os

# ================= AYARLAR =================
DATA_FILE = "data.csv"
ADMIN_PASSWORD = "1234"

# CSV yoksa oluştur
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Ad", "Soyad", "Sinif", "No", "Su"]).to_csv(DATA_FILE, index=False)

# ================= GLOBAL =================
water_used = 0

# ================= YARDIMCI =================
def save_result(player, water_used):
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([{
        "Ad": player.get("ad",""),
        "Soyad": player.get("soyad",""),
        "Sinif": player.get("sinif",""),
        "No": player.get("no",""),
        "Su": water_used
    }])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ================= OYUN =================
def routine(title, options):
    st.write(f"### {title}")
    choice = st.radio("Seçimini yap:", [opt[0] for opt in options])
    # seçilen opsiyonun su miktarını döndür
    for opt in options:
        if opt[0] == choice:
            return opt[1]
    return 0

def play_game(player):
    water_used = 0

    water_used += routine("Sabah Rutini", [
        ("Musluk açık yüz yıkama", 10),
        ("Musluk kapalı yüz yıkama", 3),
        ("Islak mendil", 1)
    ])

    water_used += routine("Diş Fırçalama", [
        ("Musluk açık", 15),
        ("Bardakla", 4),
        ("Musluk kapalı", 2)
    ])

    water_used += routine("Okulda Su Kullanımı", [
        ("Uzun el yıkama", 8),
        ("Kısa el yıkama", 4),
        ("Dezenfektan", 1)
    ])

    water_used += routine("Akşam Rutini", [
        ("Uzun duş", 30),
        ("Kısa duş", 15),
        ("Duş almadan", 0)
    ])

    save_result(player, water_used)
    return water_used

# ================= ADMIN =================
def admin_panel():
    st.write("### Yönetici Paneli")
    password = st.text_input("Şifre:", type="password")
    if st.button("Giriş"):
        if password == ADMIN_PASSWORD:
            df = pd.read_csv(DATA_FILE)
            st.write("#### Öğrenci Sonuçları")
            st.dataframe(df)
        else:
            st.error("Şifre yanlış!")

# ================= MAIN =================
def main():
    st.title("💧 WaterQuest")
    menu = ["Oyuna Başla", "Yönetici Paneli"]
    choice = st.sidebar.selectbox("Menü", menu)

    if choice == "Oyuna Başla":
        st.header("Öğrenci Kayıt")
        with st.form("register_form"):
            ad = st.text_input("Ad")
            soyad = st.text_input("Soyad")
            sinif = st.number_input("Sınıf", min_value=1, max_value=12, step=1)
            no = st.number_input("Numara", min_value=1, step=1)
            submitted = st.form_submit_button("Kaydet ve Devam Et")
        if submitted:
            player = {"ad": ad, "soyad": soyad, "sinif": sinif, "no": no}

            st.write("### Karakterini Seç")
            char = st.radio("Karakter", ["Erkek", "Kadın"])
            player["char"] = char

            st.success("Oyuna başla butonuna bas!")
            if st.button("Oyna"):
                water = play_game(player)
                st.write(f"### Günlük Su Tüketimin: {water} L")
                if water <= 50:
                    st.success("Tebrikler! Bilinçli kullandın 🎉")
                else:
                    st.warning("Daha az su kullanabilirdin")

    elif choice == "Yönetici Paneli":
        admin_panel()

if __name__ == "__main__":
    main()


