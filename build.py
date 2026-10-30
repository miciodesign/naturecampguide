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
    "nav": {"camps": "Campeggi", "beaches": "Spiagge", "pack": "Cosa portare", "review": "Scrivi una recensione", "about": "Chi siamo", "assoc": "Associazioni", "articles": "Articoli"},
    "paths": {"camps": "campeggi", "beaches": "spiagge", "pack": "cosa-portare", "review": "recensioni", "about": "chi-siamo", "assoc": "associazioni", "articles": "articoli"},
    "articles_h1": "Articoli", "articles_p": "Guide, consigli pratici e approfondimenti sul naturismo in Europa.",
    "articles_home_h2": "Ultimi articoli", "articles_home_cta": "Tutti gli articoli",
    "articles_read": "Leggi l'articolo", "articles_min_read": "min di lettura",
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
    "facts_h2": "Dati essenziali", "criteria_h2": "I nostri voti", "verdict_h2": "Il nostro giudizio", "how_to_reach_h2": "Come arrivare e informazioni pratiche",
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
    "nav": {"camps": "Campsites", "beaches": "Beaches", "pack": "What to pack", "review": "Write a review", "about": "About", "assoc": "Associations", "articles": "Articles"},
    "paths": {"camps": "campsites", "beaches": "beaches", "pack": "what-to-pack", "review": "reviews", "about": "about", "assoc": "associations", "articles": "articles"},
    "articles_h1": "Articles", "articles_p": "Guides, practical tips and in-depth pieces on naturism in Europe.",
    "articles_home_h2": "Latest articles", "articles_home_cta": "All articles",
    "articles_read": "Read article", "articles_min_read": "min read",
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
    "facts_h2": "Key facts", "criteria_h2": "Our scores", "verdict_h2": "Our verdict", "how_to_reach_h2": "How to get there and practical information",
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
    "nav": {"camps": "Campingplätze", "beaches": "Strände", "pack": "Packliste", "review": "Bewertung schreiben", "about": "Über uns", "assoc": "Verbände", "articles": "Artikel"},
    "paths": {"camps": "campingplaetze", "beaches": "straende", "pack": "packliste", "review": "bewertungen", "about": "ueber-uns", "assoc": "verbaende", "articles": "artikel"},
    "articles_h1": "Artikel", "articles_p": "Ratgeber, praktische Tipps und Hintergrundartikel zum Naturismus in Europa.",
    "articles_home_h2": "Neueste Artikel", "articles_home_cta": "Alle Artikel",
    "articles_read": "Artikel lesen", "articles_min_read": "Min. Lesezeit",
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
    "facts_h2": "Eckdaten", "criteria_h2": "Unsere Noten", "verdict_h2": "Unser Urteil", "how_to_reach_h2": "Anreise und praktische Informationen",
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
    if kind == "article": return f"/{lang}/{p['articles']}/{slug}/"
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
    return f'''<h2>{e(t["stay_h2"])}</h2>
<p class="meta">{e(t["stay_p"])}</p>
<iframe src="https://www.stay22.com/embed/gm?aid={STAY22_AID}&lat={lat}&lng={lon}&zoom=12&language={lang}" width="100%" height="420" frameborder="0" loading="lazy" style="border-radius:10px;margin-top:8px;display:block" title="{e(t['stay_h2'])}"></iframe>'''

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
    nav = "\n".join(f'<a href="{lang_url(lang, k)}">{e(t["nav"][k])}</a>' for k in ("about", "camps", "beaches", "pack", "review", "assoc", "articles"))
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
    arts_path = t["paths"]["articles"]
    art_cards = "".join(
        f'<article class="article-card">'
        f'<div class="article-meta"><time>{a["date"]}</time> · <span>{a["min_read"]} {e(t["articles_min_read"])}</span></div>'
        f'<h3 class="article-title"><a href="/{lang}/{arts_path}/{a["slug"]}/">{e(a["title"][lang])}</a></h3>'
        f'<p>{e(a["summary"][lang])}</p>'
        f'</article>'
        for a in ARTICLES[:3]
    )
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
<section class="block articles-home"><div class="wrap"><h2>{e(t['articles_home_h2'])}</h2><div class="articles-grid">{art_cards}</div><p style="margin-top:20px"><a class="btn ghost" href="{lang_url(lang, 'articles')}">{e(t['articles_home_cta'])}</a></p></div></section>
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
  {(f'<div class="beach-description"><h2>{e(t.get("how_to_reach_h2", "Come arrivare e informazioni pratiche"))}</h2><p>{e(b["description"][lang])}</p></div>') if b.get("description") else ""}
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

# ---------------------------------------------------------------- articoli
ARTICLES = [
  {
    "slug": "primo-campeggio-naturista",
    "date": "2026-10-20",
    "min_read": 7,
    "title": {
      "it": "Come prepararsi per il primo campeggio naturista",
      "en": "How to prepare for your first naturist campsite",
      "de": "So bereiten Sie sich auf Ihren ersten FKK-Campingplatz vor",
    },
    "summary": {
      "it": "La prima volta in un campeggio naturista mette un po' di agitazione, è normale. Ecco cosa aspettarsi davvero, cosa portare e come comportarsi per sentirsi subito a proprio agio.",
      "en": "A first visit to a naturist campsite brings a little nervousness — that is perfectly normal. Here is what to genuinely expect, what to bring and how to behave so you feel at ease straight away.",
      "de": "Ein erster Besuch auf einem FKK-Campingplatz sorgt für etwas Aufregung — das ist völlig normal. Hier erfahren Sie, was Sie wirklich erwartet, was Sie mitnehmen sollten und wie Sie sich verhalten, damit Sie sich sofort wohlfühlen.",
    },
    "body": {
      "it": """<p class="lead">La prima volta in un campeggio naturista mette un po' di agitazione, è normale. Tutti i naturisti esperti ci sono passati. La buona notizia è che i campeggi naturisti sono ambienti accoglienti, con regole chiare e una buona dose di normalità.</p>

<h2>Cosa aspettarsi davvero</h2>
<p>Il primo impatto è quasi sempre lo stesso: dieci minuti dopo essere arrivati, nessuno pensa più ai vestiti. L'atmosfera è rilassata, le persone sono lì per campeggiare e godersi la natura, non per giudicare gli altri. Troverai famiglie, coppie, persone sole, pensionati e giovani — un mix che non vedi in molti altri posti.</p>
<p>Le regole non scritte sono poche ma importanti: si siede sempre su un proprio telo (anche al bar o in piscina), si rispetta la privacy degli altri senza fissare, e si indossa qualcosa quando si entra nelle aree ristorante o nei negozi del campeggio. Tutto il resto è normale campeggio.</p>

<h2>Il telo: la regola numero uno</h2>
<p>Il telo personale è l'unica cosa veramente obbligatoria nei campeggi naturisti. Si porta sempre con sé e si mette sotto di sé prima di sedersi su qualsiasi superficie comune: sdraio, panchina, sedia del bar. Non è una questione di igiene eccessiva: è semplicemente la norma condivisa che rende possibile la convivenza.</p>
<p>Porta due o tre teli di diversa dimensione: uno grande per la spiaggia o la piscina, uno medio per il camping, uno piccolo da tenere in borsa per i posti imprevisti.</p>

<h2>La tessera naturista</h2>
<p>Molti campeggi in Italia, Germania e Austria richiedono la tessera INF (International Naturist Federation). La si ottiene dalla federazione del proprio paese — FENAIT per l'Italia — pagando una quota annuale. Vale quasi ovunque in Europa ed è spesso il modo più economico di entrare in un campeggio affiliato.</p>
<p>Se non ce l'hai per il primo viaggio, molti campeggi vendono una tessera giornaliera o settimanale all'ingresso. Controlla sempre prima di partire sul sito del campeggio.</p>

<h2>Cosa portare (e cosa non serve)</h2>
<p>La valigia è più leggera del solito: niente costumi, pochi vestiti serali. Quello che serve davvero: crema solare ad alta protezione (le parti che non hanno mai preso il sole si scottano facilmente), sandali per docce e vialetti caldi, un pareo o kimono leggero per i momenti in cui coprirsi è richiesto o preferito.</p>
<p>Per la spiaggia: ombrellone con picchetto a vite se prevedi vento, scarpette da scoglio se vai in Istria o in Liguria, borraccia termica perché molte spiagge naturiste sono lontane dai servizi.</p>

<h2>Come comportarsi (e cosa non fare)</h2>
<p>La regola più semplice: tratta gli altri come vorresti essere trattato. Non fissare, non fare foto senza il consenso esplicito di tutti i presenti, non fare commenti sul corpo di nessuno — né positivi né negativi. Le fotografie sono il punto più delicato: in quasi tutti i campeggi naturisti è vietato fotografare persone, anche di sfuggita, senza consenso.</p>
<p>Il naturismo non è una pratica sessuale: qualsiasi comportamento sessuale in pubblico è vietato ovunque e porta all'espulsione immediata. I campeggi naturisti sono ambienti familiari e questo confine è preso molto sul serio.</p>

<h2>Il momento del "svestirsi"</h2>
<p>Non c'è un momento preciso in cui togliersi i vestiti. Alcuni lo fanno subito arrivando, altri aspettano di essere sistemati in piazzola, altri ancora cominciano dalla spiaggia o dalla piscina. Nessuno ti guarda. Fai come ti senti: se hai bisogno di qualche ora per ambientarti, prendila. I campeggi naturisti non sono rigidi su questo punto — l'obiettivo è che tu ti senta a tuo agio, non che rispetti un cerimoniale.</p>

<h2>Dove andare per la prima volta</h2>
<p>I campeggi grandi e organizzati, come quelli in Istria (Valalta, Koversada) o nelle Landes francesi (Euronat, CHM Montalivet), sono ideali per il debutto: strutture complete, molto personale abituato ai nuovi arrivati, atmosfera internazionale. I campeggi piccoli e isolati sono più intimi ma possono sembrare meno accessibili se non conosci ancora il mondo naturista.</p>
<p>Guarda le schede nella nostra guida: ogni campeggio ha un giudizio specifico su quanto è adatto ai principianti.</p>""",
      "en": """<p class="lead">A first visit to a naturist campsite brings a little nervousness — that is perfectly normal. Every experienced naturist has been there. The good news is that naturist campsites are welcoming places with clear rules and a healthy dose of normality.</p>

<h2>What to genuinely expect</h2>
<p>The first impression is almost always the same: ten minutes after arriving, nobody is thinking about clothes any more. The atmosphere is relaxed; people are there to camp and enjoy nature, not to judge anyone. You will find families, couples, solo travellers, retirees and young people — a mix you rarely see elsewhere.</p>
<p>The unwritten rules are few but important: always sit on your own towel (even at the bar or pool), respect others' privacy without staring, and wear something when entering restaurant areas or the campsite shop. Everything else is normal camping.</p>

<h2>The towel: rule number one</h2>
<p>A personal towel is the one truly compulsory item at naturist campsites. Carry it everywhere and place it under you before sitting on any shared surface: a sun lounger, a bench, a bar chair. It is not excessive hygiene — it is simply the shared norm that makes coexistence possible.</p>
<p>Bring two or three towels of different sizes: a large one for the beach or pool, a medium one for the pitch, a small one for unexpected moments.</p>

<h2>The naturist card</h2>
<p>Many campsites in Italy, Germany and Austria require the INF (International Naturist Federation) card. You get it from your national federation — British Naturism in the UK — for an annual fee. It is recognised almost everywhere in Europe and is often the cheapest way into an affiliated campsite.</p>
<p>If you do not have one for your first trip, many campsites sell a day or week pass at the gate. Always check the campsite's website before you leave.</p>

<h2>What to pack (and what you do not need)</h2>
<p>Your bag is lighter than usual: no swimwear needed, few evening clothes. What you really need: high-factor sun cream (parts of your body that have never seen sun burn easily), sandals for showers and hot paths, a pareo or light kimono for moments when covering up is required or preferred.</p>
<p>For the beach: a corkscrew-stake umbrella if you expect wind, water shoes if you are going to Istria or rocky coasts, a thermal water bottle because many naturist beaches are far from facilities.</p>

<h2>How to behave (and what not to do)</h2>
<p>The simplest rule: treat others as you would like to be treated. Do not stare, do not take photographs without the explicit consent of everyone in the frame, do not comment on anyone's body — neither positively nor negatively. Photography is the most sensitive point: at almost all naturist campsites it is forbidden to photograph people, even in passing, without consent.</p>
<p>Naturism is not a sexual practice: any sexual behaviour in public is forbidden everywhere and leads to immediate expulsion. Naturist campsites are family environments and this boundary is taken very seriously.</p>

<h2>The moment of undressing</h2>
<p>There is no precise moment to take your clothes off. Some people do it as soon as they arrive, others wait until they are settled on their pitch, others start at the beach or pool. Nobody is watching. Do what feels right: if you need an hour or two to settle in, take it. Naturist campsites are not rigid about this — the goal is that you feel comfortable, not that you follow a ceremony.</p>

<h2>Where to go for a first visit</h2>
<p>Large, well-organised campsites — such as those in Istria (Valalta, Koversada) or in the French Landes (Euronat, CHM Montalivet) — are ideal for a first trip: full facilities, plenty of staff used to newcomers, international atmosphere. Small and remote campsites are more intimate but can feel less accessible if you do not yet know the naturist world.</p>
<p>Check the listings in our guide: each campsite has a specific rating for how beginner-friendly it is.</p>""",
      "de": """<p class="lead">Ein erster Besuch auf einem FKK-Campingplatz sorgt für etwas Aufregung — das ist völlig normal. Jeder erfahrene Naturist hat das hinter sich. Die gute Nachricht: Naturistencampingplätze sind einladende Orte mit klaren Regeln und einer gesunden Portion Normalität.</p>

<h2>Was Sie wirklich erwartet</h2>
<p>Der erste Eindruck ist fast immer gleich: Zehn Minuten nach der Ankunft denkt niemand mehr an Kleidung. Die Atmosphäre ist entspannt; die Menschen sind dort, um zu zelten und die Natur zu genießen — nicht um andere zu beurteilen. Sie finden Familien, Paare, Alleinreisende, Rentner und junge Menschen — eine Mischung, die man selten woanders sieht.</p>
<p>Die ungeschriebenen Regeln sind wenige, aber wichtig: Immer auf dem eigenen Handtuch sitzen (auch an der Bar oder am Pool), die Privatsphäre anderer durch Nichtanstarren respektieren, und etwas anziehen, wenn man den Restaurantbereich oder den Campingshop betritt. Alles andere ist normales Camping.</p>

<h2>Das Handtuch: Regel Nummer eins</h2>
<p>Ein persönliches Handtuch ist das einzige wirklich obligatorische Utensil auf Naturistencampingplätzen. Immer dabei haben und vor dem Hinsetzen auf jede gemeinsame Fläche darunter legen: Liegestuhl, Bank, Barstuhl. Das ist keine übertriebene Hygiene — es ist einfach die gemeinsame Norm, die ein gutes Miteinander ermöglicht.</p>
<p>Bringen Sie zwei bis drei Handtücher verschiedener Größen mit: ein großes für Strand oder Pool, ein mittleres für den Stellplatz, ein kleines für unvorhergesehene Momente.</p>

<h2>Der Naturistenausweis</h2>
<p>Viele Campingplätze in Italien, Deutschland und Österreich verlangen den INF-Ausweis (International Naturist Federation). Man erhält ihn beim eigenen nationalen Verband — in Deutschland beim DFK — gegen eine Jahresgebühr. Er wird fast überall in Europa anerkannt und ist oft der günstigste Weg auf einen angeschlossenen Campingplatz.</p>
<p>Wenn Sie ihn für die erste Reise noch nicht haben: Viele Campingplätze verkaufen Tages- oder Wochenkarten am Eingang. Prüfen Sie das immer vorher auf der Website des Campingplatzes.</p>

<h2>Was einpacken (und was nicht nötig ist)</h2>
<p>Die Tasche ist leichter als sonst: kein Badeanzug, wenig Abendkleidung. Was wirklich gebraucht wird: Sonnencreme mit hohem Lichtschutzfaktor (Körperstellen, die nie Sonne gesehen haben, verbrennen leicht), Sandalen für Duschen und heiße Wege, ein Pareo oder leichter Kimono für Momente, in denen Bedeckung erforderlich oder bevorzugt ist.</p>
<p>Für den Strand: Sonnenschirm mit Schraubhering bei erwartetem Wind, Badeschuhe für Istrien oder Felsenküsten, eine Thermotrinkflasche, da viele Naturistenstrände weit von der Infrastruktur entfernt liegen.</p>

<h2>Wie man sich verhält (und was man nicht tut)</h2>
<p>Die einfachste Regel: Behandeln Sie andere so, wie Sie selbst behandelt werden möchten. Nicht anstarren, keine Fotos ohne ausdrückliche Zustimmung aller Abgebildeten machen, keine Kommentare zum Körper anderer — weder positiv noch negativ. Fotografieren ist der heikelste Punkt: Auf fast allen Naturistencampingplätzen ist es verboten, Menschen auch nur im Vorbeigehen ohne Einwilligung zu fotografieren.</p>
<p>Naturismus ist keine sexuelle Praxis: Jedes sexuelle Verhalten in der Öffentlichkeit ist überall verboten und führt zur sofortigen Verweisung des Platzes. Naturistencampingplätze sind Familienumgebungen, und diese Grenze wird sehr ernst genommen.</p>

<h2>Der Moment des Ausziehens</h2>
<p>Es gibt keinen genauen Zeitpunkt, die Kleidung abzulegen. Manche tun es sofort bei der Ankunft, andere warten, bis sie auf dem Stellplatz eingerichtet sind, wieder andere beginnen am Strand oder Pool. Niemand schaut zu. Tun Sie, was sich richtig anfühlt: Wenn Sie ein oder zwei Stunden Eingewöhnungszeit brauchen, nehmen Sie sie sich. Naturistencampingplätze sind in diesem Punkt nicht starr — das Ziel ist, dass Sie sich wohlfühlen, nicht dass Sie ein Ritual befolgen.</p>

<h2>Wohin für den ersten Besuch</h2>
<p>Große, gut organisierte Campingplätze — wie in Istrien (Valalta, Koversada) oder in den französischen Landes (Euronat, CHM Montalivet) — sind ideal für den Einstieg: vollständige Ausstattung, viel Personal, das Neulinge kennt, internationale Atmosphäre. Kleine und abgelegene Campingplätze sind intimer, können aber weniger zugänglich wirken, wenn man die Naturistenwelt noch nicht kennt.</p>
<p>Schauen Sie in die Einträge unseres Führers: Jeder Campingplatz hat eine spezifische Bewertung für die Eignung für Einsteiger.</p>""",
    },
  },
  {
    "slug": "spiagge-naturiste-europa",
    "date": "2026-10-18",
    "min_read": 6,
    "title": {
      "it": "Le 10 spiagge naturiste più belle d'Europa",
      "en": "The 10 most beautiful naturist beaches in Europe",
      "de": "Die 10 schönsten Naturistenstrände Europas",
    },
    "summary": {
      "it": "Dall'Algarve all'Istria, dalla Sardegna alle Landes: una selezione delle spiagge naturiste europee più spettacolari per paesaggio, acque e atmosfera.",
      "en": "From the Algarve to Istria, from Sardinia to the Landes: a selection of the most spectacular naturist beaches in Europe for scenery, water and atmosphere.",
      "de": "Von der Algarve bis Istrien, von Sardinien bis zu den Landes: eine Auswahl der spektakulärsten Naturistenstrände Europas nach Landschaft, Wasser und Atmosphäre.",
    },
    "body": {
      "it": """<p class="lead">L'Europa ha alcune delle spiagge naturiste più belle al mondo. Alcune sono ufficiali e segnalate, altre tollerate e frequentate da decenni. Questa selezione privilegia il paesaggio, la qualità dell'acqua e l'atmosfera — non la vicinanza ai campeggi.</p>

<h2>1. Praia do Barril, Algarve (Portogallo)</h2>
<p>Una delle spiagge più suggestive dell'Algarve: si raggiunge a piedi attraverso una riserva naturale, il che significa pochi turisti e molta natura. La sabbia è fine, il mare è cristallino, le dune proteggono dal vento. Ufficialmente nudista per un lungo tratto.</p>

<h2>2. Plage de l'Horizon, Landes (Francia)</h2>
<p>Nel cuore della foresta atlantica delle Landes, questa spiaggia fa parte del comprensorio di CHM Montalivet, il primo campeggio naturista del mondo (1950). Chilometri di sabbia atlantica, onde grandi, pinete profumate. Solo per frequentatori del campeggio adiacente.</p>

<h2>3. Punta Molentis, Sardegna (Italia)</h2>
<p>Una piccola baia di granito rosa tra Villasimius e Capo Carbonara, raggiungibile solo a piedi o in barca. Acqua turchese, scogli bassi, pochissimi turisti nella prima parte della stagione. Tollerata da anni senza problemi.</p>

<h2>4. Isola delle Femmine, Sicilia (Italia)</h2>
<p>La spiaggia nord dell'isola, di fronte alla riserva marina, è uno dei posti più belli per fare il bagno nudi in Italia. Le acque sono protette, la riserva tiene lontano il turismo di massa. Tollerata senza problemi.</p>

<h2>5. Koversada, Istria (Croazia)</h2>
<p>La spiaggia del campeggio Koversada è su un'isola collegata da un pontile: fondo misto di sabbia e scogli, mare adriatico limpido, pini a pochi metri dall'acqua. Uno dei posti più iconici del naturismo europeo.</p>

<h2>6. Playa de Vera, Almería (Spagna)</h2>
<p>Una delle spiagge nudiste più lunghe d'Europa (oltre 20 km) e ufficialmente designata. Il paesaggio desertico alle spalle, il Mediterraneo davanti, e un'infrastruttura turistica sviluppata per chi vuole servizi. Ideale per chi viene dall'Europa del nord abituata al sole scarso.</p>

<h2>7. Schwarzsee, FKK-Strand, Carinzia (Austria)</h2>
<p>Un lago di montagna a oltre 1.000 metri, con acqua insolitamente calda per l'altitudine. La zona FKK è ben delimitata e molto rispettata. Il paesaggio delle Alpi carinziane è spettacolare.</p>

<h2>8. Guvano, Cinque Terre (Italia)</h2>
<p>Una delle spiagge più famose e più difficili da raggiungere d'Italia: solo a piedi attraverso un tunnel abbandonato. Il Mediterraneo ligure, le scogliere verticali, nessuna struttura. Tollerata da decenni ma soggetta ogni anno a incertezze normative.</p>

<h2>9. Cap d'Agde, Hérault (Francia)</h2>
<p>La "città naturista" più grande al mondo: una vera città con negozi, ristoranti, hotel e chilometri di spiaggia. Non è la scelta più solitaria, ma l'infrastruttura e l'atmosfera sono uniche. Ideale per chi vuole sperimentare il naturismo con tutti i comfort.</p>

<h2>10. Kanegra, Istria (Slovenia)</h2>
<p>La spiaggia del campeggio Adria vicino a Portorož: una lunga striscia di ghiaino e scogliera affacciata sul Golfo di Trieste. Meno frequentata delle spiagge istriane croate, molto amata dai frequentatori di lungo corso.</p>

<p style="margin-top:2rem"><em>Queste spiagge sono descritte nella nostra guida con voti dettagliati e informazioni pratiche aggiornate.</em></p>""",
      "en": """<p class="lead">Europe has some of the most beautiful naturist beaches in the world. Some are official and signposted; others have been tolerated for decades. This selection prioritises scenery, water quality and atmosphere — not proximity to campsites.</p>

<h2>1. Praia do Barril, Algarve (Portugal)</h2>
<p>One of the most evocative beaches on the Algarve: reached on foot through a nature reserve, which means few tourists and plenty of nature. Fine sand, crystal-clear water, dunes that shelter from the wind. Officially nudist for a long stretch.</p>

<h2>2. Plage de l'Horizon, Landes (France)</h2>
<p>In the heart of the Atlantic Landes forest, this beach is part of the CHM Montalivet complex — the world's first naturist campsite (1950). Miles of Atlantic sand, big waves, fragrant pine forests. For guests of the adjacent campsite only.</p>

<h2>3. Punta Molentis, Sardinia (Italy)</h2>
<p>A small pink granite cove between Villasimius and Capo Carbonara, reachable only on foot or by boat. Turquoise water, low rocks, very few tourists in the early season. Tolerated for years without issue.</p>

<h2>4. Isola delle Femmine, Sicily (Italy)</h2>
<p>The northern beach of this island, facing the marine reserve, is one of the best places for nude bathing in Italy. The protected waters keep mass tourism at bay. Long tolerated without incident.</p>

<h2>5. Koversada, Istria (Croatia)</h2>
<p>The beach at Koversada campsite sits on an island connected by a jetty: mixed sand and rock, clear Adriatic water, pines a few metres from the water. One of the most iconic spots in European naturism.</p>

<h2>6. Playa de Vera, Almería (Spain)</h2>
<p>One of the longest officially designated nudist beaches in Europe (over 20 km). Desert landscape behind, Mediterranean in front, and a well-developed tourist infrastructure for those who want facilities. Ideal for northern Europeans accustomed to limited sun.</p>

<h2>7. Schwarzsee FKK-Strand, Carinthia (Austria)</h2>
<p>A mountain lake above 1,000 metres with unusually warm water for the altitude. The FKK area is well marked and widely respected. The Carinthian Alpine scenery is spectacular.</p>

<h2>8. Guvano, Cinque Terre (Italy)</h2>
<p>One of Italy's most famous and most difficult beaches to reach: on foot only, through an abandoned tunnel. The Ligurian Mediterranean, vertical cliffs, no facilities. Tolerated for decades but subject to annual regulatory uncertainty.</p>

<h2>9. Cap d'Agde, Hérault (France)</h2>
<p>The world's largest naturist "town": a real village with shops, restaurants, hotels and miles of beach. Not the most solitary choice, but the infrastructure and atmosphere are unique. Ideal for those who want to experience naturism with all mod cons.</p>

<h2>10. Kanegra, Istria (Slovenia)</h2>
<p>The beach at Adria campsite near Portorož: a long stretch of shingle and rock facing the Gulf of Trieste. Less crowded than the Croatian Istrian beaches, very much loved by long-standing visitors.</p>

<p style="margin-top:2rem"><em>These beaches are described in our guide with detailed ratings and up-to-date practical information.</em></p>""",
      "de": """<p class="lead">Europa hat einige der schönsten Naturistenstrände der Welt. Manche sind offiziell und ausgeschildert; andere werden seit Jahrzehnten geduldet. Diese Auswahl priorisiert Landschaft, Wasserqualität und Atmosphäre — nicht die Nähe zu Campingplätzen.</p>

<h2>1. Praia do Barril, Algarve (Portugal)</h2>
<p>Einer der eindrucksvollsten Strände der Algarve: nur zu Fuß durch ein Naturschutzgebiet erreichbar, was wenige Touristen und viel Natur bedeutet. Feiner Sand, kristallklares Wasser, Dünen als Windschutz. Auf einer langen Strecke offiziell als Nudistenstrand ausgewiesen.</p>

<h2>2. Plage de l'Horizon, Landes (Frankreich)</h2>
<p>Im Herzen des atlantischen Landesdwaldes liegt dieser Strand zum CHM Montalivet-Komplex — dem ersten Naturistencampingplatz der Welt (1950). Kilometerlanger Atlantiksand, große Wellen, duftende Pinienwälder. Nur für Gäste des angrenzenden Campingplatzes.</p>

<h2>3. Punta Molentis, Sardinien (Italien)</h2>
<p>Eine kleine rosa Granitbucht zwischen Villasimius und Capo Carbonara, nur zu Fuß oder per Boot erreichbar. Türkisfarbenes Wasser, flache Felsen, sehr wenige Touristen in der Vorsaison. Seit Jahren problemlos geduldet.</p>

<h2>4. Isola delle Femmine, Sizilien (Italien)</h2>
<p>Der Nordstrand dieser Insel gegenüber dem Meeresschutzgebiet ist einer der schönsten Plätze zum Nacktbaden in Italien. Die geschützten Gewässer halten Massentourismus fern. Seit Langem problemlos geduldet.</p>

<h2>5. Koversada, Istrien (Kroatien)</h2>
<p>Der Strand des Campingplatzes Koversada liegt auf einer Insel, die durch einen Steg verbunden ist: gemischter Sand-Fels-Untergrund, klares Adriatikwasser, Pinien wenige Meter vom Wasser. Einer der ikonischsten Orte des europäischen Naturismus.</p>

<h2>6. Playa de Vera, Almería (Spanien)</h2>
<p>Einer der längsten offiziell ausgewiesenen Nudistenstrände Europas (über 20 km). Wüstenlandschaft im Hinterland, Mittelmeer davor und eine gut entwickelte touristische Infrastruktur für alle, die Annehmlichkeiten wünschen. Ideal für Nordeuropäer, die wenig Sonne gewohnt sind.</p>

<h2>7. Schwarzsee FKK-Strand, Kärnten (Österreich)</h2>
<p>Ein Bergsee auf über 1.000 Metern mit ungewöhnlich warmem Wasser für diese Höhenlage. Der FKK-Bereich ist gut ausgeschildert und wird respektiert. Die Kärntner Alpenlandschaft ist spektakulär.</p>

<h2>8. Guvano, Cinque Terre (Italien)</h2>
<p>Einer der bekanntesten und am schwierigsten erreichbaren Strände Italiens: nur zu Fuß durch einen verlassenen Tunnel. Das ligurische Mittelmeer, senkrechte Klippen, keine Einrichtungen. Seit Jahrzehnten geduldet, aber jedes Jahr normativer Unsicherheit ausgesetzt.</p>

<h2>9. Cap d'Agde, Hérault (Frankreich)</h2>
<p>Die größte Naturisten-„Stadt" der Welt: ein echtes Dorf mit Geschäften, Restaurants, Hotels und kilometerlangem Strand. Nicht die einsamste Wahl, aber Infrastruktur und Atmosphäre sind einzigartig. Ideal für alle, die Naturismus mit allem Komfort erleben möchten.</p>

<h2>10. Kanegra, Istrien (Slowenien)</h2>
<p>Der Strand des Campingplatzes Adria bei Portorož: ein langer Streifen aus Kies und Fels mit Blick auf den Golf von Triest. Weniger frequentiert als die kroatisch-istrischen Strände, sehr beliebt bei Stammbesuchern.</p>

<p style="margin-top:2rem"><em>Diese Strände werden in unserem Führer mit detaillierten Bewertungen und aktuellen praktischen Informationen beschrieben.</em></p>""",
    },
  },
  {
    "slug": "naturismo-famiglia",
    "date": "2026-10-15",
    "min_read": 5,
    "title": {
      "it": "Naturismo in famiglia: guida pratica",
      "en": "Family naturism: a practical guide",
      "de": "Familien-Naturismus: ein praktischer Leitfaden",
    },
    "summary": {
      "it": "Portare i bambini in un campeggio naturista è più semplice di quanto sembri. I bambini si adattano facilmente — spesso meglio degli adulti. Ecco come prepararsi e cosa scegliere.",
      "en": "Taking children to a naturist campsite is simpler than it might seem. Children adapt easily — often better than adults. Here is how to prepare and what to choose.",
      "de": "Kinder auf einen Naturistencampingplatz mitzunehmen ist einfacher als es scheint. Kinder passen sich leicht an — oft besser als Erwachsene. So bereiten Sie sich vor und treffen die richtige Wahl.",
    },
    "body": {
      "it": """<p class="lead">Il naturismo è una delle vacanze più adatte alle famiglie che esistano. I bambini sono liberi, c'è spazio, i campeggi sono sicuri e la comunità è accogliente. L'unico ostacolo è spesso la titubanza degli adulti — non dei bambini.</p>

<h2>Come reagiscono i bambini</h2>
<p>I bambini piccoli (fino a 10-12 anni) accettano il naturismo senza difficoltà. Per loro "senza vestiti" è semplicemente il modo in cui si sta in questo posto, come si indossa il costume al mare. Non c'è imbarazzo perché non c'è confronto — tutti sono nudi, nessuno è diverso.</p>
<p>I preadolescenti e gli adolescenti possono avere più riserve, ed è giusto rispettarle. Molti campeggi hanno aree miste dove chi vuole portare il costume può farlo. Non forzare mai: il naturismo funziona solo se è una scelta libera.</p>

<h2>Come spiegarlo ai bambini</h2>
<p>Non serve una spiegazione elaborata. "In questo campeggio le persone stanno senza vestiti perché è più comodo e naturale" è sufficiente per la maggior parte dei bambini. Le domande che fanno sono spesso pratiche ("anche io devo togliermi le scarpe?") più che filosofiche.</p>
<p>Il punto più importante: il corpo non è qualcosa di cui vergognarsi, e guardare il corpo degli altri non è educato. Questi due messaggi, detti in modo semplice, bastano.</p>

<h2>Quale campeggio scegliere</h2>
<p>Per le famiglie con bambini piccoli, i campeggi grandi e attrezzati sono la scelta migliore: piscine con scivoli, animazione, aree giochi, ristoranti. Valalta e Koversada in Istria, Euronat nelle Landes, Domaine de la Jenesse in Vandea hanno strutture pensate per le famiglie.</p>
<p>I campeggi piccoli e tranquilli sono adatti per famiglie con bambini più grandi o per chi cerca quiete. Controllate sempre nella nostra guida il giudizio specifico su "adatto alle famiglie".</p>

<h2>Aspetti pratici</h2>
<p>Crema solare: i bambini si scottano più in fretta degli adulti, specialmente nelle parti che non hanno mai preso il sole. Applica SPF 50 ogni due ore e usa un cappellino per il sole intenso. Portare un pareo o una maglietta leggera per le pause all'ombra è sempre utile.</p>
<p>Sandali: nei campeggi ci sono vialetti caldi, docce comuni, piscine. Un paio di sandali lavabili per ogni membro della famiglia è indispensabile.</p>
<p>Teli: ogni bambino ha bisogno del suo telo personale da portare sempre con sé. Farglielo portare da soli è un buon modo per far capire la regola.</p>

<h2>Sicurezza e regole</h2>
<p>I campeggi naturisti sono ambienti molto sicuri per i bambini: la comunità è attenta, il controllo sociale è alto, e le famiglie sono la maggioranza degli ospiti. Le regole fotografiche proteggono i bambini: in un campeggio naturista non si possono fotografare persone senza consenso, e questo vale in modo ancora più rigoroso per i minori.</p>
<p>Se un bambino dice di non voler più stare senza vestiti, rispettate la sua scelta senza discussioni. Il naturismo non funziona per tutti, e va benissimo così.</p>""",
      "en": """<p class="lead">Naturism is one of the most family-friendly holidays there is. Children are free, there is space, campsites are safe and the community is welcoming. The only obstacle is often the hesitation of adults — not children.</p>

<h2>How children react</h2>
<p>Young children (up to 10–12 years old) accept naturism without difficulty. For them, "without clothes" is simply how things are done here, just as one wears a swimsuit at the seaside. There is no embarrassment because there is no comparison — everyone is nude, nobody is different.</p>
<p>Pre-teens and teenagers may have more reservations, and it is right to respect them. Many campsites have mixed areas where those who want to wear a swimsuit can do so. Never force it: naturism only works as a free choice.</p>

<h2>How to explain it to children</h2>
<p>No elaborate explanation is needed. "At this campsite people are without clothes because it is more comfortable and natural" is enough for most children. The questions they ask are often practical ("do I have to take my shoes off too?") rather than philosophical.</p>
<p>The most important point: the body is not something to be ashamed of, and looking at other people's bodies is impolite. These two messages, said simply, are enough.</p>

<h2>Which campsite to choose</h2>
<p>For families with young children, large and well-equipped campsites are the best choice: pools with slides, activities, play areas, restaurants. Valalta and Koversada in Istria, Euronat in the Landes, Domaine de la Jenesse in the Vendée all have family-oriented facilities.</p>
<p>Small, quiet campsites suit families with older children or those looking for peace. Always check our guide's specific rating for "family-friendly".</p>

<h2>Practical points</h2>
<p>Sun cream: children burn faster than adults, especially on parts of the body that have never seen the sun. Apply SPF 50 every two hours and use a sun hat in strong sun. Bringing a pareo or light T-shirt for shaded breaks is always useful.</p>
<p>Sandals: campsites have hot paths, shared showers and pools. A pair of washable sandals for every family member is essential.</p>
<p>Towels: every child needs their own personal towel to carry at all times. Getting them to carry it themselves is a good way to explain the rule.</p>

<h2>Safety and rules</h2>
<p>Naturist campsites are very safe environments for children: the community is attentive, social oversight is high, and families are the majority of guests. The photography rules protect children: at a naturist campsite you cannot photograph people without consent, and this applies even more strictly to minors.</p>
<p>If a child says they no longer want to be without clothes, respect their choice without discussion. Naturism does not work for everyone, and that is perfectly fine.</p>""",
      "de": """<p class="lead">Naturismus ist einer der familienfreundlichsten Urlaube, die es gibt. Kinder sind frei, es gibt Raum, Campingplätze sind sicher und die Gemeinschaft ist einladend. Das einzige Hindernis ist oft das Zögern der Erwachsenen — nicht der Kinder.</p>

<h2>Wie Kinder reagieren</h2>
<p>Kleine Kinder (bis 10–12 Jahre) akzeptieren den Naturismus problemlos. Für sie ist "ohne Kleidung" einfach die Art, wie man hier ist — genauso wie man am Meer Badekleidung trägt. Es gibt keine Verlegenheit, weil es keinen Vergleich gibt — alle sind nackt, niemand ist anders.</p>
<p>Vorpubertäre Kinder und Teenager können mehr Vorbehalte haben, und es ist richtig, diese zu respektieren. Viele Campingplätze haben gemischte Bereiche, wo man einen Badeanzug tragen kann, wenn man möchte. Niemals zwingen: Naturismus funktioniert nur als freie Wahl.</p>

<h2>Wie man es Kindern erklärt</h2>
<p>Es braucht keine aufwendige Erklärung. "Auf diesem Campingplatz sind die Menschen ohne Kleidung, weil es bequemer und natürlicher ist" reicht für die meisten Kinder. Die Fragen, die sie stellen, sind oft praktisch ("muss ich auch die Schuhe ausziehen?") als philosophisch.</p>
<p>Der wichtigste Punkt: Der Körper ist nichts, wofür man sich schämen muss, und andere anzustarren ist unhöflich. Diese zwei Botschaften, einfach ausgedrückt, genügen.</p>

<h2>Welchen Campingplatz wählen</h2>
<p>Für Familien mit kleinen Kindern sind große, gut ausgestattete Campingplätze die beste Wahl: Pools mit Rutschen, Animationsprogramm, Spielplätze, Restaurants. Valalta und Koversada in Istrien, Euronat in den Landes, Domaine de la Jenesse in der Vendée haben familienorientierte Einrichtungen.</p>
<p>Kleine, ruhige Campingplätze eignen sich für Familien mit älteren Kindern oder für alle, die Ruhe suchen. Prüfen Sie immer die spezifische Bewertung für „familienfreundlich" in unserem Führer.</p>

<h2>Praktische Hinweise</h2>
<p>Sonnencreme: Kinder verbrennen schneller als Erwachsene, besonders an Körperstellen, die nie Sonne gesehen haben. LSF 50 alle zwei Stunden auftragen und bei intensiver Sonne einen Sonnenhut verwenden. Ein Pareo oder leichtes T-Shirt für Schatten-Pausen ist immer sinnvoll.</p>
<p>Sandalen: Auf Campingplätzen gibt es heiße Wege, Gemeinschaftsduschen und Pools. Ein Paar waschbare Sandalen für jedes Familienmitglied ist unverzichtbar.</p>
<p>Handtücher: Jedes Kind braucht sein eigenes persönliches Handtuch, das es immer dabei hat. Es selbst tragen zu lassen ist ein guter Weg, die Regel zu erklären.</p>

<h2>Sicherheit und Regeln</h2>
<p>Naturistencampingplätze sind sehr sichere Umgebungen für Kinder: Die Gemeinschaft ist aufmerksam, die soziale Kontrolle ist hoch, und Familien sind die Mehrheit der Gäste. Die Fotografierregeln schützen Kinder: Auf einem Naturistencampingplatz darf man Menschen ohne Einwilligung nicht fotografieren, und das gilt noch strenger für Minderjährige.</p>
<p>Wenn ein Kind sagt, es möchte nicht mehr ohne Kleidung sein, respektieren Sie die Entscheidung ohne Diskussion. Naturismus funktioniert nicht für alle, und das ist völlig in Ordnung.</p>""",
    },
  },
  {
    "slug": "tessera-inf-come-ottenerla",
    "date": "2026-10-10",
    "min_read": 4,
    "title": {
      "it": "Tessera INF: cos'è e come ottenerla",
      "en": "INF card: what it is and how to get one",
      "de": "INF-Ausweis: Was er ist und wie man ihn bekommt",
    },
    "summary": {
      "it": "La tessera INF è richiesta in molti campeggi naturisti europei. Costa poco, vale un anno intero e apre le porte a centinaia di strutture. Ecco tutto quello che devi sapere.",
      "en": "The INF card is required at many European naturist campsites. It costs little, lasts a full year and opens the doors to hundreds of facilities. Here is everything you need to know.",
      "de": "Der INF-Ausweis wird auf vielen europäischen Naturistencampingplätzen verlangt. Er kostet wenig, gilt ein volles Jahr und öffnet die Türen zu Hunderten von Einrichtungen. Alles, was Sie wissen müssen.",
    },
    "body": {
      "it": """<p class="lead">La tessera INF (International Naturist Federation) è il documento di riconoscimento del naturismo internazionale. Non è obbligatoria ovunque, ma in molti campeggi europei — specialmente in Italia, Germania, Austria e Croazia — è richiesta all'ingresso o consente uno sconto sul prezzo.</p>

<h2>Cos'è esattamente</h2>
<p>È un tesserino plastificato (fisico o digitale, dipende dalla federazione) che certifica che sei membro di una federazione naturista affiliata all'INF. Ha una foto, il tuo nome e la data di scadenza. Molti campeggi la scannerizzano all'ingresso come documento di identità aggiuntivo.</p>

<h2>Come ottenerla in Italia</h2>
<p>In Italia si ottiene attraverso la FENAIT (Federazione Naturista Italiana). Il processo è semplice: vai sul sito fenait.org, compila il modulo di iscrizione, paga la quota annuale (circa 40-50 euro per un adulto, meno per under 18 e anziani), e ricevi la tessera per posta o digitale. La quota include l'assicurazione e la rivista associativa.</p>

<h2>Come ottenerla in altri paesi</h2>
<p>Ogni paese ha la sua federazione affiliata INF. Le principali sono: FFN per la Francia (ffn-naturisme.com), DFK per la Germania (dfk.org), British Naturism per il Regno Unito (britishnaturism.org.uk), FEN per la Spagna (naturismo.org). Tutte hanno un processo di iscrizione online.</p>

<h2>Vale anche se non sono membro di una federazione locale?</h2>
<p>Se ti trovi in un paese dove non esiste una federazione INF, o se vuoi la tessera prima di completare l'iscrizione alla federazione locale, molti campeggi vendono una tessera giornaliera o settimanale all'ingresso — a un prezzo leggermente più alto. Questa opzione non dà i benefici completi dell'iscrizione annuale (assicurazione, rivista, sconti partner) ma ti permette di accedere al campeggio.</p>

<h2>Quanto risparmio con la tessera?</h2>
<p>Varia da campeggio a campeggio. Alcuni applicano uno sconto del 5-15% sul prezzo della piazzola, altri danno l'ingresso gratuito ai bambini dei soci, altri ancora hanno prezzi fissi per i soci che sono inferiori al listino. In media, in due settimane di vacanza la tessera si ripaga ampiamente.</p>

<h2>È richiesta anche per le spiagge?</h2>
<p>No. Le spiagge naturiste — siano ufficiali o tollerate — sono accessibili a tutti senza tessera. La tessera INF è richiesta solo dai campeggi affiliati e da alcune strutture private.</p>""",
      "en": """<p class="lead">The INF card (International Naturist Federation) is the international naturism membership document. It is not compulsory everywhere, but at many European campsites — especially in Italy, Germany, Austria and Croatia — it is required at the gate or earns a price discount.</p>

<h2>What it actually is</h2>
<p>It is a laminated card (physical or digital, depending on the federation) that certifies you are a member of a naturist federation affiliated with INF. It has a photo, your name and an expiry date. Many campsites scan it at the gate as an additional identity document.</p>

<h2>How to get one in the UK</h2>
<p>In the UK you get it through British Naturism (britishnaturism.org.uk). The process is straightforward: fill in the membership form online, pay the annual fee (around £35–45 for an adult, less for under-18s and seniors), and receive a physical or digital card. The fee includes insurance and the member magazine.</p>

<h2>How to get one in other countries</h2>
<p>Each country has its own INF-affiliated federation. The main ones are: FFN for France (ffn-naturisme.com), DFK for Germany (dfk.org), FENAIT for Italy (fenait.org), FEN for Spain (naturismo.org). All have an online sign-up process.</p>

<h2>What if I am not a member of a local federation?</h2>
<p>If you are in a country without an INF federation, or want the card before completing a local membership, many campsites sell a day or week pass at the gate — at a slightly higher price. This option does not give the full benefits of annual membership (insurance, magazine, partner discounts) but lets you access the campsite.</p>

<h2>How much do I save with the card?</h2>
<p>It varies by campsite. Some apply a 5–15% discount on the pitch price, others give free entry for members' children, and some have fixed member rates below the standard tariff. On average, over a two-week holiday the card pays for itself comfortably.</p>

<h2>Is it needed for beaches too?</h2>
<p>No. Naturist beaches — whether official or tolerated — are accessible to everyone without a card. The INF card is only required by affiliated campsites and some private facilities.</p>""",
      "de": """<p class="lead">Der INF-Ausweis (International Naturist Federation) ist das internationale Naturismus-Mitgliedsdokument. Er ist nicht überall Pflicht, aber auf vielen europäischen Campingplätzen — besonders in Italien, Deutschland, Österreich und Kroatien — wird er am Eingang verlangt oder gewährt einen Preisnachlass.</p>

<h2>Was er genau ist</h2>
<p>Es ist ein laminierter Ausweis (physisch oder digital, je nach Verband), der bescheinigt, dass man Mitglied eines INF-angeschlossenen Naturistenverbandes ist. Er enthält ein Foto, den Namen und das Ablaufdatum. Viele Campingplätze scannen ihn am Eingang als zusätzliches Ausweisdokument.</p>

<h2>Wie man ihn in Deutschland bekommt</h2>
<p>In Deutschland erhält man ihn über den DFK (Deutscher Verband für Freikörperkultur, dfk.org). Der Prozess ist einfach: Online-Formular ausfüllen, Jahresbeitrag bezahlen (ca. 40–60 Euro für Erwachsene, weniger für Unter-18-Jährige und Senioren), und den Ausweis per Post oder digital erhalten. Der Beitrag beinhaltet Versicherung und Verbandszeitschrift.</p>

<h2>Wie man ihn in anderen Ländern bekommt</h2>
<p>Jedes Land hat seinen eigenen INF-angeschlossenen Verband. Die wichtigsten sind: FFN für Frankreich (ffn-naturisme.com), British Naturism für das Vereinigte Königreich (britishnaturism.org.uk), FENAIT für Italien (fenait.org), FEN für Spanien (naturismo.org). Alle haben ein Online-Anmeldeverfahren.</p>

<h2>Was wenn ich kein Mitglied eines lokalen Verbands bin?</h2>
<p>Wenn Sie sich in einem Land ohne INF-Verband befinden oder den Ausweis vor dem Abschluss einer lokalen Mitgliedschaft wünschen, verkaufen viele Campingplätze eine Tages- oder Wochenkarte am Eingang — zu einem etwas höheren Preis. Diese Option bietet nicht alle Vorteile einer Jahresmitgliedschaft (Versicherung, Zeitschrift, Partnerrabatte), ermöglicht aber den Zugang zum Campingplatz.</p>

<h2>Wie viel spare ich mit dem Ausweis?</h2>
<p>Das variiert je nach Campingplatz. Manche gewähren 5–15% Rabatt auf den Stellplatzpreis, andere ermöglichen freien Eintritt für Mitgliederkinder, und wieder andere haben feste Mitgliederpreise unter dem regulären Tarif. Im Durchschnitt amortisiert sich der Ausweis bei einem zweiwöchigen Urlaub deutlich.</p>

<h2>Wird er auch für Strände benötigt?</h2>
<p>Nein. Naturistenstrände — ob offiziell oder geduldet — sind für alle ohne Ausweis zugänglich. Der INF-Ausweis wird nur von angeschlossenen Campingplätzen und einigen privaten Einrichtungen verlangt.</p>""",
    },
  },
  {
    "slug": "naturismo-principianti-faq",
    "date": "2026-10-05",
    "min_read": 5,
    "title": {
      "it": "Naturismo per principianti: le domande più frequenti",
      "en": "Naturism for beginners: the most common questions answered",
      "de": "Naturismus für Einsteiger: die häufigsten Fragen beantwortet",
    },
    "summary": {
      "it": "\"E se mi imbarazzo?\" \"Posso venire da solo?\" \"Cosa si fa se piove?\" Le domande che tutti fanno prima della prima volta — con risposte oneste.",
      "en": "\"What if I feel embarrassed?\" \"Can I come alone?\" \"What happens if it rains?\" The questions everyone asks before their first time — with honest answers.",
      "de": "\"Was wenn ich mich schäme?\" \"Kann ich alleine kommen?\" \"Was passiert bei Regen?\" Die Fragen, die alle vor dem ersten Mal stellen — mit ehrlichen Antworten.",
    },
    "body": {
      "it": """<p class="lead">Prima della prima volta in un campeggio naturista, tutti hanno le stesse domande. Alcune sono pratiche, altre sono timori che sembrano grandi ma si dissolvono in fretta. Ecco le risposte più oneste che possiamo dare.</p>

<h2>E se mi imbarazzo?</h2>
<p>Succede quasi a tutti nei primissimi minuti. Poi passa. Il fatto che tutti siano nella stessa situazione accelera moltissimo il processo: non c'è un "vestito" rispetto a cui sentirti diverso. La maggior parte delle persone riferisce che dopo 20-30 minuti non ci pensa più.</p>

<h2>Posso venire da solo/a?</h2>
<p>Sì, ed è più comune di quanto pensi. Molti naturisti vanno nei campeggi da soli, specialmente i più esperti. I campeggi naturisti sono ambienti sociali e accoglienti — di solito è più facile attaccare discorso rispetto a un campeggio normale, perché l'ambiente informale abbassa le barriere.</p>

<h2>Cosa si fa se mi viene... una reazione involontaria?</h2>
<p>È la domanda che molti si fanno e nessuno vuole fare. La risposta pratica: mettiti sull'asciugamano a pancia in giù, tuffati in acqua, o aspetta che passi. Succede raramente dopo i primissimi minuti perché il contesto non è erotico. I campeggi naturisti non sono ambienti sessualizzati.</p>

<h2>Devo togliermi tutto subito?</h2>
<p>No. Non c'è nessuna regola che impone di spogliarsi all'ingresso. Puoi togliere i vestiti quando sei pronto/a — in piazzola, in spiaggia, dove vuoi. Molti arrivano vestiti, sistemano il campeggio e si spogliano quando sono già a proprio agio.</p>

<h2>Cosa succede se piove?</h2>
<p>Come in qualsiasi campeggio: ci si mette qualcosa addosso. Nei campeggi naturisti non c'è nessuna regola che impone di stare nudi con il brutto tempo. In molti ci sono strutture coperte, bar, sale comuni dove passare le giornate piovose.</p>

<h2>Posso portare il costume da bagno?</h2>
<p>Nella maggior parte dei campeggi naturisti le aree principali (piscina, spiaggia, zone comuni) sono nudiste. Alcuni campeggi hanno aree "miste" o permettono il costume nell'area ristorante. Controlla le regole specifiche prima di partire. In ogni caso, portare un costume è sempre prudente per le situazioni impreviste.</p>

<h2>È sicuro per le donne da sole?</h2>
<p>I campeggi naturisti sono generalmente considerati molto sicuri per le donne. Le regole sono chiare, la comunità è attenta, e qualsiasi comportamento molesto viene preso sul serio. Il codice di condotta — niente fissare, niente avances non richieste — è applicato con più rigore che in molti altri contesti. Questo non significa che non esistano situazioni sgradevoli, ma la cultura dei campeggi naturisti è strutturalmente più rispettosa di molti altri ambienti estivi.</p>

<h2>E se il mio corpo non è "perfetto"?</h2>
<p>Il naturismo è forse l'unico ambiente in cui la varietà dei corpi è davvero normale e non commentata. Vedrai corpi di tutte le età, forme e dimensioni — ed è esattamente questo il punto. Nessuno giudica. L'esperienza è spesso liberatoria per chi arriva con insicurezze sul proprio corpo.</p>

<h2>Posso fare foto?</h2>
<p>No, non senza consenso esplicito. Questa regola è applicata rigorosamente in tutti i campeggi naturisti. Per foto di paesaggio o di te stesso/a, verifica sempre che non ci siano altre persone inquadrate. In caso di dubbio, chiedi.</p>

<h2>Come faccio a sapere se un campeggio è "vero" naturista?</h2>
<p>I campeggi affiliati INF o ENF sono quelli riconosciuti ufficialmente. Quelli nella nostra guida sono tutti verificati. Diffida dei siti che si definiscono "naturisti" senza affiliazione: possono avere aspettative o atmosfere molto diverse da un campeggio naturista tradizionale.</p>""",
      "en": """<p class="lead">Before a first visit to a naturist campsite, everyone has the same questions. Some are practical, others are fears that seem large but dissolve quickly. Here are the most honest answers we can give.</p>

<h2>What if I feel embarrassed?</h2>
<p>It happens to almost everyone in the very first minutes. Then it passes. The fact that everyone is in the same situation speeds the process enormously: there is no "clothed" norm against which to feel different. Most people report that after 20–30 minutes they stop thinking about it.</p>

<h2>Can I come alone?</h2>
<p>Yes, and it is more common than you might think. Many naturists visit campsites alone, especially the more experienced ones. Naturist campsites are social, welcoming environments — striking up a conversation is often easier than at a conventional campsite, because the informal setting lowers barriers.</p>

<h2>What if I have an unwanted physical reaction?</h2>
<p>This is the question many people have but nobody wants to ask. The practical answer: lie face-down on your towel, dive into the water, or wait for it to pass. It happens rarely after the very first minutes because the context is not erotic. Naturist campsites are not sexualised environments.</p>

<h2>Do I have to undress straight away?</h2>
<p>No. There is no rule requiring you to strip at the gate. You can undress when you are ready — on your pitch, at the beach, wherever. Many people arrive clothed, set up camp and undress once they are already comfortable.</p>

<h2>What happens if it rains?</h2>
<p>As at any campsite: you put something on. At naturist campsites there is no rule requiring nudity in bad weather. Many have covered facilities, bars and common rooms where you can spend rainy days.</p>

<h2>Can I bring a swimsuit?</h2>
<p>At most naturist campsites the main areas (pool, beach, common zones) are nude-only. Some campsites have "mixed" areas or allow swimwear in the restaurant area. Check the specific rules before you go. In any case, packing a swimsuit is always sensible for unexpected situations.</p>

<h2>Is it safe for women travelling alone?</h2>
<p>Naturist campsites are generally considered very safe for women. Rules are clear, the community is attentive, and any harassing behaviour is taken seriously. The code of conduct — no staring, no unwanted advances — is enforced more strictly than in many other settings. This does not mean unpleasant situations never occur, but the culture of naturist campsites is structurally more respectful than many other summer environments.</p>

<h2>What if my body is not "perfect"?</h2>
<p>Naturism is perhaps the only environment where body variety is truly normal and unremarked upon. You will see bodies of all ages, shapes and sizes — and that is exactly the point. Nobody judges. The experience is often liberating for those who arrive with body insecurities.</p>

<h2>Can I take photos?</h2>
<p>No, not without explicit consent. This rule is strictly enforced at all naturist campsites. For landscape photos or selfies, always check that no other people are in frame. When in doubt, ask.</p>

<h2>How do I know if a campsite is a "real" naturist one?</h2>
<p>INF- or ENF-affiliated campsites are the officially recognised ones. All campsites in our guide are verified. Be wary of sites that call themselves "naturist" without affiliation: their expectations and atmosphere can be very different from a traditional naturist campsite.</p>""",
      "de": """<p class="lead">Vor dem ersten Besuch auf einem Naturistencampingplatz haben alle dieselben Fragen. Manche sind praktisch, andere sind Ängste, die groß erscheinen, aber sich schnell auflösen. Hier sind die ehrlichsten Antworten, die wir geben können.</p>

<h2>Was wenn ich mich schäme?</h2>
<p>Das passiert fast allen in den allerersten Minuten. Dann vergeht es. Die Tatsache, dass alle in derselben Situation sind, beschleunigt den Prozess enorm: Es gibt keine „bekleidete" Norm, gegen die man sich anders fühlen würde. Die meisten berichten, dass sie nach 20–30 Minuten nicht mehr daran denken.</p>

<h2>Kann ich alleine kommen?</h2>
<p>Ja, und es ist häufiger als man denkt. Viele Naturisten besuchen Campingplätze alleine, besonders die erfahreneren. Naturistencampingplätze sind soziale, einladende Umgebungen — ein Gespräch zu beginnen ist oft einfacher als auf einem konventionellen Campingplatz, weil das informelle Umfeld Barrieren abbaut.</p>

<h2>Was wenn ich eine ungewollte körperliche Reaktion bekomme?</h2>
<p>Das ist die Frage, die viele haben, aber niemand stellen möchte. Die praktische Antwort: Legen Sie sich mit dem Bauch auf Ihr Handtuch, springen Sie ins Wasser oder warten Sie, bis es vergeht. Es passiert selten nach den allerersten Minuten, da der Kontext nicht erotisch ist. Naturistencampingplätze sind keine sexualisierten Umgebungen.</p>

<h2>Muss ich mich sofort ausziehen?</h2>
<p>Nein. Es gibt keine Regel, die vorschreibt, sich am Eingang auszuziehen. Sie können sich ausziehen, wenn Sie bereit sind — auf dem Stellplatz, am Strand, wo immer Sie möchten. Viele kommen bekleidet, richten das Camp ein und ziehen sich aus, wenn sie sich bereits wohlfühlen.</p>

<h2>Was passiert bei Regen?</h2>
<p>Wie auf jedem Campingplatz: Man zieht etwas an. Auf Naturistencampingplätzen gibt es keine Regel, die Nacktheit bei schlechtem Wetter vorschreibt. Viele haben überdachte Einrichtungen, Bars und Gemeinschaftsräume, in denen man Regentage verbringen kann.</p>

<h2>Kann ich einen Badeanzug mitbringen?</h2>
<p>Auf den meisten Naturistencampingplätzen sind die Hauptbereiche (Pool, Strand, Gemeinschaftszonen) nur für Nackte. Manche Campingplätze haben „gemischte" Bereiche oder erlauben Badekleidung im Restaurantbereich. Prüfen Sie die spezifischen Regeln vor der Abreise. In jedem Fall ist ein Badeanzug für unvorhergesehene Situationen immer sinnvoll.</p>

<h2>Ist es sicher für alleinreisende Frauen?</h2>
<p>Naturistencampingplätze gelten im Allgemeinen als sehr sicher für Frauen. Regeln sind klar, die Gemeinschaft ist aufmerksam, und jedes belästigende Verhalten wird ernst genommen. Der Verhaltenskodex — kein Anstarren, keine unerwünschten Annäherungsversuche — wird strenger durchgesetzt als in vielen anderen Umgebungen. Das bedeutet nicht, dass es keine unangenehmen Situationen gibt, aber die Kultur der Naturistencampingplätze ist strukturell respektvoller als viele andere Sommerumgebungen.</p>

<h2>Was wenn mein Körper nicht „perfekt" ist?</h2>
<p>Naturismus ist vielleicht die einzige Umgebung, in der Körpervielfalt wirklich normal und unremarkiert ist. Sie sehen Körper aller Altersgruppen, Formen und Größen — und das ist genau der Punkt. Niemand urteilt. Die Erfahrung ist oft befreiend für alle, die mit Körperunsicherheiten ankommen.</p>

<h2>Kann ich Fotos machen?</h2>
<p>Nein, nicht ohne ausdrückliche Zustimmung. Diese Regel wird auf allen Naturistencampingplätzen streng durchgesetzt. Prüfen Sie bei Landschaftsfotos oder Selfies immer, dass keine anderen Personen im Bild sind. Im Zweifelsfall fragen.</p>

<h2>Woher weiß ich, ob ein Campingplatz ein „echter" Naturistencampingplatz ist?</h2>
<p>INF- oder ENF-angeschlossene Campingplätze sind die offiziell anerkannten. Alle Campingplätze in unserem Führer sind verifiziert. Seien Sie vorsichtig bei Websites, die sich ohne Mitgliedschaft als „naturistisch" bezeichnen: Ihre Erwartungen und Atmosphäre können sich stark von einem traditionellen Naturistencampingplatz unterscheiden.</p>""",
    },
  },
]

def articles_list(lang):
    t = T[lang]
    p = t["paths"]
    cards = ""
    for a in ARTICLES:
        cards += f'''<article class="article-card">
  <div class="article-meta"><time>{a["date"]}</time> · <span>{a["min_read"]} {e(t["articles_min_read"])}</span></div>
  <h2 class="article-title"><a href="/{lang}/{p["articles"]}/{e(a["slug"])}/">{e(a["title"][lang])}</a></h2>
  <p>{e(a["summary"][lang])}</p>
  <a class="btn ghost small" href="/{lang}/{p["articles"]}/{e(a["slug"])}/">{e(t["articles_read"])} →</a>
</article>'''
    body = f"""<section class="block"><div class="wrap">
  <h1>{e(t["articles_h1"])}</h1>
  <p class="lead">{e(t["articles_p"])}</p>
  <div class="articles-grid">{cards}</div>
</div></section>"""
    return page(lang, "articles", f'{t["articles_h1"]} — NaturCamp Guide', t["articles_p"], body)

def article_page(a, lang):
    t = T[lang]
    p = t["paths"]
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{T[l]["paths"]["articles"]}/{e(a["slug"])}/">' for l in LANGS)
    canonical = f'{SITE}/{lang}/{p["articles"]}/{e(a["slug"])}/'
    nav_html = "\n".join(f'<a href="{lang_url(lang, k)}">{e(t["nav"][k])}</a>' for k in ("about", "camps", "beaches", "pack", "review", "assoc", "articles"))
    langs_html = "\n".join(f'<a href="/{l}/{T[l]["paths"]["articles"]}/{e(a["slug"])}/" lang="{l}" hreflang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    body_html = a["body"][lang]
    html_page = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(a["title"][lang])} — NaturCamp Guide</title>
<meta name="description" content="{e(a["summary"][lang])}">
<link rel="canonical" href="{canonical}">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE}/en/{T['en']['paths']['articles']}/{e(a['slug'])}/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;700;800&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="brand" href="{lang_url(lang, 'home')}">{LOGO}<span><b>NaturCamp</b><small>{e(t["brand_sub"])}</small></span></a>
  <nav class="nav" aria-label="Menu">{nav_html}</nav>
  <div class="lang" aria-label="Language">{langs_html}</div>
</div></header>
<main>
<article class="block article-full"><div class="wrap">
  <div class="article-meta"><time>{a["date"]}</time> · <span>{a["min_read"]} {e(t["articles_min_read"])}</span></div>
  <h1>{e(a["title"][lang])}</h1>
  <p class="lead">{e(a["summary"][lang])}</p>
  <div class="article-body">{body_html}</div>
  <p style="margin-top:2.5rem"><a class="btn ghost" href="/{lang}/{p['articles']}/">← {e(t["articles_h1"])}</a></p>
</div></article>
</main>
<footer class="site-footer"><div class="wrap">
  <span>© 2026 NaturCamp Guide — {e(t["footer"])}</span>
  <span><a href="mailto:{CONTACT}">{e(t["contact"])}</a> · <a href="{lang_url(lang, 'about')}#privacy">{e(t["privacy"])}</a></span>
</div></footer>
</body>
</html>
"""
    return html_page

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
        write(ROOT / lang / p["articles"] / "index.html", articles_list(lang))
        for a in ARTICLES:
            write(ROOT / lang / p["articles"] / a["slug"] / "index.html", article_page(a, lang))
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
        urls += [lang_url(lang, k) for k in ("home", "camps", "beaches", "pack", "review", "about", "assoc", "articles")]
        urls += [lang_url(lang, "camp", c["slug"]) for c in DATA]
        urls += [lang_url(lang, "beach", b["slug"]) for b in BEACHES]
        urls += [lang_url(lang, "article", a["slug"]) for a in ARTICLES]
    write(ROOT / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    print(f"Generato: {len(LANGS)} lingue, {len(DATA)} campeggi, {len(BEACHES)} spiagge, {len(ARTICLES)} articoli, {len(urls)} pagine.")

if __name__ == "__main__":
    main()
