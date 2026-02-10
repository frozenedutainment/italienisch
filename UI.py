import streamlit as st
from streamlit_option_menu import option_menu

import random
import DataAnalysis
from DataAnalysis import data as D

import requests

API_KEY = "AIzaSyBJiYi763xqjhWbpdH3OSh59BVqctUZzo8"
#client = genai.Client(api_key=API_KEY)



class UI:
    def __init__(self):



        self.daten = D("words.txt")
        datadict = self.daten.decode()


    def spacer(self, height):
        st.container(height=height, border=False)
    def ToDo(self):
        client_id = '89i0N2BkLobORWlim8'
        client_secret = 'LANqksEof1Ru210fHNlKSS5wSqCtdMcx'
        redirect_uri = 'http://localhost:8501'
        username = 'FrozenEdutainment Studios'
        password = '17rateko'

        url = "https://api.ticktick.com/open/v1/project"
        headers = {"Authorization": "Bearer DEIN_ACCESS_TOKEN"}

        response = requests.get(url, headers=headers)
        print(response.json())

    def TrainingPage(self, mode):

        if "selectedVerb" not in st.session_state:
            st.session_state.selectedVerb = self.daten.VerbListe("all")[0]


        def handle_generate():

            selected_mode = st.session_state.radio_choice
            if selected_mode == "irregular":
                m = "irr"
            elif selected_mode == "regular":
                m = "reg"
            else:
                m = "all"

            # Verb generieren und DIREKT in den State schreiben
            st.session_state.selectedVerb = self.daten.getRandomWort(type="verb", mode=m)

            # Inputs zurücksetzen
            for key in list(st.session_state.keys()):
                if key.startswith("input_"):
                    st.session_state[key] = ""

        st.header("Konjugations Training", anchor="left")
        st.subheader("Generate known Verb", anchor="left")

        c1, c2, c3 = st.columns([3, 1, 1])

        with c1:
            # Wir geben dem Radio einen Key, damit der Callback darauf zugreifen kann
            st.radio("Random verb selector", ["irregular", "regular", "all"], key="radio_choice")
            # Der Button triggert nun den Callback
            st.button("Generate", on_click=handle_generate)

        with c2:
            st.text("or")

        with c3:
            # Die Selectbox nutzt direkt den Key "selectedVerb".
            # Keine manuelle Zuweisung (selectedVerb = ...) mehr nötig!
            st.selectbox("select a specific verb", self.daten.VerbListe("all"), key="selectedVerb")

        st.subheader("Konjugation", anchor="left")

        pronomen = self.daten.PronomenListe()
        for p in pronomen:
            cols = st.columns([1, 5])
            with cols[0]:
                st.markdown(f"<div style='padding-top: 10px; font-weight: bold;'>{p}</div>", unsafe_allow_html=True)
            with cols[1]:
                st.text_input(p, key=f"input_{p}", label_visibility="collapsed")

        Checker = st.button("Check")

        if Checker:
            if st.session_state.selectedVerb is None:
                st.warning("Bitte zuerst ein Verb generieren")
            else:
                all_correct = True
                for p in pronomen:
                    user_input = st.session_state[f"input_{p}"].strip().lower()
                    correct_val = self.daten.Konjugation(st.session_state.selectedVerb, p)

                    if user_input == correct_val:
                        st.success(f"Konjugation {p} richtig!")
                    else:
                        st.error(f"{p}: Falsch! (Richtig wäre: {correct_val})")
                        all_correct = False

                if all_correct:
                    self.daten.IncreaseRanking(st.session_state.selectedVerb, "verb", 2)
                    st.balloons()

    def MiniGamePage(self, mode="all"):
        st.header("Dein Italienisch-Mentor 🇮🇹")

        if "streak" not in st.session_state:
            st.session_state.streak = 0

        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center;'>🔥</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center;'>{st.session_state.streak}</h2>", unsafe_allow_html=True)

        with col2:
            # 1. Initialisierung
            if "selectedVerb" not in st.session_state:
                v = self.daten.getRandomWort(type="verb", mode=mode)
                p = random.choice(self.daten.PronomenListe())
                st.session_state.selectedVerb = v  # Das ist dein "increaser"
                st.session_state.selectedPronoun = p
                st.session_state.korrekt = self.daten.Konjugation(v, p)

                frage = f"Was ist **{v}** für **{p}**?"
                st.session_state.messages = [{"role": "assistant", "content": frage}]

            chat_container = st.container(height=500, border=True)

            with chat_container:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            if prompt := st.chat_input("Deine Antwort..."):
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Hier nutzen wir session_state.selectedVerb statt der lokalen Variable increaser
                if prompt.strip().lower() == st.session_state.korrekt.lower():
                    st.session_state.streak += 1
                    antwort_text = f"**Richtig!** 🎉 '{prompt}' ist korrekt."

                    # WICHTIG: session_state nutzen!
                    self.daten.IncreaseRanking(st.session_state.selectedVerb, "verb", 1)

                    if st.session_state.streak % 5 == 0:
                        st.balloons()
                else:
                    st.session_state.streak = 0
                    antwort_text = f"Leider falsch. Die richtige Antwort wäre **{st.session_state.korrekt}** gewesen."

                # Neue Runde vorbereiten
                v_neu = self.daten.getRandomWort(type="verb", mode=mode)
                p_neu = random.choice(self.daten.PronomenListe())

                # Werte für den nächsten Durchlauf im State speichern
                st.session_state.selectedVerb = v_neu
                st.session_state.selectedPronoun = p_neu
                st.session_state.korrekt = self.daten.Konjugation(v_neu, p_neu)

                naechste_frage = f"Nächste Runde: Was ist **{v_neu}** für **{p_neu}**?"
                st.session_state.messages.append({"role": "assistant", "content": antwort_text})
                st.session_state.messages.append({"role": "assistant", "content": naechste_frage})

                st.rerun()
        ######################################################################

    def LernenKonjugation(self):

        st.title("Konjugation regulärer Verben")
        self.spacer(25)

        table_style = """
            <style>
                .italy-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: 'sans-serif';
                    margin: 25px 0;
                    font-size: 1.1em;
                    box-shadow: 0 0 5px rgba(0, 0, 0, 0.05);
                }
                .italy-table th {
                    background-color: #ffffff;
                    color: #333;
                    text-align: left;
                    padding: 15px;
                    border-bottom: 2px solid #f0f0f0;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .italy-table td {
                    padding: 12px 15px;
                    border-bottom: 1px solid #f5f5f5;
                    color: #444;
                }
                .italy-table tr:hover {
                    background-color: #f9f9f9;
                }
                .highlight {
                    color: #d63384; /* Das Magenta/Pink aus deinem Bild */
                    font-weight: bold;
                }
                .stem {
                    color: #333;
                }
            </style>
            """

        # HTML Struktur der Tabelle
        html_table = """
            <table class="italy-table">
                <thead>
                    <tr>
                        <th></th>
                        <th>IMPAR<span class="highlight">ARE</span></th>
                        <th>SCRIV<span class="highlight">ERE</span></th>
                        <th>DORM<span class="highlight">IRE</span></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>io</b></td>
                        <td>impar<span class="highlight">o</span></td>
                        <td>scriv<span class="highlight">o</span></td>
                        <td>dorm<span class="highlight">o</span></td>
                    </tr>
                    <tr>
                        <td><b>tu</b></td>
                        <td>impar<span class="highlight">i</span></td>
                        <td>scriv<span class="highlight">i</span></td>
                        <td>dorm<span class="highlight">i</span></td>
                    </tr>
                    <tr>
                        <td><b>lui, lei</b></td>
                        <td>impar<span class="highlight">a</span></td>
                        <td>scriv<span class="highlight">e</span></td>
                        <td>dorm<span class="highlight">e</span></td>
                    </tr>
                    <tr>
                        <td><b>noi</b></td>
                        <td>impar<span class="highlight">iamo</span></td>
                        <td>scriv<span class="highlight">iamo</span></td>
                        <td>dorm<span class="highlight">iamo</span></td>
                    </tr>
                    <tr>
                        <td><b>voi</b></td>
                        <td>impar<span class="highlight">ate</span></td>
                        <td>scriv<span class="highlight">ete</span></td>
                        <td>dorm<span class="highlight">ite</span></td>
                    </tr>
                    <tr>
                        <td><b>loro</b></td>
                        <td>impar<span class="highlight">ano</span></td>
                        <td>scriv<span class="highlight">ono</span></td>
                        <td>dorm<span class="highlight">ono</span></td>
                    </tr>
                </tbody>
            </table>
            """

        # Beides zusammenfügen und anzeigen
        st.markdown(table_style + html_table, unsafe_allow_html=True)

        # Optional: Eine Info-Box für die visuelle Trennung
        st.info("Die Endungen der drei Verbgruppen (-are, -ere, -ire) sind farblich markiert.")
        st.divider()
        st.title("Konjugation für spezielle Verben")
        self.spacer(25)
        VerbSelektor = st.selectbox("VerbSelector", self.daten.VerbListe())

        self.spacer(25)
        with st.container(border = True):
            self.spacer(10)

            p = self.daten.PronomenListe()


            for n in p:
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"<div style='padding-top: 10px; font-size: 20px; font-weight: bold;'>{n}</div>", unsafe_allow_html=True)
                    self.spacer(15)

                with col2:
                    with st.container(border = True):
                        st.write(self.daten.Konjugation (VerbSelektor,n))

            self.spacer(10)






