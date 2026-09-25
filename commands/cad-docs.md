---
name: cad-docs
description: Query live, up-to-date documentation, API signatures, and official code examples from Context-7 MCP for any library or framework.
---

# Cadence Docs: Live Documentation & Grounding via Context-7 MCP

Query the Context-7 MCP server to fetch current documentation, API signatures, breaking changes, and code examples for any library or framework.

## Instructions

1. If the user provided a library name and query in their prompt (e.g. `/cad-docs PyTorch DataLoader pin_memory` or `/cad-docs Next.js server actions`):
   - Use `call_mcp_tool` with server `context7` and tool `resolve-library-id`.
   - Then use `query-docs` with the resolved library ID and specific query.
   - Present the key code snippets, contract details, and official source links clearly.
2. If the user did not specify arguments, ask them which library, framework, or API concept they want to look up, or inspect the active project manifests to suggest the primary dependencies.
3. Integrate the findings directly into the current planning, TDD, or debugging context.
