---
description: Trace a function or test with CodeGraph, verify against source, and draw a Mermaid call graph with a short summary
argument-hint: "<function, method or test name>"
---

Requires CodeGraph and its MCP server; if the project has no `.codegraph/` index, fall back to Read/Grep.

Trace `$ARGUMENTS` using CodeGraph, then check it against the source.

If no name was given, use the symbol the user has selected in the IDE. If there is none, ask which symbol to trace.

Steps:

1. **Call CodeGraph** (`codegraph_explore`, passing the current project's path as `projectPath`) for the symbol and its callees. Use its source, line numbers, flow and blast-radius output as the starting point. If the project has no `.codegraph/` index, say so and trace with Read/Grep instead.
2. **Verify against the code**. For every call edge you will draw, confirm the call exists by reading the call site (for Python, parsing the file with `ast` is fine if quicker). CodeGraph shows only one path per query and can miss calls (dynamic imports, nested functions, mocks), so do not trust it alone. Where CodeGraph and the source disagree, say so and go with the source.
3. **Draw ONE Mermaid flowchart**:
   - Box = a function. Label it with its name and where it is DEFINED (file:line).
   - Arrow = a call. Label it with the line where the call HAPPENS (file:line).
   - Solid arrow = verified in the source. Dashed arrow = inferred or indirect (framework call, mock, data passed through a file). Put the reason on it.
   - Skip standard-library and builtin calls unless they matter.
   - Draw only calls that actually run for this case. If a branch does not run (for example an empty list), leave it out and mention it in the summary.

   **Notes (every function gets one)**:
   - Beside each function box, add a note box headed "WHAT IT DOES", joined to the function by a dotted line without an arrow (`FN -.- NOTE`).
   - One short plain-English sentence per note, at most about 20 words. Say what the function is for, not how it is written.
   - Style all note boxes alike: `classDef note fill:#fff8d6,stroke:#c9a227,color:#333` then `class NOTE1,NOTE2 note`.
   - In note and edge labels, do not use the characters double quote, pipe, angle brackets (other than `<br/>`) or backticks. Write the word instead (for example "pipe character"). They break Mermaid rendering.

   Complex functions (inner steps):
   - A function is complex if it has branches, loops or several distinct steps. A one-line function is not complex.
   - For a complex function, replace its single box with a `subgraph` titled with its name and definition (file:line). Inside, draw its steps in order as small boxes, and branches as decision diamonds, using only steps that run for this case.
   - Draw the call arrows to other functions from the step that makes the call, labelled with that call line.
   - Point an incoming call at the subgraph itself (its id, for example `T -- "called at test_ventry.py:83" --> TBG`), not at the first inner step. An arrow to an inner step runs through the subgraph title and covers it. An arrow to the subgraph id stops at its border.
   - Only arrows that leave the subgraph start from an inner step. Arrows entering it end at the subgraph id.
   - The note for a complex function sits beside the subgraph.
   - Example shape: `subgraph TBG["table, defined ventry.py:474"]` with `S1{"rows empty?"}`, `S2["build header and divider"]`, `S3["for each row and cell"]`, and `S3 -- "called at ventry.py:480" --> ESC`. The caller links to the subgraph id: `T -- "called at test_ventry.py:83 and :84" --> TBG`.
4. Write a short summary, at most 4 bullets, in plain words. The notes already say what each function does, so cover only:
   - the order things run in, in one sentence
   - anything surprising (a branch that does not run, a mock, a missing link)
   - which edges are inferred and why
   - anything CodeGraph and the source disagreed on, or that you could not verify

   Do not split the output into levels (no D1/D2/D3), and do not repeat the diagram as tables.
5. Do not invent edges. If you could not verify something, say so.

Explain any class or framework detail in a few plain sentences, assuming the reader may not know object-oriented programming.
