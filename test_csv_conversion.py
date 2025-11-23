"""
Test script for CSV conversion functions using dummy data.

This script demonstrates all three CSV conversion methods:
1. export_cv_review_to_csv() - Direct file export
2. build_csv() - Text generation (watsonx tool)
3. build_batch_review_result() - Structured packaging

Run: python test_csv_conversion.py
"""

import json
import sys
import os
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

# Import CSV conversion functions
from cv_review_excel import export_cv_review_to_csv
from sheet_manager_tools import build_csv
from batch_result_utils import build_batch_review_result

# Create output directory
OUTPUT_DIR = Path("output/csv_tests")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_dummy_data():
    """Load dummy data from JSON file."""
    with open("dummy-csv-data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def test_1_export_cv_review():
    """Test 1: export_cv_review_to_csv() - Direct file export"""
    print("\n" + "="*80)
    print("TEST 1: export_cv_review_to_csv() - Direct File Export")
    print("="*80)
    
    data = load_dummy_data()
    candidates = data["cv_review_candidates"]
    
    output_path = OUTPUT_DIR / "cv_review_results.csv"
    
    result_path = export_cv_review_to_csv(candidates, str(output_path))
    
    print(f"✅ CSV file created: {result_path}")
    print(f"📊 Exported {len(candidates)} candidates")
    
    # Read and display first few lines
    with open(result_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[:4]  # Header + 3 data rows
        print("\n📄 Preview (first 3 rows):")
        for line in lines:
            print("   ", line.strip())
    
    return result_path

def test_2_build_csv_from_dicts():
    """Test 2a: build_csv() with list of dictionaries"""
    print("\n" + "="*80)
    print("TEST 2a: build_csv() - From List of Dictionaries")
    print("="*80)
    
    data = load_dummy_data()
    candidates = data["cv_review_candidates"]
    
    # Prepare simplified candidate data
    simple_candidates = []
    for c in candidates:
        simple_candidates.append({
            "name": c.get("name", "N/A"),
            "email": c.get("email", "N/A"),
            "final_score": c["scores"]["final_score"],
            "decision": c["auto_decision"],
            "unreadable": c["unreadable"]
        })
    
    result = build_csv(
        rows=simple_candidates,
        file_name="candidates_simple.csv",
        preview_rows=3
    )
    
    print(f"✅ CSV generated successfully")
    print(f"📊 Headers: {result['headers']}")
    print(f"📊 Row count: {result['row_count']}")
    print(f"📊 File type: {result['file_type']}")
    
    print("\n📄 Preview table:")
    for i, row in enumerate(result['preview_table']):
        print(f"   Row {i}: {row}")
    
    print("\n📝 CSV Text (first 300 chars):")
    print("   " + result['csv_text'][:300] + "...")
    
    # Save CSV text to file
    csv_file = OUTPUT_DIR / "candidates_simple.csv"
    csv_file.write_text(result['csv_text'], encoding='utf-8')
    print(f"\n💾 Saved to: {csv_file}")
    
    return result

def test_2b_build_csv_from_lists():
    """Test 2b: build_csv() with list of lists"""
    print("\n" + "="*80)
    print("TEST 2b: build_csv() - From List of Lists with Headers")
    print("="*80)
    
    data = load_dummy_data()
    
    # Use example table data
    headers = data["simple_table_examples"]["example_2_headers"]
    rows = data["simple_table_examples"]["example_2_list_of_lists"]
    
    result = build_csv(
        rows=rows,
        headers=headers,
        file_name="employees_list.csv",
        preview_rows=10
    )
    
    print(f"✅ CSV generated successfully")
    print(f"📊 Headers: {result['headers']}")
    print(f"📊 Row count: {result['row_count']}")
    
    print("\n📝 Full CSV Text:")
    print(result['csv_text'])
    
    # Save to file
    csv_file = OUTPUT_DIR / "employees_list.csv"
    csv_file.write_text(result['csv_text'], encoding='utf-8')
    print(f"💾 Saved to: {csv_file}")
    
    return result

def test_2c_build_csv_products():
    """Test 2c: build_csv() with product data"""
    print("\n" + "="*80)
    print("TEST 2c: build_csv() - Product Inventory Example")
    print("="*80)
    
    data = load_dummy_data()
    products = data["simple_table_examples"]["example_1_list_of_dicts"]
    
    result = build_csv(
        rows=products,
        file_name="products.csv",
        preview_rows=10
    )
    
    print(f"✅ CSV generated successfully")
    print("\n📝 CSV Text:")
    print(result['csv_text'])
    
    # Save to file
    csv_file = OUTPUT_DIR / "products.csv"
    csv_file.write_text(result['csv_text'], encoding='utf-8')
    print(f"💾 Saved to: {csv_file}")
    
    return result

def test_3_batch_review_result():
    """Test 3: build_batch_review_result() - Complete workflow"""
    print("\n" + "="*80)
    print("TEST 3: build_batch_review_result() - Complete Review Package")
    print("="*80)
    
    data = load_dummy_data()
    candidates = data["cv_review_candidates"]
    rubric = data["rubric_info"]
    
    result = build_batch_review_result(rubric, candidates)
    
    print(f"✅ Batch review result generated")
    print(f"\n📋 Rubric Info:")
    print(f"   Role: {result['rubric_info']['role_title']}")
    print(f"   Threshold: {result['rubric_info']['threshold_score']}")
    print(f"   Budget: {result['rubric_info']['salary_budget']}")
    
    print(f"\n📊 Supervisor Summary:")
    print(f"   {result['supervisor_summary']['text']}")
    
    print(f"\n⚠️ Suggested Disqualifications:")
    disqual = result['supervisor_summary']['suggested_disqualifications']
    print(f"   Below threshold: {len(disqual['below_threshold'])} candidates")
    print(f"   Outside budget: {len(disqual['outside_budget'])} candidates")
    print(f"   Unreadable: {len(disqual['unreadable'])} files")
    
    if disqual['below_threshold']:
        print(f"   - Below threshold: {disqual['below_threshold']}")
    if disqual['unreadable']:
        print(f"   - Unreadable files: {disqual['unreadable']}")
    
    # Export excel_export data to CSV
    print(f"\n📊 Excel Export Section:")
    excel_data = result['excel_export']
    print(f"   Columns: {excel_data['columns']}")
    print(f"   Rows: {len(excel_data['rows'])}")
    
    # Convert to CSV using standard csv module
    import csv
    csv_file = OUTPUT_DIR / "batch_review_export.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(excel_data['columns'])
        writer.writerows(excel_data['rows'])
    
    print(f"💾 Excel export saved to: {csv_file}")
    
    # Also save full JSON result
    json_file = OUTPUT_DIR / "batch_review_full.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print(f"💾 Full JSON saved to: {json_file}")
    
    return result

def test_4_applicant_tracker():
    """Test 4: Convert applicant tracker data to CSV"""
    print("\n" + "="*80)
    print("TEST 4: Applicant Tracker CSV Generation")
    print("="*80)
    
    data = load_dummy_data()
    tracker_data = data["applicant_tracker_data"]
    
    result = build_csv(
        rows=tracker_data,
        file_name="applicant_tracker.csv",
        preview_rows=3
    )
    
    print(f"✅ Applicant tracker CSV generated")
    print(f"📊 Tracking {result['row_count']} candidates")
    print(f"\n📄 Preview (first 3 rows):")
    for i, row in enumerate(result['preview_table'][:4]):
        if i == 0:
            print(f"   HEADERS: {row}")
        else:
            print(f"   Row {i}: {row}")
    
    # Save to file
    csv_file = OUTPUT_DIR / "applicant_tracker.csv"
    csv_file.write_text(result['csv_text'], encoding='utf-8')
    print(f"\n💾 Saved to: {csv_file}")
    
    # Also show some statistics
    accepted = sum(1 for r in tracker_data if r['Status'] == 'Accepted')
    pending = sum(1 for r in tracker_data if r['Status'] == 'Pending')
    rejected = sum(1 for r in tracker_data if r['Status'] == 'Rejected')
    
    print(f"\n📈 Statistics:")
    print(f"   ✅ Accepted: {accepted}")
    print(f"   ⏳ Pending: {pending}")
    print(f"   ❌ Rejected: {rejected}")
    
    return result

def test_5_interview_summary():
    """Test 5: Create interview summary CSV"""
    print("\n" + "="*80)
    print("TEST 5: Interview Summary CSV")
    print("="*80)
    
    data = load_dummy_data()
    interviews = data["interview_transcripts"]
    
    # Extract summary data
    summary_data = []
    for interview in interviews:
        assessment = interview['assessment']
        summary_data.append({
            "Candidate": interview['candidate_name'],
            "Date": interview['interview_date'],
            "Duration_min": interview['duration_minutes'],
            "Technical": assessment['technical_score'],
            "Communication": assessment['communication_score'],
            "Cultural_Fit": assessment['cultural_fit_score'],
            "Problem_Solving": assessment['problem_solving_score'],
            "Final_Score": assessment['final_score'],
            "Recommendation": assessment['recommendation']
        })
    
    result = build_csv(
        rows=summary_data,
        file_name="interview_summary.csv",
        preview_rows=10
    )
    
    print(f"✅ Interview summary CSV generated")
    print(f"📊 {result['row_count']} interviews")
    
    print("\n📝 CSV Content:")
    print(result['csv_text'])
    
    # Save to file
    csv_file = OUTPUT_DIR / "interview_summary.csv"
    csv_file.write_text(result['csv_text'], encoding='utf-8')
    print(f"💾 Saved to: {csv_file}")
    
    return result

def main():
    """Run all CSV conversion tests"""
    print("\n" + "🚀 "*20)
    print("CSV CONVERSION FUNCTIONS - DUMMY DATA TESTS")
    print("🚀 "*20)
    
    try:
        # Test 1: Direct file export
        test_1_export_cv_review()
        
        # Test 2: build_csv with different formats
        test_2_build_csv_from_dicts()
        test_2b_build_csv_from_lists()
        test_2c_build_csv_products()
        
        # Test 3: Complete batch review
        test_3_batch_review_result()
        
        # Test 4: Applicant tracker
        test_4_applicant_tracker()
        
        # Test 5: Interview summary
        test_5_interview_summary()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"\n📁 All output files saved to: {OUTPUT_DIR.absolute()}")
        
        # List all created files
        print(f"\n📄 Created files:")
        for file in sorted(OUTPUT_DIR.glob("*")):
            size = file.stat().st_size
            print(f"   - {file.name} ({size} bytes)")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
