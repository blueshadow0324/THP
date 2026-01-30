import streamlit as st
import json
import time

st.title("Indev 1.6")
code = ""
submit = False

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
            if not code == "":
                 st.warning("Fel spelar kod")
                 time.sleep(1)

        st.session_state._process = False
        st.rerun()
elif st.session_state.step == 2:
    with st.form("FORM2"):
        pos = st.checkbox("Bra")
        med = st.checkbox("Medel")
        neg = st.checkbox("Dåligt")
        comment = st.text_input("Kommentar:")
        submit = st.form_submit_button("Enter")
        if submit:
            if pos == True:
                st.dialog("Skickat in resultatet!")
                time.sleep(1)
                st.session_state._process = False
                st.session_state.step = 1
                st.rerun()
            else:
                if med == True:
                    st.dialog("Skickat in resultatet!")
                    time.sleep(1)
                    st.session_state._process = False
                    st.session_state.step = 1
                    st.rerun()
                else:
                    if neg == True:
                        st.dialog("Skickat in resultatet!")
                        time.sleep(1)
                        st.session_state._process = False
                        st.session_state.step = 1
                        st.rerun()
                    else:
                        st.warning("Inget resultatet är sant!")