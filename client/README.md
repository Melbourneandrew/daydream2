# Daydream Client

A React + TypeScript frontend for the Daydream application built with Vite.

## Environment Configuration

The application uses environment variables to configure the API base URL for different environments:

### Development

- Copy `.env.example` to `.env`
- The default development URL is `http://localhost:8000`

### Production

- Copy `.env.production.example` to `.env.production`
- The production URL is `https://daydream.melbournedev.com`

### Environment Variables

- `VITE_API_BASE_URL`: The base URL for the API server

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for development/default environment
- `npm run build:prod`: Build for production (uses .env.production)
- `npm run preview`: Preview the built application
- `npm run lint`: Run ESLint

## Building for Different Environments

```bash
# Development build (uses .env)
npm run build

# Production build (uses .env.production)
npm run build:prod
```

The application will automatically use the correct API URL based on the environment variables configured in the respective `.env` files.
