# CSV Conversion Functions in HireIT-AI

This document lists all functions that can convert tables/data to CSV format in the HireIT-AI system.

---

## 1. `export_cv_review_to_csv()` 
**File:** `tools/cv_review_excel.py`

### Purpose
Export CV review results to a CSV file.

### Function Signature
```python
def export_cv_review_to_csv(
    candidates: List[Dict],
    output_path: str = "cv_review_results.csv"
) -> str
```

### Parameters
- **candidates** (List[Dict]): List of candidate profile objects with:
  - `file_name` (optional)
  - `name`
  - `scores.final_score` or `final_score`
  - `auto_decision`
  - `worth_range` (dict with: currency, min, max)
  - `unreadable` (bool, optional)
  - `unreadable_reason` (str, optional)

- **output_path** (str): Path to the output CSV file (default: "cv_review_results.csv")

### Returns
- **str**: Absolute path of the created CSV file

### CSV Headers
```
file_name, name, final_score, auto_decision, worth_currency, worth_min, worth_max, unreadable, unreadable_reason
```

### Example Usage
```python
candidates = [
    {
        "file_name": "john_doe_cv.pdf",
        "name": "John Doe",
        "final_score": 8.5,
        "auto_decision": "pass",
        "worth_range": {
            "currency": "USD",
            "min": 80000,
            "max": 100000
        },
        "unreadable": False,
        "unreadable_reason": ""
    }
]

csv_path = export_cv_review_to_csv(candidates, "output/results.csv")
print(f"CSV created at: {csv_path}")
```

### Features
- ✅ Automatically creates directory if it doesn't exist
- ✅ Handles nested score objects
- ✅ UTF-8 encoding
- ✅ Returns absolute path
- ✅ Flattens worth_range dict to separate columns

---

## 2. `build_csv()` (watsonx Tool)
**File:** `tools/sheet_manager_tools.py`

### Purpose
Build a CSV from rows and headers (watsonx Orchestrate tool).

### Function Signature
```python
@tool
def build_csv(
    rows: Union[str, List[Dict[str, Any]], List[List[Any]]],
    headers: Union[str, List[str], None] = None,
    file_name: str = "output.csv",
    preview_rows: int = 5,
) -> Dict[str, Any]
```

### Parameters
- **rows**: Can be:
  - JSON string of list/dict
  - List of dictionaries (each dict is a row)
  - List of lists (each inner list is a row)
  
- **headers**: Column headers (optional if rows are dicts)
  - JSON string of list
  - List of strings
  - None (auto-detected from dict keys)

- **file_name** (str): Name for the CSV file (default: "output.csv")
- **preview_rows** (int): Number of rows to show in preview (default: 5)

### Returns
Dictionary with:
```python
{
    "ok": True,
    "file_name": "output.csv",
    "file_type": "csv",
    "headers": [...],
    "rows": [...],
    "row_count": 10,
    "preview_table": [[headers], [row1], [row2], ...],
    "csv_text": "header1,header2\nvalue1,value2\n...",
    "meta": {"warnings": []}
}
```

### Key Features
- ✅ **Returns CSV as text** (no file I/O) - Can be used in JSON responses
- ✅ Flexible input format (string, dict, list)
- ✅ Auto-normalizes different data structures
- ✅ Includes preview for validation
- ✅ Returns full CSV text in `csv_text` field
- ✅ Uses `csv.DictWriter` for proper escaping

### Example Usage

**Example 1: From List of Dicts**
```python
rows = [
    {"name": "Alice", "score": 9.5, "status": "pass"},
    {"name": "Bob", "score": 7.2, "status": "borderline"},
]

result = build_csv(rows, file_name="candidates.csv")
print(result["csv_text"])
# Output:
# name,score,status
# Alice,9.5,pass
# Bob,7.2,borderline
```

**Example 2: From List of Lists with Headers**
```python
headers = ["Name", "Email", "Phone"]
rows = [
    ["John Doe", "john@example.com", "555-1234"],
    ["Jane Smith", "jane@example.com", "555-5678"]
]

result = build_csv(rows, headers=headers, file_name="contacts.csv")
print(result["csv_text"])
```

**Example 3: From JSON String**
```python
rows_json = '[{"product": "Laptop", "price": 999}, {"product": "Mouse", "price": 25}]'

result = build_csv(rows_json, file_name="products.csv")
# Automatically parses JSON and creates CSV
```

### Use Cases in watsonx
- Export agent results to CSV format
- Generate downloadable reports
- Create structured data for import
- Build applicant tracker files
- Format review results

---

## 3. `build_batch_review_result()` (Excel Export Section)
**File:** `tools/batch_result_utils.py`

### Purpose
Package CV review results into standardized JSON with Excel/CSV export section.

### Function Signature
```python
def build_batch_review_result(
    rubric_info: Dict[str, Any],
    candidates: List[Dict[str, Any]]
) -> Dict[str, Any]
```

### Parameters
- **rubric_info** (dict): Rubric summary with:
  - `role_title`: Job title
  - `threshold_score`: Minimum passing score
  - `salary_budget`: {currency, min, max}

- **candidates** (list): Candidate evaluation results

### Returns
Dictionary with `excel_export` section:
```python
{
    "rubric_info": {...},
    "candidates": [...],
    "excel_export": {
        "columns": ["file_name", "name", "final_score", ...],
        "rows": [
            ["john_cv.pdf", "John Doe", 8.5, "pass", 80000, 100000, False, ""],
            ...
        ]
    },
    "supervisor_summary": {
        "text": "Reviewed 10 candidates...",
        "suggested_disqualifications": {
            "below_threshold": ["candidate1.pdf", ...],
            "outside_budget": ["candidate2.pdf", ...],
            "unreadable": ["candidate3.pdf", ...]
        }
    }
}
```

### Excel Export Columns
```
file_name, name, final_score, auto_decision, worth_min, worth_max, unreadable, unreadable_reason
```

### Features
- ✅ Structured data ready for CSV conversion
- ✅ Includes supervisor summary
- ✅ Identifies problematic candidates
- ✅ Budget analysis
- ✅ Threshold filtering
- ✅ Unreadable file tracking

### Example Usage
```python
rubric = {
    "role_title": "Backend Engineer",
    "threshold_score": 7.0,
    "salary_budget": {
        "currency": "USD",
        "min": 70000,
        "max": 90000
    }
}

candidates = [
    {
        "file_name": "alice_cv.pdf",
        "name": "Alice Johnson",
        "scores": {"final_score": 8.5},
        "auto_decision": "pass",
        "worth_range": {"currency": "USD", "min": 75000, "max": 85000},
        "evidence_bullets": ["Strong backend experience", "Good communication"],
        "unreadable": False
    }
]

result = build_batch_review_result(rubric, candidates)

# Access Excel export data
columns = result["excel_export"]["columns"]
rows = result["excel_export"]["rows"]

# Can be converted to CSV using csv.writer
import csv
with open("review_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)
```

---

## 4. Text Parser CSV Reading (Bonus)
**File:** `tools/text_parser_tools.py`

### Purpose
Parse CSV files (reads CSV, not creates)

### CSV Detection
```python
# Line 109-110: Content-Type detection
if "csv" in ct:
    return "csv"

# Line 313: CSV parsing logic
elif file_type == "csv":
    # CSV parsing implementation
```

### Supported Operations
- ✅ Detect CSV files by content-type
- ✅ Parse CSV into structured data
- ✅ Handle various CSV formats
- ✅ Part of multi-format parser (txt/md/csv/json/pdf/xlsx)

---

## Comparison Table

| Function | File | Type | Output | Use Case |
|----------|------|------|--------|----------|
| `export_cv_review_to_csv()` | cv_review_excel.py | Standalone | Physical CSV file | Export CV reviews to disk |
| `build_csv()` | sheet_manager_tools.py | watsonx Tool | CSV text + metadata | Generate CSV in agent responses |
| `build_batch_review_result()` | batch_result_utils.py | Utility | Excel export structure | Package review data for export |
| Text Parser | text_parser_tools.py | Parser | Parsed CSV data | Read/parse existing CSV files |

---

## Recommended Usage by Scenario

### Scenario 1: Export CV Reviews to File
**Use:** `export_cv_review_to_csv()`
```python
csv_path = export_cv_review_to_csv(candidates, "results/cv_reviews.csv")
```

### Scenario 2: Return CSV in Agent Response
**Use:** `build_csv()` (watsonx tool)
```python
result = build_csv(candidates_list, file_name="reviews.csv")
# Agent can return result["csv_text"] to user
```

### Scenario 3: Package Complete Review Results
**Use:** `build_batch_review_result()` → then convert to CSV
```python
batch_result = build_batch_review_result(rubric, candidates)
excel_data = batch_result["excel_export"]
# Convert to CSV using standard csv module
```

### Scenario 4: Read CSV Files
**Use:** Text Parser tools
```python
# Automatically detects and parses CSV files
parsed_data = parse_file("data.csv")
```

---

## Integration with Agents

### Reviewer Agent
Uses `export_cv_review_to_csv()` and `build_batch_review_result()` to:
1. Score candidates
2. Package results
3. Export to CSV for Excel import

### Sheet Manager Agent
Uses `build_csv()` to:
1. Create applicant tracker templates
2. Export Google Sheets data
3. Generate downloadable reports

### DataHub Agent
Uses all CSV functions to:
1. Import/export data
2. Transform between formats
3. Store results in Google Drive

---

## Code Examples

### Complete Example: Full Workflow
```python
from tools.cv_review_excel import export_cv_review_to_csv
from tools.batch_result_utils import build_batch_review_result
from tools.sheet_manager_tools import build_csv

# Step 1: Review candidates (done by Reviewer Agent)
candidates = [
    {
        "file_name": "candidate_1.pdf",
        "name": "John Doe",
        "final_score": 8.5,
        "auto_decision": "pass",
        "worth_range": {"currency": "USD", "min": 80000, "max": 95000},
        "evidence_bullets": ["5 years Python", "AWS certified"],
        "unreadable": False
    },
    {
        "file_name": "candidate_2.pdf",
        "name": "Jane Smith",
        "final_score": 6.2,
        "auto_decision": "borderline",
        "worth_range": {"currency": "USD", "min": 70000, "max": 85000},
        "evidence_bullets": ["3 years experience", "Good communication"],
        "unreadable": False
    }
]

# Step 2: Package with rubric info
rubric = {
    "role_title": "Senior Backend Engineer",
    "threshold_score": 7.0,
    "salary_budget": {"currency": "USD", "min": 75000, "max": 100000}
}

batch_result = build_batch_review_result(rubric, candidates)

# Step 3: Export to CSV (Option A - Direct file)
csv_file_path = export_cv_review_to_csv(
    candidates, 
    "output/backend_engineer_reviews.csv"
)
print(f"✅ CSV exported to: {csv_file_path}")

# Step 4: Export to CSV (Option B - As text for agent response)
csv_result = build_csv(
    candidates, 
    file_name="backend_reviews.csv",
    preview_rows=2
)
print(f"✅ CSV text ready: {len(csv_result['csv_text'])} bytes")
print(f"Preview: {csv_result['preview_table']}")

# Step 5: Access structured data
print(f"\n📊 Summary: {batch_result['supervisor_summary']['text']}")
print(f"Below threshold: {batch_result['supervisor_summary']['suggested_disqualifications']['below_threshold']}")
```

---

## Dependencies

All CSV functions use Python's built-in `csv` module:
```python
import csv
from io import StringIO
```

No external dependencies required! ✅

---

## Best Practices

1. **Use `build_csv()` for watsonx agents** - Returns data in agent-friendly format
2. **Use `export_cv_review_to_csv()` for file output** - Creates actual CSV files
3. **Use `build_batch_review_result()` for complex reviews** - Includes analytics
4. **Always specify UTF-8 encoding** - Prevents character issues
5. **Validate data before CSV conversion** - Ensure all required fields exist
6. **Handle nested dictionaries** - Flatten before CSV export (like worth_range)

---

## Summary

The HireIT-AI system has **3 main CSV conversion functions**:

1. **`export_cv_review_to_csv()`** - Direct file export ✅
2. **`build_csv()`** - Flexible text generation (watsonx tool) ✅
3. **`build_batch_review_result()`** - Structured data packaging ✅

All functions handle different aspects of the recruitment workflow and can work together to provide complete CSV export capabilities.

**Last Updated:** November 23, 2025
