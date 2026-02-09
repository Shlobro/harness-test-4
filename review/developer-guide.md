# Review Folder Guide

## Purpose
Stores review output files produced by automated or manual code reviews. Each file is intentionally minimal and may be empty when there are no findings for that category.
Review files should contain only issue lists (no positive notes).

## Current Workflow
For each review run, write only actionable issues to the relevant category file.
If a category has no issues, leave that file empty.
When writing findings, include concrete file references so fixes can be applied directly from the report.
Keep issue wording focused on user-visible impact (for example, interaction friction, unclear prompts, or abrupt screen/state behavior).
For diff-based reviews, anchor each issue to the changed lines that introduced the user-visible behavior.
If a changed test introduces or locks in a user-visible regression expectation, report it as a review issue with the test file/line reference.

## Files
`architecture.md`
Holds architecture-related findings only.

`documentation.md`
Holds documentation-related findings only.

`efficiency.md`
Holds performance or efficiency-related findings only.

`error_handling.md`
Holds error handling and resilience findings only.

`general.md`
Holds cross-cutting or uncategorized findings only.
Leave this file empty when no issues are found in the reviewed diff.

`safety.md`
Holds security, privacy, or safety findings only.

`testing.md`
Holds test coverage or testing strategy findings only.

`ui_ux.md`
Holds user interface or user experience findings only.
