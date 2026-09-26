# Project Context: Komify

## Tech Stack
* **Frontend:** Next.js (React 19), Tailwind CSS v4, shadcn/ui, dnd-kit.
* **Backend:** NestJS, Prisma ORM, Puppeteer, Cheerio, Sharp. (Involves web scraping and image processing).
* **Database:** PostgreSQL.
* **Infrastructure:** Docker Compose (for dev and prod PostgreSQL instances).
* **Runtime/Tools:** Node.js, Bun.

## Project Structure
* `/frontend`: Contains the Next.js frontend application.
* `/backend`: Contains the NestJS backend application.
* `/infra`: Contains infrastructure configurations, including `docker-compose.yml` for running local databases (`postgres_dev` on port 6010, `postgres_prod` on port 6011).

## Overview
Komify is a full-stack web application. Based on the tools used in the backend (Puppeteer, Cheerio, and Sharp), the system likely involves scraping content (such as images, comics, or manga) from external sources, processing them, and serving them via the NestJS API to the Next.js frontend.
