"""System 2: Rule-based workflow.
Uses private data and fixed rules. No LLM.
"""

from config import STUDENT_DATA, QUESTIONS


def workflow(question):

    text = question.lower()

    # Attendance question
    if "attendance" in text or "attendence" in text:

        attendance = STUDENT_DATA["attendance"]

        return f"My attendance percentage is {attendance}%."

    # CGPA question
    if "cgpa" in text:

        cgpa = STUDENT_DATA["cgpa"]

        return f"My CGPA is {cgpa}."

    # Placement eligibility
    if "eligible" in text or "placement" in text:

        attendance = STUDENT_DATA["attendance"]
        backlogs = STUDENT_DATA["backlogs"]

        if attendance >= 75 and backlogs == 0:
            return (
                "You are eligible for placement training "
                "based on the demo rule: attendance >= 75% "
                "and no backlogs."
            )

        return (
            "You are not eligible for placement training "
            "based on the demo rule."
        )

    # Pending fees
    if "fee" in text or "fees" in text:

        fees = STUDENT_DATA["fees_due"]

        if fees > 0:
            return f"You have Rs. {fees:,} in pending fees."

        return "You have no pending fees."

    return (
        "Sorry, I do not have a rule for this type of question."
    )


if __name__ == "__main__":

    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (NO LLM) ===\n")

    for question in QUESTIONS:

        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)