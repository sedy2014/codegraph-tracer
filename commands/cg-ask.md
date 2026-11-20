---
description: Ask a question about the codebase, answered with CodeGraph's help
argument-hint: "<your question about the code>"
---

Requires CodeGraph and its MCP server; if the project has no `.codegraph/` index, fall back to Read/Grep.

Answer this question about the codebase, using CodeGraph to find the relevant code: $ARGUMENTS

How to answer:

1. Call CodeGraph (`codegraph_explore`, passing the current project's path as `projectPath`) first. Name the symbols or files in the query when you know them. If the project has no `.codegraph/` index, say so and use Read/Grep instead.
2. Read the code CodeGraph returns and answer from it. Where something matters to the answer, check it in the actual source rather than relying on CodeGraph's summary alone, since it can miss dynamic calls, nested functions and mocks.
3. Keep the answer short and in plain words. Point to code as `file:line` links. Quote only the few lines that matter.
4. Do not draw a diagram unless the user asks for one (they can use /cg-trace for a call graph).
5. Say what you could not confirm. Do not guess.

Explain any class or framework detail in a few plain sentences, assuming the reader may not know object-oriented programming.
