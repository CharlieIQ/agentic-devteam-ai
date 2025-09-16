# Backend Test Commands

## 1. Health Check (GET)
curl http://localhost:5001/api/health

## 2. Get Team Configuration (GET)
curl http://localhost:5001/api/teams/config

## 3. Save Requirements (POST)
curl -X POST http://localhost:5001/api/requirements \
  -H "Content-Type: application/json" \
  -d '{"requirements":"Build a simple todo app with React and Node.js"}'

## 4. Generate Code (POST)
curl -X POST http://localhost:5001/api/code-generation \
  -H "Content-Type: application/json" \
  -d '{"requirements":"Create a login form with validation"}'

## 5. Test Live Logs (SSE endpoint)
curl http://localhost:5001/api/logs
``` ## What We Accomplished ✨