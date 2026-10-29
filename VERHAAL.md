# Bob laat op monitor: hoe deze kaart tot stand kwam

Dit document vertelt waar de zonnepanelenkaart vandaan komt: de vraag, de databronnen, wat er met de data is gedaan, welke keuzes en benaderingen erin zitten, en hoe je hem online zet of bijwerkt. Gemaakt op 29 oktober 2026 door Thijs Hoffman (Nodefy) met Claude Code.

## 1. De vraag

> Een interactieve landkaart van Nederland en Vlaanderen waarop je ziet welke gemeenten de meeste zonnepanelen hebben. Eerst per stad, en als je op een stad klikt per gemeente, wijk, buurt enzovoort. Postcode-informatie is ook wenselijk. Het is voor Bob Laadt Op, dat thuisbatterijen verkoopt.

Het idee erachter: wie zonnepanelen heeft, is de logische klant voor een thuisbatterij. De kaart laat zien waar die mensen wonen.

## 2. Wat de kaart doet

- **Startscherm**: alle 342 Nederlandse en 285 Vlaamse gemeenten (indeling 2025), gekleurd naar het gekozen cijfer. Rechts staat een top 25, te filteren op Nederland of Vlaanderen.
- **Klik op een gemeente**:
  - Nederland: wijken, buurten of postcodegebieden (te wisselen linksboven).
  - Vlaanderen: postcodes.
- **Klik op een Nederlandse wijk**: de buurten in die wijk, met woningvoorraad, % koopwoningen, % eengezinswoningen, WOZ-waarde, inkomen en meest voorkomende postcode.
- **Cijfers om op te kleuren**:
  - % woningen met zonnepanelen
  - aantal installaties
  - *Kansen (VL)*: installaties zonder thuisbatterij
  - *Batterij % (VL)*: aandeel eigenaars van zonnepanelen met een thuisbatterij
- **Zoeken** op gemeentenaam of postcode (vier cijfers).
- Een Vlaams gebied met meer dan 200 installaties en minder dan 15% batterijen krijgt het label "Weinig batterijen, veel panelen".
- Directe link naar een gemeente: zet de code achter `#`, bijvoorbeeld `#GM0344` (Utrecht) of `#BE44021` (Gent).

## 3. Databronnen

| Wat | Bron | Peildatum | Niveau |
|---|---|---|---|
| Zonnepanelen bij woningen, NL | CBS StatLine **85005NED**, "Zonnestroom; vermogen en vermogensklasse, bedrijven en woningen, regio", sector *Woningen* | 2019 t/m 2025 (2024 en 2025 nader voorlopig) | gemeente |
| Zonnepanelen bij woningen, NL | CBS **86044NED**, "Zonnestroom; vermogen zonnepanelen woningen, wijken en buurten, 2022" | 2022 (nieuwste die bestaat) | wijk, buurt |
| Woningvoorraad, WOZ, koopwoningen, inkomen, postcode, NL | CBS **85318NED** Kerncijfers wijken en buurten 2022, en **86165NED** Kerncijfers 2025 (gemeenten) | 2022 / 2025 | gemeente, wijk, buurt |
| Grenzen NL | PDOK WFS `cbs/wijkenbuurten/2022` (wijken, buurten) en `cbs/gebiedsindelingen/2025` (gemeenten, provincies, gegeneraliseerd) | 2022 / 2025 | |
| Zonnepanelen, VL | Fluvius open data, dataset `1_20` "Lijst van decentrale productie-installaties gekoppeld aan het distributienet", type *Photovoltaic*, alleen **laagspanning** | 30-09-2026 | postcode |
| Thuisbatterijen, VL | Fluvius open data, dataset `1_22` "Energieopslagsystemen gekoppeld op distributienet", type *Thuisbatterij* | 30-09-2026 | postcode |
| Aansluitingen, VL | Fluvius open data, dataset `1_17` "Aantal actieve toegangspunten", elektriciteit, klantengroep LS, maand 2026-09 | 09-2026 | postcode, met gemeentenaam |
| Gemeente- en provinciegrenzen VL | Digitaal Vlaanderen WFS **VRBG2025** (`RefgemG10`, `RefprvG10`) | 2025 | |
| Postcodegrenzen VL | OpenStreetMap, relaties `boundary=postal_code`, via de Overpass API | oktober 2026 | |

Licenties: CBS CC BY 4.0, Fluvius open data, OpenStreetMap ODbL. De bronvermelding staat ook onderaan het paneel van de kaart. Laat die staan als je de kaart publiceert.

## 4. Wat er met de data is gedaan

### Nederland
1. Wijk- en buurtgrenzen 2022 opgehaald bij PDOK, in pagina's van 1000, alleen land (geen water). Scripts: `scripts/fetch_pdok.py`, `scripts/fetch_cbs.py`.
2. **Gemeenten 2025**: installaties 2025 gedeeld door de woningvoorraad 2025 geeft "% woningen met zonnepanelen". Daarnaast de reeks 2019–2025 (staafjes in het paneel) en de groei sinds 2022.
3. **Wijken en buurten 2022**: installaties gedeeld door de woningvoorraad 2022. Bij minder dan 10 woningen wordt geen percentage getoond.
4. Gemeentelijke herindelingen tussen 2022 en 2025 zijn opgevangen door elke buurt te koppelen aan de 2025-gemeente waarin hij ligt (punt-in-polygoon, meerderheid per 2022-gemeente). Weesp gaat zo naar Amsterdam, en Brielle, Hellevoetsluis en Westvoorne naar Voorne aan Zee. Script: `scripts/process_nl.py`.
5. **Postcodegebieden (PC4)**: CBS publiceert geen zonnepanelen per postcode. Buurten zijn daarom samengevoegd op hun *meest voorkomende postcode*. Dat is een benadering, geen echte postcodegrens.
6. Vereenvoudigd met mapshaper (12% van de punten) en per provincie weggeschreven als TopoJSON (`data/nl/<provincie>.json`, met de lagen `wijk`, `buurt` en `pc4`).

### Vlaanderen
1. Bij Fluvius geaggregeerd per postcode: aantal installaties met zonnepanelen (laagspanning) en hun vermogen, aantal thuisbatterijen en hun capaciteit, en het aantal actieve laagspanningsaansluitingen. Script: `scripts/process_be.py`.
2. Elke postcode is via de gemeentenaam in de aansluitingendata gekoppeld aan een gemeente uit VRBG 2025. Die namen volgen al de fusies van 2025, en elke postcode valt in precies één gemeente.
3. "% met panelen" = installaties gedeeld door laagspanningsaansluitingen (bij minder dan 20 aansluitingen geen percentage).
   "Batterij %" = batterijen gedeeld door installaties.
   "Kansen" = installaties min batterijen.
4. Postcodegrenzen komen van OpenStreetMap: alle 518 Vlaamse postcodes gevonden. Ze zijn bijgesneden tot Vlaanderen, vereenvoudigd en per provincie opgeslagen (`data/be/<provincie>.json`). Scripts: `scripts/fetch_osm.sh`, `scripts/build_be.sh`.

### De pagina
- `index.html` is één bestand met HTML, CSS en JavaScript. Het gebruikt d3 7.8.5 (via cdnjs) en topojson-client 3.1.0 (via jsDelivr), plus Google Fonts.
- Bij het openen laadt de pagina alleen `data/overview.json` (±130 kB gecomprimeerd). Bij een klik op een gemeente komt alleen de bijbehorende provincie erbij.
- `scripts/standalone.py` maakt een variant met alle data erin (±14 MB). Die werkt met een dubbelklik, zonder server.

## 5. Kerngetallen (bij het maken)

- **Nederland, 2025**: 3.041.543 installaties bij woningen, dus **36,8%** van de woningen.
- **Vlaanderen, september 2026**: 1.089.083 installaties op laagspanning, dus **29,7%** van de aansluitingen.
- **Vlaanderen**: 191.408 thuisbatterijen, en **897.675** installaties zonder batterij.
- Hoogste gemeenten: Tynaarlo 66,6%, Dantumadiel 61,8%, Kapelle 60,7%. In Vlaanderen is Kinrooi het hoogst met 51,3%, terwijl daar maar 10,3% van de eigenaars van zonnepanelen een batterij heeft.

## 6. Waar je op moet letten

- **Verschillende jaren in Nederland.** Gemeenten tonen 2025, wijken en buurten 2022, want nieuwere buurtcijfers bestaan niet. Een buurtpercentage ligt daardoor vaak lager dan het gemeentepercentage. Het paneel toont het label "CBS 2022".
- **Nederland en Vlaanderen zijn niet één-op-één vergelijkbaar.** Nederland deelt door woningen, Vlaanderen door laagspanningsaansluitingen, en daar zitten ook kleine bedrijven bij. Het Vlaamse percentage ligt daardoor iets te laag.
- **Een installatie is niet precies een woning.** Eén installatie op een appartementencomplex telt als één.
- **Batterijdata bestaat alleen voor Vlaanderen.** Nederland publiceert geen thuisbatterijen per gemeente.
- **Nederlandse postcodegebieden zijn een benadering** via buurten. Een PC4-gebied dat over een gemeentegrens loopt, telt de buurten van beide kanten mee.
- **Grenzen zijn vereenvoudigd.** De gegeneraliseerde gemeentegrens 2025 sluit niet altijd precies aan op de gedetailleerde wijken van 2022.

## 7. Online zetten

Er zijn drie manieren:

1. **De map uploaden** naar een gewone webhost (Netlify, Vercel, GitHub Pages, eigen server): `index.html` met `data/` ernaast. Dit werkt direct.
2. **Nodefy Pages** (page.nodefy.nl) host per slug maar één HTML-bestand, zonder datamap. Een eerste poging liep daarom vast op "De kaartgegevens konden niet laden: data/overview.json". De oplossing:
   - zet deze repo **openbaar** op GitHub;
   - vul in `index.html` bovenaan in het script het data-adres in:
     ```js
     const DATA_BASE = 'https://cdn.jsdelivr.net/gh/<organisatie>/<repo>@main/';
     ```
   - plak die `index.html` in Nodefy Pages. jsDelivr serveert de data dan gratis via zijn CDN.

   Of plak de losse variant van 14 MB, als Nodefy Pages zo'n groot bestand accepteert.
3. **Op een bestaande website** (Framer, WordPress): host de kaart met optie 1 of 2 en toon hem met een iframe:
   ```html
   <iframe src="https://.../" style="width:100%;height:800px;border:0" loading="lazy"></iframe>
   ```

Voor een publieke pagina wil je waarschijnlijk nog de ondertitel aanpassen (die zegt nu "voor Bob Laadt Op") en een knop naar de offerte- of contactpagina toevoegen.

## 8. Bijwerken

- **Vlaanderen**: Fluvius werkt maandelijks bij. Draai de aggregaties uit `scripts/process_be.py` en `scripts/build_be.sh` opnieuw.
  - De Fluvius-API heet `opendata.fluvius.be/api/explore/v2.1`. Tel installaties met `count(*)`, niet met het veld `counter`: dat is een id.
- **Nederland**: CBS publiceert 85005NED jaarlijks (rond juni). Nieuwe buurtcijfers voor zonnestroom na 2022 zijn er bij het maken nog niet.
- **Benodigde tools**: Python 3, Node met `mapshaper` en `osmtogeojson` (npm).
  - De scripts gaan uit van een werkmap met `raw/`, `build/` en `tools/`. `build_be.sh` krijgt die werkmap als argument mee.
  - De ruwe downloads zitten niet in deze repo (meer dan 500 MB). Ze zijn met de scripts opnieuw op te halen.
  - De Overpass API van OSM is soms overbelast. `fetch_osm.sh` probeert het daarom in blokken en wacht steeds langer tussen pogingen.

## 9. Verloop van het gesprek

1. Vraag gesteld: een interactieve kaart van zonnepanelen in Nederland en Vlaanderen, met drill-down, voor Bob Laadt Op.
2. Bronnen gezocht. CBS bleek tot buurtniveau te gaan (2022) en per gemeente tot 2025. Fluvius bleek per postcode zowel zonnepanelen als thuisbatterijen te hebben, wat voor de verkoop van batterijen extra waardevol is.
3. Data en grenzen opgehaald en gekoppeld. Gemeentefusies tussen 2022 en 2025 en een Nederlandse postcodelaag via buurten opgelost.
4. Kaartpagina gebouwd en getest (Utrecht, Leidsche Rijn, postcodes, Kinrooi). Eerste versie gepubliceerd als privé Claude-artifact.
5. Losse HTML met ingebakken data gemaakt (`zonnepanelenkaart.html`).
6. Code van de pagina in de chat uitgeschreven.
7. Postcodegrenzen Vlaanderen binnen (na wachten op de overbelaste Overpass-server). Getest met Gent en met zoeken op postcode 2930. Alles bijgewerkt.
8. Online zetten op page.nodefy.nl: werkte niet zonder datamap. Daarom het data-adres `DATA_BASE` toegevoegd en GitHub met jsDelivr voorgesteld.
9. Repo "Bob laat op monitor" lokaal klaargezet. Op de gebruikte Mac was geen GitHub-login, dus deze zip is gemaakt om de repo vanaf een andere computer te uploaden.
