import json
import google.generativeai as genai

from backend.app.core.config import settings
from backend.app.agent import tools

genai.configure(api_key=settings.GEMINI_API_KEY)

TOOL_DECLARATIONS = [
    {
        "name": "search_events",
        "description": "Search for published campus events by keyword and/or category.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keyword to search in event title/description"},
                "category": {"type": "string", "description": "One of: workshop, seminar, sports, cultural"},
            },
        },
    },
    {
        "name": "register_for_event",
        "description": "Register the current student for a specific event using its event_id.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The MongoDB _id of the event"},
            },
            "required": ["event_id"],
        },
    },
    {
        "name": "cancel_registration",
        "description": "Cancel the current student's registration using its registration_id.",
        "parameters": {
            "type": "object",
            "properties": {
                "registration_id": {"type": "string", "description": "The MongoDB _id of the registration"},
            },
            "required": ["registration_id"],
        },
    },
    {
        "name": "view_my_registrations",
        "description": "List all events the current student has registered for.",
        "parameters": {"type": "object", "properties": {}},
    },
]

TOOL_FUNCTIONS = {
    "search_events": tools.search_events,
    "register_for_event": tools.register_for_event,
    "cancel_registration": tools.cancel_registration,
    "view_my_registrations": tools.view_my_registrations,
}

SYSTEM_INSTRUCTION = (
    "You are a helpful AI assistant for a campus event registration system. "
    "Help students search for events, register, cancel registrations, and view their registrations. "
    "Always use the available tools to get real data instead of guessing. "
    "Be concise and friendly in your replies."
)


async def run_agent(message: str, student_id: str) -> str:
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        tools=[{"function_declarations": TOOL_DECLARATIONS}],
        system_instruction=SYSTEM_INSTRUCTION,
    )

    chat = model.start_chat()
    response = chat.send_message(message)

    part = response.candidates[0].content.parts[0]

    if hasattr(part, "function_call") and part.function_call and part.function_call.name:
        function_name = part.function_call.name
        function_args = dict(part.function_call.args)

        if function_name == "register_for_event":
            result = await TOOL_FUNCTIONS[function_name](student_id, function_args.get("event_id"))
        elif function_name == "cancel_registration":
            result = await TOOL_FUNCTIONS[function_name](student_id, function_args.get("registration_id"))
        elif function_name == "view_my_registrations":
            result = await TOOL_FUNCTIONS[function_name](student_id)
        else:
            result = await TOOL_FUNCTIONS[function_name](**function_args)

        follow_up = chat.send_message(
            genai.protos.Content(
                parts=[genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=function_name,
                        response={"result": json.dumps(result, default=str)}
                    )
                )]
            )
        )

        return follow_up.text

    return response.text