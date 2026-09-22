"""System 3: AI Agent.
LLM + Tools + Loop.
"""

import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a Student Academic Assistant.

You can answer questions about private student academic data.

Important rules:
1. Never guess private student information.
2. Use the available tools when private data is required.
3. Use check_placement_eligibility for placement eligibility.
4. Use calculate_fee_status for pending fee questions.
5. If the question does not require private data, answer normally.
"""


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # 1. REASON
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # If no tool is requested,
        # the agent has finished.
        if not message.tool_calls:

            return message.content.strip()

        # Save the assistant's tool request
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in message.tool_calls
                ]
            }
        )

        # 2. ACT + 3. OBSERVE
        for call in message.tool_calls:

            name = call.function.name

            arguments = json.loads(
                call.function.arguments or "{}"
            )

            function = TOOL_FUNCTIONS.get(name)

            if function:
                if name in {
                    "check_placement_eligibility",
                    "calculate_fee_status"
                }:
                    result = function()
                else:
                    result = function(**arguments)
            else:
                result = f"Unknown tool: {name}"

            if verbose:
                print(
                    f" step {step}: "
                    f"{name}({arguments}) -> {result}"
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                }
            )

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        print("A:", agent(question))

        print("-" * 70)