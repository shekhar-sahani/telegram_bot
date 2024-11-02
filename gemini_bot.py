import google.generativeai as genai
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE_NUMBER, GEMINI_API_KEY

# Initialize the Telegram client
client = TelegramClient('anon', API_ID, API_HASH)

# Set up Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Default reply message
DEFAULT_REPLY_MESSAGE = "Again this didn't worked!.... -_-."

# Custom messages for specific user IDs
custom_replies = {
    918603349981: "Hey, Sujata! What are you doing?",
    # Add more users as needed
}

# Function to get AI-generated reply from Gemini
async def get_ai_reply(message_text):
    try:
        # Use the GenerativeModel to get a response
        model = genai.GenerativeModel("gemini-1.5-flash")  # Make sure the model name is correct
        response = model.generate_content(message_text)
        ai_reply = response.text.strip()
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
