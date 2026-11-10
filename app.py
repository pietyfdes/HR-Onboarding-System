"""AI-Powered Employee Onboarding System (rule-based, no external APIs)."""

from datetime import date

import streamlit as st

# --------------------------------------------------------------------------
# Content data
# --------------------------------------------------------------------------

DEPARTMENT_IT_ACCESS = {
    "Engineering": [
        "GitHub / GitLab organization access",
        "CI/CD pipeline (Jenkins / GitHub Actions) access",
        "Cloud console (AWS / Azure / GCP) - sandbox environment",
        "Jira and Confluence (engineering spaces)",
        "Code editor / IDE licenses",
        "VPN and SSH key provisioning",
        "Monitoring tools (Datadog / Grafana / Sentry)",
    ],
    "Human Resources": [
        "HRIS platform (Workday / BambooHR)",
        "Applicant tracking system (ATS)",
        "Payroll system (read access)",
        "Employee records and document management",
        "Learning management system (admin)",
    ],
    "Finance": [
        "ERP / accounting system (SAP / NetSuite)",
        "Expense management platform",
        "Banking portal (view-only until approved)",
        "Financial reporting and BI dashboards",
        "Secure shared drive for finance documents",
    ],
    "Marketing": [
        "CMS and website analytics (Google Analytics)",
        "Social media management tools",
        "Email marketing platform",
        "Design tools (Adobe Creative Cloud / Canva)",
        "CRM (marketing view)",
    ],
    "Sales": [
        "CRM (Salesforce / HubSpot)",
        "Sales engagement and dialer tools",
        "Proposal and contract tools",
        "Sales analytics dashboards",
        "Shared sales collateral drive",
    ],
    "Operations": [
        "ERP / inventory management system",
        "Project management tool (Asana / Jira)",
        "Logistics and vendor portals",
        "Operations dashboards and reporting",
    ],
    "Customer Support": [
        "Helpdesk platform (Zendesk / Freshdesk)",
        "Knowledge base (editor access)",
        "Live chat and telephony tools",
        "CRM (customer view)",
        "Support analytics dashboards",
    ],
    "Product": [
        "Jira / Linear product backlog",
        "Roadmapping tool (Productboard / Aha!)",
        "Product analytics (Amplitude / Mixpanel)",
        "Design collaboration (Figma)",
        "Confluence / Notion product documentation",
    ],
}

COMMON_IT_ACCESS = [
    "Company email and calendar",
    "Single sign-on (SSO) and multi-factor authentication",
    "Corporate chat (Slack / Microsoft Teams)",
    "Video conferencing account",
    "Laptop, peripherals and device management enrollment",
    "Password manager account",
    "Intranet and shared file storage",
]

ROLE_LEVELS = {
    "Intern / Trainee": "junior",
    "Junior": "junior",
    "Associate": "junior",
    "Mid-Level": "mid",
    "Senior": "senior",
    "Lead / Principal": "senior",
    "Manager": "manager",
    "Director / Head": "manager",
}

DEPARTMENT_TRAINING = {
    "Engineering": [
        "Secure coding and OWASP Top 10 fundamentals",
        "Internal architecture and system design overview",
        "Git workflow, code review and branching standards",
        "Testing strategy: unit, integration and end-to-end",
        "Incident response and on-call basics",
    ],
    "Human Resources": [
        "Employment law and compliance essentials",
        "HRIS platform training",
        "Inclusive hiring and unconscious bias",
        "Employee relations and conflict resolution",
    ],
    "Finance": [
        "Internal controls and audit readiness",
        "ERP / accounting system walkthrough",
        "Budgeting and forecasting process",
        "Anti-fraud and expense policy training",
    ],
    "Marketing": [
        "Brand voice and style guide",
        "SEO and content strategy fundamentals",
        "Marketing analytics and attribution",
        "Campaign planning and approval workflow",
    ],
    "Sales": [
        "Product knowledge and demo certification",
        "CRM and pipeline hygiene",
        "Consultative selling methodology",
        "Pricing, discounting and contract policy",
    ],
    "Operations": [
        "Process mapping and continuous improvement (Lean basics)",
        "Vendor and supply chain management",
        "Health, safety and business continuity",
        "Operations KPIs and reporting",
    ],
    "Customer Support": [
        "Product deep-dive for support agents",
        "Customer communication and de-escalation",
        "Helpdesk workflows and SLAs",
        "Knowledge base writing best practices",
    ],
    "Product": [
        "Product discovery and user research methods",
        "Roadmapping and prioritization frameworks",
        "Agile / Scrum practices at the company",
        "Product analytics and experimentation",
    ],
}

LEVEL_TRAINING = {
    "junior": [
        "Mentorship program kick-off and goal setting",
        "Foundations course: company tools and workflows",
        "Time management and asking for help effectively",
    ],
    "mid": [
        "Cross-team collaboration and stakeholder communication",
        "Ownership and project delivery best practices",
    ],
    "senior": [
        "Technical / functional leadership and mentoring others",
        "Decision-making and architecture or strategy reviews",
        "Influencing without authority",
    ],
    "manager": [
        "People management essentials and 1:1 coaching",
        "Performance reviews and feedback culture",
        "Hiring, budgeting and resource planning",
        "Leading through change",
    ],
}

COMMON_TRAINING = [
    "Company culture, mission and values",
    "Information security and data privacy awareness (mandatory)",
    "Code of conduct and anti-harassment training (mandatory)",
    "Workplace health and safety",
]

COMMON_DOCUMENTS = [
    "Signed offer letter and employment contract",
    "Government-issued photo ID (passport / national ID / driver's license)",
    "Proof of address (utility bill or bank statement)",
    "Tax forms (e.g., W-4 / I-9 or local equivalent)",
    "Bank account details for payroll (voided cheque or bank letter)",
    "Emergency contact information form",
    "Signed non-disclosure agreement (NDA)",
    "Signed acknowledgment of employee handbook and code of conduct",
    "Educational certificates and transcripts",
    "Previous employment relieving / experience letters",
    "Passport-size photographs (for ID badge)",
    "Benefits enrollment forms (health insurance, retirement plan)",
]

ROLE_EXTRA_DOCUMENTS = {
    "manager": [
        "Signed management responsibilities and delegation-of-authority form",
        "Conflict of interest declaration",
    ],
    "senior": [
        "Conflict of interest declaration",
    ],
}

DEPARTMENT_EXTRA_DOCUMENTS = {
    "Engineering": ["Intellectual property (IP) assignment agreement"],
    "Finance": [
        "Background check consent (financial roles)",
        "Signed financial confidentiality and ethics policy",
    ],
    "Human Resources": ["Signed confidentiality agreement for employee records"],
    "Sales": ["Signed commission plan and non-solicitation agreement"],
    "Product": ["Intellectual property (IP) assignment agreement"],
}

FAQS = [
    ("What are the standard working hours?",
     "Core hours are 10:00 AM - 4:00 PM, with flexibility around them. Your manager "
     "will confirm your exact schedule on Day 1."),
    ("When and how will I be paid?",
     "Salaries are paid monthly via direct deposit. Make sure your bank details are "
     "submitted to HR in your first week."),
    ("How do I request leave?",
     "Submit leave requests through the HR portal and notify your manager. Your "
     "leave balance is available in the portal after your first week."),
    ("What is the dress code?",
     "Business casual in the office. Check with your team about client-facing days."),
    ("Who do I contact for IT issues?",
     "Raise a ticket through the IT helpdesk portal or email the IT support "
     "mailbox. Urgent issues can be escalated via the helpdesk chat channel."),
    ("What is the remote / hybrid work policy?",
     "Eligible roles follow a hybrid policy. Your manager will explain the "
     "expectations for your team during your first week."),
    ("Is there a probation period?",
     "Yes, new employees typically have a 3-6 month probation period with "
     "scheduled check-ins at 30, 60 and 90 days."),
    ("How do I enroll in benefits?",
     "Benefits enrollment opens within 30 days of joining. HR will send "
     "enrollment instructions during Week 1."),
    ("Where can I find company policies?",
     "All policies are on the intranet under 'HR > Policies', including the "
     "employee handbook and code of conduct."),
]

ROLE_FAQS = {
    "junior": [
        ("Will I have a mentor?",
         "Yes. You will be paired with a buddy or mentor for your first 90 days."),
    ],
    "mid": [
        ("How are goals and performance reviewed?",
         "You will agree on goals with your manager in the first 30 days, with "
         "reviews held semi-annually."),
    ],
    "senior": [
        ("What is the expectation for mentoring others?",
         "Senior team members are expected to support junior colleagues and "
         "contribute to team practices. Your manager will outline specifics."),
    ],
    "manager": [
        ("What management resources are available?",
         "You will get access to the leadership portal, manager training "
         "curriculum and HR business partner support."),
    ],
}

# Keyword-based role training (checked against the lower-cased role text).
ROLE_KEYWORD_TRAINING = {
    ("developer", "engineer", "programmer", "devops", "sre"): [
        "Python / JavaScript internal coding standards",
        "Docker and Kubernetes fundamentals",
        "Clean Code and design patterns",
        "Cloud architecture basics (AWS / Azure / GCP)",
    ],
    ("data", "analyst", "scientist", "bi"): [
        "SQL for analytics (advanced)",
        "Data visualization with Power BI / Tableau",
        "Statistics and experimentation fundamentals",
        "Data governance and privacy best practices",
    ],
    ("designer", "ux", "ui"): [
        "Design system and component library walkthrough",
        "Accessibility (WCAG) essentials",
        "User research and usability testing",
    ],
    ("qa", "test", "quality"): [
        "Test automation frameworks (Selenium / Playwright / pytest)",
        "Defect lifecycle and bug triage process",
    ],
    ("sales", "account", "business development"): [
        "Objection handling and negotiation skills",
        "Territory and account planning",
    ],
    ("recruit", "talent", "hr"): [
        "Structured interviewing techniques",
        "Candidate experience best practices",
    ],
    ("accountant", "finance", "auditor"): [
        "Financial reporting standards overview",
        "Month-end close process",
    ],
    ("support", "customer", "success"): [
        "Customer empathy and active listening workshop",
        "Escalation procedures",
    ],
    ("product", "project", "program"): [
        "Writing effective PRDs and user stories",
        "Stakeholder management and status reporting",
    ],
    ("marketing", "content", "seo", "social"): [
        "Content calendar and editorial workflow",
        "Digital advertising fundamentals",
    ],
}

# --------------------------------------------------------------------------
# Helper / generator functions
# --------------------------------------------------------------------------


def get_level(role: str) -> str:
    """Infer seniority level from the role text."""
    text = role.lower()
    if any(k in text for k in ("director", "head", "vp", "chief", "manager")):
        return "manager"
    if any(k in text for k in ("senior", "sr.", "sr ", "lead", "principal", "staff", "architect")):
        return "senior"
    if any(k in text for k in ("intern", "trainee", "junior", "jr", "graduate", "associate")):
        return "junior"
    return "mid"


def get_role_keyword_training(role: str) -> list:
    text = role.lower()
    items = []
    for keywords, courses in ROLE_KEYWORD_TRAINING.items():
        if any(k in text for k in keywords):
            items.extend(courses)
    return items


def generate_welcome_email(name: str, role: str, department: str, start: date) -> str:
    level = get_level(role)
    closing = {
        "manager": "As a leader, your perspective will be invaluable in shaping our "
                   "team's direction, and we look forward to supporting you as you "
                   "settle in.",
        "senior": "Your experience will be a great asset, and we're excited for you "
                  "to help guide and mentor the team.",
        "junior": "You'll be paired with a mentor who will help you learn the ropes "
                  "and grow with us.",
        "mid": "We're confident your skills will make an immediate and meaningful "
               "impact.",
    }[level]
    return f"""Subject: Welcome to the Team, {name}! Your First Day as {role}

Dear {name},

On behalf of everyone at the company, a very warm welcome! We are delighted that you are joining the {department} department as our new {role}.

Your first day is {start.strftime('%A, %B %d, %Y')}. Please arrive at 9:30 AM at the main reception, where a member of the {department} team will greet you. Your laptop, ID badge and workspace will be ready.

What to expect in your first week:
  - A welcome session with HR and an office / virtual tour
  - IT setup and access to the tools you need for your work
  - Introductions to your manager and teammates
  - A structured onboarding plan to help you get up to speed quickly

{closing}

Please bring the documents listed in your onboarding checklist. If you have any questions before your start date, feel free to reply to this email or contact HR.

We can't wait to work with you!

Warm regards,
People & Culture Team
Your Company"""


def generate_onboarding_plan(name: str, role: str, department: str) -> list:
    level = get_level(role)
    first_name = name.split()[0] if name.strip() else "the new hire"

    if level == "manager":
        day2_extra = "Meet your direct reports and HR business partner"
        day5_extra = "Draft a 30-60-90 day leadership plan"
    elif level == "senior":
        day2_extra = "Review team architecture / strategy and key stakeholders"
        day5_extra = "Identify early opportunities to contribute and mentor"
    elif level == "junior":
        day2_extra = "Meet your mentor / buddy and set learning goals"
        day5_extra = "Complete a guided starter task with your mentor"
    else:
        day2_extra = "Meet key collaborators across teams"
        day5_extra = "Pick up your first small deliverable"

    return [
        {
            "day": "Day 1 - Welcome & Orientation",
            "tasks": [
                "Welcome meeting with HR and your manager",
                "Collect laptop, ID badge and workspace",
                "Complete paperwork and submit documents",
                "Office / virtual tour and team lunch",
                f"Set up email, SSO and chat (buddy: assigned for {first_name})",
            ],
        },
        {
            "day": "Day 2 - Team & Tools",
            "tasks": [
                f"Meet the {department} team and key stakeholders",
                day2_extra,
                f"Set up {department}-specific tools and access",
                "Review the employee handbook and company policies",
            ],
        },
        {
            "day": "Day 3 - Company & Culture",
            "tasks": [
                "Company overview: mission, values, products and customers",
                "Complete mandatory security and compliance training",
                f"Session: how {department} contributes to company goals",
            ],
        },
        {
            "day": f"Day 4 - Role Deep-Dive: {role}",
            "tasks": [
                f"Review the {role} job description and expectations with your manager",
                "Walk through current projects, processes and documentation",
                "Begin role-specific training modules",
            ],
        },
        {
            "day": "Day 5 - Hands-On Start",
            "tasks": [
                day5_extra,
                "Shadow a teammate on live work",
                "Weekly check-in with your manager",
            ],
        },
        {
            "day": "Day 6 - Learning & Practice",
            "tasks": [
                "Continue role-specific training",
                "Work on your first assigned task with support",
                "Ask questions - collect notes on anything unclear",
            ],
        },
        {
            "day": "Day 7 - Review & Next Steps",
            "tasks": [
                "Week-1 feedback conversation with your manager",
                "Agree on 30-60-90 day goals",
                "Provide feedback on your onboarding experience",
                "Confirm benefits enrollment and outstanding paperwork",
            ],
        },
    ]


def generate_document_checklist(role: str, department: str) -> list:
    docs = list(COMMON_DOCUMENTS)
    level = get_level(role)
    docs.extend(ROLE_EXTRA_DOCUMENTS.get(level, []))
    for doc in DEPARTMENT_EXTRA_DOCUMENTS.get(department, []):
        if doc not in docs:
            docs.append(doc)
    return docs


def generate_it_checklist(role: str, department: str) -> tuple:
    dept_items = DEPARTMENT_IT_ACCESS.get(department, [])
    level = get_level(role)
    extra = []
    if level == "manager":
        extra = [
            "Leadership dashboards and team reporting tools",
            "Approval workflows (expenses, leave, hiring)",
        ]
    elif level == "senior" and department == "Engineering":
        extra = ["Production access request (approval required)", "Architecture review tooling"]
    return COMMON_IT_ACCESS, dept_items + extra


def generate_faqs(role: str) -> list:
    return FAQS + ROLE_FAQS.get(get_level(role), [])


def generate_training(role: str, department: str) -> dict:
    return {
        "Company-wide (mandatory)": COMMON_TRAINING,
        f"{department} department": DEPARTMENT_TRAINING.get(department, []),
        "Role-specific": get_role_keyword_training(role),
        "Career level": LEVEL_TRAINING[get_level(role)],
    }


def checklist(items: list, prefix: str) -> None:
    for i, item in enumerate(items):
        st.checkbox(item, key=f"{prefix}_{i}")


# --------------------------------------------------------------------------
# UI
# --------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="Employee Onboarding System", page_icon="🧑‍💼", layout="wide")
    st.title("🧑‍💼 AI-Powered Employee Onboarding System")
    st.caption("Enter the new hire's details to generate a complete onboarding package.")

    with st.form("onboarding_form"):
        name = st.text_input("Employee Name", placeholder="e.g., Jane Doe")
        role = st.text_input("Role", placeholder="e.g., Senior Software Engineer")
        department = st.selectbox("Department", list(DEPARTMENT_IT_ACCESS.keys()))
        start = st.date_input("Start Date", value=date.today())
        submitted = st.form_submit_button("Generate Onboarding Package")

    if submitted:
        if not name.strip() or not role.strip():
            st.error("Please enter both the employee name and role.")
            st.session_state.pop("package", None)
        else:
            st.session_state["package"] = (name.strip(), role.strip(), department, start)

    if "package" not in st.session_state:
        return

    name, role, department, start = st.session_state["package"]
    st.success(f"Onboarding package for **{name}** - {role}, {department}")

    st.header("1. Welcome Email")
    email = generate_welcome_email(name, role, department, start)
    st.code(email, language=None)

    st.header("2. 7-Day Onboarding Plan")
    for entry in generate_onboarding_plan(name, role, department):
        with st.expander(entry["day"], expanded=False):
            for task in entry["tasks"]:
                st.markdown(f"- {task}")

    st.header("3. Required Documents Checklist")
    checklist(generate_document_checklist(role, department), "doc")

    st.header("4. IT Access Checklist")
    common, dept_items = generate_it_checklist(role, department)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Standard access (all employees)")
        checklist(common, "it_common")
    with col2:
        st.subheader(f"{department} access")
        if dept_items:
            checklist(dept_items, "it_dept")
        else:
            st.info("No department-specific access defined.")

    st.header("5. FAQs for New Employees")
    for question, answer in generate_faqs(role):
        with st.expander(question):
            st.write(answer)

    st.header("6. Training Resources")
    for category, courses in generate_training(role, department).items():
        if courses:
            st.subheader(category)
            for course in courses:
                st.markdown(f"- {course}")

    st.download_button(
        "Download Welcome Email (.txt)",
        data=email,
        file_name=f"welcome_email_{name.replace(' ', '_')}.txt",
    )


if __name__ == "__main__":
    main()
