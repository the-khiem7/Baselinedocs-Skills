# Baselinedocs Skills

Skills.sh-compatible repository for the `baseline-docs` skill.

## Skills

### `baseline-docs`

Creates and maintains a resumable baseline documentation pack for a codebase. Use it when you need docs that reflect the current implementation state and can be resumed without relying on prior conversation memory.

The generated docs pack includes:

- `<prefix>.introduction.md`
- `<prefix>.roadmap.md`
- `<prefix>.hallucination.md`
- `<prefix>.sourcecode.md`
- `<prefix>.useguide.md`

## Install

Install from this local repository:

```bash
npx skills add .
```

Install only this skill:

```bash
npx skills add . --skill baseline-docs
```

Install globally without prompts:

```bash
npx skills add . --skill baseline-docs --global --yes
```

After publishing this repository to Git, install from the repo URL:

```bash
npx skills add <repo-url> --skill baseline-docs
```

## Verify

List skills available in this repository:

```bash
npx skills add . --list
```
