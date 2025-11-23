"""Test the CV review export functionality"""

from cv_review_excel import create_review_summary_from_text

# Sample agent response (like what Reviewer Agent would output)
sample_response = """
📊 CANDIDATE REVIEW RESULTS

Job: Senior Backend Developer
Total Candidates: 5

🟢 RECOMMENDED (2 candidates)

1. **John Doe** - Score: 9/10
   - Skills: Python, Django, PostgreSQL, Docker, AWS
   - Experience: 6 years
   - Why: Strong match with all must-have skills and relevant cloud experience. Proven track record with Django and PostgreSQL at scale.
   - Missing: None significant

2. **Jane Smith** - Score: 8/10
   - Skills: Python, Flask, MySQL, Kubernetes
   - Experience: 5 years
   - Why: Solid backend experience with slightly different stack but highly transferable skills. Strong DevOps background.
   - Missing: No AWS experience (has GCP instead)

🟡 CONSIDER (2 candidates)

3. **Bob Wilson** - Score: 6/10
   - Skills: Python, FastAPI, MongoDB
   - Experience: 3 years
   - Why: Good Python skills but below preferred experience level. No exposure to PostgreSQL.
   - Missing: PostgreSQL, cloud platform experience, only 3 years vs 5+ required

4. **Alice Johnson** - Score: 5.5/10
   - Skills: Python, Django, SQLite
   - Experience: 2 years
   - Why: Junior developer with Django basics but lacks production-scale experience
   - Missing: PostgreSQL, AWS, insufficient years of experience

🔴 NOT RECOMMENDED (1 candidate)

5. **Charlie Brown** - Score: 3/10
   - Skills: JavaScript, Node.js, MongoDB
   - Experience: 4 years
   - Why: Wrong tech stack entirely. No Python experience mentioned.
   - Missing: All required Python and PostgreSQL skills
"""

if __name__ == "__main__":
    result = create_review_summary_from_text(
        agent_response_text=sample_response,
        output_csv_path="test_review_summary.csv"
    )
    
    print("✅ CSV Export Successful!")
    print(f"📄 CSV Path: {result['csv_path']}")
    print(f"📊 Statistics:")
    print(f"   Total: {result['total_candidates']}")
    print(f"   🟢 Recommended: {result['recommended']}")
    print(f"   🟡 Consider: {result['consider']}")
    print(f"   🔴 Reject: {result['reject']}")
    print("\n📋 Candidates parsed:")
    for c in result['candidates']:
        print(f"   - {c['name']}: {c['final_score']}/10 ({c['auto_decision']})")
