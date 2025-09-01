from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import os
import csv
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://azureaifoundarysqlbits2025.services.ai.azure.com/api/projects/firstProject")

agent = project.agents.get_agent("asst_4fJGY1pB8KPoDZvrrFabiN0r")

thread = project.agents.threads.create()
print(f"Created thread, ID: {thread.id}")


# Get user prompt at runtime
user_prompt = input("Enter your prompt for the agent: ")

message = project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_prompt  # Use the user input here
)

# Run the agent and process the response
run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id)

# Define the path for the CSV file to store responses
csv_file = os.path.join(os.path.dirname(__file__), "agent_responses.csv")

if run.status == "failed":
    # Print error if the run failed
    print(f"Run failed: {run.last_error}")
else:
    # Get all messages in the thread in ascending order
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

    # Open the CSV file for writing responses
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["role", "message"])  # Write header row

        # Iterate through all messages and write to CSV and console
        for message in messages:
            if message.text_messages:
                response = message.text_messages[-1].text.value
                print(f"{message.role}: {response}")  # Print to console
                writer.writerow([message.role, response])  #
