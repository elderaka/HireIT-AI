"""
Simple CSV conversion demonstration using dummy data.

This script shows how to use the CSV functions with dummy data
without requiring all dependencies.

Run: python demo_csv_simple.py
"""

import json
import csv
from pathlib import Path
from io import StringIO

# Create output directory
OUTPUT_DIR = Path("output/demo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("CSV CONVERSION DEMONSTRATION WITH DUMMY DATA")
print("="*80)

# Load dummy data
print("\n📂 Loading dummy data...")
with open("dummy-csv-data.json", "r", encoding="utf-8") as f:
    dummy_data = json.load(f)

print("✅ Loaded dummy data successfully")
print(f"   - {len(dummy_data['cv_review_candidates'])} CV candidates")
print(f"   - {len(dummy_data['applicant_tracker_data'])} tracker entries")
print(f"   - {len(dummy_data['interview_transcripts'])} interview transcripts")

# ============================================================================
# DEMO 1: Simple CSV from CV Review Candidates
# ============================================================================
print("\n" + "="*80)
print("DEMO 1: CV Review Results → CSV")
print("="*80)

candidates = dummy_data['cv_review_candidates']

# Prepare data for CSV
csv_data = []
for candidate in candidates:
    csv_data.append({
        'File Name': candidate['file_name'],
        'Name': candidate.get('name', 'N/A'),
        'Email': candidate.get('email', 'N/A'),
        'Experience Years': candidate.get('experience_years', 'N/A'),
        'Final Score': candidate['scores']['final_score'],
        'Decision': candidate['auto_decision'],
        'Min Salary': candidate['worth_range'].get('min', 0),
        'Max Salary': candidate['worth_range'].get('max', 0),
        'Unreadable': candidate['unreadable']
    })

# Write to CSV
output_file = OUTPUT_DIR / "cv_review_results.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['File Name', 'Name', 'Email', 'Experience Years', 
                  'Final Score', 'Decision', 'Min Salary', 'Max Salary', 'Unreadable']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_data)

print(f"✅ Created: {output_file}")
print(f"📊 Exported {len(csv_data)} candidates")

# Show preview
print("\n📄 Preview (first 3 rows):")
with open(output_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 4:  # Header + 3 rows
            print(f"   {line.strip()}")

# ============================================================================
# DEMO 2: Applicant Tracker CSV
# ============================================================================
print("\n" + "="*80)
print("DEMO 2: Applicant Tracker → CSV")
print("="*80)

tracker_data = dummy_data['applicant_tracker_data']

output_file = OUTPUT_DIR / "applicant_tracker.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = list(tracker_data[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tracker_data)

print(f"✅ Created: {output_file}")
print(f"📊 Tracking {len(tracker_data)} candidates")

# Statistics
accepted = sum(1 for r in tracker_data if r['Status'] == 'Accepted')
pending = sum(1 for r in tracker_data if r['Status'] == 'Pending')
rejected = sum(1 for r in tracker_data if r['Status'] == 'Rejected')

print(f"\n📈 Pipeline Statistics:")
print(f"   ✅ Accepted: {accepted}")
print(f"   ⏳ Pending: {pending}")
print(f"   ❌ Rejected: {rejected}")

# ============================================================================
# DEMO 3: Interview Summary CSV
# ============================================================================
print("\n" + "="*80)
print("DEMO 3: Interview Assessment Summary → CSV")
print("="*80)

interviews = dummy_data['interview_transcripts']

interview_summary = []
for interview in interviews:
    assessment = interview['assessment']
    interview_summary.append({
        'Candidate': interview['candidate_name'],
        'Date': interview['interview_date'],
        'Duration (min)': interview['duration_minutes'],
        'Technical Score': assessment['technical_score'],
        'Communication Score': assessment['communication_score'],
        'Cultural Fit Score': assessment['cultural_fit_score'],
        'Problem Solving Score': assessment['problem_solving_score'],
        'Final Score': assessment['final_score'],
        'Recommendation': assessment['recommendation']
    })

output_file = OUTPUT_DIR / "interview_summary.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = list(interview_summary[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(interview_summary)

print(f"✅ Created: {output_file}")
print(f"📊 {len(interview_summary)} interview assessments")

print("\n📄 CSV Content:")
with open(output_file, 'r', encoding='utf-8') as f:
    print(f.read())

# ============================================================================
# DEMO 4: Simple Product Table CSV
# ============================================================================
print("\n" + "="*80)
print("DEMO 4: Simple Product Table → CSV")
print("="*80)

products = dummy_data['simple_table_examples']['example_1_list_of_dicts']

output_file = OUTPUT_DIR / "products.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = list(products[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

print(f"✅ Created: {output_file}")

print("\n📄 CSV Content:")
with open(output_file, 'r', encoding='utf-8') as f:
    print(f.read())

# ============================================================================
# DEMO 5: Employee List from Lists → CSV
# ============================================================================
print("\n" + "="*80)
print("DEMO 5: Employee List (List of Lists) → CSV")
print("="*80)

headers = dummy_data['simple_table_examples']['example_2_headers']
rows = dummy_data['simple_table_examples']['example_2_list_of_lists']

output_file = OUTPUT_DIR / "employees.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"✅ Created: {output_file}")

print("\n📄 CSV Content:")
with open(output_file, 'r', encoding='utf-8') as f:
    print(f.read())

# ============================================================================
# DEMO 6: Detailed Employee Data
# ============================================================================
print("\n" + "="*80)
print("DEMO 6: Detailed Employee Records → CSV")
print("="*80)

employee_data = dummy_data['simple_table_examples']['example_3_employee_data']

output_file = OUTPUT_DIR / "employee_records.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = list(employee_data[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(employee_data)

print(f"✅ Created: {output_file}")
print(f"📊 {len(employee_data)} employee records")

print("\n📄 CSV Content:")
with open(output_file, 'r', encoding='utf-8') as f:
    print(f.read())

# ============================================================================
# DEMO 7: Batch Review with Statistics
# ============================================================================
print("\n" + "="*80)
print("DEMO 7: Batch Review Statistics → CSV")
print("="*80)

rubric = dummy_data['rubric_info']
candidates = dummy_data['cv_review_candidates']

# Create summary statistics
stats = {
    'Total Candidates': len(candidates),
    'Pass': sum(1 for c in candidates if c['auto_decision'] == 'pass'),
    'Borderline': sum(1 for c in candidates if c['auto_decision'] == 'borderline'),
    'Fail': sum(1 for c in candidates if c['auto_decision'] == 'fail'),
    'Unreadable': sum(1 for c in candidates if c['unreadable']),
    'Average Score': sum(c['scores']['final_score'] for c in candidates if not c['unreadable']) / 
                     len([c for c in candidates if not c['unreadable']]),
    'Threshold Score': rubric['threshold_score'],
    'Role': rubric['role_title']
}

# Export detailed batch review
batch_rows = []
for c in candidates:
    batch_rows.append({
        'File': c['file_name'],
        'Name': c.get('name', 'N/A'),
        'Final Score': c['scores']['final_score'],
        'Decision': c['auto_decision'],
        'Worth Min': c['worth_range'].get('min', 0),
        'Worth Max': c['worth_range'].get('max', 0),
        'Unreadable': c['unreadable'],
        'Reason': c.get('unreadable_reason', '')
    })

output_file = OUTPUT_DIR / "batch_review.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = list(batch_rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(batch_rows)

print(f"✅ Created: {output_file}")
print(f"\n📊 Review Statistics:")
for key, value in stats.items():
    if isinstance(value, float):
        print(f"   {key}: {value:.2f}")
    else:
        print(f"   {key}: {value}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*80)
print("✅ ALL DEMOS COMPLETED SUCCESSFULLY!")
print("="*80)

print(f"\n📁 Output directory: {OUTPUT_DIR.absolute()}")
print(f"\n📄 Created files:")
for file in sorted(OUTPUT_DIR.glob("*.csv")):
    size = file.stat().st_size
    with open(file, 'r') as f:
        line_count = sum(1 for _ in f)
    print(f"   ✓ {file.name:<30} ({size:>6} bytes, {line_count:>3} lines)")

print("\n" + "="*80)
print("💡 TIP: You can open these CSV files in Excel, Google Sheets, or any")
print("   spreadsheet application to view the data in table format.")
print("="*80)
