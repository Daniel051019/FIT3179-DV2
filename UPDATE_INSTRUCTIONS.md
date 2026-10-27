# Apply the peer-feedback update

This update implements all four student critique points.

1. Extract this ZIP.
2. Copy its contents into your existing website folder, replacing files with matching names.
3. Open `index.html` in VS Code to edit it, or open it in your browser to preview.
4. Upload the extracted website files to your existing FIT3179-DV2 GitHub repository and commit. Keep `index.html` at the repository root.
5. After GitHub Pages finishes updating, refresh the existing website URL.

No terminal or build command is needed to use the supplied HTML. Its CSS, JavaScript, chart specifications and statistical data are embedded. Your existing vendor folder supplies the chart libraries; the HTML also has a pinned online fallback.

## Changes

- Section 1: **Salary levels** / **Change: 2024–2025** controls. The change view compares all 21 fields directly, including decreases, with signed dollar labels and both yearly medians in tooltips. It shares the discipline highlight.
- Section 2: **Highlight a profile** selector, clearer axis titles and denominators, zero baselines and consistent upward axes, and selected profile values with units.
- Section 3: context explanation before the gender charts, distinguishing descriptive group differences from causal or adjusted estimates.
- Section 5: weekly earnings / all-employee population clearly identified in the map heading, subtitle and adjacent note.

Paragraph and source lines remain capped at ten words.

## Files

- `index.html`: ready-to-publish complete webpage.
- `app.js` and `style.css`: updated editable authoring files.
- `source/page.html`: editable page content template.
- `specs/15_parallel_outcomes.json` and `specs/16_salary_change.json`: readable chart specifications for marking and the Chart JSON links.
- `build_specs.py`, `feedback_specs.py`, `build_html.py`: reproducible source builders.
- `README.md`: full project guidance.

If you edit the authoring files rather than the finished HTML, rebuild using `python build_specs.py` then `python build_html.py` in an environment with lxml. Publishing the supplied index.html does not require rebuilding.

The parallel chart now uses salary $0–$100,000 and 0–100% on both percentage axes. All increase upwards. Higher underemployment means more graduates want extra hours.
