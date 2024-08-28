import google.generativeai as genai
import os
import json

# Set up the API key
api_key = os.getenv("API_KEY")  # Pastikan nama variabel lingkungan yang benar
genai.configure(api_key=api_key)

class Gemini:
    def __init__(self, city, country, days, members):
        self.city = city
        self.country = country
        self.days = days
        self.members = members
        self.model = genai.GenerativeModel('gemini-pro')

    @staticmethod    
    def to_markdown(text):
        # Perbaiki format dari teks menjadi markdown
        text = text.replace('*Morning:*', '**Pagi:**')
        text = text.replace('*Afternoon:*', '**Siang:**')
        text = text.replace('*Evening:*', '**Malam:**')
        text = text.replace(':: -', '* -')  # Menyederhanakan bullet points dan format
        text = text.replace('\n*', '\n\n*')  # Menambahkan baris baru sebelum bullet 
        
        print(text)
        return text.strip()

    def parse_trip_plan(self, trip_plan, return_=True):
        # Pisahkan rencana perjalanan berdasarkan hari dan ambil detailnya
        days = trip_plan.split("**Hari ")[1:]  # Pisahkan rencana perjalanan berdasarkan "**Hari " dan hapus string kosong pertama
        trip_dict = {}
        for i, day in enumerate(days, start=1):
            day_num = f"Hari {i}"
            try:
                parts = day.split("**Pagi:**")
                pagi = parts[1].split("**Siang:**")[0].strip()
                siang = parts[1].split("**Siang:**")[1].split("**Malam:**")[0].strip()
                malam = parts[1].split("**Malam:**")[1].strip()
                trip_dict[day_num] = {
                    "Pagi": pagi,
                    "Siang": siang,
                    "Malam": malam
                }
            except IndexError:
                print(f"Peringatan: Hari {i} memiliki rencana yang tidak lengkap. Melewatkan.")
        # Simpan rencana perjalanan yang diparsing ke dalam file JSON
        with open("gemini_answer.json", "w") as json_file:
            json.dump(trip_dict, json_file, indent=4)
        if return_:
            return trip_dict
    
    def get_response(self, markdown=True):
        # Mulai dengan pembuka yang ramah
        prompt = f"""
        🌟 **Siapkan Rencana Liburan yang Tak Terlupakan ke {self.city}, {self.country}!** 🌟

        Halo! Kamu ditantang untuk membuat rencana perjalanan seru selama {self.days} hari untuk grup keren berjumlah {self.members} orang. Nah, kami ini ingin menikmati campuran yang sempurna dari:
        - 🏛️ **Jelajah Sejarah** (karena kita kan nggak mau dikira kurang gaul sama nenek moyang 🤭)
        - 🎨 **Keajaiban Budaya** (biar feed Instagram kita nggak kalah artsy sama influencer)
        - 🍽️ **Kenikmatan Kuliner** (perut kenyang, hati senang!)

        Gimana? Siap kan? Yuk, kita mulai!

        """

        # Loop untuk tiap hari
        for day in range(1, self.days + 1):
            prompt += f"""
            **Hari {day}:**
            - **Pagi:** Yuk, bangun dan mulai hari dengan semangat! 🚶‍♂️ Rekomendasiin dong dua tempat atau aktivitas seru buat memulai petualangan kita. Kalau bisa yang bikin langsung lupa kangen sama kasur! 😴
            - **Siang:** Perut mulai keroncongan? Nah, waktu yang pas buat menjelajah lebih dalam kota ini! 🌆 Kasih tau tempat menarik untuk dijelajahi, makan siang yang maknyus, atau mungkin spot budaya lokal yang bikin kita merasa jadi warga setempat (kira-kira).
            - **Malam:** Setelah seharian jalan-jalan, jangan lupa malamnya juga harus berkesan! 🌟 Rekomendasikan ide makan malam yang asyik dan kegiatan malam seru buat bikin malam ini nggak terlupakan. Kalau bisa, yang bikin kita pengen cerita ke semua orang besoknya! 😄
            """

        # Akhiri prompt dengan contoh format tanggapan
        prompt += """
        Oh iya, ada sedikit tips nih: Jangan masukin info soal harga ya. Kita kan pengen fokus nikmatin liburan, bukan ngitung-ngitung biaya! 😅

        Yuk, format tanggapannya kayak gini, biar rapi dan jelas:

        """
        
        # Format respons per hari
        for day in range(1, self.days + 1):
            prompt += f"""
            **Hari {day}:**
            **Pagi:**
            
            
            - Aktivitas 1
            - Aktivitas 2

            **Siang:**
            
            
            - Aktivitas 1
            - Aktivitas 2

            **Malam:**
            
            
            - Aktivitas 1
            - Aktivitas 2
            """

        # Penutup yang ramah dan penuh energi
        prompt += """
        ✨ Ingat ya, buat rencananya semenarik mungkin! Liburan ini harus penuh tawa, pengalaman seru, dan tentu saja... kenangan yang tak terlupakan! Jangan lupa kasih banyak emotikon biar makin seru! 😎✨

        Happy planning, dan semoga itinerary ini bikin kita semua nggak sabar buat berangkat!
        """

        # Hasilkan konten menggunakan model
        response = self.model.generate_content(prompt)
        
        print(response)
        
        if response.parts:
            response = response.parts[0].text
        
        # Proses respons berdasarkan flag markdown
        if markdown:
            response = self.to_markdown(response)
        else:
            response = self.parse_trip_plan(response)
        return response