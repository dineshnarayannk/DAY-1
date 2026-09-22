"""Tools that the AI agent is allowed to use."""

from config import STUDENT_DATA


def get_student_data(field: str) -> str:
    """Get one piece of private student information."""

    field = field.strip().lower()

    available_fields = {
        "name": "name",
        "department": "department",
        "semester": "semester",
        "attendance": "attendance",
        "cgpa": "cgpa",
        "backlogs": "backlogs",
        "fees_due": "fees_due"
    }

    key = available_fields.get(field)

    if key is None:
        return f"Unknown field: {field}"

    return str(STUDENT_DATA[key])


def check_placement_eligibility() -> str:
    """Check placement eligibility using attendance and backlog rules."""

    attendance = STUDENT_DATA["attendance"]
    backlogs = STUDENT_DATA["backlogs"]

    if attendance >= 75 and backlogs == 0:
        return (
            "Eligible: attendance is at least 75% "
            "and there are no backlogs."
        )

    return (
        "Not eligible: attendance must be at least 75% "
        "and there must be no backlogs."
    )


def calculate_fee_status() -> str:
    """Check whether the student has pending fees."""

    fees_due = STUDENT_DATA["fees_due"]

    if fees_due > 0:
        return f"Pending fees: Rs. {fees_due:,}"

    return "No pending fees."


TOOL_FUNCTIONS = {
    "get_student_data": get_student_data,
    "check_placement_eligibility": check_placement_eligibility,
    "calculate_fee_status": calculate_fee_status
}


TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_student_data",
            "description": (
                "Get private student information such as "
                "name, department, semester, attendance, "
                "CGPA, backlogs, or fees_due."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": (
                            "The student field to retrieve."
                        )
                    }
                },
                "required": ["field"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_placement_eligibility",
            "description": (
                "Check whether the student is eligible "
                "for placement training."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_fee_status",
            "description": (
                "Check whether the student has pending fees "
                "and return the amount."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


if __name__ == "__main__":

    print(
        "get_student_data('attendance') ->",
        get_student_data("attendance")
    )

    print(
        "get_student_data('cgpa') ->",
        get_student_data("cgpa")
    )

    print(
        "check_placement_eligibility() ->",
        check_placement_eligibility()
    )

    print(
        "calculate_fee_status() ->",
        calculate_fee_status()
    )