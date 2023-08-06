import pickle
import regex
import os
import sys

class Satzmetzger:
    def __init__(self):
        self.vorsichtmitdiesen = {}
        self.dictmitdomains = {}
        self.dictmitabkuerzungen = {}
        for alle in sys.path:
            if os.path.exists(alle + f"/satzmetzger/TOKEN_VORHER.PKL"):
                self.vorherchecken = self.read_pkl(alle + f"/satzmetzger/TOKEN_VORHER.PKL")
            if os.path.exists(alle + f"/satzmetzger/TOKEN_DOMAINSFINDEN.PKL"):
                self.domains = self.read_pkl(alle + f"/satzmetzger/TOKEN_DOMAINSFINDEN.PKL")
            if os.path.exists(alle + f"/satzmetzger/TOKEN_REGEXABKUERZUNGEN.PKL"):
                self.abkuerzungen = self.read_pkl(alle + f"/satzmetzger/TOKEN_REGEXABKUERZUNGEN.PKL")
            if os.path.exists(alle + f"/satzmetzger/TOKEN_DATEIENDUNGEN_IGNORECASE.PKL"):
                self.dateiendungen = self.read_pkl(alle + f"/satzmetzger/TOKEN_DATEIENDUNGEN_IGNORECASE.PKL")

        
    def zerhack_den_text(self, text, debug=False):
        """
        :type text: str
        Example:
        from satzmetzger import Satzmetzger
        losgehts = Satzmetzger()
        textzumsplitten ='''Hallo, ich bin ein Text. Zerhack mich bitte! Ich halte es nicht mehr aus. Wenn du mich bis zum 23.04. nicht zerhackst, rufe ich Papst
        Hackerpeter X. an und schicke ihm das Dokument erhatmichnichtzerhackt.docx, er wird z. B. sehr böse auf dich sein! Darauf kannst du einen lassen!'''
        textfertig = losgehts.zerhack_den_text(textzumsplitten, debug=False)
        for indi, zerhacktersatz in enumerate(textfertig):
            print(indi, end='\t\t')
            print(zerhacktersatz)

        output:
        0		Hallo, ich bin ein Text.
        1		Zerhack mich bitte!
        2		Ich halte es nicht mehr aus.
        3		Wenn du mich bis zum 23.04. nicht zerhackst, rufe ich Papst Hackerpeter X. an und schicke ihm das Dokument erhatmichnichtzerhackt.docx, er wird z. B. sehr böse auf dich sein!
        4		Darauf kannst du einen lassen!
            """
        if debug is True:
            self.checktextlaenge(text)

        text = self._gefaehrliche_woerter_satzende_checken(text)
        if debug is True:
            self.checktextlaenge(text)
        text = self._internetkram_zurechtbiegen(text)
        if debug is True:
            self.checktextlaenge(text)

        text = self._mfg_mit_freundlichen_gruessen(text)
        if debug is True:
            self.checktextlaenge(text)

        text = self._dateiendungenfiltern(text)
        if debug is True:
            self.checktextlaenge(text)

        text = self._zahlen_leerzeichen_roemisch(text)
        if debug is True:
            self.checktextlaenge(text)

        text = self._satz_satzzeichen_zusammenfuegen(text, debug=debug)
        if debug is True:
            self.checktextlaenge(text)

        text = self._vertrauen_ist_gut_kontrolle_besser(text)
        if debug is True:
            self.checktextlaenge(text)

        text = self._indirekte_rede(text)
        if debug is True:
            self.checktextlaenge(text)

        text = self._indirekte_rede_klammer_korrigieren_anfang(text)
        if debug is True:
            self.checktextlaenge(text)

        text = self._indirekte_rede_klammer_korrigieren_ende(text)
        if debug is True:
            self.checktextlaenge(text)
        self.vorsichtmitdiesen = {}
        self.dictmitdomains = {}
        self.dictmitabkuerzungen = {}
        return text.copy()

    def checktextlaenge(self, t1):
        if isinstance(t1, list):
            t1 = "".join(t1)
        t1 = regex.sub(r"\s+", "", t1)
        print(f"Textlaenge: {len(t1)}")

    def read_pkl(self, filename):
        with open(filename, "rb") as f:
            data_pickle = pickle.load(f)
        return data_pickle

    def _gefaehrliche_woerter_satzende_checken(self, texts):

        for wort in self.vorherchecken.findall(texts):
            ersetzen = regex.sub(r"\.+", "p@u@n@k@t", wort)
            ersetzen = regex.sub(r"\?+", "f@r@a@g@e@z@e@i@c@h@e@n", ersetzen)
            ersetzen = regex.sub(r"\!+", "a@u@s@r@u@f@e@z@e@i@c@h@e@n", ersetzen)
            self.vorsichtmitdiesen[wort] = ersetzen

        for v, k in self.vorsichtmitdiesen.items():
            texts = texts.replace(v, k)
        return texts

    def _internetkram_zurechtbiegen(self, texts):
        for domain in self.domains.findall(texts):
            ersetzen = regex.sub(r"\.+", "Ç", domain)
            self.dictmitdomains[domain] = ersetzen
        for v, k in self.dictmitdomains.items():
            texts = texts.replace(v, k)
        return texts

    def _mfg_mit_freundlichen_gruessen(self, texts):
        for abk in self.abkuerzungen.findall(texts):
            ersetzen = regex.sub(r"\.+", "Ç", abk)
            self.dictmitabkuerzungen[abk] = ersetzen
        for v, k in self.dictmitabkuerzungen.items():
            texts = texts.replace(v, k)
        return texts

    def _dateiendungenfiltern(self, texts):
        for abk in self.dateiendungen.findall(texts):
            ersetzen = regex.sub(r"\.+", "Ç", abk)
            self.dictmitabkuerzungen[abk] = ersetzen
        for v, k in self.dictmitabkuerzungen.items():
            texts = texts.replace(v, k)
        return texts

    def _zahlen_leerzeichen_roemisch(self, texts):
        texts = regex.sub(r"(\d\s*)\.", "\g<1>Ç", texts)
        texts = regex.sub(r"([IVXLCDM]\s*)\.", "\g<1>Ç", texts)
        texts = regex.sub(r"p@u@n@k@t", ".", texts)
        texts = regex.sub(r"f@r@a@g@e@z@e@i@c@h@e@n", "?", texts)
        texts = regex.sub(r"a@u@s@r@u@f@e@z@e@i@c@h@e@n", "!", texts)
        texts2 = regex.sub(r"[\r\t\n\v\s]+", " ", texts)
        texts2 = regex.split(r"""([.?!]+\s*["“‘‹«]*)""", texts2)
        return texts2.copy()

    def _satz_satzzeichen_zusammenfuegen(self, texts, debug=False):
        zusammengefuegt = []
        for indexi, satz in enumerate(texts):
            faengtmitsatzzeichenan = regex.findall(r"^\s*\)?\]?[?.!].*", satz)
            if any(faengtmitsatzzeichenan):
                continue
            if not any(faengtmitsatzzeichenan):
                hinzufuegen = satz.strip()
                for xxx in range(1, 10, 1):
                    try:
                        faengtmitsatzzeichenanx = regex.findall(
                            r"^\s*\)?\]?[?.!].*", texts[indexi + xxx]
                        )
                        if any(faengtmitsatzzeichenanx):
                            hinzufuegen = (
                                hinzufuegen.strip() + faengtmitsatzzeichenanx[0].strip()
                            )
                        if not any(faengtmitsatzzeichenanx):
                            zusammengefuegt.append(hinzufuegen)
                            break
                    except Exception as Fehler:
                        if debug is True:
                            print(Fehler)
                        zusammengefuegt.append(hinzufuegen)
                        break
        letzteliste = []
        for saetze in zusammengefuegt:
            if len(saetze) > 0:
                letzteliste.append(regex.sub("Ç", ".", saetze))
        return letzteliste.copy()

    def _vertrauen_ist_gut_kontrolle_besser(self, texts):
        allerletztekorrektur = []
        for indexi, letzte in enumerate(texts):
            satznochmal = letzte.strip()
            satzzeichenamanfang = regex.findall(r'^[\)\(\[\]\s.?!"“‘‹«]+$', satznochmal)
            if any(satzzeichenamanfang):
                continue
            satzzeichenamende = regex.findall(r"""([.?!]+\s*["“‘‹«]*)$""", satznochmal)
            if any(satzzeichenamende):
                allerletztekorrektur.append(satznochmal)
                continue
            try:
                faengtmitsatzzeichenanx = regex.findall(
                    r'^[\)\(\[\]\s.?!"“‘‹«]+$', texts[indexi + 1]
                )
                if any(faengtmitsatzzeichenanx):
                    allerletztekorrektur.append(satznochmal + texts[indexi + 1])

            except:
                allerletztekorrektur.append(satznochmal)
        return allerletztekorrektur.copy()

    def _indirekte_rede(self, texts):
        allerletztekorrektur = []
        for indexi, letzte in enumerate(texts):
            satznochmal = letzte.strip()
            satzzeichenamanfang = regex.findall(r"^[,;].*$", satznochmal)
            if any(satzzeichenamanfang):
                continue
            try:
                faengtmitsatzzeichenanx = regex.findall(r"^[,;].*$", texts[indexi + 1])
                if any(faengtmitsatzzeichenanx):
                    allerletztekorrektur.append(satznochmal + texts[indexi + 1])
                elif not any(faengtmitsatzzeichenanx):
                    allerletztekorrektur.append(satznochmal)
            except:
                allerletztekorrektur.append(satznochmal)
        return allerletztekorrektur.copy()

    def _indirekte_rede_klammer_korrigieren_anfang(self, texts):
        allerletztekorrektur = []
        for indexi, letzte in enumerate(texts):
            satznochmal = letzte.strip()
            satzzeichenamanfang = regex.findall(r"""[»"„‚›\(\[\{]+""", satznochmal)
            if not any(satzzeichenamanfang):
                allerletztekorrektur.append(satznochmal)
            if any(satzzeichenamanfang):
                satzzeichenamende = regex.findall(r"""["“‘‹«\)\]\}]""", satznochmal)
                if any(satzzeichenamende):
                    allerletztekorrektur.append(satznochmal)
                if not any(satzzeichenamende):
                    satznochmal = regex.sub(r"""[»"„‚›\(\[\{]+""", "", satznochmal)
                    allerletztekorrektur.append(satznochmal)
        return allerletztekorrektur.copy()

    def _indirekte_rede_klammer_korrigieren_ende(self, texts):
        allerletztekorrektur = []
        for indexi, letzte in enumerate(texts):
            satznochmal = letzte.strip()
            satzzeichenamende = regex.findall(r"""["“‘‹«\)\]\}]""", satznochmal)
            if not any(satzzeichenamende):
                allerletztekorrektur.append(satznochmal)
            if any(satzzeichenamende):
                satzzeichenamanfang = regex.findall(r"""^[»"„‚›\(\[\{]+""", satznochmal)
                if any(satzzeichenamanfang):
                    allerletztekorrektur.append(satznochmal)
                if not any(satzzeichenamanfang):
                    satznochmal = regex.sub(r"""["“‘‹«\)\]\}]""", "", satznochmal)
                    allerletztekorrektur.append(satznochmal)
        return allerletztekorrektur.copy()
