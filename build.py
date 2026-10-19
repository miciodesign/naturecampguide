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
    "nav": {"camps": "Campeggi", "beaches": "Spiagge", "review": "Scrivi una recensione", "about": "Chi siamo"},
    "paths": {"camps": "campeggi", "beaches": "spiagge", "review": "recensioni", "about": "chi-siamo"},
    "beaches_h1": "Spiagge naturiste", "beaches_p": "Ufficiali e tollerate, ordinate per paese. Il numero è il voto complessivo su 5.",
    "beaches_home_h2": "Spiagge naturiste", "beaches_home_p": "Dove si può stare nudi in spiaggia, con stato ufficiale, accesso e servizi verificati.",
    "beaches_all": "Tutte le spiagge",
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
    "verified": "Verificato da fonti", "price_na": "non pubblicato: chiedere al campeggio", "sources_h2": "Fonti", "desk_note": "Scheda compilata da sito ufficiale e recensioni pubbliche, non da una visita: i voti riflettono quanto documentato alla data indicata. Hai informazioni più recenti? Scrivi una recensione.",
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
    "nav": {"camps": "Campsites", "beaches": "Beaches", "review": "Write a review", "about": "About"},
    "paths": {"camps": "campsites", "beaches": "beaches", "review": "reviews", "about": "about"},
    "beaches_h1": "Naturist beaches", "beaches_p": "Official and tolerated, sorted by country. The number is the overall score out of 5.",
    "beaches_home_h2": "Naturist beaches", "beaches_home_p": "Where you can be nude on the beach, with official status, access and services checked.",
    "beaches_all": "All beaches",
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
    "verified": "Verified from sources", "price_na": "not published: ask the campsite", "sources_h2": "Sources", "desk_note": "Listing compiled from the official website and public reviews, not from a visit: the scores reflect what was documented on the date shown. Have more recent information? Write a review.",
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
    "nav": {"camps": "Campingplätze", "beaches": "Strände", "review": "Bewertung schreiben", "about": "Über uns"},
    "paths": {"camps": "campingplaetze", "beaches": "straende", "review": "bewertungen", "about": "ueber-uns"},
    "beaches_h1": "FKK-Strände", "beaches_p": "Offiziell und geduldet, nach Land sortiert. Die Zahl ist die Gesamtnote von 5.",
    "beaches_home_h2": "FKK-Strände", "beaches_home_p": "Wo man nackt am Strand sein darf, mit geprüftem Status, Zugang und Ausstattung.",
    "beaches_all": "Alle Strände",
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
    "verified": "Geprüft anhand von Quellen", "price_na": "nicht veröffentlicht: beim Platz erfragen", "sources_h2": "Quellen", "desk_note": "Eintrag anhand der offiziellen Website und öffentlicher Bewertungen erstellt, nicht nach einem Besuch: Die Noten spiegeln den dokumentierten Stand zum angegebenen Datum wider. Haben Sie neuere Informationen? Schreiben Sie eine Bewertung.",
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
FORM_ACTION = "#"  # sostituire con l'endpoint del modulo (es. Formspree) — vedi README

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
    return f"/{lang}/{p[kind]}/"

def basis_label(x, lang):
    t = T[lang]
    if x.get("basis") == "desk":
        return f'{t["verified"]} {x["visited"]}'
    return f'{t["facts"]["visited"]} {x["visited"]}'

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
    nav = "\n".join(f'<a href="{lang_url(lang, k)}">{e(t["nav"][k])}</a>' for k in ("camps", "beaches", "review", "about"))
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
<section class="block"><div class="wrap"><h2>{e(t['countries_h2'])}</h2><ul class="countries">{cl}</ul></div></section>
<section class="block"><div class="wrap"><h2>{e(t['latest_h2'])}</h2><ul class="camps">{latest}</ul></div></section>
<section class="block"><div class="wrap"><h2>{e(t['beaches_home_h2'])}</h2><p class="lead">{e(t['beaches_home_p'])}</p><ul class="camps">{beach_latest}</ul><p style="margin-top:20px"><a class="btn ghost" href="{lang_url(lang, 'beaches')}">{e(t['beaches_all'])}</a></p></div></section>
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
    rows = "".join(f"<tr><th scope='row'>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in facts)
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
  {sources_block(b, lang)}
</div></section>"""
    return page(lang, "beach", f'{b["name"]} — NaturCamp Guide', b["summary"][lang], body, b["slug"])

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

def about(lang):
    t = T[lang]
    body = f"""<section class="block"><div class="wrap">
  <h1>{e(t['about_h1'])}</h1>
  <p class="lead">{e(t['about_p1'])}</p>
  <p>{e(t['about_p2'])}</p>
  <p>{e(t['about_p3'])}<a href="mailto:{CONTACT}">{CONTACT}</a></p>
  <h2 id="privacy">{e(t['privacy'])}</h2>
  <p>[TESTO PRIVACY — da completare con i dati del titolare e la gestione delle e-mail ricevute tramite il modulo recensioni]</p>
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
        urls += [lang_url(lang, k) for k in ("home", "camps", "beaches", "review", "about")]
        urls += [lang_url(lang, "camp", c["slug"]) for c in DATA]
        urls += [lang_url(lang, "beach", b["slug"]) for b in BEACHES]
    write(ROOT / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    print(f"Generato: {len(LANGS)} lingue, {len(DATA)} campeggi, {len(BEACHES)} spiagge, {len(urls)} pagine.")

if __name__ == "__main__":
    main()
