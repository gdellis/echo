## Brief overview
This rule file specifies the git workflow guidelines for the Transcriber project. It emphasizes using feature branches for all development work and maintaining a clean main branch.

## Git workflow guidelines

### Branch naming convention
- Use hyphens (`-`) to separate words in branch names (kebab-case)
- Prefix branches with a type indicator:
  - `feature/` - New features or enhancements
  - `fix/` - Bug fixes
  - `docs/` - Documentation updates
  - `refactor/` - Code refactoring
  - `test/` - Test additions or modifications
- Examples: `feature/add-agents-documentation`, `fix/upload-bug`, `docs/update-readme`

### Never commit directly to main branch
- Always create a feature branch before making changes
- Main branch should only contain reviewed and merged code
- All pull requests should target main branch
- This ensures code quality and proper review process

### Commit message conventions
- Use imperative mood: "Add feature" not "Added feature"
- Keep first line under 72 characters
- Reference issue numbers when applicable: `fix #123`
- Format: `<type>: <description>`
- Examples:
  - `feat: add AGENTS.md with AI agent documentation`
  - `fix: resolve file upload timeout`
  - `docs: update API endpoint documentation`

### When to branch
- Creating a new feature or enhancement
- Fixing a bug
- Writing new tests
- Updating documentation
- Any non-trivial change to the codebase

### Pull request workflow
1. Create feature branch from main
2. Make commits with clear messages
3. Test changes locally
4. Push branch to remote
5. Create pull request for review
6. Merge after approval