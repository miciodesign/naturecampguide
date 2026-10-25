#!/usr/bin/env python3
"""Genera il sito statico NaturCamp Guide in tre lingue.

Uso:  python3 build.py
Legge data/campeggi.json e src/, scrive index.html, it/, en/, de/, assets/.
"""
import json, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data" / "campeggi.json").read_text(encoding="utf-8"))
BEACHES = json.loads((ROOT / "data" / "spiagge.json").read_text(encoding="utf-8"))
SITE = "https://naturcampguide.com"
LANGS = ["it", "en", "de"]

# ---------------------------------------------------------------- testi
T = {
  "it": {
    "brand_sub": "Guide", "lang_name": "Italiano",
    "nav": {"camps": "Campeggi", "beaches": "Spiagge", "pack": "Cosa portare", "review": "Scrivi una recensione", "about": "Chi siamo", "assoc": "Associazioni"},
    "paths": {"camps": "campeggi", "beaches": "spiagge", "pack": "cosa-portare", "review": "recensioni", "about": "chi-siamo", "assoc": "associazioni"},
    "assoc_h1": "Associazioni naturiste in Europa", "assoc_p": "Le principali federazioni che promuovono e tutelano il naturismo, paese per paese. Attraverso queste organizzazioni puoi trovare campeggi affiliati, tessere riconosciute a livello internazionale e informazioni aggiornate sulle spiagge.",
    "assoc_int_h2": "Organizzazioni internazionali", "assoc_nat_h2": "Federazioni nazionali",
    "assoc_website": "Sito ufficiale", "assoc_members": "Soci affiliati",
    "assoc_home_h2": "Associazioni naturiste", "assoc_home_p": "Le federazioni europee che rilasciano tessere e gestiscono campeggi affiliati.",
    "assoc_home_cta": "Tutte le associazioni",
    "beaches_h1": "Spiagge naturiste", "beaches_p": "Ufficiali e tollerate, ordinate per paese. Il numero è il voto complessivo su 5.",
    "beaches_home_h2": "Spiagge naturiste", "beaches_home_p": "Dove si può stare nudi in spiaggia, con stato ufficiale, accesso e servizi verificati.",
    "beaches_all": "Tutte le spiagge",
    "map_h2": "Dove siamo", "map_p": "Tutti i campeggi (🏕) e le spiagge (🏖) naturiste in mappa. Clicca su un segnaposto per aprire la scheda.",
    "europe_h2": "Tutta Europa", "europe_p": "Tutti i posti nella guida, per paese. Le schede complete hanno il voto; gli altri sono in preparazione.",
    "europe_camps": "Campeggi", "europe_beaches": "Spiagge", "europe_soon": "scheda in arrivo",
    "news_h2": "Novità", "news_all": "Tutte le novità",
    "weather_h2": "Meteo nelle zone naturiste", "weather_p": "Prima di partire controlla le previsioni locali.",
    "weather_check": "Previsioni",
    "weather_zones": [
      {"name": "Istria (Croazia)", "lat": 45.14, "lon": 13.62},
      {"name": "Landes (Francia)", "lat": 43.93, "lon": -1.35},
      {"name": "Ravenna (Italia)", "lat": 44.39, "lon": 12.20},
      {"name": "Algarve (Portogallo)", "lat": 37.10, "lon": -8.67},
    ],
    "weather_link": "Vedi il meteo vicino a",
    "bfacts": {"status": "Stato", "ground": "Fondo e fondale", "length": "Lunghezza", "access": "Accesso", "services": "Servizi", "season": "Periodo", "coords": "Coordinate", "nearby": "Campeggi vicini"},
    "status": {"official": "ufficiale, segnalata con cartelli", "tolerated": "tollerata, non segnalata", "unofficial": "non ufficiale: possibili controlli"},
    "status_short": {"official": "ufficiale", "tolerated": "tollerata", "unofficial": "non ufficiale"},
    "bcriteria": {"setting": "Natura e paesaggio", "clean": "Pulizia", "access": "Facilità di accesso", "services": "Servizi", "atmosphere": "Atmosfera e tranquillità", "crowd": "Spazio e affollamento"},
    "status_note": "Lo stato può cambiare: ordinanze comunali e stagioni balneari variano ogni anno. Verifica i cartelli sul posto.",
    "title": "NaturCamp Guide — campeggi naturisti in Europa",
    "desc": "Guida indipendente ai campeggi naturisti e nudisti in Europa: schede verificate, voti su sette criteri, recensioni oneste in italiano, inglese e tedesco.",
    "hero_h1": "Campeggi naturisti in Europa, raccontati con onestà",
    "hero_p": "Schede verificate di persona, sette criteri di voto, e per ogni posto una risposta chiara: per chi è, per chi no.",
    "hero_cta": "Vedi i campeggi", "hero_cta2": "Come votiamo",
    "countries_h2": "Scegli un paese",
    "latest_h2": "Ultime schede",
    "how_h2": "Come votiamo",
    "how_p": "Ogni campeggio riceve un voto da 1 a 5 su sette criteri, sempre motivato con un fatto concreto. Il voto complessivo è la media. Indichiamo sempre quando siamo stati sul posto, perché prezzi e servizi cambiano ogni stagione.",
    "camps_h1": "Tutti i campeggi", "camps_p": "Ordinati per paese. Il numero è il voto complessivo su 5.",
    "count": "{n} schede",
    "facts_h2": "Dati essenziali", "criteria_h2": "I nostri voti", "verdict_h2": "Il nostro giudizio",
    "facts": {"region": "Regione", "season": "Stagione", "price": "Prezzo indicativo", "price_note": "piazzola per 2 persone, alta stagione, a notte", "affiliation": "Affiliazione", "card": "Tessera naturista", "type": "Tipo", "accommodation": "Sistemazioni", "website": "Sito ufficiale", "visited": "Visitato"},
    "card": {"yes": "richiesta", "no": "non richiesta", "recommended": "consigliata"},
    "criteria": {"clean": "Pulizia e manutenzione", "location": "Posizione e natura", "facilities": "Servizi", "atmosphere": "Atmosfera e rispetto delle regole", "family": "Adatto alle famiglie", "beginner": "Adatto ai principianti", "value": "Rapporto qualità-prezzo"},
    "overall": "voto", "strengths": "Punti forti", "weaknesses": "Punti deboli", "for": "Per chi è", "not_for": "Per chi no", "tip": "Consiglio pratico",
    "demo": "Scheda dimostrativa: dati inventati per mostrare il formato. Le schede reali riportano solo informazioni verificate.",
    "verified": "Verificato da fonti", "stay_h2": "Dove dormire nelle vicinanze", "stay_p": "Hotel e appartamenti vicino a questo posto. Se prenoti da qui, riceviamo una piccola commissione senza costi per te: è così che la guida resta gratuita e senza pubblicità.", "price_na": "non pubblicato: chiedere al campeggio", "sources_h2": "Fonti", "desk_note": "Scheda compilata da sito ufficiale e recensioni pubbliche, non da una visita: i voti riflettono quanto documentato alla data indicata. Hai informazioni più recenti? Scrivi una recensione.",
    "review_h1": "Scrivi una recensione", "review_p": "Ci sei stato? Racconta com'è andata. Le recensioni vengono lette prima della pubblicazione e restano anonime: il cognome e l'e-mail non vengono mai mostrati.",
    "f": {"camp": "Campeggio o spiaggia", "camp_other": "Altro (scrivilo nel testo)", "name": "Nome o nickname", "email": "E-mail (non pubblicata)", "when": "Mese e anno del soggiorno", "trip": "Tipo di viaggio", "trips": ["Coppia", "Famiglia", "Da solo/a", "Gruppo"], "acc": "Sistemazione usata", "ratings": "I tuoi voti (1–5)", "text": "La tua recensione (almeno 300 caratteri)", "tip": "Consigli pratici (facoltativo)", "consent": "Ho letto le regole e accetto che la recensione venga pubblicata con il mio nickname.", "send": "Invia la recensione"},
    "rules_h3": "Regole in breve",
    "rules": ["Solo esperienze dirette, con mese e anno del soggiorno.", "Niente contenuti sessuali o allusivi, niente descrizioni di altri ospiti.", "Le critiche sono benvenute se concrete; il gestore può rispondere.", "Niente foto con persone riconoscibili."],
    "about_h1": "Chi siamo", "about_p1": "NaturCamp Guide è una guida indipendente ai campeggi naturisti e nudisti in Europa, scritta in italiano, inglese e tedesco. Non siamo un'agenzia e non vendiamo soggiorni: raccontiamo i posti come li abbiamo trovati.", "about_p2": "Ogni scheda nasce da una visita o da fonti verificate con data. Se un campeggio ci sembra deludente lo scriviamo; se è eccellente anche.", "about_p3": "Hai una correzione o un campeggio da segnalare? Scrivici: ",
    "footer": "Guida indipendente ai campeggi naturisti in Europa.", "privacy": "Privacy", "contact": "Contatti",
    "country_names": {"IT": "Italia", "FR": "Francia", "ES": "Spagna", "HR": "Croazia", "DE": "Germania", "AT": "Austria", "PT": "Portogallo", "NL": "Paesi Bassi", "GR": "Grecia", "SI": "Slovenia"},
  },
  "en": {
    "brand_sub": "Guide", "lang_name": "English",
    "nav": {"camps": "Campsites", "beaches": "Beaches", "pack": "What to pack", "review": "Write a review", "about": "About", "assoc": "Associations"},
    "paths": {"camps": "campsites", "beaches": "beaches", "pack": "what-to-pack", "review": "reviews", "about": "about", "assoc": "associations"},
    "assoc_h1": "Naturist associations in Europe", "assoc_p": "The main federations that promote and protect naturism, country by country. Through these organisations you can find affiliated campsites, internationally recognised membership cards and up-to-date information on beaches.",
    "assoc_int_h2": "International organisations", "assoc_nat_h2": "National federations",
    "assoc_website": "Official website", "assoc_members": "Affiliated members",
    "assoc_home_h2": "Naturist associations", "assoc_home_p": "European federations that issue membership cards and manage affiliated campsites.",
    "assoc_home_cta": "All associations",
    "beaches_h1": "Naturist beaches", "beaches_p": "Official and tolerated, sorted by country. The number is the overall score out of 5.",
    "beaches_home_h2": "Naturist beaches", "beaches_home_p": "Where you can be nude on the beach, with official status, access and services checked.",
    "beaches_all": "All beaches",
    "map_h2": "Where we are", "map_p": "All naturist campsites (🏕) and beaches (🏖) on the map. Click a pin to open the listing.",
    "europe_h2": "All of Europe", "europe_p": "Every place in the guide, by country. Listings with a score are complete; others are in preparation.",
    "europe_camps": "Campsites", "europe_beaches": "Beaches", "europe_soon": "listing coming soon",
    "news_h2": "News", "news_all": "All news",
    "weather_h2": "Weather in naturist areas", "weather_p": "Check the local forecast before you set off.",
    "weather_check": "Forecast",
    "weather_zones": [
      {"name": "Istria (Croatia)", "lat": 45.14, "lon": 13.62},
      {"name": "Landes (France)", "lat": 43.93, "lon": -1.35},
      {"name": "Ravenna (Italy)", "lat": 44.39, "lon": 12.20},
      {"name": "Algarve (Portugal)", "lat": 37.10, "lon": -8.67},
    ],
    "weather_link": "See weather near",
    "bfacts": {"status": "Status", "ground": "Ground and seabed", "length": "Length", "access": "Access", "services": "Services", "season": "Season", "coords": "Coordinates", "nearby": "Campsites nearby"},
    "status": {"official": "official, signposted", "tolerated": "tolerated, not signposted", "unofficial": "unofficial: checks possible"},
    "status_short": {"official": "official", "tolerated": "tolerated", "unofficial": "unofficial"},
    "bcriteria": {"setting": "Nature and scenery", "clean": "Cleanliness", "access": "Ease of access", "services": "Services", "atmosphere": "Atmosphere and peace", "crowd": "Space and crowds"},
    "status_note": "Status can change: municipal rules and bathing seasons vary every year. Check the signs on site.",
    "title": "NaturCamp Guide — naturist campsites in Europe",
    "desc": "Independent guide to naturist and nudist campsites in Europe: verified listings, seven-criteria ratings and honest reviews in English, Italian and German.",
    "hero_h1": "Naturist campsites in Europe, told honestly",
    "hero_p": "Listings checked in person, seven rating criteria, and for every place a clear answer: who it's for, who should skip it.",
    "hero_cta": "See the campsites", "hero_cta2": "How we rate",
    "countries_h2": "Pick a country",
    "latest_h2": "Latest reviews",
    "how_h2": "How we rate",
    "how_p": "Every campsite gets a score from 1 to 5 on seven criteria, each backed by a concrete fact. The overall score is the average. We always say when we were there, because prices and facilities change every season.",
    "camps_h1": "All campsites", "camps_p": "Sorted by country. The number is the overall score out of 5.",
    "count": "{n} listings",
    "facts_h2": "Key facts", "criteria_h2": "Our scores", "verdict_h2": "Our verdict",
    "facts": {"region": "Region", "season": "Season", "price": "Indicative price", "price_note": "pitch for 2 people, high season, per night", "affiliation": "Affiliation", "card": "Naturist card", "type": "Type", "accommodation": "Accommodation", "website": "Official website", "visited": "Visited"},
    "card": {"yes": "required", "no": "not required", "recommended": "recommended"},
    "criteria": {"clean": "Cleanliness and upkeep", "location": "Location and nature", "facilities": "Facilities", "atmosphere": "Atmosphere and respect for the rules", "family": "Family-friendly", "beginner": "Beginner-friendly", "value": "Value for money"},
    "overall": "score", "strengths": "Strengths", "weaknesses": "Weaknesses", "for": "Who it's for", "not_for": "Who should skip it", "tip": "Practical tip",
    "demo": "Sample listing: invented data to show the format. Real listings contain verified information only.",
    "verified": "Verified from sources", "stay_h2": "Where to stay nearby", "stay_p": "Hotels and apartments near this place. If you book from here we earn a small commission at no cost to you: that is how the guide stays free and ad-free.", "price_na": "not published: ask the campsite", "sources_h2": "Sources", "desk_note": "Listing compiled from the official website and public reviews, not from a visit: the scores reflect what was documented on the date shown. Have more recent information? Write a review.",
    "review_h1": "Write a review", "review_p": "Been there? Tell us how it went. Reviews are read before publication and stay anonymous: your surname and e-mail are never shown.",
    "f": {"camp": "Campsite or beach", "camp_other": "Other (name it in the text)", "name": "Name or nickname", "email": "E-mail (not published)", "when": "Month and year of your stay", "trip": "Type of trip", "trips": ["Couple", "Family", "Solo", "Group"], "acc": "Accommodation used", "ratings": "Your scores (1–5)", "text": "Your review (at least 300 characters)", "tip": "Practical tips (optional)", "consent": "I have read the rules and agree to have my review published under my nickname.", "send": "Send review"},
    "rules_h3": "Rules in short",
    "rules": ["First-hand experiences only, with month and year of the stay.", "No sexual or suggestive content, no descriptions of other guests.", "Criticism is welcome when concrete; the owner may reply.", "No photos with recognisable people."],
    "about_h1": "About", "about_p1": "NaturCamp Guide is an independent guide to naturist and nudist campsites in Europe, written in English, Italian and German. We are not an agency and we don't sell holidays: we describe places as we found them.", "about_p2": "Every listing comes from a visit or from dated, verified sources. If a campsite disappoints we say so; if it is excellent, we say that too.", "about_p3": "Have a correction or a campsite to suggest? Write to us: ",
    "footer": "Independent guide to naturist campsites in Europe.", "privacy": "Privacy", "contact": "Contact",
    "country_names": {"IT": "Italy", "FR": "France", "ES": "Spain", "HR": "Croatia", "DE": "Germany", "AT": "Austria", "PT": "Portugal", "NL": "Netherlands", "GR": "Greece", "SI": "Slovenia"},
  },
  "de": {
    "brand_sub": "Guide", "lang_name": "Deutsch",
    "nav": {"camps": "Campingplätze", "beaches": "Strände", "pack": "Packliste", "review": "Bewertung schreiben", "about": "Über uns", "assoc": "Verbände"},
    "paths": {"camps": "campingplaetze", "beaches": "straende", "pack": "packliste", "review": "bewertungen", "about": "ueber-uns", "assoc": "verbaende"},
    "assoc_h1": "Naturistenverbände in Europa", "assoc_p": "Die wichtigsten Verbände, die den Naturismus fördern und schützen, Land für Land. Über diese Organisationen finden Sie angeschlossene Campingplätze, international anerkannte Mitgliedsausweise und aktuelle Informationen zu Stränden.",
    "assoc_int_h2": "Internationale Organisationen", "assoc_nat_h2": "Nationale Verbände",
    "assoc_website": "Offizielle Website", "assoc_members": "Angeschlossene Mitglieder",
    "assoc_home_h2": "Naturistenverbände", "assoc_home_p": "Europäische Verbände, die Ausweise ausstellen und angeschlossene Campingplätze verwalten.",
    "assoc_home_cta": "Alle Verbände",
    "beaches_h1": "FKK-Strände", "beaches_p": "Offiziell und geduldet, nach Land sortiert. Die Zahl ist die Gesamtnote von 5.",
    "beaches_home_h2": "FKK-Strände", "beaches_home_p": "Wo man nackt am Strand sein darf, mit geprüftem Status, Zugang und Ausstattung.",
    "beaches_all": "Alle Strände",
    "map_h2": "Wo wir sind", "map_p": "Alle FKK-Campingplätze (🏕) und Strände (🏖) auf der Karte. Auf einen Marker klicken, um den Eintrag zu öffnen.",
    "europe_h2": "Ganz Europa", "europe_p": "Alle Orte im Führer, nach Land. Einträge mit Note sind fertig; andere sind in Vorbereitung.",
    "europe_camps": "Campingplätze", "europe_beaches": "Strände", "europe_soon": "Eintrag folgt",
    "news_h2": "Neuigkeiten", "news_all": "Alle Neuigkeiten",
    "weather_h2": "Wetter in FKK-Gebieten", "weather_p": "Lokale Vorhersage vor der Abreise prüfen.",
    "weather_check": "Vorhersage",
    "weather_zones": [
      {"name": "Istrien (Kroatien)", "lat": 45.14, "lon": 13.62},
      {"name": "Landes (Frankreich)", "lat": 43.93, "lon": -1.35},
      {"name": "Ravenna (Italien)", "lat": 44.39, "lon": 12.20},
      {"name": "Algarve (Portugal)", "lat": 37.10, "lon": -8.67},
    ],
    "weather_link": "Wetter bei",
    "bfacts": {"status": "Status", "ground": "Untergrund und Wasser", "length": "Länge", "access": "Zugang", "services": "Ausstattung", "season": "Zeitraum", "coords": "Koordinaten", "nearby": "Campingplätze in der Nähe"},
    "status": {"official": "offiziell, ausgeschildert", "tolerated": "geduldet, nicht ausgeschildert", "unofficial": "inoffiziell: Kontrollen möglich"},
    "status_short": {"official": "offiziell", "tolerated": "geduldet", "unofficial": "inoffiziell"},
    "bcriteria": {"setting": "Natur und Landschaft", "clean": "Sauberkeit", "access": "Zugänglichkeit", "services": "Ausstattung", "atmosphere": "Atmosphäre und Ruhe", "crowd": "Platz und Andrang"},
    "status_note": "Der Status kann sich ändern: Gemeindeverordnungen und Badesaisons variieren jedes Jahr. Beschilderung vor Ort beachten.",
    "title": "NaturCamp Guide — FKK-Campingplätze in Europa",
    "desc": "Unabhängiger Führer zu FKK- und Naturisten-Campingplätzen in Europa: geprüfte Einträge, Bewertung nach sieben Kriterien, ehrliche Erfahrungsberichte auf Deutsch, Englisch und Italienisch.",
    "hero_h1": "FKK-Campingplätze in Europa, ehrlich beschrieben",
    "hero_p": "Vor Ort geprüfte Einträge, sieben Bewertungskriterien und für jeden Platz eine klare Antwort: für wen er passt, für wen nicht.",
    "hero_cta": "Zu den Campingplätzen", "hero_cta2": "So bewerten wir",
    "countries_h2": "Land wählen",
    "latest_h2": "Neueste Bewertungen",
    "how_h2": "So bewerten wir",
    "how_p": "Jeder Platz bekommt eine Note von 1 bis 5 in sieben Kriterien, jede mit einem konkreten Fakt begründet. Die Gesamtnote ist der Durchschnitt. Wir nennen immer, wann wir dort waren, denn Preise und Ausstattung ändern sich jede Saison.",
    "camps_h1": "Alle Campingplätze", "camps_p": "Nach Land sortiert. Die Zahl ist die Gesamtnote von 5.",
    "count": "{n} Einträge",
    "facts_h2": "Eckdaten", "criteria_h2": "Unsere Noten", "verdict_h2": "Unser Urteil",
    "facts": {"region": "Region", "season": "Saison", "price": "Richtpreis", "price_note": "Stellplatz für 2 Personen, Hauptsaison, pro Nacht", "affiliation": "Verband", "card": "Naturistenausweis", "type": "Art", "accommodation": "Unterkünfte", "website": "Offizielle Website", "visited": "Besucht"},
    "card": {"yes": "erforderlich", "no": "nicht erforderlich", "recommended": "empfohlen"},
    "criteria": {"clean": "Sauberkeit und Pflege", "location": "Lage und Natur", "facilities": "Ausstattung", "atmosphere": "Atmosphäre und Einhaltung der Regeln", "family": "Familienfreundlich", "beginner": "Für Einsteiger geeignet", "value": "Preis-Leistungs-Verhältnis"},
    "overall": "Note", "strengths": "Stärken", "weaknesses": "Schwächen", "for": "Für wen", "not_for": "Für wen nicht", "tip": "Praktischer Tipp",
    "demo": "Beispieleintrag: erfundene Daten, um das Format zu zeigen. Echte Einträge enthalten nur geprüfte Angaben.",
    "verified": "Geprüft anhand von Quellen", "stay_h2": "Übernachten in der Nähe", "stay_p": "Hotels und Apartments in der Nähe. Wer hier bucht, beschert uns eine kleine Provision ohne Mehrkosten: So bleibt der Führer kostenlos und werbefrei.", "price_na": "nicht veröffentlicht: beim Platz erfragen", "sources_h2": "Quellen", "desk_note": "Eintrag anhand der offiziellen Website und öffentlicher Bewertungen erstellt, nicht nach einem Besuch: Die Noten spiegeln den dokumentierten Stand zum angegebenen Datum wider. Haben Sie neuere Informationen? Schreiben Sie eine Bewertung.",
    "review_h1": "Bewertung schreiben", "review_p": "Waren Sie dort? Erzählen Sie, wie es war. Bewertungen werden vor der Veröffentlichung gelesen und bleiben anonym: Nachname und E-Mail werden nie angezeigt.",
    "f": {"camp": "Campingplatz oder Strand", "camp_other": "Anderer (im Text nennen)", "name": "Name oder Nickname", "email": "E-Mail (wird nicht veröffentlicht)", "when": "Monat und Jahr des Aufenthalts", "trip": "Art der Reise", "trips": ["Paar", "Familie", "Allein", "Gruppe"], "acc": "Genutzte Unterkunft", "ratings": "Ihre Noten (1–5)", "text": "Ihre Bewertung (mindestens 300 Zeichen)", "tip": "Praktische Tipps (optional)", "consent": "Ich habe die Regeln gelesen und bin einverstanden, dass meine Bewertung unter meinem Nickname veröffentlicht wird.", "send": "Bewertung senden"},
    "rules_h3": "Regeln in Kürze",
    "rules": ["Nur eigene Erfahrungen, mit Monat und Jahr des Aufenthalts.", "Keine sexuellen oder anzüglichen Inhalte, keine Beschreibungen anderer Gäste.", "Kritik ist willkommen, wenn sie konkret ist; der Betreiber darf antworten.", "Keine Fotos mit erkennbaren Personen."],
    "about_h1": "Über uns", "about_p1": "NaturCamp Guide ist ein unabhängiger Führer zu FKK- und Naturisten-Campingplätzen in Europa, auf Deutsch, Englisch und Italienisch. Wir sind keine Agentur und verkaufen keine Reisen: Wir beschreiben die Plätze so, wie wir sie vorgefunden haben.", "about_p2": "Jeder Eintrag beruht auf einem Besuch oder auf datierten, geprüften Quellen. Enttäuscht uns ein Platz, schreiben wir das; ist er ausgezeichnet, ebenfalls.", "about_p3": "Haben Sie eine Korrektur oder einen Platz vorzuschlagen? Schreiben Sie uns: ",
    "footer": "Unabhängiger Führer zu FKK-Campingplätzen in Europa.", "privacy": "Datenschutz", "contact": "Kontakt",
    "country_names": {"IT": "Italien", "FR": "Frankreich", "ES": "Spanien", "HR": "Kroatien", "DE": "Deutschland", "AT": "Österreich", "PT": "Portugal", "NL": "Niederlande", "GR": "Griechenland", "SI": "Slowenien"},
  },
}
CONTACT = "info@naturcampguide.com"
FORM_ACTION = "https://formspree.io/f/mbggrnyn"
STAY22_AID = "naturcampguide"
AMAZON_TAGS = {"it": "", "en": "", "de": ""}  # tag Amazon Associates per amazon.it / .co.uk / .de; vuoto = link senza affiliazione
AMAZON_HOST = {"it": "www.amazon.it", "en": "www.amazon.co.uk", "de": "www.amazon.de"}  # il tuo ID affiliato Stay22 (es. "naturcampguide"); vuoto = blocco nascosto  # sostituire con l'endpoint del modulo (es. Formspree) — vedi README

LOGO = (ROOT / "src" / "logo.svg").read_text(encoding="utf-8").replace('role="img" aria-label="NaturCamp Guide"', 'aria-hidden="true"')
HORIZON = """<svg class="horizon" viewBox="0 0 1200 160" aria-hidden="true" preserveAspectRatio="none">
  <circle cx="900" cy="120" r="70" fill="#F2B33D"/>
  <rect x="0" y="120" width="1200" height="40" fill="#1F5A3C"/>
  <path d="M0 120 Q 150 100 300 120 T 600 120 T 900 120 T 1200 120 V 160 H 0 Z" fill="#1F5A3C"/>
</svg>"""

def e(s): return html.escape(str(s), quote=True)

def lang_url(lang, kind, slug=None):
    p = T[lang]["paths"]
    if kind == "home": return f"/{lang}/"
    if kind == "camp": return f"/{lang}/{p['camps']}/{slug}/"
    if kind == "beach": return f"/{lang}/{p['beaches']}/{slug}/"
    if kind in p: return f"/{lang}/{p[kind]}/"
    return f"/{lang}/{kind}/"

def basis_label(x, lang):
    t = T[lang]
    if x.get("basis") == "desk":
        return f'{t["verified"]} {x["visited"]}'
    return f'{t["facts"]["visited"]} {x["visited"]}'

def stay_block(x, lang):
    if not STAY22_AID or not x.get("coords"):
        return ""
    t = T[lang]
    lat, lon = [v.strip() for v in x["coords"].split(",")]
    stay_url = f"https://www.stay22.com/map?aid={STAY22_AID}&lat={lat}&lng={lon}&language={lang}"
    return f'''<h2>{e(t["stay_h2"])}</h2>
<p class="meta">{e(t["stay_p"])}</p>
<a class="stay-link" href="{stay_url}" rel="nofollow noopener" target="_blank">
  <span class="stay-icon">🏨</span>
  <span class="stay-text">{e(t["stay_h2"])}</span>
  <span class="stay-arrow">→</span>
</a>'''

def sources_block(x, lang):
    t = T[lang]
    out = ""
    if x.get("basis") == "desk":
        out += f'<p class="meta">{e(t["desk_note"])}</p>'
    if x.get("sources"):
        items = "".join(f'<li><a href="{e(u)}" rel="nofollow">{e(u.replace("https://", "").replace("http://", "").rstrip("/"))}</a></li>' for u in x["sources"])
        out += f'<h2>{e(t["sources_h2"])}</h2><ul class="sources">{items}</ul>'
    return out

def overall(c):
    vals = [v[0] for v in c["scores"].values()]
    return round(sum(vals) / len(vals) * 2) / 2

def fmt_score(x, lang):
    s = f"{x:.1f}".rstrip("0").rstrip(".")
    return s.replace(".", ",") if lang in ("it", "de") else s

def dots(x):
    out = []
    for i in range(1, 6):
        cls = "on" if x >= i else ("half" if x >= i - 0.5 else "")
        out.append(f'<i class="{cls}"></i>')
    return f'<span class="dots" aria-hidden="true">{"".join(out)}</span>'

def page(lang, kind, title, desc, body, slug=None):
    t = T[lang]
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{lang_url(l, kind, slug)}">' for l in LANGS)
    nav = "\n".join(f'<a href="{lang_url(lang, k)}">{e(t["nav"][k])}</a>' for k in ("about", "camps", "beaches", "pack", "review", "assoc"))
    langs = "\n".join(f'<a href="{lang_url(l, kind, slug)}" lang="{l}" hreflang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{lang_url(lang, kind, slug)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE}/en/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;700;800&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="brand" href="{lang_url(lang, 'home')}">{LOGO}<span><b>NaturCamp</b><small>{e(t["brand_sub"])}</small></span></a>
  <nav class="nav" aria-label="Menu">{nav}</nav>
  <div class="lang" aria-label="Language">{langs}</div>
</div></header>
<main>
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <span>© 2026 NaturCamp Guide — {e(t["footer"])}</span>
  <span><a href="mailto:{CONTACT}">{e(t["contact"])}</a> · <a href="{lang_url(lang, 'about')}#privacy">{e(t["privacy"])}</a></span>
</div></footer>
</body>
</html>
"""

NEWS = [
  {
    "date": "2026-10-01",
    "slug": "apertura-guida",
    "title": {"it": "NaturCamp Guide è online", "en": "NaturCamp Guide is live", "de": "NaturCamp Guide ist online"},
    "summary": {"it": "La guida indipendente ai campeggi naturisti in Europa apre con 11 campeggi e 6 spiagge verificate in 6 paesi.", "en": "The independent guide to naturist campsites in Europe launches with 11 campsites and 6 verified beaches across 6 countries.", "de": "Der unabhängige Führer zu FKK-Campingplätzen in Europa startet mit 11 Campingplätzen und 6 geprüften Stränden in 6 Ländern."},
  },
  {
    "date": "2026-10-15",
    "slug": "nuove-schede-croazia",
    "title": {"it": "Nuove schede: Croazia e Landes", "en": "New listings: Croatia and Landes", "de": "Neue Einträge: Kroatien und Landes"},
    "summary": {"it": "Aggiunte le schede di Valalta, Koversada e Solaris in Istria, e di Arnaoutchot nelle Landes francesi.", "en": "Added listings for Valalta, Koversada and Solaris in Istria, and Arnaoutchot in the French Landes.", "de": "Neue Einträge für Valalta, Koversada und Solaris in Istrien sowie Arnaoutchot in den französischen Landes."},
  },
]

def europe_section(lang):
    t = T[lang]
    countries = {}
    for c in DATA:
        countries.setdefault(c["country"], {"camps": [], "beaches": []})["camps"].append(c)
    for b in BEACHES:
        countries.setdefault(b["country"], {"camps": [], "beaches": []})["beaches"].append(b)
    html_out = ""
    for k in sorted(countries, key=lambda k: t["country_names"].get(k, k)):
        grp = countries[k]
        items = ""
        for c in sorted(grp["camps"], key=lambda x: x["name"]):
            sc = overall(c)
            score = f'<span class="eu-score">{fmt_score(sc, lang)}/5</span>'
            items += f'<li><a href="{lang_url(lang, "camp", c["slug"])}">{e(c["name"])}</a>{score}</li>'
        for b in sorted(grp["beaches"], key=lambda x: x["name"]):
            sc = overall(b)
            score = f'<span class="eu-score">{fmt_score(sc, lang)}/5</span>'
            items += f'<li><a href="{lang_url(lang, "beach", b["slug"])}">{e(b["name"])}</a>{score} <small>({e(t["europe_beaches"].lower())})</small></li>'
        html_out += f'<div class="eu-country"><h3>{e(t["country_names"].get(k, k))}</h3><ul class="eu-list">{items}</ul></div>'
    return f"""<section class="block" id="europa"><div class="wrap">
  <h2>{e(t['europe_h2'])}</h2>
  <p class="lead">{e(t['europe_p'])}</p>
  <div class="eu-grid">{html_out}</div>
</div></section>"""

def news_section(lang):
    t = T[lang]
    items = ""
    for n in NEWS[:3]:
        items += f'<article class="news-item"><time>{n["date"]}</time><h3>{e(n["title"][lang])}</h3><p>{e(n["summary"][lang])}</p></article>'
    return f"""<section class="block" id="news"><div class="wrap">
  <h2>{e(t['news_h2'])}</h2>
  <div class="news-grid">{items}</div>
</div></section>"""

def weather_section(lang):
    t = T[lang]
    zones = t["weather_zones"]
    cards = ""
    for z in zones:
        yr_url = f"https://www.yr.no/en/forecast/daily-table/{z['lat']},{z['lon']}"
        cards += f'<div class="wx-card"><div class="wx-name">{e(z["name"])}</div><a class="btn ghost small" href="{yr_url}" rel="nofollow noopener" target="_blank">{e(t["weather_check"])}</a></div>'
    return f"""<section class="block" id="meteo"><div class="wrap">
  <h2>{e(t['weather_h2'])}</h2>
  <p class="lead">{e(t['weather_p'])}</p>
  <div class="wx-grid">{cards}</div>
</div></section>"""

def weather_widget(x, lang):
    """Widget meteo Open-Meteo (fetch lato client) per scheda campeggio/spiaggia."""
    if not x.get("coords"):
        return ""
    t = T[lang]
    lat, lon = [v.strip() for v in x["coords"].split(",")]
    wmo_it = {0:"Sereno",1:"Prevalentemente sereno",2:"Parzialmente nuvoloso",3:"Nuvoloso",45:"Nebbia",48:"Nebbia con brina",51:"Pioggerella leggera",53:"Pioggerella",55:"Pioggerella intensa",61:"Pioggia leggera",63:"Pioggia",65:"Pioggia intensa",71:"Neve leggera",73:"Neve",75:"Neve intensa",77:"Granuli di neve",80:"Rovesci leggeri",81:"Rovesci",82:"Rovesci forti",85:"Rovesci di neve",86:"Rovesci di neve forti",95:"Temporale",96:"Temporale con grandine",99:"Temporale con grandine forte"}
    wmo_en = {0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",45:"Fog",48:"Icy fog",51:"Light drizzle",53:"Drizzle",55:"Dense drizzle",61:"Slight rain",63:"Rain",65:"Heavy rain",71:"Slight snow",73:"Snow",75:"Heavy snow",77:"Snow grains",80:"Slight showers",81:"Showers",82:"Heavy showers",85:"Snow showers",86:"Heavy snow showers",95:"Thunderstorm",96:"Thunderstorm w/ hail",99:"Thunderstorm w/ heavy hail"}
    wmo_de = {0:"Klar",1:"Überwiegend klar",2:"Teils bewölkt",3:"Bedeckt",45:"Nebel",48:"Nebel mit Reif",51:"Leichter Nieselregen",53:"Nieselregen",55:"Starker Nieselregen",61:"Leichter Regen",63:"Regen",65:"Starker Regen",71:"Leichter Schnee",73:"Schnee",75:"Starker Schnee",77:"Schneekörner",80:"Leichte Schauer",81:"Schauer",82:"Starke Schauer",85:"Schneeschauer",86:"Starke Schneeschauer",95:"Gewitter",96:"Gewitter mit Hagel",99:"Gewitter mit starkem Hagel"}
    wmo_map = {"it": wmo_it, "en": wmo_en, "de": wmo_de}
    wmo_json = json.dumps(wmo_map[lang])
    widget_id = f"wx-{x['slug'].replace('-','')}"
    labels = {
        "it": {"title": "Meteo nei prossimi giorni", "loading": "Caricamento meteo…", "min": "min", "max": "max", "error": "Meteo non disponibile"},
        "en": {"title": "Weather forecast", "loading": "Loading weather…", "min": "min", "max": "max", "error": "Weather unavailable"},
        "de": {"title": "Wettervorhersage", "loading": "Wetter wird geladen…", "min": "min", "max": "max", "error": "Wetter nicht verfügbar"},
    }[lang]
    return f'''<h2>{e(labels["title"])}</h2>
<div id="{widget_id}" class="wx-widget"><p class="meta wx-loading">{e(labels["loading"])}</p></div>
<script>
(function(){{
  var el = document.getElementById('{widget_id}');
  var wmo = {wmo_json};
  fetch('https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=5')
    .then(function(r){{ return r.json(); }})
    .then(function(d){{
      var days = d.daily;
      var html = '<div class="wx-days">';
      for(var i=0;i<days.time.length;i++){{
        var dt = new Date(days.time[i]);
        var dn = dt.toLocaleDateString('{lang}',{{weekday:'short',day:'numeric',month:'short'}});
        var code = days.weathercode[i];
        var desc = wmo[code] || code;
        var icons = [['☀','🌤','⛅','☁','🌫','🌫','🌦','🌦','🌧','🌧','🌧','❄','❄','❄','🌨','🌦','🌦','🌧','🌨','🌨','⛈','⛈','⛈'][Math.floor(i/1)]||'🌡'];
        var icon = ['☀','🌤','⛅','☁','🌫','🌫','🌦','🌦','🌧','🌧','🌧','❄','❄','❄','🌨','🌦','🌦','🌧','🌨','🌨','⛈','⛈','⛈'][[0,1,2,3,45,48,51,53,55,61,63,65,71,73,75,77,80,81,82,85,86,95,96,99].indexOf(code)]||'🌡';
        html += '<div class="wx-day"><div class="wx-dn">'+dn+'</div><div class="wx-icon">'+icon+'</div><div class="wx-desc">'+desc+'</div><div class="wx-temp"><span class="wx-max">'+Math.round(days.temperature_2m_max[i])+'°</span> <span class="wx-min">{e(labels["min"])} '+Math.round(days.temperature_2m_min[i])+'°</span></div></div>';
      }}
      html += '</div>';
      el.innerHTML = html;
    }})
    .catch(function(){{ el.innerHTML = '<p class="meta">{e(labels["error"])}</p>'; }});
}})();
</script>'''

def season_bar(x, lang):
    """Barra mesi apertura/chiusura dalla stringa season tipo '01-05 → 10-10'."""
    season = x.get("season", "")
    if not season or "→" not in season:
        return ""
    labels = {
        "it": ["gen","feb","mar","apr","mag","giu","lug","ago","set","ott","nov","dic"],
        "en": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        "de": ["Jan","Feb","Mrz","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"],
    }[lang]
    title = {"it": "Apertura", "en": "Open", "de": "Saison"}[lang]
    try:
        parts = season.replace(" ", "").split("→")
        start = parts[0]  # "01-05"
        end = parts[1]    # "10-10"
        sm = int(start.split("-")[1])  # mese inizio
        em = int(end.split("-")[1])    # mese fine
    except Exception:
        return ""
    months = ""
    for i in range(1, 13):
        active = (sm <= i <= em) if sm <= em else (i >= sm or i <= em)
        cls = "sx-on" if active else "sx-off"
        months += f'<span class="{cls}">{labels[i-1]}</span>'
    return f'<div class="season-bar"><span class="sx-label">{title}:</span>{months}</div>'

def weather_link(x, lang):
    """Bottone meteo yr.no per scheda campeggio/spiaggia (fallback)."""
    t = T[lang]
    if not x.get("coords"):
        return ""
    lat, lon = [v.strip() for v in x["coords"].split(",")]
    yr_url = f"https://www.yr.no/en/forecast/daily-table/{lat},{lon}"
    return f'<p style="margin-top:12px"><a class="btn ghost small" href="{yr_url}" rel="nofollow noopener" target="_blank">🌤 {e(t["weather_link"])} {e(x["name"])}</a></p>'

def map_section(lang):
    import json as _json
    t = T[lang]
    markers = []
    for c in DATA:
        if c.get("coords"):
            lat, lon = [v.strip() for v in c["coords"].split(",")]
            markers.append({"type": "camp", "lat": float(lat), "lon": float(lon),
                            "name": c["name"], "url": lang_url(lang, "camp", c["slug"])})
    for b in BEACHES:
        if b.get("coords"):
            lat, lon = [v.strip() for v in b["coords"].split(",")]
            markers.append({"type": "beach", "lat": float(lat), "lon": float(lon),
                            "name": b["name"], "url": lang_url(lang, "beach", b["slug"])})
    markers_json = _json.dumps(markers, ensure_ascii=False)
    return f"""<section class="block" id="mappa"><div class="wrap">
  <h2>{e(t['map_h2'])}</h2>
  <p class="lead">{e(t['map_p'])}</p>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <div id="naturmap" style="height:480px;border-radius:12px;overflow:hidden;margin-top:16px"></div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
  (function(){{
    var markers = {markers_json};
    var map = L.map('naturmap', {{scrollWheelZoom: false}}).setView([46, 8], 5);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18
    }}).addTo(map);
    var campIcon = L.divIcon({{className:'', html:'<span style="font-size:22px;line-height:1;filter:drop-shadow(0 1px 2px #0006)">🏕</span>', iconSize:[28,28], iconAnchor:[14,14], popupAnchor:[0,-14]}});
    var beachIcon = L.divIcon({{className:'', html:'<span style="font-size:22px;line-height:1;filter:drop-shadow(0 1px 2px #0006)">🏖</span>', iconSize:[28,28], iconAnchor:[14,14], popupAnchor:[0,-14]}});
    markers.forEach(function(m){{
      L.marker([m.lat, m.lon], {{icon: m.type==='camp' ? campIcon : beachIcon}})
        .addTo(map)
        .bindPopup('<a href="'+m.url+'" style="font-weight:700;color:#1F5A3C">'+m.name+'</a>');
    }});
  }})();
  </script>
</div></section>"""

def camp_item(c, lang):
    t = T[lang]
    sc = overall(c)
    return f"""<li class="camp">
  <div class="score"><b>{fmt_score(sc, lang)}</b><small>/5</small></div>
  <div>
    <h3><a href="{lang_url(lang, 'camp', c['slug'])}">{e(c['name'])}</a></h3>
    <p class="meta"><span>{e(t['country_names'].get(c['country'], c['country']))}, {e(c['region'][lang])}</span><span>{e(c['season'])}</span><span>{'€ ' + str(c['price']) if c.get('price') else e(t['price_na'])}</span></p>
    <p class="forwhom"><strong>{e(t['for'])}:</strong> {e(c['for'][lang])}</p>
  </div>
</li>"""

def home(lang):
    t = T[lang]
    countries = {}
    for c in DATA: countries[c["country"]] = countries.get(c["country"], 0) + 1
    cl = "".join(f'<li><a href="{lang_url(lang, "camps")}#{k}">{e(t["country_names"].get(k, k))}<span>{n}</span></a></li>' for k, n in sorted(countries.items(), key=lambda kv: t["country_names"].get(kv[0], kv[0])))
    latest = "".join(camp_item(c, lang) for c in sorted(DATA, key=lambda c: c["visited"], reverse=True)[:5])
    beach_latest = "".join(beach_item(b, lang) for b in sorted(BEACHES, key=lambda b: b["visited"], reverse=True)[:3])
    body = f"""<section class="hero"><div class="wrap">
  <h1>{e(t['hero_h1'])}</h1>
  <p>{e(t['hero_p'])}</p>
  <div class="hero-actions"><a class="btn" href="{lang_url(lang, 'camps')}">{e(t['hero_cta'])}</a><a class="btn ghost" href="#how">{e(t['hero_cta2'])}</a></div>
  {HORIZON}
</div></section>
<section class="block home-about"><div class="wrap">
  <h2>{e(t['about_h1'])}</h2>
  <p class="lead">{e(t['about_p1'])}</p>
  <p>{e(t['about_p2'])}</p>
  <p>{e(t['about_p3'])}<a href="mailto:{CONTACT}">{CONTACT}</a> · <a href="{lang_url(lang, 'about')}">{e(t['about_h1'])}</a></p>
</div></section>
<section class="block"><div class="wrap"><h2>{e(t['countries_h2'])}</h2><ul class="countries">{cl}</ul></div></section>
<section class="block"><div class="wrap"><h2>{e(t['latest_h2'])}</h2><ul class="camps">{latest}</ul></div></section>
<section class="block"><div class="wrap"><h2>{e(t['beaches_home_h2'])}</h2><p class="lead">{e(t['beaches_home_p'])}</p><ul class="camps">{beach_latest}</ul><p style="margin-top:20px"><a class="btn ghost" href="{lang_url(lang, 'beaches')}">{e(t['beaches_all'])}</a></p></div></section>
<section class="block assoc-home"><div class="wrap"><h2>{e(t['assoc_home_h2'])}</h2><p class="lead">{e(t['assoc_home_p'])}</p><ul class="assoc-home-list">{"".join(f'<li><span class="assoc-flag">' + {"IT":"🇮🇹","FR":"🇫🇷","DE":"🇩🇪","ES":"🇪🇸","HR":"🇭🇷","GB":"🇬🇧","NL":"🇳🇱","DK":"🇩🇰","PT":"🇵🇹","GR":"🇬🇷"}.get(a["country"],"") + f'</span> <a href="{e(a["url"])}" rel="nofollow noopener" target="_blank">{e(a["name"].split("–")[0].strip() if "–" in a["name"] else a["name"].split("(")[0].strip())}</a></li>' for a in ASSOC["national"][:6])}</ul><p style="margin-top:20px"><a class="btn ghost" href="{lang_url(lang, 'assoc')}">{e(t['assoc_home_cta'])}</a></p></div></section>
{map_section(lang)}
{europe_section(lang)}
{news_section(lang)}
{weather_section(lang)}
<section class="block" id="how"><div class="wrap"><h2>{e(t['how_h2'])}</h2><p class="lead">{e(t['how_p'])}</p></div></section>"""
    return page(lang, "home", t["title"], t["desc"], body)

def camps(lang):
    t = T[lang]
    groups = {}
    for c in DATA: groups.setdefault(c["country"], []).append(c)
    sections = ""
    for k in sorted(groups, key=lambda k: t["country_names"].get(k, k)):
        items = "".join(camp_item(c, lang) for c in sorted(groups[k], key=overall, reverse=True))
        sections += f'<section class="block" id="{k}"><div class="wrap"><h2>{e(t["country_names"].get(k, k))}</h2><ul class="camps">{items}</ul></div></section>'
    body = f'<section class="block"><div class="wrap"><h1>{e(t["camps_h1"])}</h1><p class="lead">{e(t["camps_p"])} {e(t["count"].format(n=len(DATA)))}.</p></div></section>{sections}'
    return page(lang, "camps", f'{t["camps_h1"]} — NaturCamp Guide', t["camps_p"], body)

def sheet(c, lang):
    t = T[lang]; f = t["facts"]; sc = overall(c)
    facts = [
        (f["region"], f'{t["country_names"].get(c["country"], c["country"])}, {c["region"][lang]}'),
        (f["season"], c["season"]),
        (f["price"], f'€ {c["price"]} — {f["price_note"]}' if c.get("price") else t["price_na"]),
        (f["affiliation"], c["affiliation"]),
        (f["card"], t["card"][c["card"]]),
        (f["type"], c["type"][lang]),
        (f["accommodation"], c["accommodation"][lang]),
        (f["visited"] if c.get("basis") != "desk" else t["verified"], c["visited"]),
    ]
    rows = "".join(f"<tr><th scope='row'>{e(k)}</th><td>{e(v)}{season_bar(c, lang) if k == f['season'] else ''}</td></tr>" for k, v in facts)
    rows += f'<tr><th scope="row">{e(f["website"])}</th><td><a href="{e(c["website"])}" rel="nofollow">{e(c["website"].replace("https://", ""))}</a></td></tr>'
    crit = "".join(f'<li><span class="name">{e(t["criteria"][k])}</span><span>{dots(v[0])} <strong>{fmt_score(v[0], lang)}</strong></span><span class="why">{e(v[1][lang])}</span></li>' for k, v in c["scores"].items())
    demo = f'<div class="demo">{e(t["demo"])}</div>' if c.get("demo") else ""
    body = f"""<section class="block"><div class="wrap">
  <div class="sheet-head">
    <div><h1>{e(c['name'])}</h1><p class="meta"><span>{e(t['country_names'].get(c['country'], c['country']))}, {e(c['region'][lang])}</span><span>{e(basis_label(c, lang))}</span></p><p class="lead">{e(c['summary'][lang])}</p></div>
    <div class="score"><b>{fmt_score(sc, lang)}</b><small>{e(t['overall'])} /5</small></div>
  </div>
  {demo}
  <h2>{e(t['facts_h2'])}</h2>
  <table class="facts"><tbody>{rows}</tbody></table>
  <h2>{e(t['criteria_h2'])}</h2>
  <ul class="criteria">{crit}</ul>
  <h2>{e(t['verdict_h2'])}</h2>
  <div class="verdict">
    <div><h3>{e(t['strengths'])}</h3><p>{e(c['strengths'][lang])}</p></div>
    <div class="no"><h3>{e(t['weaknesses'])}</h3><p>{e(c['weaknesses'][lang])}</p></div>
    <div><h3>{e(t['for'])}</h3><p>{e(c['for'][lang])}</p></div>
    <div class="no"><h3>{e(t['not_for'])}</h3><p>{e(c['not_for'][lang])}</p></div>
    <div class="tip"><h3>{e(t['tip'])}</h3><p>{e(c['tip'][lang])}</p></div>
  </div>
  {stay_block(c, lang)}
  {weather_widget(c, lang)}
  {sources_block(c, lang)}
</div></section>"""
    return page(lang, "camp", f'{c["name"]} — NaturCamp Guide', c["summary"][lang], body, c["slug"])

def beach_item(b, lang):
    t = T[lang]
    sc = overall(b)
    return f"""<li class="camp">
  <div class="score"><b>{fmt_score(sc, lang)}</b><small>/5</small></div>
  <div>
    <h3><a href="{lang_url(lang, 'beach', b['slug'])}">{e(b['name'])}</a></h3>
    <p class="meta"><span>{e(t['country_names'].get(b['country'], b['country']))}, {e(b['region'][lang])}</span><span>{e(t['status_short'][b['status']])}</span><span>{e(b['ground'][lang])}</span></p>
    <p class="forwhom"><strong>{e(t['for'])}:</strong> {e(b['for'][lang])}</p>
  </div>
</li>"""

def beaches(lang):
    t = T[lang]
    groups = {}
    for b in BEACHES: groups.setdefault(b["country"], []).append(b)
    sections = ""
    for k in sorted(groups, key=lambda k: t["country_names"].get(k, k)):
        items = "".join(beach_item(b, lang) for b in sorted(groups[k], key=overall, reverse=True))
        sections += f'<section class="block" id="{k}"><div class="wrap"><h2>{e(t["country_names"].get(k, k))}</h2><ul class="camps">{items}</ul></div></section>'
    body = f'<section class="block"><div class="wrap"><h1>{e(t["beaches_h1"])}</h1><p class="lead">{e(t["beaches_p"])} {e(t["count"].format(n=len(BEACHES)))}.</p><p class="meta">{e(t["status_note"])}</p></div></section>{sections}'
    return page(lang, "beaches", f'{t["beaches_h1"]} — NaturCamp Guide', t["beaches_p"], body)

def beach_sheet(b, lang):
    t = T[lang]; f = t["bfacts"]; sc = overall(b)
    by_slug = {c["slug"]: c for c in DATA}
    facts = [
        (f["status"], t["status"][b["status"]]),
        (f["ground"], b["ground"][lang]),
        (f["length"], b["length"]),
        (f["access"], b["access"][lang]),
        (f["services"], b["services"][lang]),
        (f["season"], b["season"][lang]),
        (t["facts"]["visited"] if b.get("basis") != "desk" else t["verified"], b["visited"]),
    ]
    rows = "".join(f"<tr><th scope='row'>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in facts)
    lat, lon = [x.strip() for x in b["coords"].split(",")]
    rows += f'<tr><th scope="row">{e(f["coords"])}</th><td><a href="https://www.openstreetmap.org/?mlat={lat}&amp;mlon={lon}#map=15/{lat}/{lon}" rel="nofollow">{e(b["coords"])}</a></td></tr>'
    near = [by_slug[s] for s in b.get("nearby", []) if s in by_slug]
    if near:
        rows += f'<tr><th scope="row">{e(f["nearby"])}</th><td>' + ", ".join(f'<a href="{lang_url(lang, "camp", c["slug"])}">{e(c["name"])}</a>' for c in near) + "</td></tr>"
    crit = "".join(f'<li><span class="name">{e(t["bcriteria"][k])}</span><span>{dots(v[0])} <strong>{fmt_score(v[0], lang)}</strong></span><span class="why">{e(v[1][lang])}</span></li>' for k, v in b["scores"].items())
    demo = f'<div class="demo">{e(t["demo"])}</div>' if b.get("demo") else ""
    body = f"""<section class="block"><div class="wrap">
  <div class="sheet-head">
    <div><h1>{e(b['name'])}</h1><p class="meta"><span>{e(t['country_names'].get(b['country'], b['country']))}, {e(b['region'][lang])}</span><span>{e(t['status_short'][b['status']])}</span><span>{e(basis_label(b, lang))}</span></p><p class="lead">{e(b['summary'][lang])}</p></div>
    <div class="score"><b>{fmt_score(sc, lang)}</b><small>{e(t['overall'])} /5</small></div>
  </div>
  {demo}
  <h2>{e(t['facts_h2'])}</h2>
  <table class="facts"><tbody>{rows}</tbody></table>
  <p class="meta">{e(t['status_note'])}</p>
  <h2>{e(t['criteria_h2'])}</h2>
  <ul class="criteria">{crit}</ul>
  <h2>{e(t['verdict_h2'])}</h2>
  <div class="verdict">
    <div><h3>{e(t['for'])}</h3><p>{e(b['for'][lang])}</p></div>
    <div class="no"><h3>{e(t['not_for'])}</h3><p>{e(b['not_for'][lang])}</p></div>
    <div class="tip"><h3>{e(t['tip'])}</h3><p>{e(b['tip'][lang])}</p></div>
  </div>
  {stay_block(b, lang)}
  {weather_widget(b, lang)}
  {sources_block(b, lang)}
</div></section>"""
    return page(lang, "beach", f'{b["name"]} — NaturCamp Guide', b["summary"][lang], body, b["slug"])

PACK = {
  "it": {
    "h1": "Cosa portare in un campeggio naturista",
    "lead": "Meno di quanto pensi. Il naturismo semplifica la valigia, ma alcune cose sono obbligatorie e altre fanno la differenza tra una vacanza comoda e una scomoda. Ecco la lista che useremmo noi, divisa per situazione.",
    "disclosure": "I link ai prodotti portano ad Amazon: se acquisti da lì riceviamo una piccola commissione, senza costi per te. Non indichiamo marche: scegli il prodotto che preferisci.",
    "btn": "Vedi su Amazon",
    "sections": [
      {"h": "Obbligatorio o quasi", "items": [
        ["Telo da sedia", "La regola numero uno del naturismo: ci si siede sempre su un telo proprio, anche al bar e in piscina. Portane due, uno piccolo da tenere in borsa.", "telo mare microfibra"],
        ["Tessera naturista INF", "Richiesta in molti campeggi italiani e tedeschi, consigliata ovunque. Si ottiene dalla federazione del proprio paese (FENAIT, DFK, FFN) e vale un anno.", None],
        ["Crema solare SPF 50", "Senza costume si scottano parti che non hanno mai visto il sole. Serve un formato grande e un'applicazione ogni due ore.", "crema solare spf 50 resistente acqua"],
        ["Sandali o ciabatte lavabili", "Per docce, sanitari e vialetti caldi. Meglio un modello che si asciuga in fretta.", "sandali acqua uomo donna"]
      ]},
      {"h": "Spiaggia e mare", "items": [
        ["Scarpette da scoglio", "Istria, Calabria, Liguria: costa di scogli e ciottoli. Le spiagge di Solaris, Pizzo Greco e Guvano le richiedono.", "scarpe scoglio"],
        ["Ombrellone con picchetto a vite", "Molte spiagge naturiste non hanno ombra né noleggio; il picchetto a vite tiene con il vento dell'Atlantico e del Mare del Nord.", "ombrellone spiaggia picchetto antivento"],
        ["Zaino da spiaggia impermeabile", "Per i 20 minuti di sabbia a Maspalomas o il sentiero di Montalivet: mani libere e telefono asciutto.", "zaino mare impermeabile"],
        ["Borraccia termica", "Nessun chiosco nel tratto centrale di molte spiagge: un litro d'acqua fredda a testa.", "borraccia termica 1 litro"]
      ]},
      {"h": "Campeggio", "items": [
        ["Frigo portatile", "In piazzola, con l'elettricità inclusa nel prezzo, un frigo elettrico vale più di qualsiasi borsa termica.", "frigo portatile elettrico campeggio"],
        ["Prolunga da campeggio CEE", "Le colonnine europee usano la presa blu CEE 16 A; servono 25 metri e un adattatore per le prese nazionali.", "cavo prolunga campeggio cee"],
        ["Lampada frontale", "Molti campeggi naturisti sono poco illuminati di notte, La Sablière per esempio.", "lampada frontale ricaricabile"],
        ["Telo e mollette", "Per stendere costumi che non userai e teli che userai sempre.", "stendibiancheria campeggio"]
      ]},
      {"h": "Piccole cose che si dimenticano", "items": [
        ["Pareo o kimono leggero", "Per i momenti in cui coprirsi è richiesto: ristorante, negozio, zone tessili di resort misti come Koversada.", "pareo uomo donna"],
        ["Repellente per zanzare", "Pinete e fiumi, da Euronat alla Cèze, ne sono pieni al tramonto.", "repellente zanzare"],
        ["Monete da 1 €", "Per le docce a gettone (Hilsbachtal) e le lavatrici.", None],
        ["Guida cartacea", "Dove il Wi-Fi è a pagamento o assente: la guida naturista INF-FNI o una guida ai campeggi.", "guida campeggi europa"]
      ]}
    ]
  },
  "en": {
    "h1": "What to pack for a naturist campsite",
    "lead": "Less than you think. Naturism simplifies the suitcase, but some things are compulsory and others make the difference between a comfortable holiday and an awkward one. Here is the list we would use, by situation.",
    "disclosure": "Product links go to Amazon: if you buy there we earn a small commission at no cost to you. We don't name brands: pick the product you prefer.",
    "btn": "See on Amazon",
    "sections": [
      {"h": "Compulsory, or nearly", "items": [
        ["Sitting towel", "Rule number one of naturism: always sit on your own towel, at the bar and by the pool too. Bring two, one small enough for your bag.", "microfibre beach towel"],
        ["INF naturist card", "Required at many Italian and German campsites, recommended everywhere. Issued by your national federation (British Naturism, FFN, DFK) and valid for a year.", None],
        ["SPF 50 sunscreen", "Without a swimsuit, parts that have never seen the sun will burn. Get a large bottle and reapply every two hours.", "spf 50 sunscreen water resistant"],
        ["Washable sandals or flip-flops", "For showers, sanitary blocks and hot paths. Choose a quick-drying model.", "water sandals"]
      ]},
      {"h": "Beach and sea", "items": [
        ["Rock shoes", "Istria, Calabria, Liguria: rocky and pebbly coasts. The beaches at Solaris, Pizzo Greco and Guvano all need them.", "water shoes rocks"],
        ["Parasol with screw anchor", "Many naturist beaches have no shade and no hire; a screw anchor holds in Atlantic and North Sea winds.", "beach umbrella sand anchor windproof"],
        ["Waterproof beach backpack", "For the 20 minutes of sand at Maspalomas or the path at Montalivet: hands free and phone dry.", "waterproof beach backpack"],
        ["Insulated bottle", "No kiosk in the central stretch of many beaches: a litre of cold water each.", "insulated water bottle 1 litre"]
      ]},
      {"h": "Campsite", "items": [
        ["Portable fridge", "On a pitch with electricity included, an electric cool box beats any cool bag.", "electric cool box camping"],
        ["CEE camping extension lead", "European hook-ups use the blue 16 A CEE plug; you need 25 metres and an adapter for national sockets.", "camping extension lead cee 16a"],
        ["Head torch", "Many naturist campsites are poorly lit at night, La Sablière for one.", "rechargeable head torch"],
        ["Washing line and pegs", "For the swimsuits you won't use and the towels you always will.", "camping washing line"]
      ]},
      {"h": "Small things people forget", "items": [
        ["Sarong or light kimono", "For moments when covering up is required: restaurant, shop, textile zones of mixed resorts such as Koversada.", "sarong unisex"],
        ["Mosquito repellent", "Pine forests and rivers, from Euronat to the Cèze, are full of them at dusk.", "mosquito repellent"],
        ["€1 coins", "For token showers (Hilsbachtal) and washing machines.", None],
        ["Paper guide", "Where Wi-Fi is paid or absent: the INF-FNI naturist guide or a campsite guide.", "europe campsite guide book"]
      ]}
    ]
  },
  "de": {
    "h1": "Packliste für den FKK-Campingplatz",
    "lead": "Weniger, als man denkt. FKK vereinfacht den Koffer, aber einiges ist Pflicht und anderes macht den Unterschied zwischen einem bequemen und einem mühsamen Urlaub. Hier unsere Liste, nach Situation.",
    "disclosure": "Produktlinks führen zu Amazon: Wer dort kauft, beschert uns eine kleine Provision ohne Mehrkosten. Wir nennen keine Marken: Wählen Sie das Produkt, das Ihnen gefällt.",
    "btn": "Bei Amazon ansehen",
    "sections": [
      {"h": "Pflicht oder fast", "items": [
        ["Sitzhandtuch", "Regel Nummer eins beim FKK: Man sitzt immer auf dem eigenen Handtuch, auch an der Bar und am Pool. Zwei mitnehmen, eines klein genug für die Tasche.", "mikrofaser handtuch strand"],
        ["INF-Naturistenausweis", "Auf vielen italienischen und deutschen Plätzen Pflicht, überall empfohlen. Gibt es beim DFK (bzw. FENAIT, FFN) und gilt ein Jahr.", None],
        ["Sonnencreme LSF 50", "Ohne Badehose verbrennen Stellen, die nie Sonne gesehen haben. Große Flasche, alle zwei Stunden nachcremen.", "sonnencreme lsf 50 wasserfest"],
        ["Abwaschbare Sandalen oder Badelatschen", "Für Duschen, Sanitärgebäude und heiße Wege. Am besten ein schnell trocknendes Modell.", "wassersandalen"]
      ]},
      {"h": "Strand und Meer", "items": [
        ["Badeschuhe", "Istrien, Kalabrien, Ligurien: Fels- und Kieselküsten. Die Strände von Solaris, Pizzo Greco und Guvano verlangen sie.", "badeschuhe felsen"],
        ["Sonnenschirm mit Schraubanker", "Viele FKK-Strände haben weder Schatten noch Verleih; der Schraubanker hält bei Atlantik- und Nordseewind.", "sonnenschirm strand bodenhülse windfest"],
        ["Wasserdichter Strandrucksack", "Für die 20 Minuten Sand in Maspalomas oder den Weg in Montalivet: Hände frei, Handy trocken.", "strandrucksack wasserdicht"],
        ["Thermoflasche", "Kein Kiosk im mittleren Abschnitt vieler Strände: ein Liter kaltes Wasser pro Person.", "thermoflasche 1 liter"]
      ]},
      {"h": "Campingplatz", "items": [
        ["Kühlbox elektrisch", "Am Stellplatz mit inklusivem Strom schlägt eine elektrische Kühlbox jede Kühltasche.", "kühlbox elektrisch camping"],
        ["CEE-Verlängerungskabel", "Europäische Stromsäulen haben den blauen CEE-Stecker 16 A; 25 Meter und ein Adapter für Landessteckdosen sind nötig.", "camping verlängerungskabel cee 16a"],
        ["Stirnlampe", "Viele FKK-Plätze sind nachts schlecht beleuchtet, La Sablière zum Beispiel.", "stirnlampe aufladbar"],
        ["Wäscheleine und Klammern", "Für die Badesachen, die man nicht braucht, und die Handtücher, die man immer braucht.", "wäscheleine camping"]
      ]},
      {"h": "Kleinigkeiten, die man vergisst", "items": [
        ["Pareo oder leichter Kimono", "Für Momente, in denen Bekleidung verlangt wird: Restaurant, Laden, Textilbereiche gemischter Resorts wie Koversada.", "pareo unisex"],
        ["Mückenschutz", "Pinienwälder und Flüsse, von Euronat bis zur Cèze, sind abends voll davon.", "mückenschutz spray"],
        ["1-Euro-Münzen", "Für Münzduschen (Hilsbachtal) und Waschmaschinen.", None],
        ["Gedruckter Führer", "Wo WLAN kostet oder fehlt: der INF-FNI-Naturistenführer oder ein Campingführer.", "campingführer europa buch"]
      ]}
    ]
  },
}

def amazon_url(lang, q):
    from urllib.parse import quote_plus
    u = f"https://{AMAZON_HOST[lang]}/s?k={quote_plus(q)}"
    if AMAZON_TAGS.get(lang):
        u += f"&tag={AMAZON_TAGS[lang]}"
    return u

def pack(lang):
    t = T[lang]; pk = PACK[lang]
    secs = ""
    for sec in pk["sections"]:
        items = ""
        for name, why, q in sec["items"]:
            link = f'<a class="btn ghost small" href="{amazon_url(lang, q)}" rel="nofollow sponsored noopener" target="_blank">{e(pk["btn"])}</a>' if q else ""
            items += f'<li><div><h3>{e(name)}</h3><p>{e(why)}</p></div>{link}</li>'
        secs += f'<h2>{e(sec["h"])}</h2><ul class="pack">{items}</ul>'
    body = f"""<section class="block"><div class="wrap">
  <h1>{e(pk['h1'])}</h1>
  <p class="lead">{e(pk['lead'])}</p>
  {('<p class="meta">' + e(pk['disclosure']) + '</p>') if AMAZON_TAGS.get(lang) else ''}
  {secs}
</div></section>"""
    return page(lang, "pack", f'{pk["h1"]} — NaturCamp Guide', pk["lead"], body)

# ---------------------------------------------------------------- associazioni naturiste
ASSOC = {
  "international": [
    {
      "name": "International Naturist Federation (INF-FNI)",
      "url": "https://www.inf-fni.org/",
      "desc": {
        "it": "La federazione mondiale del naturismo, fondata nel 1953. Raggruppa le federazioni nazionali di oltre 30 paesi e rilascia la tessera internazionale INF, riconosciuta dalla maggior parte dei campeggi e spiagge affiliati.",
        "en": "The world federation of naturism, founded in 1953. It groups national federations from over 30 countries and issues the INF international membership card, recognised by most affiliated campsites and beaches.",
        "de": "Der weltweite Dachverband des Naturismus, gegründet 1953. Er vereint nationale Verbände aus über 30 Ländern und gibt den internationalen INF-Ausweis heraus, der von den meisten angeschlossenen Campingplätzen und Stränden anerkannt wird.",
      },
      "members": None,
    },
    {
      "name": "European Naturist Federation (ENF)",
      "url": "https://www.european-naturism.eu/",
      "desc": {
        "it": "Il ramo europeo dell'INF, che coordina le federazioni del continente e organizza eventi come l'Europade, raduno europeo naturista itinerante.",
        "en": "The European branch of INF, coordinating the continent's federations and organising events like the Europade, a roving European naturist gathering.",
        "de": "Der europäische Zweig des INF, der die Verbände des Kontinents koordiniert und Veranstaltungen wie die Europade, ein wanderndes europäisches Naturistentreffen, organisiert.",
      },
      "members": None,
    },
  ],
  "national": [
    {
      "country": "IT",
      "name": "FENAIT – Federazione Naturista Italiana",
      "url": "https://www.fenait.org/",
      "desc": {
        "it": "La federazione italiana del naturismo, affiliata all'INF. Rilascia la tessera INF per l'Italia e gestisce l'elenco dei campeggi e circoli naturisti affiliati.",
        "en": "The Italian naturist federation, affiliated with INF. Issues the INF card for Italy and maintains the list of affiliated naturist campsites and clubs.",
        "de": "Der italienische Naturistenverband, Mitglied des INF. Stellt den INF-Ausweis für Italien aus und pflegt die Liste der angeschlossenen Campingplätze und Clubs.",
      },
    },
    {
      "country": "FR",
      "name": "FFN – Fédération Française de Naturisme",
      "url": "https://www.ffn-naturisme.com/",
      "desc": {
        "it": "La più grande federazione naturista d'Europa per numero di soci. Gestisce numerosi campeggi naturisti in Francia, soprattutto nella regione delle Landes, e rilascia la tessera annuale FFN.",
        "en": "The largest naturist federation in Europe by membership. It manages many naturist campsites in France, especially in the Landes region, and issues the annual FFN card.",
        "de": "Der mitgliederstärkste Naturistenverband Europas. Er betreibt viele Naturistencampingplätze in Frankreich, besonders in den Landes, und gibt den jährlichen FFN-Ausweis heraus.",
      },
    },
    {
      "country": "DE",
      "name": "DFK – Deutscher Verband für Freikörperkultur",
      "url": "https://www.dfk.org/",
      "desc": {
        "it": "Il più antico movimento nudista organizzato al mondo (1898). Raggruppa i club FKK tedeschi e gestisce campeggi in tutta la Germania, rilasciando la tessera DFK riconosciuta a livello INF.",
        "en": "The world's oldest organised nudist movement (1898). Groups German FKK clubs and manages campsites across Germany, issuing the DFK card recognised at INF level.",
        "de": "Die älteste organisierte Freikörperkultur-Bewegung der Welt (1898). Vereint deutsche FKK-Vereine und betreibt Campingplätze in ganz Deutschland; gibt den INF-anerkannten DFK-Ausweis aus.",
      },
    },
    {
      "country": "ES",
      "name": "FEN – Federación Española de Naturismo",
      "url": "https://www.naturismo.org/",
      "desc": {
        "it": "La federazione spagnola, affiliata INF. Coordina i club e i campeggi naturisti in Spagna e promuove le spiagge naturiste ufficiali.",
        "en": "The Spanish federation, INF-affiliated. Coordinates naturist clubs and campsites in Spain and promotes official naturist beaches.",
        "de": "Der spanische Verband, INF-Mitglied. Koordiniert Naturistenvereine und -Campingplätze in Spanien und fördert offizielle Naturistenstrände.",
      },
    },
    {
      "country": "HR",
      "name": "HNS – Hrvatska naturistička savez",
      "url": "https://www.naturizam.hr/",
      "desc": {
        "it": "La federazione croata del naturismo. La Croazia è uno dei paesi con la più lunga tradizione naturista in Europa, con numerosi campeggi e spiagge FKK, soprattutto in Istria.",
        "en": "The Croatian naturist federation. Croatia has one of the longest naturist traditions in Europe, with numerous FKK campsites and beaches, especially in Istria.",
        "de": "Der kroatische Naturistenverband. Kroatien hat eine der längsten Naturistentraditionen in Europa, mit zahlreichen FKK-Campingplätzen und -Stränden, besonders in Istrien.",
      },
    },
    {
      "country": "GB",
      "name": "British Naturism (BN)",
      "url": "https://www.britishnaturism.org.uk/",
      "desc": {
        "it": "Il principale organismo britannico del naturismo, fondato nel 1964. Rilascia la tessera BN/INF e promuove spiagge, club e campeggi naturisti nel Regno Unito.",
        "en": "The main British naturism body, founded in 1964. Issues the BN/INF card and promotes naturist beaches, clubs and campsites across the UK.",
        "de": "Das wichtigste britische Naturismusgremium, gegründet 1964. Gibt den BN/INF-Ausweis heraus und fördert Naturistenstrände, -Clubs und -Campingplätze im Vereinigten Königreich.",
      },
    },
    {
      "country": "NL",
      "name": "NFN – Nederlandse Federatie van Naturisten",
      "url": "https://www.naturisme.nl/",
      "desc": {
        "it": "La federazione olandese, con una rete di campeggi e club affiliati nei Paesi Bassi. Rilascia la tessera INF e organizza eventi nazionali.",
        "en": "The Dutch federation, with a network of affiliated campsites and clubs in the Netherlands. Issues the INF card and organises national events.",
        "de": "Der niederländische Verband mit einem Netz angeschlossener Campingplätze und Vereine. Gibt den INF-Ausweis heraus und organisiert nationale Veranstaltungen.",
      },
    },
    {
      "country": "DK",
      "name": "DNF – Dansk Naturist Forbund",
      "url": "https://www.dnf.dk/",
      "desc": {
        "it": "La federazione naturista danese, affiliata INF. Gestisce i club e le strutture naturiste in Danimarca.",
        "en": "The Danish naturist federation, INF-affiliated. Manages naturist clubs and facilities in Denmark.",
        "de": "Der dänische Naturistenverband, INF-Mitglied. Betreibt Naturistenvereine und -Einrichtungen in Dänemark.",
      },
    },
    {
      "country": "PT",
      "name": "FPN – Federação Portuguesa de Naturismo",
      "url": "https://www.naturismo.pt/",
      "desc": {
        "it": "La federazione portoghese, affiliata INF. Il Portogallo ha spiagge naturiste tra le più belle d'Europa, specialmente in Algarve.",
        "en": "The Portuguese federation, INF-affiliated. Portugal has some of Europe's finest naturist beaches, especially in the Algarve.",
        "de": "Der portugiesische Verband, INF-Mitglied. Portugal bietet einige der schönsten Naturistenstrände Europas, besonders an der Algarve.",
      },
    },
    {
      "country": "GR",
      "name": "HNF – Hellenic Naturist Federation",
      "url": "https://www.naturism.gr/",
      "desc": {
        "it": "La federazione greca del naturismo. La Grecia conta numerose spiagge naturiste ufficiali e tolerate, specie sulle isole.",
        "en": "The Greek naturist federation. Greece has numerous official and tolerated naturist beaches, especially on the islands.",
        "de": "Der griechische Naturistenverband. Griechenland hat zahlreiche offizielle und geduldete Naturistenstrände, besonders auf den Inseln.",
      },
    },
  ],
}

def assoc(lang):
    t = T[lang]
    country_names = t["country_names"]
    flag = {"IT": "🇮🇹", "FR": "🇫🇷", "DE": "🇩🇪", "ES": "🇪🇸", "HR": "🇭🇷", "GB": "🇬🇧", "NL": "🇳🇱", "DK": "🇩🇰", "PT": "🇵🇹", "GR": "🇬🇷"}

    int_cards = ""
    for a in ASSOC["international"]:
        int_cards += f'''<div class="assoc-card">
  <div class="assoc-info">
    <h3 class="assoc-name">{e(a["name"])}</h3>
    <p>{e(a["desc"][lang])}</p>
  </div>
  <a class="btn ghost small" href="{e(a["url"])}" rel="nofollow noopener" target="_blank">{e(t["assoc_website"])} ↗</a>
</div>'''

    nat_cards = ""
    for a in ASSOC["national"]:
        c = a["country"]
        country_label = f'{flag.get(c, "")} {country_names.get(c, c)}'
        nat_cards += f'''<div class="assoc-card">
  <div class="assoc-info">
    <span class="assoc-country">{e(country_label)}</span>
    <h3 class="assoc-name">{e(a["name"])}</h3>
    <p>{e(a["desc"][lang])}</p>
  </div>
  <a class="btn ghost small" href="{e(a["url"])}" rel="nofollow noopener" target="_blank">{e(t["assoc_website"])} ↗</a>
</div>'''

    body = f"""<section class="block"><div class="wrap">
  <h1>{e(t['assoc_h1'])}</h1>
  <p class="lead">{e(t['assoc_p'])}</p>
  <h2>{e(t['assoc_int_h2'])}</h2>
  <div class="assoc-grid">{int_cards}</div>
  <h2 style="margin-top:2.5rem">{e(t['assoc_nat_h2'])}</h2>
  <div class="assoc-grid">{nat_cards}</div>
</div></section>"""
    return page(lang, "assoc", f'{t["assoc_h1"]} — NaturCamp Guide', t["assoc_p"], body)

def review(lang):
    t = T[lang]; f = t["f"]
    opts = f'<optgroup label="{e(t["nav"]["camps"])}">' + "".join(f'<option value="camp:{e(c["slug"])}">{e(c["name"])}</option>' for c in sorted(DATA, key=lambda c: c["name"])) + "</optgroup>"
    opts += f'<optgroup label="{e(t["nav"]["beaches"])}">' + "".join(f'<option value="beach:{e(b["slug"])}">{e(b["name"])}</option>' for b in sorted(BEACHES, key=lambda b: b["name"])) + "</optgroup>"
    trips = "".join(f'<option>{e(x)}</option>' for x in f["trips"])
    sel = '<select name="{k}" id="r-{k}" required><option value=""></option>' + "".join(f'<option>{x}</option>' for x in ["1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]) + "</select>"
    ratings = "".join(f'<label for="r-{k}">{e(v)}{sel.format(k=k)}</label>' for k, v in t["criteria"].items())
    rules = "".join(f"<li>{e(r)}</li>" for r in t["rules"])
    body = f"""<section class="block"><div class="wrap">
  <h1>{e(t['review_h1'])}</h1>
  <p class="lead">{e(t['review_p'])}</p>
  <form class="review" method="post" action="{FORM_ACTION}">
    <label for="camp">{e(f['camp'])}<select id="camp" name="camp" required><option value=""></option>{opts}<option value="other">{e(f['camp_other'])}</option></select></label>
    <div class="row">
      <label for="name">{e(f['name'])}<input id="name" name="name" required maxlength="40"></label>
      <label for="email">{e(f['email'])}<input id="email" name="email" type="email" required></label>
    </div>
    <div class="row">
      <label for="when">{e(f['when'])}<input id="when" name="when" type="month" required></label>
      <label for="trip">{e(f['trip'])}<select id="trip" name="trip" required>{trips}</select></label>
      <label for="acc">{e(f['acc'])}<input id="acc" name="accommodation"></label>
    </div>
    <fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;margin-bottom:8px">{e(f['ratings'])}</legend><div class="ratings">{ratings}</div></fieldset>
    <label for="text">{e(f['text'])}<textarea id="text" name="text" minlength="300" required></textarea></label>
    <label for="tip">{e(f['tip'])}<textarea id="tip" name="tip" style="min-height:90px"></textarea></label>
    <label style="grid-template-columns:auto 1fr;align-items:start;font-weight:500"><input type="checkbox" name="consent" required style="min-height:0;width:20px;height:20px;margin-top:4px"> <span>{e(f['consent'])}</span></label>
    <div><button class="btn" type="submit">{e(f['send'])}</button></div>
  </form>
  <div class="rules" style="margin-top:40px;max-width:720px"><h3>{e(t['rules_h3'])}</h3><ul>{rules}</ul></div>
</div></section>"""
    return page(lang, "review", f'{t["review_h1"]} — NaturCamp Guide', t["review_p"], body)

PRIVACY = {
  "it": """<p>Titolare del trattamento: Roberto — <a href="mailto:info@naturcampguide.com">info@naturcampguide.com</a>.</p>
<p><strong>Dati raccolti.</strong> Questo sito non installa cookie di profilazione né sistemi di analisi del traffico. L'unico dato personale raccolto è l'indirizzo e-mail inserito volontariamente nel modulo recensioni. L'e-mail viene utilizzata esclusivamente per verificare l'autenticità della recensione e non viene mai pubblicata né ceduta a terzi.</p>
<p><strong>Servizi terzi.</strong> Il modulo recensioni è gestito da Formspree Inc. (USA). I dati inviati tramite il modulo vengono trasmessi e conservati sui server di Formspree secondo la loro <a href="https://formspree.io/legal/privacy-policy/" rel="nofollow">informativa sulla privacy</a>. Le mappe interattive utilizzano OpenStreetMap (dati © <a href="https://www.openstreetmap.org/copyright" rel="nofollow">OpenStreetMap contributors</a>). I link alle previsioni meteo aprono yr.no (MET Norway), sito esterno.</p>
<p><strong>Diritti dell'interessato.</strong> Puoi richiedere in qualsiasi momento la cancellazione dei dati inviati scrivendo a <a href="mailto:info@naturcampguide.com">info@naturcampguide.com</a>. Hai inoltre il diritto di accesso, rettifica, limitazione del trattamento e portabilità ai sensi del Regolamento UE 2016/679 (GDPR).</p>
<p><small>Informativa aggiornata al 2026.</small></p>""",
  "en": """<p>Data controller: Roberto — <a href="mailto:info@naturcampguide.com">info@naturcampguide.com</a>.</p>
<p><strong>Data collected.</strong> This site does not use tracking cookies or traffic-analysis tools. The only personal data collected is the e-mail address voluntarily entered in the review form. It is used solely to verify the authenticity of the review and is never published or shared with third parties.</p>
<p><strong>Third-party services.</strong> The review form is handled by Formspree Inc. (USA). Data submitted through the form is transmitted to and stored on Formspree's servers under their <a href="https://formspree.io/legal/privacy-policy/" rel="nofollow">privacy policy</a>. Interactive maps use OpenStreetMap (data © <a href="https://www.openstreetmap.org/copyright" rel="nofollow">OpenStreetMap contributors</a>). Weather forecast links open yr.no (MET Norway), an external site.</p>
<p><strong>Your rights.</strong> You may request deletion of any data you have submitted by writing to <a href="mailto:info@naturcampguide.com">info@naturcampguide.com</a>. You also have the right of access, rectification, restriction of processing and data portability under EU Regulation 2016/679 (GDPR).</p>
<p><small>Privacy policy last updated 2026.</small></p>""",
  "de": """<p>Verantwortlicher: Roberto — <a href="mailto:info@naturcampguide.com">info@naturcampguide.com</a>.</p>
<p><strong>Erhobene Daten.</strong> Diese Website verwendet keine Tracking-Cookies oder Analysetools. Die einzige erhobene personenbezogene Information ist die E-Mail-Adresse, die freiwillig im Bewertungsformular angegeben wird. Sie wird ausschließlich zur Überprüfung der Echtheit der Bewertung verwendet und wird weder veröffentlicht noch an Dritte weitergegeben.</p>
<p><strong>Drittanbieter.</strong> Das Bewertungsformular wird von Formspree Inc. (USA) verwaltet. Über das Formular übermittelte Daten werden gemäß deren <a href="https://formspree.io/legal/privacy-policy/" rel="nofollow">Datenschutzrichtlinie</a> auf Formspree-Servern gespeichert. Interaktive Karten verwenden OpenStreetMap (Daten © <a href="https://www.openstreetmap.org/copyright" rel="nofollow">OpenStreetMap contributors</a>). Wettervorschau-Links öffnen yr.no (MET Norway), eine externe Website.</p>
<p><strong>Ihre Rechte.</strong> Sie können jederzeit die Löschung übermittelter Daten unter <a href="mailto:info@naturcampguide.com">info@naturcampguide.com</a> beantragen. Darüber hinaus haben Sie gemäß EU-Verordnung 2016/679 (DSGVO) das Recht auf Auskunft, Berichtigung, Einschränkung der Verarbeitung und Datenübertragbarkeit.</p>
<p><small>Datenschutzerklärung zuletzt aktualisiert 2026.</small></p>""",
}

def privacy_block(lang):
    return PRIVACY[lang]

def about(lang):
    t = T[lang]
    body = f"""<section class="block"><div class="wrap">
  <h1>{e(t['about_h1'])}</h1>
  <p class="lead">{e(t['about_p1'])}</p>
  <p>{e(t['about_p2'])}</p>
  <p>{e(t['about_p3'])}<a href="mailto:{CONTACT}">{CONTACT}</a></p>
</div></section>
<section class="block privacy-section" id="privacy"><div class="wrap">
  <h2 class="privacy-h2">{e(t['privacy'])}</h2>
  <div class="privacy-body">{privacy_block(lang)}</div>
</div></section>"""
    return page(lang, "about", f'{t["about_h1"]} — NaturCamp Guide', t["about_p1"], body)

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def main():
    for lang in LANGS:
        shutil.rmtree(ROOT / lang, ignore_errors=True)
    assets = ROOT / "assets"; assets.mkdir(exist_ok=True)
    for name in ("style.css", "logo.svg", "favicon.svg"):
        shutil.copy(ROOT / "src" / name, assets / name)
    for lang in LANGS:
        p = T[lang]["paths"]
        write(ROOT / lang / "index.html", home(lang))
        write(ROOT / lang / p["camps"] / "index.html", camps(lang))
        write(ROOT / lang / p["review"] / "index.html", review(lang))
        write(ROOT / lang / p["about"] / "index.html", about(lang))
        write(ROOT / lang / p["pack"] / "index.html", pack(lang))
        write(ROOT / lang / p["assoc"] / "index.html", assoc(lang))
        for c in DATA:
            write(ROOT / lang / p["camps"] / c["slug"] / "index.html", sheet(c, lang))
        write(ROOT / lang / p["beaches"] / "index.html", beaches(lang))
        for b in BEACHES:
            write(ROOT / lang / p["beaches"] / b["slug"] / "index.html", beach_sheet(b, lang))
    # Pagina radice: sceglie la lingua del browser, altrimenti inglese
    write(ROOT / "index.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>NaturCamp Guide</title>
<meta name="robots" content="noindex">
<link rel="alternate" hreflang="it" href="%s/it/"><link rel="alternate" hreflang="en" href="%s/en/"><link rel="alternate" hreflang="de" href="%s/de/">
<script>var l=(navigator.language||"en").slice(0,2);location.replace(["it","de"].indexOf(l)>-1?"/"+l+"/":"/en/");</script>
</head><body><p><a href="/it/">Italiano</a> · <a href="/en/">English</a> · <a href="/de/">Deutsch</a></p></body></html>
""" % (SITE, SITE, SITE))
    write(ROOT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = []
    for lang in LANGS:
        urls += [lang_url(lang, k) for k in ("home", "camps", "beaches", "pack", "review", "about", "assoc")]
        urls += [lang_url(lang, "camp", c["slug"]) for c in DATA]
        urls += [lang_url(lang, "beach", b["slug"]) for b in BEACHES]
    write(ROOT / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    print(f"Generato: {len(LANGS)} lingue, {len(DATA)} campeggi, {len(BEACHES)} spiagge, {len(urls)} pagine.")

if __name__ == "__main__":
    main()
