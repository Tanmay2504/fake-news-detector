# Fake News Detector - Frontend

React + TypeScript + Vite frontend with beautiful animated UI using shadcn/ui and Framer Motion.

## Features

- **Animated Landing Page**: Beautiful background paths animation with letter-by-letter text reveal
- **Text Analysis**: Paste news articles and get instant AI-powered fake news detection
- **Real-time Results**: See confidence scores, probability breakdowns, and model predictions
- **Rule-based Indicators**: View fake/real pattern analysis
- **Dark Mode Ready**: Full dark mode support
- **Responsive Design**: Works on all screen sizes

## Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running on `http://localhost:8000`

### Installation

```powershell
cd frontend
npm install
```

### Development

Start the dev server with API proxy:

```powershell
npm run dev
```

The app will be available at `http://localhost:5173` and automatically proxy API calls to your backend.

### Build for Production

```powershell
npm run build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── button.tsx           # shadcn/ui Button component
│   │   │   └── background-paths.tsx  # Animated landing page
│   │   └── FakeNewsDetector.tsx     # Main detection interface
│   ├── lib/
│   │   ├── api.ts                   # Backend API client
│   │   └── utils.ts                 # Tailwind utilities
│   ├── App.tsx                      # Main app component
│   ├── main.tsx                     # Entry point
│   └── index.css                    # Global styles
├── package.json
├── vite.config.ts                   # Vite config with proxy
├── tailwind.config.js               # Tailwind CSS config
└── tsconfig.json                    # TypeScript config
```

## API Integration

The frontend communicates with the FastAPI backend via proxy configuration in `vite.config.ts`:

```typescript
'/api' → 'http://localhost:8000'
```

All API calls in `src/lib/api.ts` use the `/api` prefix which gets rewritten to hit the backend.

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful component library
- **Framer Motion** - Smooth animations
- **Lucide React** - Icons
- **Axios** - HTTP client

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Deployment

### Build Static Files

```powershell
npm run build
```

Output will be in `dist/` folder. Serve these files with any static host (Netlify, Vercel, etc.) and configure the API base URL.

### Environment Variables

For production, update the API base URL in `src/lib/api.ts`:

```typescript
const API_BASE_URL = process.env.VITE_API_URL || '/api';
```

Then set `VITE_API_URL` in your deployment environment.

## License

MIT
