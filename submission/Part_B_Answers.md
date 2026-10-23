# Part B answers

## Domain

My visualisation investigates starting salaries and employment outcomes for domestic undergraduate graduates in Australia. It compares study areas and female and male salary medians, then examines salary changes from 2016 to 2025 after accounting for inflation. A final section adds regional context through employee earnings and the distribution of residents whose highest qualification is a bachelor degree. These regional measures are explicitly separated from graduate starting salaries. The page compares disciplines and labour-market outcomes rather than ranking universities.

## Why and Who

The intended audience is Malaysian students and recent graduates who want to understand Australian graduate work, including students considering further study or employment in Australia. The visualisation helps them compare the pay associated with different fields while recognising that a high salary among full-time workers does not necessarily mean that full-time work is easy to obtain. Readers can identify salary differences, compare gender medians within a discipline, and distinguish nominal pay growth from changes in purchasing power. Short explanations introduce the median, employment denominators and inflation adjustment without requiring statistical training.

## What

The main source is the 2025 Graduate Outcomes Survey national report and published tables, produced by the Social Research Centre for the Australian Government Department of Education. The survey measures outcomes approximately four to six months after course completion. I use domestic undergraduate results from all provider types. The data include annual full-time salary medians, employment rates, part-time and underemployment shares, occupation shares, and 2024 salary comparisons. Salary history comes from Figure 6 of the report.

The second source is the Australian Bureau of Statistics. Employee earnings, August 2025 supplies regional median weekly main-job earnings for all employees. Education and Work, May 2025 supplies state estimates and proportions of people aged 15-74 whose highest qualification is a bachelor degree. CPI series A2325846C supplies matching June-quarter price indices for 2016-2025. Natural Earth supplies public-domain boundary geometry.

Study-area tables are joined by their original labels and year; regional tables are joined by state name. Suppressed values remain missing. Inflation-adjusted salary equals nominal salary multiplied by the 2025 CPI divided by that year's CPI. The downloadable source manifest records URLs, worksheets, cells, populations and calculations. No person-level linkage is performed.

## How

The single scrolling page follows five chapters: study-area pay, access to work, gender differences, change over time, and regional context. Horizontal bars support direct salary comparisons. Bullet charts relate selected fields to the national median. A scatterplot connects salary with full-time employment; parallel coordinates compare pay, employment access and wanting more hours using three separately labelled scales. A heatmap highlights part-time and underemployment patterns, a waffle shows employment composition, and a treemap shows occupation shares.

Connected dots compare female and male medians, while diverging bars show the percentage gap. A line chart separates reported salary from salary in 2025 dollars, a waterfall decomposes the nominal increase into inflation and real gain, and a slope chart compares the latest salary cohorts. A choropleth shows all-employee regional earnings, a proportional-symbol map shows bachelor-degree-holder counts, and an equal-size tile cartogram shows qualification proportions. The two geographic maps use a conic equal-area projection; the cartogram is schematic.

A year selector and hover tooltips support targeted comparison. Consistent colours, readable labels, chapter headings and annotations guide the story. Definitions distinguish graduate salaries from regional context and explain the 2025 break in employment-rate comparability. Charts use Vega-Lite, except the treemap, which uses Vega.

AI acknowledgement: ChatGPT assisted with source research, extraction, calculations, chart specifications, webpage code and draft text.