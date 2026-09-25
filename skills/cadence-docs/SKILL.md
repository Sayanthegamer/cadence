---
name: cadence-docs
description: >-
  Query up-to-date documentation, version details, and authoritative code examples for any
  library, framework, SDK, or CLI tool using the Context-7 MCP server (resolve-library-id and query-docs).
---

# Cadence Docs: Live Library & Framework Grounding (Context-7 MCP)

Use this skill whenever you or the user need authoritative, current documentation, API signatures, migration guides, or official code examples for any third-party library, framework, SDK, or CLI tool (e.g. PyTorch, Next.js, FastAPI, Prisma, Tailwind, Spring Boot, etc.).

Even when you think you know the API, training data may be stale or miss recent breaking changes. Always prefer **Context-7 MCP** over broad web search when available.

---

## ⚠️ Pre-Flight: Check if Context-7 is Installed (Opt-In Superpower)

Context-7 MCP is an optional capability installed at the user's choice. Before calling `context7`:
1. Check `<mcp_servers>` in your active session.
2. **If `context7` is NOT configured or installed:**
   - Do NOT fail or crash the workflow.
   - Gracefully fall back to web search (`search_web`) or local type inspection.
   - Gently inform the user:
     > 💡 *Tip: Context-7 MCP is not currently installed. To enable live documentation and verified code snippets for any library, you can install it anytime with:*  
     > `agy mcp add context7 https://mcp.context7.com/mcp`
3. **If `context7` IS installed:**
   - Proceed with the Two-Step Protocol below.

---

## The Context-7 Two-Step Protocol

```text
[1. Resolve Library ID] -> [2. Query Documentation] -> [3. Ground Architecture / Code]
```

### Step 1: Resolve Library ID (`resolve-library-id`)
1. Call `call_mcp_tool` on server `context7` with tool `resolve-library-id`:
   - `libraryName`: Official library name with proper punctuation (e.g. `'PyTorch'`, `'Next.js'`, `'Prisma'`, `'FastAPI'`).
   - `query`: The specific concept or capability to search for.
2. Select the most relevant Context-7 compatible library ID (format: `/org/project` or `/org/project/version`) based on:
   - Benchmark Score (higher is better, 100 max)
   - Code Snippet count & documentation coverage
   - Target version match (e.g. `v2.5.1`)

### Step 2: Query Documentation (`query-docs`)
1. Call `call_mcp_tool` on server `context7` with tool `query-docs`:
   - `libraryId`: The exact ID obtained from Step 1 (e.g. `'/pytorch/pytorch'` or `'/vercel/next.js'`).
   - `query`: A focused query scoped to a single concept (e.g. `'torch.nn.Linear weight shape convention'` or `'Server Actions with revalidatePath'`).
2. Extract the official source URLs, code snippets, and contract specifications.
3. *Limit:* Do not call `query-docs` more than 3 times per question to preserve token efficiency.

### Step 3: Ground the Workflow
1. **In Architecture / Planning (`cadence-plan`):** Lock the exact API contract into the UI Artifact.
2. **In TDD Execution (`cadence-flow`):** Use the official snippet as the basis for the RED-phase test or GREEN-phase implementation.
3. **In Debugging (`cadence-debug`):** Compare the project's actual usage against the documented signature to confirm root causes.
4. **User Guidance:** Share the official documentation links and relevant code snippets directly with the user.

---

## Proactive User Grounding Prompt

Whenever the user is planning or debugging an external library and seems uncertain or asks for advice, proactively prompt them:

> 💡 **Grounding Available:** *If you'd like live, up-to-date documentation, breaking changes, or official code examples for **[Library]**, we can query the Context-7 MCP directly (run `/cad-docs <library>` or ask me to check Context-7).*
