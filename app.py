import streamlit as st
import google.generativeai as genai
import os
import json
from gemini import Gemini
import spacy

# Setel API key dan model NLP
api_key = os.getenv("AIzaSyAwnWCj9gkgGN9v397HROgWlLzU_7M6ms0") or "AIzaSyAwnWCj9gkgGN9v397HROgWlLzU_7M6ms0"
genai.configure(api_key=api_key)  # Ganti dengan API key yang sesuai
# nlp = spacy.load("en_core_web_sm")

# Inisialisasi session states
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'generate_button_clicked' not in st.session_state:
    st.session_state["generate_button_clicked"] = False
if 'model' not in st.session_state:
    st.session_state["model"] = None
if 'response' not in st.session_state:
    st.session_state["response"] = {}

# Fungsi utama untuk menjalankan aplikasi
def main():
    session_state = st.session_state

    # Judul dan tata letak
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            color: #1E90FF; /* DodgerBlue untuk tampilan segar */
            font-size: 3rem;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #32CD32; /* LimeGreen untuk kesan cerah */
            font-size: 1.5rem;
        }
        .image {
            display: block;
            margin: 0 auto;
            width: 400px;
            border-radius: 10px;
        }
        .day-header {
            text-align: center;
            color: #1E90FF;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .button {
            background-color: #32CD32;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #228B22; /* Warna hijau lebih gelap untuk efek hover */
        }
        .container {
            padding: 20px;
        }
        </style>
        <div class="title">
            <h1>PUNGGAWA TRAVEL 🛫</h1>
        </div>
        <div class="subtitle">
            <h3>Rencanakan perjalanan yang tak terlupakan dengan Travel Planner</h3>
        </div>
        <img src='https://i.pinimg.com/originals/20/cb/f3/20cbf31ecf279ccab1a3264a2cec80c6.jpg' 
             alt='Gambar Perjalanan' class='image'>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.sidebar.header("📋 **Detail Perjalanan**")

    # Input sidebar untuk detail perjalanan
    with st.sidebar.form("trip_form"):
        country = st.text_input("🌍 Masukkan negara", "Rusia")
        city = st.text_input("🏙️ Masukkan kota", "Moskow")
        days = st.number_input("📅 Untuk berapa hari?", min_value=1, value=3)
        members = st.number_input("👥 Berapa anggota grup?", min_value=1, value=1)
        generate_plan = st.form_submit_button("Buat Rencana Perjalanan 🗺️")

    if generate_plan:
        # Reset counter dan response ketika rencana baru dihasilkan
        st.session_state['counter'] = 0
        model = Gemini(city, country, days, members)
        model.get_response(markdown=False)
        st.session_state["model"] = model
        session_state["generate_button_clicked"] = True
        st.session_state["response"] = {}
        try:
            with open(r'./gemini_answer.json', 'r', encoding="utf-8") as file:
                st.session_state["response"] = json.load(file)
        except FileNotFoundError:
            st.error("File respons tidak ditemukan. Pastikan path dan nama file sudah benar.")

    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        response = st.session_state.get("response", {})
        current_day = f"Hari {st.session_state['counter'] + 1}"
        st.markdown(f"<h3 class='day-header'>{current_day} 📅</h3>", unsafe_allow_html=True)

        model = st.session_state.get("model")
        
        current_day_infos = st.empty()
        
        if model is not None:
            if current_day in response:
                info = "".join([f"**{key}**: {value}\n" for key, value in response[current_day].items()])
                current_day_infos.write(model.to_markdown(info))
            else:
                current_day_infos.write("Buat Rencana Perjalanan untuk melihat detail di sini! ✨")

        st.markdown("---")
        
        if st.button("Hari Selanjutnya ➡️", help="Klik untuk melihat rencana hari berikutnya."):
            if st.session_state['counter'] < len(response) - 1:
                st.session_state['counter'] += 1
                current_day = f"Hari {st.session_state['counter'] + 1}"
                if current_day in response:
                    current_day_infos.empty()
                    info = "".join([f"**{key}**: {value.strip()}\n" for key, value in response[current_day].items()])
                    current_day_infos.write(model.to_markdown(info))
                else:
                    current_day_infos.empty()
                    current_day_infos.write("Tidak ada informasi untuk hari ini. 🛑")

if __name__ == '__main__':
    main()