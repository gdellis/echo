# AI Agents Documentation

This document describes the AI agents and their responsibilities for the Transcriber project.

## Overview

The Transcriber project uses specialized AI agents for different aspects of development, debugging, and documentation. Each agent has a focused role and access to specific tools and knowledge.

## Agent Types

### 1. Frontend Agent (`frontend-dev`)

**Role**: React/TypeScript development, UI component creation, frontend architecture

**Responsibilities**:

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
- `.markdownlint.yaml` - Markdown linting configuration
- `.clinerules/markdown-linting.md` - Detailed markdown linting rules

**Commands**:

- `generate docs` - Create new documentation file
- `update existing docs` - Modify documentation
- `add mermaid diagram` - Create architecture/flow diagrams
- `fix markdown linting` - Fix markdown linting issues

---

## Markdown Linting Guidelines

This section specifies the markdown linting guidelines for the Echo (Transcriber) project using [markdownlint](https://github.com/markdownlint/markdownlint). These rules ensure consistent, high-quality documentation across all markdown files in the project.

### Rules to Enable (by default)

1. **MD001 - Heading levels should only increment by one**
   - Ensures proper document structure
   - Example: `# Main Title` → `## Section` (not `###`)

2. **MD002 - First heading should be a top-level heading**
   - All documents should start with `#`

3. **MD003 - Heading style should be consistent**
   - Use ATX-style headings (`#`, `##`, `###`) throughout
   - Not Setext-style (`===`, `---`)

4. **MD004 - Unordered list style should be consistent**
   - Use asterisks (`*`) for unordered lists
   - Example: `* First item`, `* Second item`

5. **MD005 - List indentation should be consistent**
   - Indent nested list items by 2 spaces
   - Example: 2 spaces for second level, 4 for third

6. **MD007 - Unordered list indentation should be 2 spaces**
   - Consistent indentation for list readability

7. **MD009 - Trailing spaces should be removed**
   - No trailing whitespace at the end of lines

8. **MD010 - Hard tabs should not be used**
   - Use spaces for indentation only

9. **MD011 - Reversed link syntax should not be used**
   - Use standard `[text](url)` format
   - Not `(url): text` reversed syntax

10. **MD012 - Multiple consecutive blank lines should be reduced**
    - Maximum one blank line between sections

11. **MD013 - Line length should be limited**
    - Maximum 80 characters per line for readability
    - Allow longer lines for code blocks and tables

12. **MD014 - Code block indentation should be consistent**
    - Code blocks should not be indented

13. **MD018 - No space after hash on atx-style heading**
    - Use `# Heading` not `#  Heading`

14. **MD019 - No multiple spaces after hash on atx-style heading**
    - Single space only after `#`

15. **MD020 - No space inside headings**
    - `# Heading` not `# Heading ` or ` # Heading`

16. **MD022 - Headings should end with appropriate punctuation**
    - Headings should not end with punctuation (except code blocks)

17. **MD023 - Headings must start at column 1**
    - No leading spaces before heading markers

18. **MD024 - No duplicate heading levels**
    - Avoid having multiple `##` headings at the same level without intermediate headings

19. **MD025 - Multiple top-level headings in the same document**
    - Documents should have only one `#` heading (title)

20. **MD026 - Trailing punctuation in heading should be removed**
    - Remove trailing `:`, `;`, `.`, `!`, `?` from headings

21. **MD027 - Multiple consecutive blank lines after list item should be reduced**
    - Keep list items close to subsequent content

22. **MD028 - Blank line after blockquote is required**
    - Blockquotes should be followed by a blank line

23. **MD029 - Ordered list item prefix should be consistent**
    - Use `1.` or `a.` consistently (prefer `1.`)

24. **MD030 - Spaces after list markers should be consistent**
    - Single space after list markers (`* `, `1. `)

25. **MD031 - Fenced code blocks should have blank lines before and after**
    - Separate code blocks from surrounding content

26. **MD032 - Lists inside blockquotes should be indented**
    - Proper indentation for nested lists

27. **MD033 - Inline HTML should be allowed**
    - Basic HTML like `<br>`, `<sub>`, `<sup>` is permitted

28. **MD034 - Bare URL should be converted to link**
    - Use `[url](url)` format for URLs

29. **MD035 - Horizontal rule style should be consistent**
    - Use `---` (three dashes) for horizontal rules

30. **MD036 - Emphasis should not use spaces inside markers**
    - Use `*word*` not `* word *`

31. **MD037 - Spaces inside emphasis markers should be removed**
    - `**bold**` not `** bold **`

32. **MD038 - Spaces inside code span markers should be removed**
    - Use `` `code` `` not `` ` code ` ``

33. **MD039 - Spaces inside link text should be preserved**
    - `[link text](url)` is correct

34. **MD040 - Fenced code blocks should have a language specified**
    - Use syntax highlighting: ```` ```python ````

35. **MD041 - First line should be top-level heading**
    - Documents should start with `#`

36. **MD042 - No empty URLs**
    - All links must have valid URLs

37. **MD043 - Headings should have consistent capitalization**
    - Use sentence case for headings (first letter capitalized only)

38. **MD044 - Code block content should match language**
    - Ensure code block language matches actual content

39. **MD045 - No images without alt text**
    - All images need descriptive alt text: `![alt](image.png)`

40. **MD046 - Code block style should be consistent**
    - Use fenced code blocks (```` ``` ````) not indented blocks

### Rules to Configure

1. **MD013 - Line length**
   - `line_length: 120` - Allow 120 characters for better readability with modern screens

2. **MD033 - Allowed HTML elements**
   - `allowed_elements: ['br', 'sub', 'sup', 'span', 'div', 'img']`

3. **MD025 - Allow multiple top-level headings in includes**
   - Configure for projects with markdown includes

## Rules to Disable

1. **MD006 - Considered too strict for some cases**
   - May disable depending on team preference

2. **MD021 - Header closing markers**
   - Not required for most documentation

### Tools and Integration

#### Installation

```bash
# npm
npm install markdownlint --save-dev

# Or globally
npm install -g markdownlint-cli
```

#### VS Code Extension

Install the "Markdownlint" extension (kddejong.vscode-markdownlint) for real-time linting.

#### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
markdownlint "**/*.md" || exit 1
```

#### CI Integration

Add to `.github/workflows/lint.yml`:

```yaml
- name: Lint Markdown files
  run: npx markdownlint "**/*.md"
```

### Documentation Style Guidelines

#### File Structure

1. **README.md and docs**:
   - Start with `# Title`
   - Use `##` for main sections
   - Use `###` for subsections
   - Maximum 3-4 heading levels

2. **Code Comments in Markdown**:
   - Use `<!-- -->` for HTML comments
   - Use `//` style comments for code examples

3. **Code Blocks**:
   - Always specify language: ```` ```python ````
   - Use proper indentation (2 or 4 spaces)
   - Keep lines under 120 characters

4. **Links**:
   - Use relative links for internal documentation
   - Use absolute links for external resources

5. **Images**:
   - Always include descriptive alt text
   - Place images near relevant content
   - Use proper sizing with HTML attributes if needed

#### Examples

**Good:**

```markdown
# Project Title

## Overview

This is a paragraph with [a link](https://example.com).

### Subsection

- First item
- Second item

```python
def example():
    return "Hello"
```
```

**Bad:**
```markdown
# Project Title #
## Overview ##

This has [a reversed link](https://example.com).

- item one
   - nested (wrong indent)

```python
print("missing language")
```

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