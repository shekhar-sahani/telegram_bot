import openai
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE_NUMBER, OPENAI_API_KEY

# Initialize the Telegram client
client = TelegramClient('anon', API_ID, API_HASH)

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Default reply message
DEFAULT_REPLY_MESSAGE = "Hello! I received your message. I'll get back to you soon."

# Custom messages for specific user IDs
custom_replies = {
    918603349981: "Hey, Sujata! What are you doing?",
    # Add more users as needed
}

# Function to get AI-generated reply
async def get_ai_reply(message_text):
    try:
        # Call the OpenAI API to get a response using ChatCompletion
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if available
            messages=[
                {"role": "user", "content": message_text}
            ]
        )
        ai_reply = response['choices'][0]['message']['content'].strip()
        return ai_reply
    except Exception as e:
        print(f"Error generating AI reply: {e}")
        return DEFAULT_REPLY_MESSAGE

# Define the auto-reply function
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    # Ignore messages from yourself
    if event.sender_id != (await client.get_me()).id:
        # Check if there's a custom reply for this user
        custom_message = custom_replies.get(event.sender_id, None)
        
        # Choose reply: custom message > AI-generated reply > default reply
        if custom_message:
            reply_message = custom_message
        else:
            # Use AI to generate a response if no custom reply is found
            reply_message = await get_ai_reply(event.message.message)

        # Reply to the sender
        await event.reply(reply_message)
        print(f"Replied to user: {event.sender_id} with message: {reply_message}")

async def main():
    # Connect to Telegram
    await client.start(PHONE_NUMBER)
    print("AI-powered auto-reply bot is running...")

    # Send a message to yourself indicating the bot has started
    me = await client.get_me()
    await client.send_message(me.id, "AI-powered auto-reply bot has started and is running.")
    print("Sent startup message to myself")

# Run the client and listen for messages
with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
