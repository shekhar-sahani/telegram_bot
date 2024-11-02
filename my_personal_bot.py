from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE_NUMBER

# Initialize the Telegram client
client = TelegramClient('anon', API_ID, API_HASH)

# Default reply message
DEFAULT_REPLY_MESSAGE = "Hello! I received your message. I'll get back to you soon."

# Custom messages for specific user IDs
custom_replies = {
    375292313469: "Hello, Maria! Master is away. How can I help you?..",  
    918603349987: "Hey, Sujata! What are you doing?",
    # Add more users as needed
}

# Custom replies based on message content
message_replies = { 
    "hi": "Hi there! How can I help you?",
    "hello": "Hello! Hope you’re having a great day!",
    "how are you": "I’m just a bot, but thanks for asking! How are you?",
    "who are you": "I'm your personal assistant bot here to help you!",
    # Add more phrases as needed
}

# Define the auto-reply function
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    # Ignore messages from yourself
    if event.sender_id != (await client.get_me()).id:
        
        # Check if there's a custom reply for this user
        custom_message = custom_replies.get(event.sender_id, None)
        
        # Check if the message text has a specific reply
        message_text = event.message.message.lower()  # Convert to lowercase for case-insensitive matching
        keyword_reply = None
        
        for keyword, reply in message_replies.items():
            if keyword in message_text:
                keyword_reply = reply
                break
        
        # Choose reply: custom message > keyword-based reply > default reply
        reply_message = custom_message or keyword_reply or DEFAULT_REPLY_MESSAGE

        # Reply to the sender
        await event.reply(reply_message)
        print(f"Replied to user: {event.sender_id} with message: {reply_message}")

async def main():
    # Connect to Telegram
    await client.start(PHONE_NUMBER)
    print("Auto-reply bot is running...")

    # Send a message to yourself indicating the bot has started
    me = await client.get_me()
    await client.send_message(me.id, "Auto-reply bot has started and is running.")
    print("Sent startup message to myself")

# Run the client and listen for messages
with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
