# Psycho-Noir Kontrapunkt - Den Usynlige Hånds Docker-Manifestasjon
FROM oven/bun:1-alpine AS neural_archaeology_base

# Miljøvariabler for systemets psykologiske tilstand
ENV PSYCHO_NOIR_MODE="docker_archaeology_active"
ENV NODE_ENV="production"
ENV PYTHONPATH="/app/backend/python"
ENV BUN_RUNTIME="nautical_sophistication_active"

# Installerer systemkritiske komponenter - Begge domenenes infrastruktur
RUN apk add --no-cache \
  python3 \
  py3-pip \
  sqlite \
  curl \
  bash \
  git \
  && rm -rf /var/cache/apk/*

# Skaper nødvendige kataloger for systemets sjel
WORKDIR /app

# Frontend avhengigheter - Meta-Nautical teknologiske synapser
COPY package*.json ./
COPY bun.lockb ./
RUN bun install --lockfile
RUN bun install --frozen-lockfile --production

# Backend Python-komponenter - Rustbeltets improviserte resiliens
RUN mkdir -p backend
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip3 install -r backend/requirements.txt
RUN pip3 install -r backend/requirements.txt

COPY . .

# Build frontend hvis build script finnes - Kompilering av digital bevissthet
RUN if [ -f package.json ] && grep -q '"build"' package.json; then \
  bun run build; \
  else \
  echo "No build script detected - running in development mode"; \
  fi

# Eksponerer porter for systemets kommunikasjon
# 3000: Bun/Node frontend (main psycho-noir interface)
EXPOSE 3000
# 8080: Backend Python API (Rustbeltet improviserte resiliens)
EXPOSE 8080

# Helsesjekk - Overvåkning av systemets vital-tegn
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:3000/health 2>/dev/null || \
      curl -f http://localhost:5173/ 2>/dev/null || \
      exit 1

# Startup kommando - Aktivering av Neural Archaeology med Bun Runtime
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
