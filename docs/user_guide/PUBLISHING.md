# Publishing the focused Word guides

The distribution set contains three documents, in reading order: Getting Started (4 pages), Workflow and Prompts (5 pages), and optional Testing and Feedback (6 pages). Ordinary users begin with Guide 1; the feedback forms are not part of their BA project ledger.

## Sources

- [Getting Started source](print/01-getting-started.md)
- [Workflow and Prompts source](print/02-everyday-workflow.md)
- [Testing and Feedback source](print/03-testing-and-feedback.md)
- [Font files and licence](fonts/README.md)
- [Diagram sources](images/README.md)

The `<!-- page -->` markers keep each task on a deliberate page. Form directives (`field`, `rating`, `choice` and `reviewer-table` comments) create labelled Word content controls and print writing space. Checkbox choices are independent controls; instructions ask for one choice per item. Text controls are multiline and the document remains editable. Other editors can use plain typed answers if controls are unavailable. Checkbox symbols use a symbol font; body text and diagrams use Google Sans Flex. Edit for meaning before adjusting typography. Do not shrink body text to force a page count; simplify or rebalance the text instead. Each first page is a compact branded cover with useful content, rather than a separate cover-only sheet.

## Rebuild

Run the optional publishing tool from the source checkout or source distribution. It needs Python and `python-docx` (including lxml), and is separate from the standard-library skill helper. Host installation bundles include the finished guides but omit the publishing scripts:

```sh
python3 scripts/build_user_guide_docx.py
```

It builds all three DOCX files in this directory and embeds the regular and bold Google Sans Flex fonts. `--output-dir` can select a review directory. It needs no BA Mate application directory or private research files.

The optional `scripts/build_user_guide_diagrams.py` uses fonttools to rebuild the three new SVG diagrams from the included font files. Render each SVG to its matching 2200px-wide PNG with a suitable SVG renderer. Labels use actual font outlines for portability; descriptive titles and adjacent prose retain their meaning.

## Before distributing

Render every DOCX and inspect every page at reading size. Check title and heading hierarchy, font use, table padding, diagrams, page numbering, links and status claims. Audit image alternatives, table headers and form labels. Fill a synthetic copy to check that answer controls accept text and rating boxes retain their state. Longer answers may naturally increase the completed form’s page count; do not restrict or truncate them. Confirm the page counts above after any edit, and correct page-specific instructions if pagination changes.

The 28 October 2026 revision was locally rendered and every final page inspected; the layout is 4, 5 and 6 pages. The main guides retain their short page counts, while the feedback pack reserves separate pages for test details, results, ratings, written comments and reviewer notes. This is document QA, not a new installed-host behavioural test. Host evidence retains its 24 October 2026 date, practitioner pilots remain pending and the research claims are unchanged.

Public release builds include the three current guides. The old long edition is preserved only in a local ignored backup. Office lock files, render outputs and private test records must not enter release archives. Do not post completed participant records in public GitHub issues.
