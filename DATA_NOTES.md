# Data notes

## Populations and measures

The main story uses **domestic undergraduate completers**, surveyed about four to six months after completion, from all provider types in the QILT national tables. “Undergraduate” here means a completed qualification, not a current student. The group includes people over 30 and people with previous work experience. It is not a pure sample of first-ever jobs or school leavers.

Salary is the **median annual full-time salary** in Australia, across all jobs. “Median” is the middle reported salary after sorting. It is not the mean, an advertised pay rate, or an individual salary guarantee. Salary data are self-reported and nominal unless labelled as 2025 dollars. Broad study-area labels are retained in CSVs; some display labels are shortened without merging categories.

The full-time employment rate has a different denominator from the full-time share among employed graduates. The 75.4% rate refers to those available for full-time employment. The 59.4% share refers to all employed graduates. The infographic does not subtract the full-time rate from 100 to invent a part-time or unemployment rate.

The part-time and underemployment heatmap uses percentages of all employed graduates within each study area. “Want more hours” is a subset of employed part-time graduates. Not everyone working part-time is underemployed.

Occupation treemap values are shares among all employed domestic undergraduates. They sum to 100.1% due to source rounding. Vega normalises areas by their sum; labels show original published values. No counts are invented from these percentages.

## Source extraction and linkage

1. The QILT ZIP was downloaded from its official site. Values were read from the XLSX source, using cached cell values and the workbook's shared strings. The relevant worksheets are named in `sources.json`.
2. Salary, employment and part-time records were joined by exact original study-area label. The combined table contains 21 study areas × 2 years = 42 rows.
3. Dentistry's male salary and tourism/hospitality/recreation's female salary are unavailable in 2025. These remain null. Both fields are retained in total-salary charts but omitted from comparisons requiring both gender values. Nulls are never interpreted as zero. Total medians are taken from the source; they are not calculated by averaging gender medians.
4. The salary trend has ten annual observations transcribed from the labelled undergraduate series in QILT Figure 6, printed page 7, PDF page 18. The last two years agree with the workbook totals. The earlier salary values are not inferred or interpolated.
5. CPI series A2325846C was read from ABS Table 1/2 Data1, column J, June-quarter observations for 2016–25. It is the all-groups weighted average of eight capital cities.
6. The eight regional records join ABS Employee earnings and Education and Work by state name. Employee earnings uses August 2025, Persons, Australia, median weekly earnings in the main job, Total column O. Education and Work uses Table 21, Persons, Bachelor Degree as highest attainment: row 11 estimates and row 23 published proportions. Survey counts are in thousands. Higher postgraduate qualifications are excluded by that definition.
7. The degree-holder maps do not represent new graduates, employment counts or current student enrolments. The earnings map covers all employees, including part-time workers. The datasets are presented together as context, not merged at person level or used to calculate a state graduate salary estimate.

## Calculations

- Gender gap (%) = 100 × (male median − female median) / male median. This is an unadjusted descriptive gap.
- Salary in 2025 dollars = salary in year t × CPI June 2025 / CPI June t.
- Nominal growth 2016–25 = 100 × (77,000 / 57,900 − 1) = 32.99%.
- CPI grew from 108.6 to 141.7 over the matched June quarters, about 30.48%.
- Maintaining the 2016 salary's purchasing power in 2025 would require $75,547.24. The $19,100 nominal salary increase therefore splits into $17,647.24 inflation catch-up and $1,452.76 beyond inflation.
- Real salary growth = 100 × (77,000 / 75,547.24 − 1) = about 1.92%.
- Highest minus lowest study-area median, 2025 = $103,100 − $62,600 = $40,500.
- The national gender gap is 100 × (79,000 − 75,300) / 79,000 = 4.68%, displayed as 4.7%.

## Comparability

QILT changed its labour-force definition in 2025. Graduates not working and only passively looking for work are no longer treated as in the labour force. Full-time and overall employment rates are not directly comparable with earlier results. The site compares those rates within 2025 and uses its year selector for salary, not an unqualified employment trend.

Salary trends compare annual graduate cohorts. They do not track individual workers' wage growth. Gender and study-area differences can also reflect occupation, experience, age, hours, location and other factors. The page does not claim a causal return on choosing a degree or gender discrimination from medians alone.

The latest relevant QILT salary release is 2025, published in 2026. Regional ABS series are their 2025 releases; Education and Work ceased after 2025. CPI is deliberately matched to the salary window ending in 2025. Newer CPI observations alone would not justify inventing a 2026 graduate salary.

## Geography

The choropleth and proportional-symbol map use a conic equal-area projection, standard parallels 18°S and 36°S, centred for Australia. It preserves area, not local angles or every distance. Natural Earth 1:50m boundaries are filtered to the eight states and territories and rounded to three decimal places to keep the transfer small. The ACT is small on the geographic maps but is visible as its own tile in the cartogram.

Circle **area**, not radius, is proportional to estimated bachelor-degree holders. Marker anchors are approximate state centres, not exact residence locations or institutions. The equal-size tile cartogram is schematic and has no conventional map projection. It gives small territories equal visual space to compare proportions. No map ranks universities.
