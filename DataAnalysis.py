from http.cookiejar import cut_port_re
from logging import raiseExceptions

import streamlit as st
from streamlit_option_menu import option_menu

import random

API_KEY = "AIzaSyBJiYi763xqjhWbpdH3OSh59BVqctUZzo8"
#client = genai.Client(api_key=API_KEY)


class data:
    def __init__(self,filename):

        self.filename = filename

    def opendata(self):

        with (open(self.filename, "r", encoding="utf-8") as f):

            vocab = f.read()
            return vocab


    def decode(self):

        self.type = ["wort", "idiom", "verb"]
        self.words = self.opendata()

        self.dictionary = {}
        lines = self.words.split("\n")

        for n in lines:
            if n == "###":
                break
            if not n.strip():
                continue

            self.splitted = n.split(",")
            splitted = self.splitted


            if "wort" in splitted or "Idiom" in splitted:
                wort = splitted[0].split(":")
                try:
                    if wort[0] not in self.dictionary:
                        self.dictionary[wort[0]] = {"Übersetzung": wort[1], "Type": splitted[1], "Rating": splitted[2]}
                except IndexError:
                    raise IndexError("Format bei wort/Idiom falsch")


            elif "verb" in splitted:
                wort = splitted[0].split(":")
                try:
                    konjugation = splitted[2]
                    konsplit = konjugation.split("*")

                    if wort[0] not in self.dictionary:
                        self.dictionary[wort[0]] = {
                            "Übersetzung": wort[1],
                            "Type": splitted[1],
                            "Verb_Typ" : splitted[3],
                            "Konjugation": {
                                "io": konsplit[0],
                                "tu": konsplit[1],
                                "lui/lei": konsplit[2],
                                "noi": konsplit[3],
                                "voi": konsplit[4],
                                "loro": konsplit[5],
                                "inf": konsplit[6]
                            },
                            "Rating" : splitted[4]
                        }
                except IndexError:
                    raise IndexError("Format bei verb (Konjugation) falsch", wort)

        return self.dictionary

    def Konjugation(self, verb, Pronomen):
        try:
            trywort = self.dictionary[verb]

            if trywort["Type"] != "verb":
                raise TypeError



            Konjugiert = self.dictionary[verb]["Konjugation"][Pronomen]
            return Konjugiert


        except:
            print("did not work")

    def VerbListe(self, mode = "all"):

        allowedmodes = ["all", "reg", "irr"]

        if mode not in allowedmodes:
            print("pls type in valid mode")

        VerbListe = []

        if mode == "all":
            for n in self.dictionary:
                if self.dictionary[n]["Type"] == "verb":
                    VerbListe.append(self.Konjugation(n, "inf"))


        elif mode == "irr":
            for n in self.dictionary:
                if self.dictionary[n]["Type"] == "verb":
                    if self.dictionary[n]["Verb_Typ"] == "irregular":
                        VerbListe.append(self.Konjugation(n, "inf"))



        elif mode == "reg":
            for n in self.dictionary:
                if self.dictionary[n]["Type"] == "verb":
                    if self.dictionary[n]["Verb_Typ"] == "regular":
                        VerbListe.append(self.Konjugation(n, "inf"))

        return VerbListe

    def PronomenListe(self):
        PronomenListe = ["io", "tu", "lui/lei", "noi", "voi", "loro"]
        return PronomenListe

    def ChangeStat(self, wort, type, var, new_value):

        neue_zeilen = []


        with open(self.filename, 'r', encoding='utf-8') as file:
            zeilen = file.readlines()


        for zeile in zeilen:
            if zeile.startswith(f"{wort}:"):
                parts = zeile.strip().split(',')


                try:
                    if type == "verb":
                        HashWort = {"Übersetzung" : parts[0], "Type" : parts[1], "Konjugation" : parts[2], "Verb_Typ" : parts[3], "Rating" : parts[4]}
                    else:
                        HashWort = {"Übersetzung": parts[0], "Type": parts[1], "Rating": parts[2]}
                except IndexError:
                    print("etwas hat nicht geklappt")

                if var in HashWort:
                    HashWort[var] = new_value
                    grr = HashWort.values()
                    neue_zeile = ",".join(HashWort.values()) + "\n"
                    neue_zeilen.append(neue_zeile)
                    print(neue_zeile)
            else:
                neue_zeilen.append(zeile)

        with open(self.filename, 'w', encoding='utf-8') as file:
            file.writelines(neue_zeilen)










    def IncreaseRanking(self, wort, type, value):
        if wort not in self.dictionary:
            print("Falsches Wort")
            return None
        else:
            currentranking = int(self.dictionary[wort]["Rating"])
            currentranking += value
            self.dictionary[wort]["Rating"] = currentranking
            try:
                self.ChangeStat( wort, type, "Rating", str(currentranking))
                return True
            except:
                "check input"
                return False
    def getRandomWort(self, type = "all", mode = "all"):
        r = 0
        Formel = 1/(2**r)
        OutputList = []

        if mode not in ["all", "irr", "reg"]:
            print("pls type in valid mode")

        if type not in self.type:
            print("pls type in valid type")#

        if type == "verb":
            self.all_verbs = self.VerbListe(mode = mode)
            for n in self.all_verbs:
                r = int(self.dictionary[n]["Rating"])
                prob = 1/(2**r)
                prop_tup = (n, prob)
                OutputList.append(prop_tup)

        worte, gewichte = zip(*OutputList)
        auswahl = random.choices(worte, weights=gewichte, k=1)[0]

        return auswahl













d = data("words.txt")
d.decode()
d.VerbListe("irr")
print(d.getRandomWort(type = "verb", mode = "all"))


