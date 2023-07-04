# bito_slack_app
run app.py using
export LC_ALL=en_US.utf8
uvicorn app:app --host 127.0.0.1 --port 5002

expose the port using 
ngrok http 5002

use the ngrok endpoint/slack/events in event subscription for slack app
bot event subscriptions

Event Name	Description	Required Scope
app_mention
Subscribe to only the message events that mention your app or bot

app_mentions:read

message.channels
A message was posted to a channel

channels:history

message.im
A message was posted in a direct message channel

im:history



bot oauth scopes


Bot Token Scopes
Scopes that govern what your app can access.

OAuth Scope
Description
 
app_mentions:read
View messages that directly mention @bito_app in conversations that the app is in

channels:history
View messages and other content in public channels that bito_app has been added to

chat:write
Send messages as @bito_app

im:history
View messages and other content in direct messages that bito_app has been added to


use the token in fast api

invite slack app
and use like 

@bito_app summarize in short: java vs javascript 

install and authenticate bito on server where fast api will be running

you can also use curl call like 
curl -s -H 'Content-Type: application/json' -d '{"message":"tell me a joke"}' 'https://<ngrok-end-point>/execute_command_post' | echo -e $(cat)
