import streamlit as st
from streamlit_option_menu import option_menu

import random
import DataAnalysis
from DataAnalysis import data as data

class Webiste:
    def __init__(self):



        self.daten = data("words.txt")
        datadict = self.daten.decode()
        st.sidebar.title("Mein Menü")
        from UI import UI as UI
        self.ui = UI()

        with st.sidebar:
            auswahl_italienisch = option_menu(
                menu_title="Italienisch",
                options=["Verben", "Abfrage", "Chat","Lernen","Satzbau"],
                menu_icon="translate",
                default_index=0,
            )
        #with st.sidebar:
        #    auswahl_ToDo = option_menu(
        #        menu_title="To-Dos",
        #        options=["To-Do", "Kalender", "Einkaufen", "Lernen"],
        #        menu_icon="translate",
        #        default_index=0,
        #    )
        ########################################################################
        if auswahl_italienisch == "Verben":

            sub_auswahl = option_menu(
                menu_title=None,
                options=["Mini-Game","Training", "Statistiken", "Wortliste"],
                icons=["play-fill", "graph-up", "list-ul"],
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"},
                }
            )

            if sub_auswahl == "Training":
                self.ui.TrainingPage("all")
            if sub_auswahl == "Mini-Game":
                self.ui.MiniGamePage("all")

        if auswahl_italienisch == "Lernen":
            self.ui.LernenKonjugation()

        if auswahl_italienisch == "Abfrage":
            self.ui.AbfragePage()

        if auswahl_italienisch == "Satzbau":
            self.ui.SatzbauSpiel()
        ######################################################################

Webiste()
