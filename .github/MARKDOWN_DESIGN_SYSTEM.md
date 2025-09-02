# 🎭 **Psycho-Noir Markdown DESIGN SYSTEM**

## **Kreativ Dokumentasjon & Styling Standarder**

> _"I en verden av kaos og kompleksitet, blir dokumentasjon vårt mentale kart gjennom mørket"_

---

## 📋 **INNHOLDSFORTEGNELSE**

- [🎯 Design Filosofi](#-design-filosofi)
- [📏 Linting Standarder](#-linting-standarder)
- [🎨 Kreativ Styling](#-kreativ-styling)
- [📝 Dokumentasjon Templates](#-dokumentasjon-templates)
- [🔧 Verktøy & Automatisering](#-verktøy--automatisering)
- [📊 Kvalitetssikring](#-kvalitetssikring)

---

## 🎯 **DESIGN FILOSOFI**

### **Psyko-Noir Estetikk**
- **Atmosfærisk**: Dokumentasjon som et narrativt element
- **Dualitet**: Balanse mellom teknisk presisjon og kreativ utfoldelse
- **Symbolikk**: Bruk av ikoner og metaforer for dypere forståelse
- **Interaktivitet**: Dokumentasjon som guider brukeren gjennom kompleksitet

### **Kjerneprinsipper**
```markdown
🌙 **Mørk Eleganse** - Sophisticated yet accessible
🔮 **Intuitiv Guidning** - Clear paths through complexity
🎭 **Narrativ Flyt** - Documentation as storytelling
⚡ **Teknisk Presisjon** - Accuracy without sacrificing style
```

---

## 📏 **LINTING STANDARDER**

### **1. Struktur & Formatering**

#### **Overskrifter**

```markdown
# 🎭 HOVEDTITTEL (Level 1)
## 🔍 Undertittel (Level 2)
### ⚡ Seksjon (Level 3)
#### 📝 Underseksjon (Level 4)
##### 💡 Detalj (Level 5)
```

#### **Avsnitt & Linjeskift**

```markdown
<!-- ✅ KORREKT -->
Dette er et avsnitt med naturlig flyt.
Neste avsnitt starter her.

<!-- ❌ FEIL -->
Dette er et avsnitt med naturlig flyt.
Neste avsnitt starter her.
```

### **2. Lenker & Referanser**

#### **Interne Lenker**
```markdown
<!-- ✅ KORREKT -->
[Se også](#seksjon-navn)
[Detaljert guide](./docs/guide.md)

<!-- ❌ FEIL -->
[se også](#seksjon-navn)
[guide](./docs/guide.md)
```

#### **Eksterne Lenker**
```markdown
<!-- ✅ KORREKT -->
[GitHub Repository](https://github.com/poisontr33s/PsychoNoir-Kontrapunkt)
[VS Code Marketplace](https://marketplace.visualstudio.com/)

<!-- ❌ FEIL -->
[GitHub](https://github.com/poisontr33s/PsychoNoir-Kontrapunkt)
[Marketplace](https://marketplace.visualstudio.com/)
```

### **3. Kodeblokker**

#### **Syntax Highlighting**
```markdown
<!-- ✅ KORREKT -->
```typescript
const example: string = "Hello World";
```

```python
def example_function():
    return "Hello World"
```

<!-- ❌ FEIL -->
```
const example = "Hello World";
```

def example_function():
    return "Hello World"
```

#### **Inline Kode**
```markdown
<!-- ✅ KORREKT -->
Bruk `npm install` for å installere dependencies.

<!-- ❌ FEIL -->
Bruk npm install for å installere dependencies.
```

### **4. Lister**

#### **Oppgave Lister**
```markdown
<!-- ✅ KORREKT -->
- [x] ✅ Fullført oppgave
- [ ] ⏳ Pågående oppgave
- [ ] ❌ Blokkerende issue

<!-- ❌ FEIL -->
- Fullført oppgave
- Pågående oppgave
- Blokkerende issue
```

#### **Nummererte Lister**
```markdown
<!-- ✅ KORREKT -->
1. 📋 Forberedelse
2. 🔧 Implementering
3. ✅ Testing
4. 🚀 Deployment

<!-- ❌ FEIL -->
1. Forberedelse
2. Implementering
3. Testing
4. Deployment
```

---

## 🎨 **KREATIV STYLING**

### **1. Ikonografi System**

#### **Funksjonelle Ikoner**
```markdown
🎯 **Mål/Objektiv** - Target/goal oriented content
🔍 **Analyse** - Investigation, research, inspection
⚡ **Handling** - Action, execution, implementation
📊 **Data/Analyse** - Statistics, metrics, reporting
🔧 **Verktøy** - Tools, utilities, configuration
🎭 **Psyko-Noir** - Core branding, main features
```

#### **Status Ikoner**
```markdown
✅ **Fullført** - Completed, successful
⏳ **Pågående** - In progress, pending
❌ **Feil/Problem** - Error, issue, blocker
⚠️ **Advarsel** - Warning, caution needed
🔄 **Iterasjon** - Cycle, iteration, update
```

#### **Type Ikoner**
```markdown
📋 **Dokumentasjon** - Guides, manuals, references
🔬 **Teknisk** - Code, implementation details
🎨 **Design** - UI/UX, styling, aesthetics
🧠 **AI/ML** - Artificial intelligence, machine learning
🌐 **Web/Cloud** - Web technologies, cloud services
```

### **2. Fargekodet Status System**

#### **Prioritetsfarger**
```markdown
🔴 **KRITISK** - Critical issues, immediate action required
🟠 **HØY** - High priority, important but not urgent
🟡 **MEDIUM** - Medium priority, plan for next sprint
🟢 **LAV** - Low priority, nice to have
```

#### **Kvalitetsfarger**
```markdown
💎 **PLATINUM** - Exceptional quality, gold standard
🏆 **GOLD** - High quality, well above average
🥈 **SILVER** - Good quality, meets expectations
🥉 **BRONZE** - Acceptable quality, needs improvement
```

### **3. Narrativ Struktur**

#### **Storytelling Framework**
```markdown
# 🎭 [DRAMATISK TITTEL]

> *"Hook line som fanger oppmerksomheten"*

## 🌙 Bakgrunn (Context)
*Hvorfor er dette viktig? Hva er problemet vi løser?*

## 🔍 Analyse (Investigation)
*Hva har vi oppdaget? Hvilke mønstre finnes?*

## ⚡ Løsning (Solution)
*Hvordan løser vi problemet? Hva er strategien?*

## 🎯 Implementering (Implementation)
*Konkrerte steg og handlinger*

## 📊 Resultater (Results)
*Målinger, metrics, suksesskriterier*

## 🚀 Neste Steg (Next Steps)
*Hva kommer videre? Fremtidige muligheter*
```

---

## 📝 **DOKUMENTASJON TEMPLATES**

### **1. Prosjekt Dokumentasjon**

```markdown
# 🎭 [PROSJEKT NAVN]
## [Kort beskrivelse av formål]

> *"Inspirerende sitat eller hook"*

### 📋 Oversikt
- **Status:** [🟢 Aktiv | 🟡 Vedlikehold | 🔴 Arkivert]
- **Prioritet:** [🔴 Kritisk | 🟠 Høy | 🟡 Medium | 🟢 Lav]
- **Kompleksitet:** [💎 Platinum | 🏆 Gold | 🥈 Silver | 🥉 Bronze]

### 🎯 Mål & Omfang
*Hva skal oppnås? Hvilke grenser gjelder?*

### 🔧 Teknisk Arkitektur
*System design, komponenter, teknologier*

### 📊 Suksess Metrics
*Hvordan måler vi suksess? KPI-er?*

### 🚀 Implementeringsplan
1. [ ] Fase 1: [Beskrivelse]
2. [ ] Fase 2: [Beskrivelse]
3. [ ] Fase 3: [Beskrivelse]

### 👥 Team & Ansvar
*Hvem gjør hva? Roller og ansvar*

---
*Generert: [Dato] | Forfatter: [Navn]*
```

### **2. API Dokumentasjon**

```markdown
# 🔌 [API NAVN] API
## [Versjon] - [Status]

### 🌐 Base URL
```
https://api.psycho-noir.example.com/v1
```

### 🔐 Autentisering
```bash
Authorization: Bearer <token>
```

### 📚 Endepunkter

#### `GET /sessions`
**Beskrivelse:** Henter alle aktive økter

**Parametere:**
- `limit` (number, optional): Maks antall resultater (default: 50)
- `offset` (number, optional): Offset for paginering (default: 0)

**Respons:**
```json
{
  "sessions": [
    {
      "id": "string",
      "name": "string",
      "status": "active",
      "created_at": "2025-08-31T12:00:00Z"
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

**Eksempel:**
```bash
curl -H "Authorization: Bearer <token>" \
     "https://api.psycho-noir.example.com/v1/sessions?limit=10"
```

### ❌ Feilkoder
- `400` - Ugyldig forespørsel
- `401` - Uautorisert
- `404` - Ikke funnet
- `500` - Serverfeil
```

### **3. Feilsøking Guide**

```markdown
# 🔧 FEILSØKING: [PROBLEM TYPE]
## Systematisk problemløsning

### 🚨 Symptom
*Hva observeres? Feilmeldinger? Uventet oppførsel?*

### 🔍 Diagnose Steg

#### 1. **Grunnleggende Sjekker**
```bash
# Sjekk system status
systemctl status psycho-noir

# Verifiser konfigurasjon
cat /etc/psycho-noir/config.json

# Sjekk logger
tail -f /var/log/psycho-noir/app.log
```

#### 2. **Avansert Diagnostikk**
- [ ] Nettverkskonnektivitet
- [ ] Database tilkobling
- [ ] Minne og CPU bruk
- [ ] Disk plass

### 💡 Løsninger

#### **Løsning A: [Beskrivelse]**
```bash
# Konkret kommando eller steg
sudo systemctl restart psycho-noir
```

**Forventet resultat:** Systemet starter på nytt og fungerer normalt

#### **Løsning B: [Alternativ tilnærming]**
*Hvis løsning A ikke fungerer*

### 📞 Kontakt Support
Hvis problemet vedvarer:
- 📧 Email: support@psycho-noir.example.com
- 💬 Discord: [Link]
- 📋 Issue Tracker: [GitHub Issues]
```

---

## 🔧 **VERKTØY & AUTOMATISERING**

### **1. Linting Verktøy**

#### **markdownlint Configuration**
```json
{
  "default": true,
  "MD001": false,  // Heading levels should only increment by one
  "MD013": false,  // Line length
  "MD024": false,  // Multiple headers with the same content
  "MD033": false,  // Inline HTML
  "MD036": false,  // Emphasis used instead of header
  "MD041": false   // First line in file should be a top level header
}
```

#### **Prettier Configuration**
```json
{
  "proseWrap": "preserve",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": false,
  "singleQuote": true,
  "quoteProps": "as-needed",
  "trailingComma": "es5",
  "bracketSpacing": true,
  "bracketSameLine": false,
  "arrowParens": "avoid"
}
```

### **2. Automatiske Verktøy**

#### **Git Hooks for MD Quality**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Lint all markdown files
find . -name "*.md" -not -path "./node_modules/*" | xargs npx markdownlint

# Format markdown files
find . -name "*.md" -not -path "./node_modules/*" | xargs npx prettier --write
```

#### **VS Code Extensions**
```json
{
  "recommendations": [
    "DavidAnson.vscode-markdownlint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

---

## 📊 **KVALITETSSIKRING**

### **1. Kvalitetskriterier**

#### **A. Innholdskvalitet**
- [ ] **Relevans**: Informasjonen er oppdatert og relevant
- [ ] **Nøyaktighet**: Teknisk informasjon er korrekt
- [ ] **Kompletthet**: Alle nødvendige detaljer er inkludert
- [ ] **Konsistens**: Stil og terminologi er konsekvent

#### **B. Teknisk Kvalitet**
- [ ] **Linting**: Ingen linting feil
- [ ] **Formatering**: Konsistent formatering
- [ ] **Lenker**: Alle lenker fungerer
- [ ] **Kode**: Kodeeksempler er syntaktisk korrekte

#### **C. Brukeropplevelse**
- [ ] **Navigasjon**: Lett å finne informasjon
- [ ] **Lesbarhet**: Tekst er lett å lese
- [ ] **Tilgjengelighet**: Fungerer med skjermlesere
- [ ] **Mobil**: Responsiv design

### **2. Review Prosess**

#### **Review Checklist**
```markdown
## 📋 Dokumentasjon Review

### ✅ Godkjent Av
- [ ] **Teknisk Reviewer**: [Navn]
- [ ] **Innholdsspesialist**: [Navn]
- [ ] **UX Reviewer**: [Navn]

### 🔍 Review Kriterier
- [ ] Teknisk nøyaktighet
- [ ] Språk og grammatikk
- [ ] Konsistent styling
- [ ] Fungerende lenker
- [ ] Komplett innhold

### 💡 Forbedringsforslag
*

### 🎯 Endelig Vurdering
- [ ] **Godkjent** - Kan publiseres
- [ ] **Godkjent med endringer** - Små justeringer nødvendig
- [ ] **Avvist** - Krever betydelig revisjon
```

### **3. Metrikker & Målinger**

#### **Kvalitetsmetrikker**
```markdown
📊 **Dokumentasjonskvalitet Score**
- Teknisk Nøyaktighet: 95%
- Lesbarhet: 88%
- Kompletthet: 92%
- Bruker Tilfredshet: 91%

🎯 **Forbedringsområder**
- API dokumentasjon (+15%)
- Feilsøking guider (+12%)
- Video tutorials (+20%)
```

---

## 🎭 **IMPLEMENTERING**

### **1. Umiddelbare AKSJONER**

#### **Dag 1: Oppsett**
- [ ] Installer markdownlint og prettier
- [ ] Konfigurer VS Code extensions
- [ ] Sett opp git hooks
- [ ] Kjør baseline linting

#### **Dag 2-3: Standardisering**
- [ ] Oppdater eksisterende dokumentasjon
- [ ] Implementer templates
- [ ] Lage stilguide referanse
- [ ] Trene teamet

#### **Dag 4-5: Automatisering**
- [ ] Implementer CI/CD linting
- [ ] Lage dokumentasjon generatorer
- [ ] Automatiske kvalitetsrapporter
- [ ] Overvåkingsdashboard

### **2. Fremtidige Utvidelser**

#### **AI-Assistert Dokumentasjon**
- Automatisk generering av API docs
- Intelligente templates basert på kode
- Naturlig språk søk i dokumentasjon
- Personlige læringsstier

#### **Interaktiv Dokumentasjon**
- Live kode-eksempler
- Interaktive diagrammer
- Video tutorials
- Gamified læring

---

## 📞 **KONTAKT & SUPPORT**

### **Dokumentasjonsteam**
- **Lead**: [Navn] - [Email]
- **Teknisk Reviewer**: [Navn] - [Email]
- **UX Specialist**: [Navn] - [Email]

### **Ressurser**
- 📖 [Stilguide](./docs/style-guide.md)
- 🔧 [Verktøy Setup](./docs/tools-setup.md)
- 📚 [Templates](./docs/templates/)
- 💬 [Discord Community](https://discord.gg/psycho-noir)

---

> *"Dokumentasjon er ikke bare teknisk nødvendighet - det er kunstformen som gjør kompleksitet tilgjengelig"*

*Generert med ❤️ av Psycho-Noir Design System | Versjon 1.0.0*
