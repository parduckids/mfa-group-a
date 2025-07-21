# GitHub Team Workflow

## Making Changes

1. Create a new branch: `git checkout -b feature/your-feature-name` ()
2. Make your changes and commit
3. Push branch: `git push origin feature/your-feature-name`
4. Create Pull Request on GitHub

## Pull Request Requirements

### Title Format:

`[TYPE]: Brief description`

**Examples:**

- `feat: Add user authentication`
- `fix: Resolve database connection issue`
- `docs: Update README installation steps`

### PR Description Template:

```
## What changed?
- Brief description of changes

## Why?
- Reason for the change
- Issue/ticket reference if there is any
```

## Approval Process

### For Reviewers (1 person from the group)

**When Approving:**

1. Click **Review changes**
2. Select **Approve**
3. **Required:** Add comment explaining:
   - What was reviewed
   - Why it's approved

**Example Approval Comment:**

```
✅ **APPROVED**

**Reviewed:** Database connection logic and error handling
**Reason:** Code follows best practices, includes proper error handling, and tests pass
```

**When Requesting Changes:**

1. Click **Review changes**
2. Select **Request changes**
3. **Required:** Add specific feedback:
   - What needs to be fixed
   - Why it's being rejected
   - How to resolve the issues

**Example Rejection Comment:**

```
❌ **CHANGES REQUESTED**

**Issues Found:**
1. Database connection not properly closed
2. Unit tests failing

**Required Actions:**
- Add try/catch blocks for database operations
- Implement connection cleanup in finally block
- Fix failing tests in test.py

**Resubmit when:** All issues are resolved and tests pass
```


## Team Communication Rules

### For All Collaborators

1. **Never push directly to main branch**
2. **Always create descriptive commit messages**
3. **Use conventional commit format:**

   ```
   type(scope): description

   feat: add new feature
   fix: bug fix
   docs: documentation
   style: formatting
   refactor: code refactoring
   test: adding tests
   chore: maintenance
   ```

### PR Etiquette

- **Request review on Teams**
- **Respond to feedback within 24 hours**
- **Test your changes before submitting**
- **Update PR description if changes are made**

## Enforcement Notes

- These rules will prevent direct pushes to main branch
- All changes must go through PR process
- At least 1 approval required before merge
- Reviewers must provide detailed comments
- Failed reviews block the merge until resolved
