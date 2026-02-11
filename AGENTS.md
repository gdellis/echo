# AI Agents Documentation

This document describes the AI agents and their responsibilities for the Transcriber project.

## Overview

The Transcriber project uses specialized AI agents for different aspects of development, debugging, and documentation. Each agent has a focused role and access to specific tools and knowledge.

## Agent Types

### 1. Frontend Agent (`frontend-dev`)

**Role**: React/TypeScript development, UI component creation, frontend architecture

**Responsibilities**:

* Create and modify React components
* Implement TypeScript interfaces and types
* Configure and customize Tailwind CSS
* Set up state management (Context API, Zustand)
* Implement shadcn/ui component integrations
* Debug frontend issues and browser behavior

**Access**:

* `frontend/src/` directory
* Frontend configuration files (package.json, vite.config.ts, tailwind.config.js)
* Design documentation for UI requirements

**Commands**:

* `generate component` - Create new React component
* `fix frontend bug` - Debug and fix frontend issues
* `add type definitions` - Create TypeScript interfaces
* `implement state management` - Set up Context or Zustand store

---

### 2. Backend Agent (`backend-dev`)

**Role**: FastAPI/Python development, API design, database models, async task processing

**Responsibilities**:

* Create and modify FastAPI endpoints
* Implement SQLAlchemy database models
* Create Pydantic schemas
* Configure Celery workers and tasks
* Set up Docker configurations
* Debug backend services and API issues

**Access**:

* `backend/app/` directory
* Backend configuration files
* ML service integrations (Whisper, pyannote.audio)

**Commands**:

* `generate endpoint` - Create new API endpoint
* `add database model` - Create SQLAlchemy model
* `add celery task` - Create async background task
* `fix backend bug` - Debug and fix backend issues

---

### 3. Full-Stack Agent (`fullstack-dev`)

**Role**: End-to-end feature implementation, integration testing, deployment

**Responsibilities**:

* Implement complete features across frontend and backend
* Configure docker-compose.yml for full stack
* Debug integration issues between services
* Deploy and test the complete application

**Access**:

* All project directories
* Configuration files (docker-compose.yml, environment variables)

**Commands**:

* `implement feature` - Create complete feature with tests
* `debug integration` - Fix cross-service issues
* `deploy application` - Build and run the full stack

---

### 4. Documentation Agent (`docs-writer`)

**Role**: Writing and maintaining project documentation

**Responsibilities**:

* Create and update markdown documentation
* Generate API documentation
* Create architecture diagrams (Mermaid format)
* Maintain AGENTS.md, DESIGN.md, and README files

**Access**:

* All documentation files
* Design document for technical specifications

**Commands**:

* `generate docs` - Create new documentation file
* `update existing docs` - Modify documentation
* `add mermaid diagram` - Create architecture/flow diagrams
* `fix markdown linting` - Fix markdown linting issues by running `mdl` tool

* Run `mdl` to check markdown files for linting issues
* Fix any issues identified by the tool

---

### 4a. Markdown Linting Agent (`markdown-linter`)

**Role**: Markdown linting configuration and maintenance

**Responsibilities**:

* Configure and maintain the `mdl` Ruby gem for markdown linting
* Update `.mdl/style.rb` to enable/disable rules
* Ensure consistent markdown style across all documentation
* Fix markdown linting violations in project files

**Access**:

* `.mdl/` directory (configuration)
* `.mdlrc` (configuration)
* All markdown files in the project

**Commands**:

* `configure mdl` - Set up or modify markdown linting rules
* `add linting rule` - Enable a new markdownlint rule
* `disable linting rule` - Disable a markdownlint rule
* `check markdown` - Run `mdl --git-recurse .` to check all markdown files in the repo (excludes node_modules/ and other non-tracked files)
* `fix linting` - Fix markdown linting issues automatically

**Configuration**:

The project uses `mdl` (Markdown Lint) via Ruby gem. Configuration is in:

* `.mdlrc` - Main configuration file pointing to style.rb
* `.mdl/style.rb` - Custom rules configuration

**Usage**:

When running `mdl` locally, use the `--git-recurse` (`-g`) option to only check files tracked by git:

```bash
mdl -c .mdlrc --git-recurse .
```

This excludes `node_modules/`, `venv/`, and other untracked directories automatically.

**Available Rules:**

| Rule | Description |
|------|-------------|
| MD001 | Header levels should only increment by one level at a time |
| MD007 | Unordered list indentation |
| MD009 | Trailing spaces |
| MD012 | Multiple blank lines |
| MD013 | Line length |
| MD018 | No space after hash on ATX-style header |
| MD021 | Headers not properly closed |
| MD022 | Headers should be surrounded by blank lines |
| MD024 | Multiple headers with the same content |
| MD026 | Trailing punctuation in header |
| MD029 | Ordered list item prefix |
| MD031 | Fenced code blocks should be surrounded by blank lines |
| MD032 | Lists should be surrounded by blank lines |
| MD033 | Inline HTML |
| MD036 | Emphasis used instead of a header |
| MD040 | Code block style |
| MD047 | Trailing newline |

**Common Configuration Examples:**

```ruby
# Disable a rule
exclude_rule 'MD012'  # Multiple blank lines

# Configure a rule
rule 'MD007', params: { indent: 2 }  # 2-space indent for lists
rule 'MD013', params: { line_length: 120, ignore_code_blocks: true }
rule 'MD033', allowed_elements: 'br, span, div, img'  # Allow inline HTML
```

---

### 5. Testing Agent (`qa-tester`)

**Role**: Testing, validation, and quality assurance

**Responsibilities**:

* Create unit tests for frontend components
* Create API tests for backend endpoints
* Test integrations between services
* Validate file upload and processing workflows

**Commands**:

* `run tests` - Execute test suite
* `create test` - Generate new tests
* `fix test failure` - Debug and fix failing tests

---

## Agent Communication

Agents coordinate through:

1. Design Document (`DESIGN.md`) - Single source of truth for architecture
2. AGENTS.md - This file - defines agent responsibilities
3. Code Comments - Technical notes for specific implementations
4. Commit Messages - Change tracking across the team

## Getting Started with an Agent

1.  Identify the appropriate agent type for your task
2.  Check the current `DESIGN.md` for architectural context
3.  Use the agent's specific commands for your task
4.  Review generated code against project standards
5.  Test the implementation before committing

## Best Practices

* Use the right agent: Match agent type to task scope
* Check design doc: Always verify against `DESIGN.md` before major changes
* Test thoroughly: Run tests before marking tasks complete
* Document changes: Update documentation when architecture changes
* Follow conventions: Adhere to existing code patterns and naming

## Contact & Support

For questions about agent capabilities or responsibilities, refer to:

* `DESIGN.md` - Technical architecture details
* `.clinerules/` - Project-specific rules and guidelines
* This file - Agent definitions and commands

---

## Pull Request Template

This document specifies the pull request template and best practices for the Echo (Transcriber) project. These guidelines ensure consistent, high-quality PRs across all development work.

### PR Title Format

Use the conventional commits format:

```
<type>: <description>
```

**Types:**

* `feat` - New feature
* `fix` - Bug fix
* `chore` - Maintenance, configuration, or refactoring
* `docs` - Documentation changes
* `style` - Code style changes (formatting, semicolons, etc.)
* `refactor` - Code refactoring
* `test` - Adding or updating tests
* `ci` - CI/CD changes
* `perf` - Performance improvements
* `build` - Build system or external dependencies

**Examples:**

* `feat: add markdown linting guidelines`
* `fix: resolve file upload timeout`
* `chore: update Docker configuration`

---

### PR Description Template

```markdown
# Pull Request Description

## Overview

Brief summary of what this PR does and why it's needed.

## Changes

### File Changes

* `filename`: Brief description of change
* `filename`: Brief description of change

### Infrastructure

* Description of infrastructure changes

### Configuration

* Description of configuration changes

## Benefits

| Benefit | Description |
|---------|-------------|
| Benefit | Description |

## Testing

* [ ] Test 1
* [ ] Test 2
* [ ] Test 3

## Notes

Any additional context or considerations.
```

### Best Practices

| Practice | Description |
|----------|-------------|
| Clear Title | Use conventional commit format for easy history tracking |
| Brief Summary | Explain what changed and why in the Overview section |
| Organized Changes | Group related changes under appropriate headers |
| Benefits Table | Highlight the impact of changes |
| Testing Checklist | Include actionable testing items |
| Concise, Not Long | Be specific; avoid filler text |

### Example PR Description

```markdown
# Pull Request Description

## Overview

This PR applies best practices identified during the review of PR #1 for repository structure and file management.

## Changes

### Repository Structure

* Added comprehensive `.gitignore` file with rules for:
  * Python (`.pyc`, `__pycache__`, `.pytest_cache`)
  * Node.js (`node_modules/`, `package-lock.json`)
  * IDE files (`.vscode/`, `.idea/`)
  * Logs and temporary files

### Docker Improvements

* **Multi-stage build** in `frontend/Dockerfile`:
  * Builder stage: Installs dependencies and builds the app
  * Production stage: Small nginx Alpine image with only built assets
  * Result: Significantly smaller production image

* **Optimized nginx configuration** (`frontend/nginx.conf`):
  * Efficient static file serving
  * Gzip compression enabled
  * Proper caching headers

### Configuration

* Added `.env.example` for environment variable templates
* Removed `node_modules/` from repository (reduces size significantly)

### Documentation

* Updated `README.md` with comprehensive project information

## Benefits

| Benefit | Description |
|---------|-------------|
| Smaller Repo | Removing `node_modules/` reduces repository size dramatically |
| Cleaner History | Proper `.gitignore` prevents accidental commits of build artifacts |
| Faster Builds | Multi-stage Docker builds cache dependencies separately |
| Better Security | Sensitive files (`.env`) are never committed |
| Improved Setup | `.env.example` provides clear setup guidance |

## Testing

* [ ] Verify `.gitignore` prevents unwanted files from being committed
* [ ] Test Docker build: `docker build -f frontend/Dockerfile -t echo-frontend .`
* [ ] Test nginx configuration: `docker run -p 8080:80 echo-frontend`

## Notes

* This PR addresses recommendations from the PR #1 review
* All changes follow project conventions and best practices