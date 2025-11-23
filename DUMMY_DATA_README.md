# Dummy Data for CSV Conversion Testing

This directory contains dummy data and demo scripts for testing the CSV conversion functions in HireIT-AI.

## Files

### 📄 Data Files

1. **`dummy-csv-data.json`** - Complete dummy data set including:
   - 6 CV review candidates (with scores, evidence, decisions)
   - Rubric information for Mid-Level Backend Engineer role
   - 6 applicant tracker entries with pipeline stages
   - 2 complete interview transcripts with assessments
   - Simple table examples (products, employees, etc.)
   - Job listing intake template

### 🐍 Demo Scripts

2. **`demo_csv_simple.py`** ⭐ RECOMMENDED
   - Simple, standalone demonstration
   - Creates 7 different CSV files from dummy data
   - Uses only Python standard library (no custom imports)
   - **Run:** `python demo_csv_simple.py`

3. **`test_csv_conversion.py`** (Advanced)
   - Comprehensive test suite
   - Tests all three CSV conversion functions
   - Requires tools directory in Python path
   - **Run:** `python test_csv_conversion.py`

## Quick Start

### Run the Demo

```bash
# Simple demo (recommended)
python demo_csv_simple.py
```

This will create CSV files in `output/demo/` directory:
- ✅ `cv_review_results.csv` - Candidate review results
- ✅ `applicant_tracker.csv` - Recruitment pipeline tracker
- ✅ `interview_summary.csv` - Interview assessment scores
- ✅ `products.csv` - Simple product inventory
- ✅ `employees.csv` - Employee contact list
- ✅ `employee_records.csv` - Detailed employee records
- ✅ `batch_review.csv` - Complete batch review export

## Generated CSV Files

### 1. CV Review Results (`cv_review_results.csv`)

**Columns:** File Name, Name, Email, Experience Years, Final Score, Decision, Min Salary, Max Salary, Unreadable

**Sample Data:**
```csv
File Name,Name,Email,Experience Years,Final Score,Decision,Min Salary,Max Salary,Unreadable
john_doe_cv.pdf,John Doe,john.doe@email.com,5,8.4,pass,85000,105000,False
jane_smith_cv.pdf,Jane Smith,jane.smith@email.com,3.5,7.0,borderline,70000,85000,False
michael_chen_cv.pdf,Michael Chen,michael.chen@email.com,8,9.2,pass,110000,135000,False
```

**Use Case:** Export CV review results for hiring managers

---

### 2. Applicant Tracker (`applicant_tracker.csv`)

**Columns:** Name, Email, Phone, Submitted, Filtered, Interviewed, Tested, Status, Notes

**Sample Data:**
```csv
Name,Email,Phone,Submitted,Filtered,Interviewed,Tested,Status,Notes
John Doe,john.doe@email.com,+1-555-0101,2025-11-01,2025-11-05,2025-11-12,2025-11-15,Accepted,Excellent candidate
Jane Smith,jane.smith@email.com,+1-555-0102,2025-11-02,2025-11-06,2025-11-13,,Pending,Awaiting second interview
```

**Use Case:** Track candidates through recruitment pipeline

**Statistics:**
- ✅ Accepted: 2 candidates
- ⏳ Pending: 3 candidates  
- ❌ Rejected: 1 candidate

---

### 3. Interview Summary (`interview_summary.csv`)

**Columns:** Candidate, Date, Duration (min), Technical Score, Communication Score, Cultural Fit Score, Problem Solving Score, Final Score, Recommendation

**Sample Data:**
```csv
Candidate,Date,Duration (min),Technical Score,Communication Score,Cultural Fit Score,Problem Solving Score,Final Score,Recommendation
John Doe,2025-11-12,45,9.0,8.5,9.0,8.5,8.75,Strong Hire
Jane Smith,2025-11-13,40,6.5,7.0,7.5,6.0,6.75,Maybe - Second Interview
```

**Use Case:** Summarize interview performance across dimensions

---

### 4. Products (`products.csv`)

**Columns:** Product, Price, Stock

**Sample Data:**
```csv
Product,Price,Stock
Laptop,999,50
Mouse,25,200
Keyboard,75,150
```

**Use Case:** Simple product inventory example

---

### 5. Employees (`employees.csv`)

**Columns:** Name, Email, Department

**Sample Data:**
```csv
Name,Email,Department
Alice Johnson,alice@example.com,Engineering
Bob Smith,bob@example.com,Marketing
Carol White,carol@example.com,Sales
```

**Use Case:** Basic employee contact list

---

### 6. Employee Records (`employee_records.csv`)

**Columns:** ID, Name, Department, Salary, Hire_Date

**Sample Data:**
```csv
ID,Name,Department,Salary,Hire_Date
E001,John Doe,IT,85000,2020-03-15
E002,Jane Smith,HR,72000,2019-07-22
E003,Mike Johnson,IT,95000,2018-01-10
E004,Sarah Williams,Finance,88000,2021-05-03
```

**Use Case:** Detailed HR records export

---

### 7. Batch Review (`batch_review.csv`)

**Columns:** File, Name, Final Score, Decision, Worth Min, Worth Max, Unreadable, Reason

**Sample Data:**
```csv
File,Name,Final Score,Decision,Worth Min,Worth Max,Unreadable,Reason
john_doe_cv.pdf,John Doe,8.4,pass,85000,105000,False,
jane_smith_cv.pdf,Jane Smith,7.0,borderline,70000,85000,False,
corrupted_file_123.pdf,N/A,0.0,fail,0,0,True,PDF parsing error
```

**Statistics:**
- Total Candidates: 6
- Pass: 3
- Borderline: 1
- Fail: 2
- Unreadable: 1
- Average Score: 7.52
- Threshold: 6.50

**Use Case:** Complete batch review with analytics

---

## Dummy Data Overview

### Candidates Profile Summary

| Name | Experience | Score | Decision | Status |
|------|------------|-------|----------|--------|
| **John Doe** | 5 years | 8.4 | Pass | ✅ Accepted |
| **Jane Smith** | 3.5 years | 7.0 | Borderline | ⏳ Pending |
| **Michael Chen** | 8 years | 9.2 | Pass | ✅ Accepted |
| **Sarah Wilson** | 2 years | 5.4 | Fail | ❌ Rejected |
| **David Garcia** | 6 years | 7.6 | Pass | ⏳ Pending |
| **Corrupted File** | N/A | 0.0 | Fail | N/A |

### Rubric Details

**Role:** Mid-Level Backend Engineer  
**Department:** Engineering  
**Threshold Score:** 6.5  
**Salary Budget:** $75,000 - $100,000 USD

**Must-Have Skills:**
- Python
- REST API development
- SQL databases
- Git version control
- Unit testing

**Nice-to-Have Skills:**
- Docker, Kubernetes
- AWS or cloud platforms
- GraphQL, Redis
- Microservices architecture

**Experience:** 3-7 years  
**Education:** Bachelor's degree in Computer Science or related field

---

## Using the Dummy Data

### In Python Scripts

```python
import json

# Load dummy data
with open('dummy-csv-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access candidates
candidates = data['cv_review_candidates']
for candidate in candidates:
    print(f"{candidate['name']}: {candidate['scores']['final_score']}")

# Access rubric
rubric = data['rubric_info']
print(f"Role: {rubric['role_title']}")
print(f"Threshold: {rubric['threshold_score']}")

# Access tracker data
tracker = data['applicant_tracker_data']
print(f"Total applicants: {len(tracker)}")
```

### With CSV Conversion Functions

```python
from tools.cv_review_excel import export_cv_review_to_csv
from tools.sheet_manager_tools import build_csv
from tools.batch_result_utils import build_batch_review_result

# Method 1: Direct file export
csv_path = export_cv_review_to_csv(
    candidates, 
    "output/results.csv"
)

# Method 2: Text generation (watsonx tool)
result = build_csv(
    rows=candidates,
    file_name="results.csv",
    preview_rows=5
)
print(result['csv_text'])

# Method 3: Complete batch review
batch_result = build_batch_review_result(rubric, candidates)
print(batch_result['supervisor_summary']['text'])
```

---

## Output Structure

```
output/
└── demo/
    ├── cv_review_results.csv       (561 bytes, 7 lines)
    ├── applicant_tracker.csv       (929 bytes, 7 lines)
    ├── interview_summary.csv       (264 bytes, 3 lines)
    ├── products.csv                (67 bytes, 4 lines)
    ├── employees.csv               (142 bytes, 4 lines)
    ├── employee_records.csv        (194 bytes, 5 lines)
    └── batch_review.csv            (481 bytes, 7 lines)
```

---

## Testing Scenarios

### Scenario 1: Happy Path
- **Candidate:** John Doe, Michael Chen, David Garcia
- **Score:** Above threshold (≥6.5)
- **Decision:** Pass
- **Expected:** Accepted for next round

### Scenario 2: Borderline Case
- **Candidate:** Jane Smith
- **Score:** Exactly at threshold (7.0)
- **Decision:** Borderline
- **Expected:** Second interview or technical assessment

### Scenario 3: Below Threshold
- **Candidate:** Sarah Wilson
- **Score:** Below threshold (5.4)
- **Decision:** Fail
- **Expected:** Rejected

### Scenario 4: Unreadable File
- **Candidate:** corrupted_file_123.pdf
- **Score:** 0.0 (auto-fail)
- **Decision:** Fail
- **Expected:** Manual review or request resubmission

### Scenario 5: Overqualified
- **Candidate:** Michael Chen (PhD, 8 years)
- **Score:** 9.2
- **Salary:** $110k-$135k (above budget)
- **Expected:** Consider for senior role

---

## Integration with HireIT-AI

### Agents Using This Data

1. **Job Listing Agent** - Uses job listing intake template
2. **Reviewer Agent** - Uses CV candidates and rubric for scoring
3. **Interviewer Agent** - Uses interview transcripts for assessment
4. **Applicant Tracker Agent** - Uses tracker data for pipeline management
5. **DataHub Agent** - Exports data to CSV formats

### Workflow Example

```
1. Load rubric → Reviewer Agent
2. Score CVs → Generate cv_review_results.csv
3. Update tracker → applicant_tracker.csv
4. Conduct interviews → interview_summary.csv
5. Final decision → batch_review.csv
```

---

## Requirements

- Python 3.7+
- Standard library only (no external packages required for demo)
- Optional: `tools/` directory for full test suite

---

## Tips

1. **Open CSVs in Excel/Google Sheets** for better visualization
2. **Modify dummy data** in `dummy-csv-data.json` for custom scenarios
3. **Add more candidates** to test larger datasets
4. **Test edge cases** like missing fields, special characters, etc.
5. **Use as API test data** for frontend/backend integration testing

---

## Next Steps

1. ✅ Run `python demo_csv_simple.py`
2. ✅ Review generated CSV files in `output/demo/`
3. ✅ Modify dummy data for your specific needs
4. ✅ Integrate with watsonx agents
5. ✅ Deploy to production with real data

---

## Support

For questions or issues:
- See `CSV_CONVERSION_FUNCTIONS.md` for function documentation
- See `FUNCTIONAL_REQUIREMENTS.md` for system overview
- Check `tools/` directory for implementation details

---

**Last Updated:** November 23, 2025  
**Status:** ✅ Fully Functional  
**Test Coverage:** 7 CSV scenarios
