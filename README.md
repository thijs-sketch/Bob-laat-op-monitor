# Bob laat op monitor

Interactieve kaart van zonnepanelen in Nederland en Vlaanderen, per gemeente, wijk, buurt en postcode. Voor Vlaanderen ook thuisbatterijen.

- `index.html`: de kaart
- `data/overview.json`: alle gemeenten (NL + VL) met provinciegrenzen
- `data/nl_pc4.json`: zoekindex voor Nederlandse postcodes
- `data/nl/<provincie>.json`: wijken, buurten en postcodegebieden per Nederlandse provincie
- `data/be/<provincie>.json`: postcodes per Vlaamse provincie

## Bronnen
- CBS 85005NED (zonnestroom per gemeente, 2025), 86044NED (wijken en buurten, 2022), Kerncijfers wijken en buurten 2022 en 2025 (CC BY 4.0)
- Fluvius open data, peildatum 30-09-2026
- Grenzen: CBS/PDOK, Digitaal Vlaanderen (VRBG 2025), postcodezones © OpenStreetMap-bijdragers (ODbL)
