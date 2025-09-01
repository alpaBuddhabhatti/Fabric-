from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import csv
import os

# Initialize the AIProjectClient with Azure credentials and endpoint
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://azureaifoundarysqlbits2025.services.ai.azure.com/api/projects/firstProject")

# Get the agent by its ID
agent = project.agents.get_agent("asst_wCvXV5ypMn9HmdIFKCoEE4bw")

# Create a new thread for the conversation
thread = project.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Prompt the user for input to send to the agent
user_prompt = input("Enter your prompt for the agent: ")

# Create a message in the thread with the user's input
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