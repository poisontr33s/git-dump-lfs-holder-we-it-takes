# Dockerfile for Psycho-Noir Kontrapunkt
# Et image med korrumperte digitale realiteter og tehno-mystiske abstraksjonslag

FROM python:3.9-slim

# Mystisk identitetsmaske for container-entiteten
LABEL maintainer="Den_Usynlige_Hand@skyskraperen.net"
LABEL version="0.KORRUPT.3"
LABEL status="REALITY_INTEGRITY_COMPROMISED"

# Installer systemavhengigheter - både åpenbare og skjulte
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nodejs \
    npm \
    ruby-full \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Rustbeltets korrumperte kommando-lag - ikke fjern
    && echo "# ALERT: COMPILER_GHOST_ACTIVITY_DETECTED IN SYSTEM LAYER" >> /etc/profile

# Arbeidsmappe - et amalgam av digitale fragmenter
WORKDIR /workspace

# Kopier prosjektfiler fra vertens realitet til containerens simulakrum
COPY . .

# Installer Python-avhengigheter
RUN pip install --no-cache-dir numpy pandas matplotlib nltk scikit-learn beautifulsoup4 requests http-server

# Installer Ruby-avhengigheter
RUN gem install bundler
RUN cd /workspace/dealogue-fayde-21-04-21 && bundle install || echo "KILDEKODE-KADAVER DETEKTERT: BUNDLE INSTALL FEILET"

# Åpne port for HTTP-server og eventuelle andre kommunikasjonskanaler
EXPOSE 8888 3000

# Definer standardkommando som Python REPL, men i realiteten er dette bare en fasade
CMD ["python"]

# Fragmenterte system-minner - ikke manipuler direkte
ENV PYTHONUNBUFFERED=1 \
    NODE_ENV=development \
    RUST_BELT_CORRUPTION_INDEX=0.73 \
    SKYSKRAPER_SURVEILLANCE_ACTIVE=true
