# 📱 GITHUB OAUTH COPILOT-STYLE SETUP GUIDE
# ==========================================

## 🎯 **AKKURAT SOM VS CODE GITHUB COPILOT AUTHENTICATION**

Dette systemet implementerer **nøyaktig samme autentiseringsflow** som VS Code GitHub Copilot bruker:

1. **Device Flow** - Generate device code
2. **Mobile/Browser** - User opens GitHub mobilapp eller browser
3. **Kode Input** - Skriver inn device code (akkurat som Copilot)
4. **Automatic Completion** - Automatic redirect tilbake til portal

## 🔧 **OPPSETT INSTRUKSJONER**

### **Steg 1: Opprett GitHub OAuth App**

1. Gå til: https://github.com/settings/applications/new
2. Fyll ut:
   - **Application name:** `PsychoNoir Kontrapunkt Copilot Connector`
   - **Homepage URL:** `http://localhost:5002`
   - **Application description:** `Cross-platform AI session archaeology and GitHub Copilot integration`
   - **Authorization callback URL:** `http://localhost:5002/callback`

3. Klikk **"Register application"**

4. På den nye app-siden, kopier:
   - **Client ID** (ser ut som: `Iv1.a6b7c8d9e0f1g2h3`)
   - **Client Secret** (klikk "Generate a new client secret")

### **Steg 2: Konfigurer OAuth Credentials**

Rediger filen: `backend/python/github_oauth_copilot_auth.py`

```python
# Erstatt disse linjene med dine faktiske verdier:
GITHUB_CLIENT_ID = "din_client_id_her"           # Fra GitHub OAuth app
GITHUB_CLIENT_SECRET = "din_client_secret_her"   # Fra GitHub OAuth app
```

### **Steg 3: Start OAuth Server**

```bash
# Start OAuth authentication server
python3 backend/python/github_oauth_copilot_auth.py

# Serveren starter på: http://localhost:5002
```

### **Steg 4: Test Authentication Flow**

1. **Åpne OAuth Portal:** http://localhost:5002
2. **Klikk "Start GitHub Authentication"**
3. **Få device code** (f.eks. `WDJB-MJHT`)
4. **Åpne GitHub mobilapp** eller gå til: https://github.com/login/device
5. **Skriv inn device code**
6. **Autoriser appen**
7. **Automatic redirect** tilbake til Copilot Portal

## 🔄 **AUTHENTICATION FLOW DIAGRAM**

```
1. User → [Start Auth] → OAuth Server
2. OAuth Server → GitHub API → [Device Code Request]
3. GitHub API → OAuth Server → [device_code + user_code]
4. OAuth Server → User → [Display user_code + QR]
5. User → GitHub Mobile/Browser → [Enter user_code]
6. GitHub → User → [Authorize App]
7. OAuth Server ← GitHub API ← [Poll for token]
8. OAuth Server → User → [Authentication Success]
9. User → Copilot Portal → [Full Access]
```

## 📱 **MOBILE EXPERIENCE (Akkurat som VS Code)**

### **QR Code Option:**
- Automatisk generert QR-kode
- Skann med GitHub mobilapp
- Direct link til authorization

### **Manual Code Entry:**
- Display device code (f.eks. `WDJB-MJHT`)
- User opens GitHub mobilapp
- Navigate to Settings → Developer settings → Personal access tokens
- Eller gå direkte til: github.com/login/device

### **Automatic Completion:**
- Polling hver 5 sekunder
- Automatic detection når user authorizes
- Seamless redirect til Copilot Portal

## 🔐 **SECURITY FEATURES**

### **OAuth 2.0 Device Flow:**
- **No secrets exposed** i frontend
- **Time-limited codes** (15 minutter expiry)
- **Rate limiting** på polling
- **Secure token storage** på server

### **Copilot-Style Scopes:**
```python
scopes = [
    "user:email",     # Basic user info
    "read:user",      # Read user profile
    "repo",           # Repository access (for Copilot features)
    "copilot"         # GitHub Copilot access (if available)
]
```

## 🚀 **INTEGRATION MED HOVEDSYSTEM**

### **Session Bridging:**
```python
# Etter vellykket OAuth:
session_id = secrets.token_urlsafe(32)
authenticated_sessions[session_id] = {
    "access_token": access_token,
    "user": user_info,
    "has_copilot": check_copilot_access(access_token)
}

# Redirect til hovedportal med session:
redirect(f'http://127.0.0.1:5001?github_session={session_id}')
```

### **API Integration:**
- **GitHub API calls** med OAuth token
- **Copilot billing check** for subscription status
- **Repository access** for session storage
- **User profile** for personalization

## 🎭 **PSYCHO-NOIR THEMING**

OAuth portalen bruker samme Psycho-Noir estetikk:
- **Dark theme** med gradient bakgrunner
- **Terminal-style** fonts og farger
- **Glitch effects** på feilmeldinger
- **Neural pattern** animasjoner under authentication

## 📊 **TESTING CHECKLIST**

- [ ] GitHub OAuth app opprettet og konfigurert
- [ ] Client ID og Secret oppdatert i kode
- [ ] OAuth server starter på port 5002
- [ ] Device code generation fungerer
- [ ] QR code genereres riktig
- [ ] Mobile authorization flow fungerer
- [ ] Automatic polling og completion
- [ ] Session redirect til hovedportal
- [ ] Copilot access detection
- [ ] Error handling for expired/denied codes

## 🔧 **TROUBLESHOOTING**

### **"Client ID not found" error:**
- Sjekk at GITHUB_CLIENT_ID er riktig oppdatert
- Verifiser at OAuth app er "Public" ikke "Private"

### **"Invalid redirect URI" error:**
- Sjekk at callback URL er: `http://localhost:5002/callback`
- Ikke glem http:// prefix

### **"Authorization pending" stuck:**
- User må faktisk authorere appen på GitHub
- Sjekk at device code ikke er expired (15 min)

### **Copilot access ikke detektert:**
- User trenger aktiv GitHub Copilot subscription
- Eller app trenger "copilot" scope (kun for business accounts)

## 🎯 **READY FOR POISONTR33S GITHUB INTEGRATION**

Med dette systemet kan du:
1. **Autentisere akkurat som VS Code Copilot**
2. **Bruke GitHub mobilappen for kode-input**
3. **Få full access til dine GitHub repos og Copilot features**
4. **Seamless integration med hovedportal**
5. **Session archaeology på tvers av GitHub og andre AI platforms**

**Start OAuth server og test authentication flow!** 🚀
