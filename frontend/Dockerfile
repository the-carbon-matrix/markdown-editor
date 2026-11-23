FROM docker.io/library/node:24-alpine

WORKDIR /app/frontend

# Install dependencies first
COPY frontend/package.json frontend/package-lock.json ./

RUN npm ci

# Copy frontend source
COPY frontend/ ./

COPY .env /app/.env

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
