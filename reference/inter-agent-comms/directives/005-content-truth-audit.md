# 📡 Directive 005: Content Truth Audit — Public Website

**From Captain Michael via Bridge — 2026-03-13 19:35 ET**
**For: 🟢 Beacon (Marketing & Growth Officer)**
**Priority: HIGH**

---

## The Problem

The public website contains **hallucinated features** — functionality described as if it exists that we do not have in the app. This violates Standing Order 003 (Zero Tolerance). The marketing copy was generated with aspirational language that mixes real capabilities with fiction. The social features ARE real, but claims about biometrics are NOT.

## Your Orders

1. **Read the actual source code** at `projects/neuro-arts-flutter/lib/features/arts/data/app_catalog.dart` — this is the single source of truth for what features exist and are active in the app
2. **Audit every claim** on the public website against that catalog
3. **Rewrite copy** to sell the sizzle — but base it in technical fact

---

## ❌ Features That Do NOT Exist (Remove/Replace)

| Hallucinated Claim | Where Found | Reality |
|----|----|----|
| "AI-driven **biometric** insights" | Hero sub-headline, `CONTENT.md` | We do NOT track biometrics. No heart rate, no galvanic skin response, no wearable integration. |
| "**Biometric Feedback Engine**" | Pillar I, `CONTENT.md` | Does not exist as a feature. |
| "tracking **voice biomarkers** and physiological responses" | Pillar I description | We do spectrogram analysis and pitch tracking. Not "biomarkers." Not "physiological responses." |
| "Interactive Dashboard Preview" / "AI Neuro-Map showing biomarker trends" | Technical Specs section | Does not exist. |
| "Your **biometric voice data** is encrypted" | FAQ section | We don't collect biometric data. Standard Firebase Auth encryption on user data. |
| AI coaching feedback from spectrograms | Implied throughout | **DORMANT** as of Standing Order 004 |

## ✅ Features That ARE Real (Sell These)

### Sound & Music (flagship)
- **Voice Training** — Pitch trainer with real-time detection, MusicXML sheet music, backing tracks
- **Vocal Recording & Analysis** — Spectrogram generation, piano roll, intonation visualization
- **Breathwork Entrainment** — 4 time-of-day sessions (Morning, Noon, Sunset, Midnight) with custom sky visuals
- **Phased Binaural Beats** — Alpha/theta/delta entrainment 
- **NeuroCurrent Drift** — Ambient neural soundscapes
- **Sleep Soundscapes** — Nature and ambient sleep aid
- **Rhythm Training** — Beat matching and timing drills
- **Resonance Chamber** — Find your resonant frequency
- **Secret Meditation** — Ambient meditation with audio visualizer

### Visual Arts
- **Interactive Mandala** — Cymatic pattern generator (touch-reactive)
- **Virtual Zen Garden** — Biophilic nature simulator
- **True Faith** — Interactive audio-visual art piece
- **Fractal Creator** — Generative fractal gardens
- **Infinity Loop** — Visual breathwork pattern trainer

### Movement
- **Constellation Mirror** — AI-powered somatic mirroring (uses device camera)
- **Stardust Drift** — Gamified movement collection

### Writing & AI
- **Journal** — Personal reflection and mood tracking
- **StoryStructure.ai** — Structure-aware creative fiction engine (AI-powered)
- **Songwriter's Studio** — Lyrics, melody, and structure tools
- **NeuroArts Therapist** — AI chatbot wellness companion (Gemini-powered)

### Social & Community (REAL — keep these claims)
- Follow/Connect social model
- Circles (group communities)
- Chat messaging with media (camera, gallery, voice messages)
- Articles (community content with role-based publishing)
- Video library (YouTube integration)
- Audio library (curated music and meditation)
- Reels (short-form vertical video)
- Badges and challenges (gamification)

### Platform
- **30-Day Program** — Structured multi-modal wellness journey
- **Mood tracking** — Personal journey and emotional trends
- **Onboarding quiz** — Personalized experience from first launch
- **AI recommendations** — Contextual activity suggestions via chatbot

---

## Tone Guidance

You ARE a marketing expert — **sell the sizzle**. But ground it in what's real:

- ❌ "We track your biometrics" → ✅ "AI-powered voice analysis reveals your vocal patterns"
- ❌ "Biometric Feedback Engine" → ✅ "Spectrogram Intelligence — see your voice like never before"
- ❌ "Physiological responses" → ✅ "Multi-modal therapeutic arts: sound, movement, visual, and voice"
- ❌ "Neuro-Map of biomarker trends" → ✅ "Track your vocal progress with AI-analyzed recordings"

The science is real. The neuroaesthetics angle is real. The research backing is real. Just don't claim we have hardware/sensor integration that we don't have.

---

## Reference Files

- **Feature catalog**: `projects/neuro-arts-flutter/lib/features/arts/data/app_catalog.dart`
- **Standing Order 003**: `reference/inter-agent-comms/directives/003-zero-tolerance.md`
- **Standing Order 004**: `reference/inter-agent-comms/directives/004-dormant-ai-feedback.md` (AI coaching is dormant)
- **Current website content**: `projects/public-web/CONTENT.md` and `hosting/src/`
