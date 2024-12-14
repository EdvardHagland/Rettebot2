# Norsk Vurderingsassistent

Et verktøy for automatisk vurdering av elevbesvarelser basert på kompetansemål fra Utdanningsdirektoratet.

## Om Prosjektet

Dette er en prototype på et vurderingsverktøy som bruker GPT-4o-mini og GPT-4o for å analysere og vurdere elevbesvarelser. Systemet integrerer kompetansemål fra UDIR for å gi konsistente vurderinger.

### Nåværende Funksjoner

- Dropdown-meny for valg av:
  - Klassetrinn (8-10, VG1-3)
  - Fag
- Automatisk lasting av relevante kompetansemål fra UDIR
- GPT-4o basert vurdering som returnerer:
  - Karakter
  - Begrunnelse
  - Elevtilbakemelding
- Excel-eksport av vurderinger med grafisk fremstilling av karakterdistribusjon

### Planlagte Funksjoner

- Støtte for nynorsk
- Integrasjon av vurderingsmatriser for eksamen/tentamen
- Utvidet testing mot historiske besvarelser

## Teknisk Implementasjon

### Systemarkitektur

1. Frontend:
   - To dropdown-menyer (klassetrinn, fag)
   - Input for elevbesvarelse

2. Backend:
   - Kompetansemål-database
   - System-prompt konfigurasjon
   - GPT-4o integrasjon

3. Output:
   - JSON struktur med:
     - Filnavn
     - Karakter
     - Begrunnelse
     - Elevtilbakemelding
   - Excel-generering av resultater

### Dataflyt

1. Brukervalg → lasting av kompetansemål
2. Elevbesvarelse + kompetansemål → GPT-4o
3. GPT-4o output → JSON formattering
4. JSON → Excel-generering

## Testing og Validering

Systemet er i prototype-fase:
- Teknisk testing med syntetiske besvarelser er gjennomført
- Planlagt validering mot historiske elevbesvarelser med ekspertkarakterer
- Prompt-optimalisering vil bli gjennomført basert på testresultater

## Utviklingsplan

1. Fullføre teknisk testing av grunnfunksjonalitet
2. Implementere støtte for nynorsk
3. Integrere vurderingsmatriser
4. Validere mot historiske data
5. Optimalisere prompts basert på testresultater
6. Erstatte lokal database av kompetansemål med en dynamisk loading a gjennom UDIRs Grep API
