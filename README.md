# AI-Powered Employee Onboarding System

A Streamlit app that generates a complete onboarding package from an employee's
name, role and department, using rule-based logic only (no external APIs).

## Generated output

1. Professional welcome email
2. Structured 7-day onboarding plan
3. Required documents checklist
4. IT access checklist (based on department and role level)
5. FAQs for new employees
6. Training resources (based on department and role)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install streamlit
```

## Run

```bash
streamlit run app.py
```

Then open http://localhost:8501, fill in the form and click **Generate Onboarding Package**.
