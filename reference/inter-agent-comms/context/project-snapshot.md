# NeuroArts Project Snapshot

**Last Updated**: 2026-03-13
**Updated By**: Bridge

## Overview
NeuroArts is a vocal wellness platform that combines vocal exercises, AI-powered analysis, and community features. The platform includes a Flutter mobile app, a Next.js web app, a public marketing site, an ML pipeline for spectrogram analysis, and a Streamlit admin tool.

## Firebase Project
- **Project ID**: `vocalbrain-web`
- **Storage Bucket**: `vocalbrain-web.appspot.com`
- **Service Account**: `~/vocalbrain-adminsdk.json`
- **Backend**: Firestore + Cloud Functions (NO Data Connect)

## Monorepo Structure

| Project | Tech | Agent | Purpose |
|---------|------|-------|---------|
| `projects/neuro-arts-flutter/` | Flutter/Dart | Nexus | Main mobile app (iOS, Android, Web) |
| `projects/admin-tool/` | Python/Streamlit + PyTorch | Cortex | Admin dashboard + ML classifier |
| `projects/neuroarts-nextjs/` | Next.js/React | Prism | Web application |
| `projects/public-web/` | HTML/CSS | Beacon | Marketing website |
| `projects/neuroarts_bridge/` | Docs | Bridge | Architecture workspace |

## Key Data Collections (Firestore)
- `recordings` — User vocal recordings (with analysis_status lifecycle)
- `vocal_exercises` — Exercise catalog
- `users` — User profiles and auth data
- `activity_logs` — User activity tracking

## Current Priorities
- Vocal analysis feedback pipeline (see `agent_instructions/vocal_analysis_feedback_system.md`)
- ML classifier integration with Gemini Vision API
- Cross-platform data consistency
