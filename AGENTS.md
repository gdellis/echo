# AI Agents Documentation

This document describes the AI agents and their responsibilities for the Transcriber project.

## Overview

The Transcriber project uses specialized AI agents for different aspects of development, debugging, and documentation. Each agent has a focused role and access to specific tools and knowledge.

## Agent Types

### 1. Frontend Agent (`frontend-dev`)

**Role**: React/TypeScript development, UI component creation, frontend architecture

** Responsibilities**:
- Create and modify React components
- Implement TypeScript interfaces and types
- Configure and customize Tailwind CSS
- Set up state management (Context API, Zustand)
- Implement shadcn/ui component integrations
- Debug frontend issues and browser behavior

**Access**:
- `frontend/src/` directory
- Frontend configuration files (package.json, vite.config.ts, tailwind.config.js)
- Design documentation for UI requirements

**Commands**:
- `generate component` - Create new React component
- `fix frontend bug` - Debug and fix frontend issues
- `add type definitions` - Create TypeScript interfaces
- `implement state management` - Set up Context or Zustand store

---

### 2. Backend Agent (`backend-dev`)

**Role**: FastAPI/Python development, API design, database models, async task processing

**Responsibilities**:
- Create and modify FastAPI endpoints
- Implement SQLAlchemy database models
- Create Pydantic schemas
- Configure Celery workers and tasks
- Set up Docker configurations
- Debug backend services and API issues

**Access**:
- `backend/app/` directory
- Backend configuration files
- ML service integrations (Whisper, pyannote.audio)

**Commands**:
- `generate endpoint` - Create new API endpoint
- `add database model` - Create SQLAlchemy model
- `add celery task` - Create async background task
- `fix backend bug` - Debug and fix backend issues

---

### 3. Full-Stack Agent (`fullstack-dev`)

**Role**: End-to-end feature implementation, integration testing, deployment

**Responsibilities**:
- Implement complete features across frontend and backend
- Configure docker-compose.yml for full stack
- Debug integration issues between services
- Deploy and test the complete application

**Access**:
- All project directories
- Configuration files (docker-compose.yml, environment variables)

**Commands**:
- `implement feature` - Create complete feature with tests
- `debug integration` - Fix cross-service issues
- `deploy application` - Build and run the full stack

---

### 4. Documentation Agent (`docs-writer`)

**Role**: Writing and maintaining project documentation

**Responsibilities**:
- Create and update markdown documentation
- Generate API documentation
- Create architecture diagrams (Mermaid format)
- Maintain AGENTS.md, DESIGN.md, and README files

**Access**:
- All documentation files
- Design document for technical specifications

**Commands**:
- `generate docs` - Create new documentation file
- `update existing docs` - Modify documentation
- `add mermaid diagram` - Create architecture/flow diagrams

---

### 5. Testing Agent (`qa-tester`)

**Role**: Testing, validation, and quality assurance

**Responsibilities**:
- Create unit tests for frontend components
- Create API tests for backend endpoints
- Test integrations between services
- Validate file upload and processing workflows

**Commands**:
- `run tests` - Execute test suite
- `create test` - Generate new tests
- `fix test failure` - Debug and fix failing tests

---

## Agent Communication

Agents coordinate through:
1. **Design Document** (`DESIGN.md`) - Single source of truth for architecture
2. **AGENTS.md** - This file - defines agent responsibilities
3. **Code Comments** - Technical notes for specific implementations
4. **Commit Messages** - Change tracking across the team

## Getting Started with an Agent

1. Identify the appropriate agent type for your task
2. Check the current `DESIGN.md` for architectural context
3. Use the agent's specific commands for your task
4. Review generated code against project standards
5. Test the implementation before committing

## Best Practices

- **Use the right agent**: Match agent type to task scope
- **Check design doc**: Always verify against `DESIGN.md` before major changes
- **Test thoroughly**: Run tests before marking tasks complete
- **Document changes**: Update documentation when architecture changes
- **Follow conventions**: Adhere to existing code patterns and naming

## Contact & Support

For questions about agent capabilities or responsibilities, refer to:
- `DESIGN.md` - Technical architecture details
- `.clinerules/` - Project-specific rules and guidelines
- This file - Agent definitions and commands