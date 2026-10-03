"""Illustrative BRCGS-style readiness questions.

These items are short, paraphrased check points grouped by the main sections of
the BRCGS Global Standard for Food Safety. They are NOT the licensed standard
text. Replace this list with the site's licensed clause list (roughly 300
clauses) when the full questionnaire is loaded.

severity: "fundamental" (weight 10), "major" (weight 5), "minor" (weight 2)
fix: default corrective-action hint, used when the local AI model is offline.
"""

SEVERITY_WEIGHTS = {"fundamental": 10, "major": 5, "minor": 2}

SECTIONS = {
    1: "Senior management commitment",
    2: "Food safety plan (HACCP)",
    3: "Food safety and quality management system",
    4: "Site standards",
    5: "Product control",
    6: "Process control",
    7: "Personnel",
}

QUESTIONS = [
    # 1 Senior management commitment
    {"id": "1.1", "section": 1, "severity": "fundamental",
     "text": "A documented food safety and quality policy is approved by senior management and communicated to all staff.",
     "fix": "Draft a signed policy, display it on site and brief every shift."},
    {"id": "1.2", "section": 1, "severity": "major",
     "text": "Measurable food safety objectives are set and reviewed at least annually.",
     "fix": "Define 3-5 measurable objectives and add them to the annual management review."},
    {"id": "1.3", "section": 1, "severity": "major",
     "text": "Management review meetings are held and minuted, with actions tracked to closure.",
     "fix": "Schedule a recurring review with a standard agenda and an action log."},
    {"id": "1.4", "section": 1, "severity": "minor",
     "text": "A confidential reporting route exists for staff to raise food safety concerns.",
     "fix": "Set up an anonymous reporting channel and tell staff how to use it."},
    # 2 HACCP
    {"id": "2.1", "section": 2, "severity": "fundamental",
     "text": "A multidisciplinary HACCP team with documented training is in place.",
     "fix": "Nominate team members from QA, production and engineering and record HACCP training."},
    {"id": "2.2", "section": 2, "severity": "fundamental",
     "text": "Process flow diagrams and hazard analysis cover every product and process, and are verified on site.",
     "fix": "Walk the line, correct each flow diagram and re-run the hazard analysis."},
    {"id": "2.3", "section": 2, "severity": "major",
     "text": "Critical control points have validated critical limits, monitoring and corrective actions.",
     "fix": "Validate each critical limit and record monitoring checks and deviation actions."},
    {"id": "2.4", "section": 2, "severity": "minor",
     "text": "The HACCP plan is reviewed at least annually and after any process or product change.",
     "fix": "Add an annual HACCP review date and a change-control trigger."},
    # 3 FSQMS
    {"id": "3.1", "section": 3, "severity": "fundamental",
     "text": "An internal audit programme covers the whole standard and findings are closed on time.",
     "fix": "Build an annual audit schedule, train auditors and track findings to closure."},
    {"id": "3.2", "section": 3, "severity": "fundamental",
     "text": "A documented corrective and preventive action process finds root causes and verifies effectiveness.",
     "fix": "Introduce a corrective action form with a root-cause step and a follow-up check."},
    {"id": "3.3", "section": 3, "severity": "major",
     "text": "Suppliers are approved and monitored using a risk-based approach.",
     "fix": "Create a supplier approval list with risk rating and periodic review."},
    {"id": "3.4", "section": 3, "severity": "fundamental",
     "text": "Traceability from raw material to finished product is tested at least annually.",
     "fix": "Run a mock trace and recall exercise and record mass-balance results."},
    # 4 Site standards
    {"id": "4.1", "section": 4, "severity": "major",
     "text": "Site layout and product flow minimise cross-contamination between raw and ready-to-eat areas.",
     "fix": "Mark zones, separate flows and review layout drawings with production."},
    {"id": "4.2", "section": 4, "severity": "major",
     "text": "A documented pest control programme is run by competent staff or a contractor, with trend analysis.",
     "fix": "Contract a licensed provider, map devices and review trends monthly."},
    {"id": "4.3", "section": 4, "severity": "major",
     "text": "Cleaning and sanitation schedules are documented, with verification (visual and microbiological).",
     "fix": "Write schedules per area and add swab or ATP verification."},
    {"id": "4.4", "section": 4, "severity": "minor",
     "text": "Maintenance is planned and engineering work is controlled to avoid contamination.",
     "fix": "Add hygiene clearance steps to maintenance work orders."},
    # 5 Product control
    {"id": "5.1", "section": 5, "severity": "major",
     "text": "Allergen risks are assessed, controlled and segregated, with changeover cleaning validated.",
     "fix": "Create an allergen matrix and validate changeover cleaning."},
    {"id": "5.2", "section": 5, "severity": "major",
     "text": "Product labelling is checked against specification, including allergen declarations.",
     "fix": "Add label verification checks at line start and at changeover."},
    {"id": "5.3", "section": 5, "severity": "minor",
     "text": "Foreign-body controls (metal detection, sieves, glass and brittle plastic registers) are in place.",
     "fix": "Create a glass and brittle plastic register and test detectors each shift."},
    {"id": "5.4", "section": 5, "severity": "minor",
     "text": "Product shelf life and storage conditions are validated and documented.",
     "fix": "Run shelf-life studies and record storage limits per product."},
    # 6 Process control
    {"id": "6.1", "section": 6, "severity": "major",
     "text": "Quality control checks and in-process specifications are documented and recorded.",
     "fix": "Standardise check sheets with limits and sign-off."},
    {"id": "6.2", "section": 6, "severity": "major",
     "text": "Measuring equipment is identified, calibrated and traceable to a standard.",
     "fix": "List all critical instruments and schedule calibration with certificates."},
    {"id": "6.3", "section": 6, "severity": "minor",
     "text": "Non-conforming product is identified, segregated and has a documented disposition.",
     "fix": "Introduce hold tags, a quarantine area and a disposition record."},
    # 7 Personnel
    {"id": "7.1", "section": 7, "severity": "fundamental",
     "text": "All staff are trained for their role, and training is recorded and assessed for competence.",
     "fix": "Build a training matrix per role with induction and competence sign-off."},
    {"id": "7.2", "section": 7, "severity": "major",
     "text": "Personal hygiene rules (hand washing, protective clothing, jewellery) are enforced and audited.",
     "fix": "Add daily hygiene checks at entry points and record results."},
    {"id": "7.3", "section": 7, "severity": "minor",
     "text": "A medical screening and illness reporting procedure applies to staff and visitors.",
     "fix": "Write a fitness-to-work procedure and a visitor declaration."},
]

QUESTIONS_BY_ID = {q["id"]: q for q in QUESTIONS}
