import streamlit as st
import requests

# API Key ของผู้พัฒนา
API_KEY = "324b8ac5466a7035cd7bd7ce5b3ab073"

st.set_page_config(page_title="ระบบประเมินสถานการณ์ฝนสำหรับแม่ค้า", layout="centered")

st.title("ระบบประเมินสถานการณ์ฝนสำหรับแม่ค้า")
st.write("ตรวจสอบสภาพอากาศและประเมินความเสี่ยงฝนตกเพื่อการวางแผนขายของ")

city = st.text_input("กรุณากรอกชื่อเมืองหรือจังหวัด (ภาษาอังกฤษ):", value="Bangkok")

if st.button("ตรวจสอบสภาพอากาศ"):
    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY:
        st.error("ผู้พัฒนาลืมใส่ API Key ในตัวแปร API_KEY ครับ")
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=th"
        
        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                city_name = data['name']
                weather_main = data['weather'][0]['main']
                weather_desc = data['weather'][0]['description']
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed'] * 3.6
                rain_1h = data.get('rain', {}).get('1h', 0)

                st.subheader(f"รายงานสภาพอากาศ: {city_name}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("อุณหภูมิ", f"{temp:.1f} °C")
                col2.metric("ความชื้น", f"{humidity}%")
                col3.metric("ความเร็วลม", f"{wind_speed:.1f} กม./ชม.")
                
                st.write(f"**สภาพอากาศปัจจุบัน:** {weather_desc}")
                st.divider()

                st.subheader("ผลการประเมินสำหรับแม่ค้า")

                if weather_main in ['Rain', 'Drizzle', 'Thunderstorm'] or rain_1h > 0:
                    st.error("สถานะ: ฝนตกอยู่ / ฝนกำลังตก")
                    st.write("คำแนะนำ: เก็บร้านหรือคลุมผ้าใบพลาสติกทันที ยกปลั๊กไฟให้พ้นระดับน้ำ")

                elif humidity >= 85:
                    st.warning("สถานะ: ความชื้นสูงมาก มีโอกาสฝนตกในเร็วๆ นี้")
                    st.write("คำแนะนำ: เตรียมกางเต็นท์หรือเตรียมผ้าใบไว้ใกล้ตัว")

                elif weather_main == 'Clouds':
                    st.info("สถานะ: มีเมฆมาก ฝนยังไม่ตก")
                    st.write("คำแนะนำ: ตั้งร้านได้ตามปกติ แต่ควรเฝ้าระวังลมและฟ้าฝน")

                else:
                    st.success("สถานะ: ฝนไม่ตก ขายของได้ตามปกติ")
                    st.write("คำแนะนำ: สภาพอากาศปกติ เหมาะแก่การตั้งร้านขายของ")

                if wind_speed > 20:
                    st.warning(f"คำเตือนลมแรง: ความเร็วลม {wind_speed:.1f} กม./ชม. ควรใช้ของหนักถ่วงขาเต็นท์")

            else:
                st.error(f"ไม่พบข้อมูลเมืองนี้ หรือเกิดข้อผิดพลาด: {data.get('message')}")

        except Exception as e:
            st.error(f"ไม่สามารถเชื่อมต่อได้: {e}")
