from fastapi import FastAPI,Response
import re
import subprocess,httpx
from pydantic import BaseModel
import logging
import time

logger = logging.getLogger("uvicorn")
app = FastAPI()

last_event  = {}  # Store the last event time for each user

class SlackRequest(BaseModel):
    token: str
    challenge: str
    type: str

class Item(BaseModel):
    message: str

@app.post("/execute_command")
async def execute_command(channel_id: str, message: str):
    logger.info(channel_id)
    logger.info(message)
    logger.info("logging command")
    command = f'echo "{message}" | bito'
    logger.info(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    logger.info(output)
    logger.info(error)

    post_message_to_slack(channel_id, str(output.decode('utf-8').strip()))

def post_message_to_slack(channel_id: str, text: str):
    url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Authorization": "Bearer <>",
        "Content-Type": "application/json"
    }

    data = {
        "channel": channel_id,
        "text": text
    }

    with httpx.Client(timeout=120.0) as client:
        response = client.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Request to Slack API failed with status {response.status_code}, response: {response.text}")

    data = response.json()
    if not data['ok']:
        raise Exception(f"Slack API returned an error: {data['error']}")

@app.post("/slack/events")
async def handle_slack_events(request_data: dict):
    logger.info(f"Received event: {request_data}")
    # Handle URL verification
    if request_data['type'] == 'url_verification':
        return request_data['challenge']
    elif request_data['type'] == 'event_callback':
        event = request_data['event']
        user_id = event.get('user')
        # Check if the event is a duplicate
        if user_id in last_event and last_event[user_id] == event:
            # If yes, ignore this event
            return Response(status_code=200)
        last_event[user_id] = event  # Update the last event for this user
        # Continue processing the event
        if event['type'] == 'app_mention':
            channel_id = event['channel']
            # Ignore messages that don't contain any text
            if 'text' in event:
                message = event['text']
                pattern = "<@U[A-Z0-9]+>\s*"
                bot_id = re.search(pattern, message).group()
                message = re.sub(re.escape(bot_id), "", message)
                await execute_command(channel_id, message)
    return Response(status_code=200)

@app.post("/execute_command_post")
async def execute_command_post(item: Item):
    command = f'echo "{item.message}" | bito'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output
