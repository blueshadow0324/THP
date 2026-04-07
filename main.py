import streamlit as st
import json
import time
import datetime
from mail import send

st.title("Indev 1.8")
code = ""
submit = False
date = datetime.datetime.now().date()
print(date)

def get_body():
    with open(f"{date}.json", "r") as f:
        raw = json.load(f)
        list = []
        for players, states in raw.items():
            physical = states["phy"]
            fysical = states["fys"]

            physicalState = None
            fysicalState = None

            phyNumb = {"p": 0, "m": 0, "n": 0}
            fysNumb = {"p": 0, "m": 0, "n": 0}

            for i in physical:
                if physical[i] == True:
                    if i == "pos":
                        physicalState = "Bra!"
                        phyNumb["p"] = phyNumb["p"] + 1
                    if i == "mid":
                        physicalState = "Medel"
                        phyNumb["m"] = phyNumb["m"] + 1
                    if i == "neg":
                        physicalState = "Dåligt"
                        phyNumb["n"] = phyNumb["n"] + 1
            for j in fysical:
                if physical[j] == True:
                    if j == "pos":
                        fysicalState = "Bra!"
                        fysNumb["p"] = fysNumb["p"] + 1
                    if j == "mid":
                        fysicalState = "Medel"
                        fysNumb["m"] = fysNumb["m"] + 1
                    if j == "neg":
                        fysicalState = "Dåligt"
                        fysNumb["n"] = fysNumb["n"] + 1

            list.append(f"{players}|Knopp: {physicalState}|Kropp: {fysicalState}|Kommentar: (Kropp, Knopp): {fysical["comment"]}, {physical["comment"]}")
        totalPlayers = fysNumb["p"] + fysNumb["m"] + fysNumb["n"]
        procentGoodFys = fysNumb["p"] / totalPlayers * 100
        procentGoodPhy = phyNumb["p"] / totalPlayers * 100
        procentMidFys = fysNumb["m"] / totalPlayers * 100
        procentMidPhy = phyNumb["m"] / totalPlayers * 100
        procentNegFys = fysNumb["n"] / totalPlayers * 100
        procentNegPhy = phyNumb["n"] / totalPlayers * 100

        list.append(f"Kropp: Bra:{procentGoodFys}, Medel:{procentMidFys}, Dåligt:{procentNegFys}")
        list.append(f"Knopp: Bra:{procentGoodPhy}, Medel:{procentMidPhy}, Dåligt:{procentNegPhy}")

        with open("reportCache", "w") as f:
            f.write("\n".joon(list))

        return "\n".join(list)

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
    with st. form("FORM"):
        code = st.text_input("Kod:")
        submit = st.form_submit_button("Enter")

    if submit:
        if not submit == "Admin":
            st.session_state._submitted_code = code
            st.session_state._process = True
        else:
            st.dialog("Skickat Mail!")
            send(get_body())
            print("sent")

if st.session_state.get("_process"):
    with open("codes.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        try:
            player_ID = data[st.session_state._submitted_code]  # String
            st.session_state.step = 2
        except:
            if not code == "":
                if code == "Admin":
                    send(get_body())
                else:
                    st.warning("Fel spelar kod")
                    time.sleep(1)
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