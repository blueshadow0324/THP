import streamlit as st
import json
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests

st.title("Svarsform")
code = ""
submit = False
date = datetime.datetime.now().date()

sender_email = "olsonwilliam11@gmail.com"
email = "hinke71@gmail.com"

# Initialize state
if "step" not in st.session_state:
    st.session_state.step = 1

# CHANGED: messages survive st.rerun() so you can actually see send results
def notify(text, ok=True):
    st.session_state.msg = (text, ok)

def send():
    # CHANGED: send over HTTPS (Brevo API) instead of SMTP
    api_key = os.environ.get("BREVO_API_KEY") or st.secrets.get("BREVO_API_KEY", "")
    try:
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": api_key, "accept": "application/json", "content-type": "application/json"},
            json={
                "sender": {"name": "Svarsform", "email": sender_email},
                "to": [{"email": email}],
                "subject": str(date),
                "textContent": body_text,
            },
            timeout=20,
        )
        if r.status_code in (200, 201):
            notify("Email sent successfully.")
        else:
            notify(f"Failed to send email: {r.status_code} {r.text}", False)
    except requests.RequestException as e:
        notify(f"Failed to send email: {e}", False)

    body_text = json.dumps(data, indent=2, ensure_ascii=False)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = str(date)
    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        notify("Email sent sucessfully.")
    except smtplib.SMTPAuthenticationError:
        notify("Login failed — check that GMAIL_APP_PASSWORD is a valid Gmail App Password.", False)
    except smtplib.SMTPException as e:
        notify(f"Failed to send email: {e}", False)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# CHANGED: show a pending message (if any) once
if "msg" in st.session_state:
    text, ok = st.session_state.pop("msg")
    (st.success if ok else st.error)(text)

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
        except KeyError:  # CHANGED: was a bare except
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

        # TODO (after training): add the actual questions here, and store their
        # answers in extra dicts (e.g. q = {}) the same way as phy / fys above.
        # Then add them to the `data[code]` entry in the save block below.

        submit = st.form_submit_button("Skicka In!")

        if submit:
            # CHANGED: only the checkboxes count (a comment alone used to pass the check)
            if any(phy[k] for k in ("pos", "med", "neg")) and any(fys[k] for k in ("pos", "med", "neg")):
                code = st.session_state._submitted_code
                try:
                    with open(f"{date}.json", "r", encoding="utf-8") as file:
                        data = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {}  # CHANGED: old code wrote to a file named "{}.json"

                data[code] = {"phy": phy, "fys": fys}
                with open(f"{date}.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)

                notify("Skickat in resultatet!")  # CHANGED: st.dialog is a decorator, not a message
                st.session_state._process = False
                st.session_state.step = 1
                st.rerun()
            else:
                st.warning("Inget resultatet är sant!")
