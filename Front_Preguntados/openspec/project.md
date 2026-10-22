# Project declaration

## What this system is

A web-based multiplayer trivia game inspired by "Preguntados", designed for two players playing locally on the same web browser. It features the classic spinning roulette wheel, category-specific visual styling and colors, turn management, and real-time questions fetched via an external REST API.

## Runtime and language

| | |
|---|---|
| Language and version | TypeScript 5.x / JavaScript (ESNext) |
| Pinned by | `package-lock.json` |
| One command to build | `npm run build` |
| One command to test | `npm test` |
| One command to lint and format | `npm run lint` |
| One command to type-check | `npx tsc --noEmit` |
| Coverage bar | 70% of statements and branches measured over core components |

## Frameworks and libraries

- **Web / API**: FastAPI (external backend service running at `http://localhost:8000`) connected to PostgreSQL.
- **Frontend SPA**: React 18+ with Vite.
- **Styling**: Tailwind CSS for custom category colors, responsive layout, and roulette animations.
- **Data access**: Native `fetch` API / Axios for querying questions at `http://localhost:8000/questions/<id>`.
- **Testing**: Vitest & React Testing Library.

## Datastores

| Store | Holds | Migrations run by |
|---|---|---|
| PostgreSQL (External Backend) | Questions, categories, and options managed by FastAPI | FastAPI backend migrations (Alembic) |

## Identity and authorization

- **How a request proves who it is**: Not required (local 2-player game on the same web browser).
- **Where the authorization check happens**: N/A
- **Acting as the user versus as the service**: N/A
- **What gets audited, and where the event is emitted**: Client-side game errors and API connectivity issues logged to browser console.

## Secrets

- **Where they live**: `.env` / environment variables (`VITE_API_BASE_URL`).
- **How a process obtains one**: Loaded at build/runtime via Vite config.
- **Never**: in source, in logs, or client-side hardcoded secrets.

## Service boundaries

| Service | Owns | Talks to | Over |
|---|---|---|---|
| Frontend Web App | UI, game state, turn mechanics, roulette animation | FastAPI Backend | HTTP REST (`http://localhost:8000/questions/<id>`) |

## Deployment

- **Target**: Static web hosting (Vercel, Netlify, or local static server).
- **Pipeline**: Standard GitHub Actions CI.
- **Artifact signing**: N/A for frontend static bundle.
- **Infrastructure as code**: None.
- **Rollback bar**: Instant rollback via static deployment history.

## Observability

- **Log shape**: Standard console logging with structured timestamps for API errors.
- **Metrics**: Browser performance insights.
- **Correlation id**: N/A for local client session.

## Conventions this project has settled

- Functional React components with hooks.
- Tailwind CSS utility classes following the classic Preguntados color palette (Geografía = Blue, Historia = Orange, Ciencia = Green, Entretenimiento = Pink, Arte = Magenta, Deportes = Yellow).
- Strict TypeScript types for question response structures: `{ id: number; question: string; answer: string; category: string; source: string }`.

## Recorded exceptions

| Deviation | Approved | ADR |
|---|---|---|
| — | — | — |
