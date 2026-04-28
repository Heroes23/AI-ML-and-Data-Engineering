from os import getcwd
from json import dump
from langgraph.prebuilt import create_react_agent


# Custom modules
from db_connection import sql_toolkit, model

# Put the agent together
agent = create_react_agent(model=model, tools=sql_toolkit.get_tools())

# Instructions
instructions = [
    'Find the common customers between the north and south regions.'
]

# Raw result
result = agent.invoke(input={'messages' : instructions})

print(result.keys())

# Messages
messages = [result.model_dump() for result in result['messages']]

print("Agent finished response.")

print(f"Response: \n {messages}")

# Dump the messages into a JSON file
json_path = getcwd() + "/data/json/agent_responses/sql_postgres_agent_response.json"

with open(json_path, "w") as buffer:
    # Dump the messages into the JSON file
    dump(messages, buffer)

    # Close the context manager
    buffer.close()

print("Response saved to JSON successfully.")

