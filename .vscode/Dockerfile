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
COPY package*.json bun.lockb* ./
RUN bun install --frozen-lockfile --production

# Backend Python-komponenter - Rustbeltets improviserte resiliens
RUN mkdir -p backend
RUN if [ -f backend/requirements.txt ]; then \
    cp backend/requirements.txt ./backend/requirements.txt; \
  else \
    echo "# No Python requirements found - Den Usynlige Hånd's glitch detected" > ./backend/requirements.txt; \
  fi
RUN pip3 install -r backend/requirements.txt

# Kopierer applikasjonskoden - Begge domenenes essens
COPY . .

# Build frontend hvis build script finnes - Kompilering av digital bevissthet
RUN if [ -f package.json ] && grep -q '"build"' package.json; then \
  bun run build; \
  else \
  echo "No build script detected - running in development mode"; \
  fi

# Eksponerer porter for systemets kommunikasjon
EXPOSE 3000 8080 5173

# Helsesjekk - Overvåkning av systemets vital-tegn
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:3000/health 2>/dev/null || \
  curl -f http://localhost:5173/ 2>/dev/null || \
  echo "System consciousness verification failed" && exit 1

# Startup kommando - Aktivering av Neural Archaeology med Bun Runtime
CMD if [ -f package.json ] && grep -q '"start"' package.json; then \
  bun start; \
  elif [ -f package.json ] && grep -q '"dev"' package.json; then \
  bun dev --host 0.0.0.0; \
  else \
  echo "ERROR: NEURAL_PATHWAYS_NOT_FOUND - No start or dev script detected" && \
  echo "Available scripts:" && bun run || true && \
  sleep infinity; \
  fi
