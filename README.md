# Job Keyword Analyzer
A Python command-line tool that scans job descriptions for predefined keywords and produces categorized summaries, rankings, and matched line breakdowns in both TXT and CSV formats.

## Features
- Detects keyword mentions across job postings
- Supports keyword synonyms (e.g., "SQL" → relational databases)
- Categorizes keywords by domain (e.g., Workflow & Automation)
- Outputs detailed reports that are spreadsheet-ready

## Usage
```bash
python job_analyzer.py <file_path> [--all] [--keywords "Keyword1,Keyword2"]
```

### Examples
Analyze all keywords:
```bash
python job_analyzer.py data_analyst_jobs.txt --all
```
Analyze a specific subset:
```bash
python job_analyzer.py data_analyst_jobs.txt --keywords "SQL,Python,Tableau"
```

If no flags are provided, the script will prompt you to enter all keywords or specific subset.

## Installation
1. **Clone the repo**

```bash
git clone https://github.com/minchodos/job-analyzer.git
cd job-analyzer
```

2. **(Optional)**: Create a virtual environment

Using `venv`:
```bash
python -m venv venv
source venv/bin/activate
```

Using `conda`:
```bash
conda create --name job-analyzer python=3.12
conda activate job-analyzer
```

3. Install requirements (currently only standard library modules used)

```bash
# Note: Currently no external dependencies
# pip install -r requirements.txt
```

> You can safely skip this step unless external libraries are added later.

## Output Files
- `job_rank.txt` / `.csv` — Job rankings by keyword presence
- `all_keyword_lines.txt` / `.csv` — All matching lines with keyword tagging
- `unique_keyword_lines.txt` / `.csv` — Unique lines grouped by keyword match count
- `keyword_summary.txt` — Summary of keyword prevalence across job postings
- `keyword_mapping.csv` — All keyword variations and categories

## Input File Format
The input text file should contain multiple job descriptions, each labeled with a line like:

```
Job ID: 42
```

## Future Improvements
- Multi-category support per keyword
- Output folder customization
- JSON export for dashboarding

