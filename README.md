# NaturCamp Guide — sito statico

Guida ai campeggi naturisti in Europa in italiano, inglese e tedesco.
Il sito è HTML puro: nessun server, nessun database, si pubblica copiando i file.

## Struttura

```
build.py            genera tutte le pagine (python3 build.py)
data/campeggi.json  i campeggi: UNA voce per campeggio, con i testi nelle tre lingue
data/spiagge.json   le spiagge naturiste, stessa logica
src/                CSS, logo e favicon (sorgenti)
assets/             copia di src/ usata dal sito (generata)
index.html          pagina radice: manda alla lingua del browser
it/  en/  de/       le pagine generate, una cartella per lingua
sitemap.xml robots.txt
```

Le cartelle `it/ en/ de/ assets/`, `index.html`, `sitemap.xml` e `robots.txt`
sono generate: non modificarle a mano, modifica `data/`, `src/` o `build.py`
e rilancia `python3 build.py`.

## Aggiungere un campeggio

1. Apri `data/campeggi.json` e copia una delle voci esistenti.
2. Cambia `slug` (solo lettere minuscole, numeri e trattini: diventa l'indirizzo della pagina),
   `country` (codice a due lettere), nome, stagione, prezzo, voti e testi nelle tre lingue.
3. Togli `"demo": true` (quella riga mostra l'avviso "scheda dimostrativa").
4. Lancia `python3 build.py`. Il voto complessivo si calcola da solo.

Le due schede presenti sono **esempi con dati inventati**: vanno sostituite con schede reali.

Per aggiungere un paese nuovo basta usare il suo codice in `country`; i nomi
dei paesi nelle tre lingue sono in `build.py` → `country_names`.

## Aggiungere una spiaggia

Stessa procedura in `data/spiagge.json`. Campi particolari:
- `status`: `official` (segnalata con cartelli), `tolerated`, `unofficial`
- `coords`: "lat, lon" — diventa un link alla mappa
- `nearby`: lista di `slug` di campeggi vicini (facoltativo)
- sei criteri: natura, pulizia, accesso, servizi, atmosfera, affollamento

## Pubblicare su Hostinger tramite GitHub

1. Crea un repository su GitHub (es. `naturcampguide`) e carica questa cartella:
   ```
   git init
   git add .
   git commit -m "Primo sito"
   git branch -M main
   git remote add origin https://github.com/<tuo-utente>/naturcampguide.git
   git push -u origin main
   ```
2. In hPanel di Hostinger: **Siti web → Gestisci → Avanzate → Git**.
3. Inserisci l'URL del repository, ramo `main`, cartella di destinazione `public_html`
   (per un repository privato Hostinger ti dà una chiave SSH da aggiungere su GitHub in
   *Settings → Deploy keys*).
4. Premi **Crea** e poi **Deploy**. Da quel momento ogni `git push` si pubblica
   premendo Deploy (o automaticamente, se attivi il webhook che Hostinger mostra nella stessa pagina).
5. Collega i tre domini allo stesso sito: `.com` come principale, `.it` e `.eu` come
   redirect verso il `.com` (hPanel → Domini → Reindirizzamenti).

Il generatore (`build.py`) va lanciato sul computer prima del push: le pagine generate
sono incluse nel repository, così Hostinger non deve eseguire nulla.

## Modulo recensioni

Il modulo in `it/recensioni/` (e nelle altre lingue) è pronto ma non invia ancora da nessuna parte.
Opzioni semplici senza backend:

- **Formspree** (o Web3Forms, Basin): crea un modulo, copia l'endpoint e mettilo in
  `build.py` nella variabile `FORM_ACTION`. Le recensioni arrivano via e-mail e le pubblichi
  tu aggiungendole al JSON (moderazione manuale, come da regole).
- In futuro, con più traffico: un piccolo backend o una piattaforma di recensioni.

## Affiliazione Stay22 (dove dormire)

Ogni scheda può mostrare una mappa Stay22 con hotel e appartamenti vicini.
Iscriviti su stay22.com, copia il tuo `aid` e mettilo in `build.py` → `STAY22_AID`.
Finché è vuoto il blocco non compare. Rilancia `python3 build.py`.

## Da completare prima della pubblicazione

- [x] Prime schede reali: 11 campeggi e 6 spiagge (da fonti, ottobre 2026)
- [ ] Impostare `FORM_ACTION` con l'endpoint del modulo
- [x] Stay22 attivo (AID naturcampguide)
- [ ] Scrivere il testo privacy in `build.py` (funzione `about`) nelle tre lingue
- [ ] Verificare l'indirizzo e-mail `CONTACT` in `build.py`
- [ ] Se il dominio principale non è `naturcampguide.com`, cambiare `SITE` in `build.py`
