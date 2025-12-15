# Tasks: Interactive AI-Powered Physical AI & Humanoid Robotics Textbook

## Phase 1: Setup
- [ ] T001 Initialize project structure with Docusaurus v3 and FastAPI backend
- [ ] T002 Set up environment variables for API keys and database connections
- [ ] T003 Configure project dependencies in package.json and requirements.txt

## Phase 2: Foundational Infrastructure
- [ ] T004 [P] Fix backend Gemini initialization using google.generativeai in backend/app.py
- [ ] T005 [P] Correct Cohere input_type in ingest and query endpoints in backend/app.py
- [ ] T006 [P] Enable CORS and configure Docusaurus proxy to backend in backend/app.py and docusaurus.config.js
- [ ] T007 [P] Set up Qdrant vector database connection and test in backend/app.py
- [ ] T008 Re-run ingestion script to load all content into Qdrant in backend/ingest.py

## Phase 3: [US1] User Authentication & Background Capture
- [ ] T009 [US1] Implement Better-Auth login/signup with background questions in src/components/LoginButton.jsx
- [ ] T010 [US1] Create user profile storage for personalization preferences in backend/auth.py
- [ ] T011 [US1] Add user background capture form in src/components/UserBackgroundForm.jsx
- [ ] T012 [US1] Store user background data in database in backend/models/user.py

## Phase 4: [US2] RAG Chatbot Enhancement
- [ ] T013 [US2] Fix RAG chatbot to support selected text queries in src/components/ChatbotWidget.jsx
- [ ] T014 [US2] Enhance chatbot to answer general questions from book content in backend/app.py
- [ ] T015 [US2] Add chatbot widget to all documentation pages in src/theme/Layout/index.js
- [ ] T016 [US2] Test chatbot functionality on mobile and desktop in src/components/ChatbotWidget.jsx

## Phase 5: [US3] Content Personalization
- [ ] T017 [US3] Create Personalize button component in src/components/PersonalizeButton.jsx
- [ ] T018 [US3] Implement content adaptation logic based on user background in src/services/personalization.js
- [ ] T019 [US3] Integrate personalization with user's software/hardware background in backend/personalization.py
- [ ] T020 [US3] Add personalization button to global layout in src/theme/Layout/index.js

## Phase 6: [US4] Urdu Translation
- [ ] T021 [US4] Create Urdu Translate button component in src/components/UrduTranslateButton.jsx
- [ ] T022 [US4] Implement Urdu translation using Gemini in backend/translation.py
- [ ] T023 [US4] Add translation functionality to current page content in src/components/UrduTranslateButton.jsx
- [ ] T024 [US4] Add translation button to global layout in src/theme/Layout/index.js

## Phase 7: [US5] Global Integration & UI
- [ ] T025 [US5] Add all new buttons to global layout in src/theme/Layout/index.js
- [ ] T026 [US5] Ensure all buttons visible and functional on every documentation page
- [ ] T027 [US5] Make features responsive for mobile and desktop in src/components/*

## Phase 8: [US6] Testing & Deployment
- [ ] T028 [US6] Test all features locally on localhost:3000
- [ ] T029 [US6] Fix any backend initialization or connection errors
- [ ] T030 [US6] Prepare for Vercel deployment with proper configuration in vercel.json
- [ ] T031 [US6] Verify all features work on deployed version

## Dependencies
- User Story 1 (Authentication) must be completed before User Stories 3 and 4 (which rely on user background)
- Foundational infrastructure (Phase 2) must be completed before any user story implementation

## Parallel Execution Opportunities
- Authentication (US1), Chatbot (US2), Personalization (US3), and Translation (US4) can be developed in parallel after foundational infrastructure is complete
- Backend services and frontend components can be developed in parallel within each user story

## Implementation Strategy
- Start with MVP: Basic authentication + RAG chatbot functionality
- Incrementally add personalization and translation features
- Test each feature independently before integration