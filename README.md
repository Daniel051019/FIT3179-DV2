# Graduate Starting Salaries — FIT3179 DV2

Start with `index.html`. The generated HTML includes the CSS, JavaScript, data and 15 readable chart definitions. The separate JSON specifications remain in `specs/` for assignment marking. There is no build step for viewing the page.

## Open in VS Code

1. Extract the ZIP. Open the `graduate-salaries` folder in VS Code.
2. Install the **Live Server** extension by Ritwick Dey if it is not already installed.
3. Right-click `index.html` and choose **Open with Live Server**.
4. Confirm that all 15 charts appear. Try the year selector above chart 1. Its reference line changes to $75,000 for 2024 and $77,000 for 2025. Select a discipline, or click a linked chart mark, to highlight that field across six related charts. Clear the highlight to restore the full view.

Alternative if Python is already installed: open the terminal in this folder, run `python -m http.server 8000`, and visit `http://localhost:8000`. On some systems the command is `python3 -m http.server 8000`.

The complete standalone HTML can also be opened by double-clicking it. All chart data are embedded, so there are no local JSON requests. Keep the `vendor` folder alongside the HTML for local chart libraries; otherwise an internet connection is required for the pinned CDN fallback. Use the complete project ZIP for GitHub Pages so the separate chart JSON files are also published. There is no npm installation or compilation step.

## Publish on your GitHub account

1. Sign in to GitHub and create a **public** repository, for example `FIT3179-DV2`.
2. Choose **Add file → Upload files**. Upload the **contents** of this folder, so `index.html` sits at the repository root. Include `vendor`, `data`, `specs`, `style.css`, and `app.js`.
3. Commit the files.
4. Open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select **main** and **/(root)**, then save.
6. Wait for GitHub Pages to show the deployed URL. It will normally have the form `https://YOUR-USERNAME.github.io/FIT3179-DV2/`.
7. Open the **actual returned URL** in an incognito/private window. Confirm every chart and the JSON/data links work. Do not submit the example URL above.

The `.nojekyll` file is included for static hosting. If the upload UI omits it, the supplied filenames still work without it.

## Finish the assignment submission

Open `submission/DV2_Draft.docx`. It contains the domain and Why/Who/What/How answers, following the supplied template. Review the wording against your final webpage.

You still need to:

- Verify your name/student ID and enter your studio session.
- Paste the live GitHub Pages URL into Part A.
- Draw your own sketch **by hand on A4**, following the final page structure. Do not submit a digitally produced sketch. See `SKETCH_GUIDE.md`.
- Photograph or scan the sketch, export it as `sketch.pdf`, and upload it to your GitHub repository.
- Paste the sketch PDF URL into Part C. A repository URL such as `https://github.com/YOUR-USERNAME/FIT3179-DV2/blob/main/sketch.pdf` is suitable if publicly accessible. Also insert a legible image of the sketch into Part C.
- Take a full-page screenshot of the finished live webpage and insert it into Part D. In Chrome or Edge: press F12, then Ctrl+Shift+P, search for **Capture full size screenshot**, and choose it. On macOS use Cmd+Option+I, then Cmd+Shift+P.
- Check both links in incognito mode, confirm the AI acknowledgement reflects your actual use, and submit the completed template on Moodle.
- Prepare to explain the data, projections, marks/channels, denominators, interactivity, and the 2025 QILT methodology change at the Week 12 interview.

The brief gives the deadline as **25 October 2026, 11:55 pm**. The local files are not yet a publicly hosted submission.

## Data and provenance

`data/sources.json` gives the original download URLs, authors, source worksheets/cells, populations, filters and calculations. `DATA_NOTES.md` explains the decisions in plain language. Every chart has a readable specification in `specs/`; use `python build_specs.py` to regenerate them after editing data or chart code. Run `python build_html.py` afterwards to embed the updated specifications, data, CSS and JavaScript into `index.html`. The HTML builder uses lxml; this is needed only for rebuilding, not for viewing the finished page.

Main salary/employment data are QILT's 2025 national tables, including 2024 comparisons. Salary history is Figure 6 of its report. ABS regional earnings and qualification data are **context**, explicitly labelled as different populations. They must not be interpreted as state graduate starting salaries. CPI is matched to 2016–25, not extrapolated beyond the graduate salary period.

The generated HTML is about 0.36 MB and the three local chart libraries total about 0.83 MB. The normal page load is around 1.2 MB, below a few megabytes. Data are embedded and no API key is needed. Local libraries avoid a CDN dependency in the complete project. The original multi-megabyte workbooks are linked as sources rather than sent to each visitor.

## Chart count and complexity

| No. | Specification | Idiom | Complexity planning |
|---|---|---|---|
| 1 | 01_salary | Horizontal bars | Basic |
| 2 | 02_bullet | Bullet chart with national benchmark | Advanced candidate |
| 3 | 03_salary_employment | Scatterplot | Basic |
| 4 | 04_parttime_heatmap | Heatmap | Advanced |
| 5 | 05_waffle | Waffle chart, including fractional square | Advanced |
| 6 | 06_occupations | Treemap (Vega) | Advanced |
| 7 | 07_gender_dumbbell | Connected dot / dumbbell | Do not rely on this for advanced count |
| 8 | 08_gender_gap | Diverging bars | Basic |
| 9 | 09_salary_trend | Multi-line chart | Basic |
| 10 | 10_waterfall | Waterfall | Advanced |
| 11 | 11_earnings_map | Choropleth | Advanced map idiom 1 |
| 12 | 12_degree_symbols | Proportional-symbol map | Advanced map idiom 2 |
| 13 | 13_degree_cartogram | Equal-size tile cartogram | Advanced map idiom 3 |
| 14 | 14_salary_slope | Slope chart | Do not rely on this for advanced count |
| 15 | 15_parallel_outcomes | Parallel coordinates with separately labelled scales | Advanced |

There are eight planned advanced forms even without counting the bullet chart: heatmap, waffle, treemap, waterfall, three map idioms and parallel coordinates. The rubric's classification is the tutor's decision, so discuss the bullet and tile cartogram with your tutor before relying on the HD complexity count. Fifteen charts exceed the ten-chart minimum; changing the year does not count as a separate chart.

## Lecturer-feedback revision

- Paragraphs and source notes have explicit bounded line spans with a maximum of ten words. Hyphenated terms and numbers are counted conservatively, so rendered lines can contain fewer words. Narrow screens can wrap within a span but cannot merge two bounded lines.
- Body paragraphs are 18 px, captions 16 px, and source notes 14 px on larger screens.
- Main sections share a common left edge. Captions use the same two-column grid as the paired charts.
- Pay remains teal; employment shares use blue; gender uses consistent coral/indigo; inflation-adjusted salary uses gold; qualification maps use violet. Study-area colours agree between the slope and parallel-coordinate charts.
- Salary labels are selective: extremes and the selected field. Other values remain in tooltips. The heatmap follows the same selective-label approach.
- The year control is above the chart; its national benchmark changes with the year.
- Discipline highlighting links six charts without hiding major page sections.

The Word file in `submission/` remains a draft; update its How description after finalising the webpage and add the required URL, sketch and screenshot.

## Verification completed here

- All 15 specifications compiled, executed and rendered as SVG through Vega/Vega-Lite, and were visually inspected.
- Source joins, missing-value handling, headline arithmetic, CPI adjustment, state coverage and local asset paths were checked.
- The Word draft was rendered and visually inspected.
- Browser automation was unavailable in this environment. Check the complete webpage layout, hover interactions, mobile/laptop sizing and GitHub Pages delivery in your browser before submission. The live URL, hand-drawn sketch and final webpage screenshot still require your account/work.

## Authorship and AI use

Daniel Ooi Kean Siong. Prepared 15 October 2026. ChatGPT assisted with source research, extraction, calculations, chart specifications, code and draft writing. Review and adapt the work, retain an accurate acknowledgement, and understand the decisions before the interview.

## Third-party code

Vega 5.33.0, Vega-Lite 5.23.0 and Vega-Embed 6.29.0 are included under their BSD-3-Clause licenses. See `vendor/THIRD_PARTY.md`. Natural Earth boundaries are public domain. ABS materials are attributed in the webpage and source manifest. QILT datasets remain subject to their original terms; the project redistributes only the small derived statistical extracts used in its charts.
