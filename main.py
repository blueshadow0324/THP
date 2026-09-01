import streamlit as st
import json
import time
import datetime
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

st.title("Indev 1.8")
code = ""
submit = False
date = datetime.datetime.now().date()
print(date)
password = "amkn krcs yhdv nskp"
email = "hinke71@gmai.com"

# Initialize state
if "step" not in st.session_state:
    st.session_state.step = 1

st.markdown("""
<style>
/* Hide main menu */
#MainMenu {visibility: hidden;}

/* Hide footer */
footer {visibility: hidden;}

/* Hide header (Deploy button, etc.) */
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if st.session_state.step == 1:
    with st.form("FORM"):
        code = st.text_input("Kod:")
        submit = st.form_submit_button("Enter")

    if submit:
      st.session_state._submitted_code = code
      st.session_state._process = True

if st.session_state.get("_process"):
    with open("codes.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        try:
            player_ID = data[st.session_state._submitted_code]  # String
            st.session_state.step = 2
        except:
            if "admin" == st.session_state._submitted_code:
                send()

        st.session_state._process = False
        st.rerun()
elif st.session_state.step == 2:
    with st.form("FORM2"):
        phy = {}
        fys = {}

        st.text("Knopp")
        phy["pos"] = st.checkbox("Bra👍")
        phy["med"] = st.checkbox("Medel😐")
        phy["neg"] = st.checkbox("Dåligt👎 ")
        phy["comment"] = st.text_input("Kommentar:")

        st.divider()

        st.text("Kropp")
        fys["pos"] = st.checkbox(" Bra👍 ")
        fys["med"] = st.checkbox(" Medel😐 ")
        fys["neg"] = st.checkbox(" Dåligt👎 ")
        fys["comment"] = st.text_input("Kommentar: ")
        submit = st.form_submit_button("Skicka In!")

        currentCode = st.session_state._submitted_code

        if submit:
            for key in fys:
                if fys[key]:
                    for k in phy:
                        if phy[k]:
                            st.dialog("Skickat in resultatet!")
                            try:
                                with open(f"{date}.json", "r") as file:
                                    data = json.load(file)
                            except:
                                data = {}
                                with open(f"{data}.json", "w") as file:
                                    json.dump(data, file, indent=4)
                            try:
                                with open(f"{date}.json", "r") as file:
                                    data = json.load(file)
                            except:
                                with open(f"{data}.json", "w") as file:
                                    json.dump(data, file, indent=4)

                            if st.session_state._submitted_code not in data:
                                data[st.session_state._submitted_code] = {}
                                data[st.session_state._submitted_code]["phy"] = {}
                                data[st.session_state._submitted_code]["fys"] = {}
                            with open(f"{date}.json", "w") as file:
                                json.dump(data, file, indent=4)
                            with open(f"{date}.json", "r") as file:
                                data = json.load(file)
                            for i in fys:
                                data[st.session_state._submitted_code]["fys"][i] = fys[i]
                            for j in phy:
                                data[st.session_state._submitted_code]["phy"][j] = phy[j]
                            with open(f"{date}.json", "w") as file:
                                json.dump(data, file, indent=4)
                            time.sleep(1)
                            st.session_state._process = False
                            st.session_state.step = 1
                            st.rerun()
            st.warning("Inget resultatet är sant!")
def send():
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = email
    msg["Subject"] = str(date)
    msg.attach(MIMEText(body, "test - debug"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email, password)
        server.send_message(msg)

    print("Email sent successfully.")
    
