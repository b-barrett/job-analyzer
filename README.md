# Job Analyzer

A Python tool for analyzing job descriptions to identify keyword patterns and generate insights about skill requirements across job listings.

## Overview

Job Analyzer parses text files containing job descriptions, identifies predefined keywords and their variations, and generates detailed reports on keyword frequency, distribution, and patterns across job listings. This tool is especially useful for:

- Recruiters and hiring managers analyzing industry trends
- Job seekers tailoring their resumes to match market demands
- Career counselors providing data-driven guidance
- Researchers studying labor market skills requirements

## Features

- **Keyword detection**: Identifies 33 predefined keywords across 7 different categories
- **Comprehensive analysis**: Reports on keyword frequency, distribution across job postings, and co-occurrence patterns
- **Multiple output formats**: Generates both plain text and CSV reports for flexibility in further analysis
- **Sheet ID tracking**: Maintains job identity throughout the analysis for traceability
- **Categorized insights**: Organizes keywords into logical skill categories for easier interpretation

## Installation

```bash
git clone https://github.com/minchodos/job-analyzer.git
cd job-analyzer
```

## Usage

Basic usage:
```bash
python job_analyzer.py data_analyst_jobs.txt
```

Analyze all keywords without prompt:
```bash
python job_analyzer.py data_analyst_jobs.txt --all
```

Specify particular keywords for analysis:
```bash
python job_analyzer.py data_analyst_jobs.txt --keywords "SQL,Python,Tableau"
```

## Output Files

The script generates several output files:

| File | Description |
|------|-------------|
| `keyword_summary.txt` | Summary of keyword occurrences across all job listings |
| `all_keyword_lines.txt` | All matching lines organized by keyword category |
| `all_keyword_lines.csv` | CSV version of all matching lines with metadata |
| `unique_keyword_lines.txt` | Unique matching lines organized by keyword count |
| `unique_keyword_lines.csv` | CSV version of unique matching lines with metadata |
| `job_rank.txt` | Jobs ranked by keyword match frequency |
| `job_rank.csv` | CSV version of job rankings |
| `keyword_mapping.csv` | Mapping of keywords to categories and variations |

## Keyword Categories

The script analyzes keywords across seven categories:

1. **Analytical Techniques**: A/B Testing, Data Science, Exploratory, Forecasting, Large Datasets, Machine Learning, Predictive Analytics, Quantitative, Segmentation, Statistics
2. **Business Impact**: Actionable, Data-Driven, GTM Support, KPI, Patterns and Trends
3. **Data Visualization & Reporting**: Dashboards, Reporting, Storytelling, Tableau, Visualization
4. **Data Quality & Integrity**: Attention to Detail, Data Collection, Data Governance
5. **Workflow & Automation**: Automate, Data Pipelines, Data Warehousing, Integration
6. **Stakeholder Communication**: Cross-functional, Interpret, Non-Technical Audiences, Translate
7. **Programming Languages & Tools**: Python, R, SQL

## Input File Format

The script expects a text file where each job description is preceded by a "Sheet ID:" line, such as:

```
Sheet ID: 1
[Job description text...]

Sheet ID: 2
[Job description text...]
```

## Example Output

When run on a file with job descriptions, the script provides a summary in the console:

```
=== Keyword Totals (number of lines in which the keyword, or its close synonyms, appear) ===
 1. SQL: 45
 2. Python: 32
 3. Data-Driven: 26
...

Total Keywords: 33

Total Non-Unique Matching Lines Across All Keywords: 285
Total Unique Matching Lines Across All Keywords: 186

1. Analytical Techniques (10 keywords)

    • Statistics - 15 lines in 58.1% of jobs
    • Machine Learning - 18 lines in 48.4% of jobs
    ...
```

## Customization

You can customize the tool by modifying:

- `keyword_to_categories`: Add or change keyword category assignments
- `keyword_variations`: Add or modify variations of keywords to detect
- `OUTPUT_FILES`: Change output file names

## Requirements

- Python 3.6+
- Standard libraries: argparse, re, csv, collections

## License

[Specify your license here]

## Contributing

[Your contribution guidelines]

## Contact

[Your contact information]