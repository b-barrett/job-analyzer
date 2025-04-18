"""
Usage:
  python job_analyzer.py data_analyst_jobs.txt
  python job_analyzer.py data_analyst_jobs.txt --all
"""

import argparse
import re
import csv
from collections import defaultdict

# Note: first line of data analyst jobs text file starts on line 2; if line 1, Sheet ID: 1 not detected. For later: investigate why
# file_path = '04_data_analyst_62_job_descriptions_raw.txt'

# Centralized mapping for output file names; modify values to rename files
OUTPUT_FILES = {
    "job_rank_txt": "job_rank.txt",
    "job_rank_csv": "job_rank.csv",

    "all_lines_txt": "all_keyword_lines.txt",
    "all_lines_csv": "all_keyword_lines.csv",

    "unique_lines_txt": "unique_keyword_lines.txt",
    "unique_lines_csv": "unique_keyword_lines.csv",
}

# Current: each keyword is assigned to exactly one category
# Future: consider multi-category assignments for keywords that naturally span two or more categories.

keyword_to_categories = {
    # === Analytical Techniques	 ===
    "A/B Testing": ["Analytical Techniques"],
    "Data Science": ["Analytical Techniques"],
    "Exploratory": ["Analytical Techniques"],
    "Forecasting": ["Analytical Techniques"],
    "Large Datasets": ["Analytical Techniques"],
    "Machine Learning": ["Analytical Techniques"],
    "Predictive Analytics": ["Analytical Techniques"],
    "Quantitative": ["Analytical Techniques"],
    "Segmentation": ["Analytical Techniques"],
    "Statistics": ["Analytical Techniques"],

    # === Business Impact ===
    "Actionable": ["Business Impact"],
    "Data-Driven": ["Business Impact"],
    "GTM Support": ["Business Impact"],
    "KPI": ["Business Impact"],
    "Patterns and Trends": ["Business Impact"],

    # === Data Visualization & Reporting ===
    "Dashboards": ["Data Visualization & Reporting"],
    "Reporting": ["Data Visualization & Reporting"],
    "Storytelling": ["Data Visualization & Reporting"],
    "Tableau": ["Data Visualization & Reporting"],
    "Visualization": ["Data Visualization & Reporting"],

    # === Data Quality & Integrity ===
    "Attention to Detail": ["Data Quality & Integrity"],
    "Data Collection": ["Data Quality & Integrity"],
    "Data Governance": ["Data Quality & Integrity"],

    # === Workflow & Automation ===
    "Automate": ["Workflow & Automation"],
    "Data Pipelines": ["Workflow & Automation"],
    "Data Warehousing": ["Workflow & Automation"],
    "Integration": ["Workflow & Automation"],

    # === Stakeholder Communication ===
    "Cross-functional": ["Stakeholder Communication"],
    "Interpret": ["Stakeholder Communication"],
    "Non-Technical Audiences": ["Stakeholder Communication"],
    "Translate": ["Stakeholder Communication"],

    # === Programming Languages & Tools ===
    "Python": ["Programming Languages & Tools"],
    "R": ["Programming Languages & Tools"],
    "SQL": ["Programming Languages & Tools"]
}

def invert_keyword_category_mapping(keyword_to_categories):
    category_to_keywords = defaultdict(list)

    for keyword, categories in keyword_to_categories.items():
        for category in categories:
            category_to_keywords[category].append(keyword)

    for category in category_to_keywords:
        category_to_keywords[category] = sorted(set(category_to_keywords[category]))

    return dict(category_to_keywords)

category_to_keywords = invert_keyword_category_mapping(keyword_to_categories)

keyword_variations = {
    "Dashboards": ["dashboard", "dashboards", "dashboarding"],
    "SQL": ["SQL", "SQLs", "query", "queries", "querying", "database", "databases", "relational"],
    "Python": ["Python"],
    "Visualization": ["visualization", "visualizations"],
    "Tableau": ["Tableau"],
    "Automate": ["automate", "automated", "automates", "automating", "automation", "automations"],
    "Translate": ["translate", "translating", "translated", "translates"],
    "Cross-functional": ["cross-functional", "cross functional", "cross-functionally"],
    "Reporting": ["reporting"],
    "Non-Technical Audiences": ["non-technical"],
    "Data-Driven": ["data-driven", "data driven"],
    "Data Science": ["data science", "data scientist", "data scientists"],
    "R": [" R ", "/R", "R/"],
    "Forecasting": ["forecast", "forecasting", "forecasts"],
    "KPI": ["KPI", "KPIs","key performance indicator", "key performance indicators", "KPI reporting"],
    "Machine Learning": ["machine learning"],
    "Predictive Analytics": ["predictive"],
    "Data Collection": ["data collection"],
    "A/B Testing": ["A/B testing", "AB testing", "A/B", "A/B test", "A/B tests", "experiment", "experiments", "experimentation"],
    "Data Governance": ["governance", "integrity", "data quality", "validation"],
    "Integration": ["integration", "integrate", "integrated"],
    "Actionable": ["actionable"],
    "Large Datasets": ["large datasets", "large data sets", "large dataset", "large data set", "large"],
    "Statistics": ["statistics", "statistical","hypothesis testing"],
    "Interpret": ["interpret", "interpreting", "interpretation", "interpretations"],
    "Segmentation": ["segmentation", "segment", "segments"],
    "Storytelling": ["storytelling", "story", "storyteller", "story teller", "stories"],
    "Attention to Detail": ["detail", "details", "detailed", "detail-oriented", "attention to detail"],
    "Patterns and Trends": ["patterns", "trends", "trend", "pattern"],
    "Data Pipelines": ["data pipeline", "data pipelines", "ETL pipeline", "ETL pipelines", "ETL processes", "Extract Transform Load", "Extract, Transform, Load"],
    "Data Warehousing": ["data warehouse", "data warehouses", "data warehousing", "warehouse", "warehouses", "architecture"],
    "Quantitative": ["quantitative"],
    "GTM Support": ["GTM", "go-to-market"],
    "Exploratory": ["exploratory", "explore", "exploring"],
}

def compile_keyword_patterns(keyword_variations):
    patterns = {}
    for keyword, variations in keyword_variations.items():
        pattern = r'\b(?:' + '|'.join(re.escape(v) for v in variations) + r')\b'
        # pattern = r'(?<!\w)(?:' + '|'.join(re.escape(v) for v in variations) + r')(?!\w)'
        patterns[keyword] = re.compile(pattern, re.IGNORECASE)
    return patterns

def get_all_sheet_ids(file_path):
    sheet_ids = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("Sheet ID:"):
                sheet_id = line.replace("Sheet ID:", "").strip()
                sheet_ids.add(sheet_id)
    return sheet_ids

def count_matching_lines(file_path, keyword_patterns):
    counts = {k: 0 for k in keyword_patterns}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for keyword, pattern in keyword_patterns.items():
            seen = set()
            for line in lines:
                if pattern.search(line) and line not in seen:
                    counts[keyword] += 1
                    seen.add(line)
    return counts

def extract_matching_lines(file_path, keyword_patterns, selected_keywords):
    matches = {k: [] for k in selected_keywords}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for keyword in selected_keywords:
        seen = set()
        for line in lines:
            stripped_line = line.strip()
            if keyword_patterns[keyword].search(line) and stripped_line not in seen:
                matches[keyword].append(stripped_line)
                seen.add(stripped_line)
    return matches

def get_unique_matched_lines(file_path, keyword_patterns):
    unique_matches = {}
    current_sheet_id = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for raw_line in file:
            # line = raw_line.strip()
            line = raw_line.strip().replace('\r', '')


            if not line or set(line) == {"_"}:
                continue

            if "Sheet ID:" in line:
                try:
                    current_sheet_id = line.split("Sheet ID:")[1].strip()
                    print(f"✅ Detected Sheet ID: {current_sheet_id}")
                except IndexError:
                    print(f"⚠️ Could not extract Sheet ID from line: {repr(line)}")
                continue

            matched_keywords = [kw for kw, pattern in keyword_patterns.items() if pattern.search(line)]

            if matched_keywords:
                if current_sheet_id:
                    unique_matches[line] = (matched_keywords, current_sheet_id)
                else:    
                    print(f"⚠️ Sheet ID missing or not found for line:\n{line[:100]}...")
    
    return unique_matches

def generate_keyword_mapping_csv():
    output_path = "keyword_mapping.csv"
    keyword_variations_lower = {k.lower(): [v.lower() for v in vals] for k, vals in keyword_variations.items()}

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="|")
        writer.writerow([
            "keyword",
            "original_keyword",
            "keyword_variations",
            "category",
            "original_category"
        ])

        entries = []
        for keyword_raw, categories in keyword_to_categories.items():
            keyword = keyword_raw.lower()
            variations = keyword_variations_lower.get(keyword, [])
            variations_lower = [v.lower() for v in variations]

            for category_raw in categories:
                category = category_raw.lower()
                entries.append([
                    keyword,
                    keyword_raw,
                    "~".join(variations_lower),
                    category,
                    category_raw
                ])

        # Toggle sort order below:
        entries.sort(key=lambda row: row[0])  # Sort by keyword
        # entries.sort(key=lambda row: row[3])    # Sort by category

        writer.writerows(entries)

    print(f"\nWrote keyword mapping to {output_path}\n")

def main(file_path, export_all, keywords_arg):
    keyword_patterns = compile_keyword_patterns(keyword_variations)
    line_totals = count_matching_lines(file_path, keyword_patterns)

    print("=== Keyword Totals (number of lines in which the keyword, or its close synonyms, appear) ===")
    for i, (keyword, count) in enumerate(sorted(line_totals.items(), key=lambda x: x[1], reverse=True), 1):
        print(f"{i:>2}. {keyword}: {count}")
    print(f"\nTotal Keywords: {len(line_totals)}")

    total_lines = sum(line_totals.values())
    print(f"\nTotal Non-Unique Matching Lines Across All Keywords: {total_lines}")

    unique_lines = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            for pattern in keyword_patterns.values():
                if pattern.search(line):
                    unique_lines.add(line.strip())
                    break  # Stop searching after the first match

    print(f"Total Unique Matching Lines Across All Keywords:: {len(unique_lines)}")


    if export_all:
        selected_keywords = sorted(line_totals, key=line_totals.get, reverse=True)

    elif keywords_arg:
        raw_keywords = [kw.strip() for kw in keywords_arg.split(",")]
        valid_keywords = [kw for kw in raw_keywords if kw in keyword_variations]
        selected_keywords = sorted(valid_keywords, key=line_totals.get, reverse=True)
        
    else:
        print("\nEnter comma-separated keywords you'd like to see matching lines for (or press Enter to skip):")
        selected = input("Keywords: ").strip()
        selected_keywords = []

        if selected:
            if selected.lower() == "all":
                selected_keywords = sorted(line_totals, key=line_totals.get, reverse=True)
            else:
                raw_keywords = [kw.strip() for kw in selected.split(",")]
                valid_keywords = [kw for kw in raw_keywords if kw in keyword_variations]
                selected_keywords = sorted(valid_keywords, key=line_totals.get, reverse=True)

    if not selected_keywords:
        print("No valid keywords entered.")
        return

    matching_lines = extract_matching_lines(file_path, keyword_patterns, selected_keywords)
    unique_matches = get_unique_matched_lines(file_path, keyword_patterns)
    keyword_sheet_coverage = defaultdict(set)
    for line, (keywords, sheet_id) in unique_matches.items():
        for keyword in keywords:
            keyword_sheet_coverage[keyword].add(sheet_id)

    total_jobs = len(get_all_sheet_ids(file_path))

    summary_lines = []
    for keyword in sorted(selected_keywords, key=lambda k: len(keyword_sheet_coverage.get(k, set())) / total_jobs, reverse=True):
        count = line_totals[keyword]
        jobs_with_keyword = len(keyword_sheet_coverage.get(keyword, set()))
        job_percent = (jobs_with_keyword / total_jobs) * 100
        summary_line = f"{keyword} ({count} lines in {jobs_with_keyword} of {total_jobs} jobs – {job_percent:.1f}%)"
        summary_lines.append(summary_line)

    summary_txt_path = "keyword_summary.txt"
    with open(summary_txt_path, "w", encoding="utf-8") as f:
        for line in summary_lines:
            f.write(line + "\n")

    print(f"\nWrote keyword summary to:\n  • {summary_txt_path}")

    all_lines_txt = OUTPUT_FILES["all_lines_txt"]
    with open(all_lines_txt, 'w', encoding='utf-8') as out_file:
    
        for i, category in enumerate(sorted(category_to_keywords), 1):
            category_keywords = [k for k in category_to_keywords[category] if k in selected_keywords]
            out_file.write(f"\n\n{i}. {category}\n\n")
            print(f"\n{i}. {category} ({len(category_keywords)} keyword{'s' if len(category_keywords) != 1 else ''})\n")

            category_keywords_sorted = sorted(
                category_keywords,
                key=lambda k: len(keyword_sheet_coverage.get(k, set())) / total_jobs,
                reverse=True
            )
            for keyword in category_keywords_sorted:
                
                lines = matching_lines.get(keyword, [])
                if not lines:
                    continue

                match_word = "line" if len(lines) == 1 else "lines"
                jobs_with_keyword = len(keyword_sheet_coverage.get(keyword, set()))
                job_percent = (jobs_with_keyword / total_jobs) * 100
                header = f"{keyword} - {len(lines)} {match_word} in {job_percent:.1f}% of jobs"
                out_file.write(f"{header}\n\n")

                for line in lines:
                    all_keywords = [kw for kw in keyword_patterns if keyword_patterns[kw].search(line)]

                    # OPTION 1: Alphabetical order (default)
                    other_keywords = sorted([kw for kw in all_keywords if kw != keyword])

                    # OPTION 2: Order of appearance in the line
                    # other_keywords = [kw for kw in all_keywords if kw != keyword]

                    all_keywords_ordered = [f"*{keyword}*"] + other_keywords

                    keyword_word = "keyword" if len(all_keywords) == 1 else "keywords"
                    tagged_line = f"    • {line} ||| {len(all_keywords)} {keyword_word}: {', '.join(all_keywords_ordered)}"
                    out_file.write(f"{tagged_line}\n\n")

                match_count = len(lines)
                jobs_with_keyword = len(keyword_sheet_coverage.get(keyword, set()))
                job_percent = (jobs_with_keyword / total_jobs) * 100
                line_word = "line" if match_count == 1 else "lines"
                print(f"    • {match_count} {line_word} for {keyword} ({jobs_with_keyword} of {total_jobs} jobs – {job_percent:.1f}%)")

    all_lines_csv = OUTPUT_FILES["all_lines_csv"]
    with open(all_lines_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['Keyword', 'Line', 'CharacterCount', 'Category', 'AllKeywords', 'SheetID', 'MatchCount', 'MultiKeyword'])
        
        for keyword in selected_keywords:
            for line in matching_lines[keyword]:
                category = keyword_to_categories[keyword][0]
                matched_keywords, sheet_id = unique_matches.get(line, ([], None))
                keyword_list = " ~ ".join(sorted(matched_keywords))
                match_count = len(matched_keywords)
                is_multi = match_count > 1
                writer.writerow([keyword, line, len(line), category, keyword_list, sheet_id, match_count, is_multi])

    print(f"\nWrote {total_lines} matching lines (non-unique).")
    print("Saved to:")
    print(f"  • {all_lines_txt}")
    print(f"  • {all_lines_csv}")

    all_sheet_ids = get_all_sheet_ids(file_path)
    sheet_id_counts = {sheet_id: 0 for sheet_id in all_sheet_ids}

    for line, (_, sheet_id) in unique_matches.items():
        if sheet_id in sheet_id_counts:
            sheet_id_counts[sheet_id] += 1
        else:
            print(f"⚠️ Sheet ID missing or not found for line:\n{line[:100]}...\n")

    total_unique_lines = len(unique_matches)
    sorted_sheet_ids = sorted(sheet_id_counts.items(), key=lambda x: (-x[1], int(x[0])))

    print(f"\n=== Job Stats (ranked by unique keyword counts across {total_unique_lines} unique lines) ===")

    keyword_count_by_sheet_id = defaultdict(set)
    line_count_by_sheet_id = defaultdict(int)

    for line, (keywords, sheet_id) in unique_matches.items():
        keyword_count_by_sheet_id[sheet_id].update(keywords)

        line_count_by_sheet_id[sheet_id] += 1
    
    sheet_stats = []
    for sheet_id in sheet_id_counts:
        line_count = line_count_by_sheet_id[sheet_id]
        keyword_count = len(keyword_count_by_sheet_id[sheet_id])
        percent = (line_count / total_unique_lines) * 100
        sheet_stats.append((sheet_id, keyword_count, line_count, percent))

    sheet_stats_sorted = sorted(sheet_stats, key=lambda x: (-x[1], -x[2], -x[3]))

    for rank, (sheet_id, keyword_count, line_count, percent) in enumerate(sheet_stats_sorted, 1):
        line_word = "line" if line_count == 1 else "lines"
        keyword_word = "keyword" if keyword_count == 1 else "keywords"
        print(f"{rank:>2}. Job ID {sheet_id:<2} - {line_count:>2} {line_word} ({keyword_count} {keyword_word})")

        total_lines_check = sum(line_count for _, _, line_count, _ in sheet_stats_sorted)
        assert total_lines_check == total_unique_lines, f"Mismatch! Expected {total_unique_lines}, but summed {total_lines_check}."
    
    print(f"\nTOTAL: {total_lines_check} lines across {len(sheet_stats_sorted)} job descriptions (100% of total)")

    total_keyword_matches = sum(len(s) for s in keyword_count_by_sheet_id.values())

    sorted_sheet_keyword_data = sorted(
        keyword_count_by_sheet_id.items(),
        key=lambda x: (-len(x[1]), int(x[0]))  # sort by keyword count (desc), then Sheet ID (asc)
    )

    job_rank_txt = OUTPUT_FILES["job_rank_txt"]
    with open(job_rank_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(f"\n=== Sheet ID Summary by Total Keyword Matches (out of {total_keyword_matches} total keyword matches) ===\n\n")
        for rank, (sheet_id, keyword_count) in enumerate(sorted_sheet_keyword_data, 1):
            line_count = line_count_by_sheet_id[sheet_id]
            percent = (len(keyword_count) / total_keyword_matches) * 100
            line_word = "line" if line_count == 1 else "lines"
            txt_file.write(f"{rank:>2}. Sheet ID {sheet_id}: {keyword_count} keywords in {line_count} {line_word} ({percent:.2f}%)\n")
    print(f"\nWrote Sheet ID keyword counts to:\n  • {job_rank_txt}")

    job_rank_csv = OUTPUT_FILES["job_rank_csv"]
    with open(job_rank_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank', 'Sheet ID', 'Unique Matching Lines', 'Percentage of Total'])
        for rank, (sheet_id, count) in enumerate(sorted_sheet_ids, 1):
            percent = (count / total_unique_lines) * 100
            writer.writerow([rank, sheet_id, count, f"{percent:.2f}%"])

    print(f"\nWrote Sheet ID keyword counts to:\n  • {job_rank_csv}")

    lines_by_match_count = defaultdict(list)

    for line, (keywords, sheet_id) in unique_matches.items():
        match_count = len(keywords)
        char_count = len(line)

        tagged_line = (
            f"• {line}\n"
            f"Keywords: {', '.join(keywords)}\n"
            f"Sheet ID: {sheet_id}"
        )

        lines_by_match_count[match_count].append(tagged_line)

    unique_lines_txt = OUTPUT_FILES["unique_lines_txt"]

    with open(unique_lines_txt, 'w', encoding='utf-8') as txt_file:
        for count in sorted(lines_by_match_count.keys(), reverse=True):
            section_lines = lines_by_match_count[count]
                                
            percentage = (len(section_lines) / len(unique_matches)) * 100
            
            line_word = "line" if len(section_lines) == 1 else "lines"
            section_header = (
                f"=== Lines with {count} Keyword{'s' if count > 1 else ''} "
                f"({len(section_lines)} {line_word}, {percentage:.1f}% of total) ==="
            )

            txt_file.write(section_header + "\n")

            for tagged_line in section_lines:
                txt_file.write(f"{tagged_line}\n\n")

    with open(unique_lines_txt, 'a', encoding='utf-8') as txt_file:
        txt_file.write(f"\n=== Unique Keyword Line Counts by Sheet ID (out of {len(unique_matches)} total unique lines) ===\n\n")

        for rank, (sheet_id, count) in enumerate(sorted_sheet_ids, 1):
            percent = (count / len(unique_matches)) * 100
        
            line_word = "line" if count == 1 else "lines"
            txt_file.write(f"{rank:>2}. Sheet ID {sheet_id}: {count} {line_word} ({percent:.1f}%)\n") 

        lines_by_match_count = defaultdict(int)
        for line, (keywords, _) in unique_matches.items():
            match_count = len(keywords)
            lines_by_match_count[match_count] += 1

        total_lines = len(unique_matches)
        txt_file.write("\n=== Lines Grouped by Number of Matched Keywords ===\n\n")

        for match_count in sorted(lines_by_match_count.keys(), reverse=True):
            count = lines_by_match_count[match_count]
            percentage = (count / total_lines) * 100
            keyword_word = "Keyword" if match_count == 1 else "Keywords"
            line_word = "line" if count == 1 else "lines"
            txt_file.write(f"Lines with {match_count} {keyword_word} ({count} {line_word}, {percentage:.1f}% of total)\n")

        txt_file.write(f"\nTotal lines ({total_lines}, 100% of total)\n")
    
        longest_lines = sorted(unique_matches.items(), key=lambda x: len(x[0]), reverse=True)[:10]

        txt_file.write(f"\n=== Top 10 Longest Unique Lines by Character Count ===\n\n")
        for i, (line, (keywords, sheet_id)) in enumerate(longest_lines, 1):
            txt_file.write(f"{i:>2}. ({len(line)} chars) Sheet ID {sheet_id} – {len(keywords)} keyword(s):\n")
            txt_file.write(f"    {line}\n\n")

    unique_lines_csv = OUTPUT_FILES["unique_lines_csv"]

    with open(unique_lines_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Sheet ID', 'Line', 'Matching Keywords', 'CharacterCount', 'MatchCount'])

        sorted_lines = sorted(unique_matches.items(), key=lambda x: len(x[1][0]), reverse=True)

        for line, (keywords, sheet_id) in sorted_lines:
            writer.writerow([sheet_id, line, ', '.join(keywords), len(line), len(keywords)])

    print(f"\nWrote {len(unique_matches)} matching lines (unique).")
    print("Saved to:")
    print(f"  • {unique_lines_txt}")
    print(f"  • {unique_lines_csv}")

    generate_keyword_mapping_csv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze job descriptions.")
    parser.add_argument("file_path", help="Path to the job descriptions text file.")
    parser.add_argument("--all", action="store_true", help="Export all matching lines without prompt")
    parser.add_argument("--keywords",type=str,help="Comma-separated list of keywords (e.g., 'SQL,Python')")

    args = parser.parse_args()
    main(args.file_path, args.all, args.keywords)
