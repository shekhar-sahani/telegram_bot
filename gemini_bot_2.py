# Twinkle AI chat assistant for telegram!..
import google.generativeai as genai
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE_NUMBER, GEMINI_API_KEY

# Initialize the Telegram client
client = TelegramClient('twinkle', API_ID, API_HASH)

# Set up Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Default reply message
DEFAULT_REPLY_MESSAGE = "Oops! It seems like that didn't work out for me! 😅"

# Custom messages for specific user IDs
custom_replies = {
    918603349981: "Hey, ! What are you doing?",
}

# Flag to track if the bot is active
bot_active = False

# Function to get AI-generated reply from Gemini
async def get_ai_reply(message_text, user_name=None):
    try:
        # Use the GenerativeModel to get a response
        if user_name:
            prompt = f"You are Twinkle, a friendly human assistant created by starlord. The user's name is {user_name}. Respond to the user's message in a warm, conversational, and helpful manner. User says: '{message_text}'"
        else:   
            prompt = f"You are Twinkle, a friendly human assistant created by starlord. Respond to the user's message in a warm, conversational, and helpful manner. User says: '{message_text}'"
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        ai_reply = response.text.strip()
        return ai_reply
    except Exception as e:
        print(f"Error generating AI reply: {e}")
        return DEFAULT_REPLY_MESSAGE

# Define the auto-reply function
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    global bot_active
    
    # Ignore messages from yourself
    if event.sender_id != (await client.get_me()).id:
        # Handle start and stop commands
        if event.message.message.lower() == "start":
            bot_active = True
            await event.reply("✨ Yay! Twinkle is here to spread joy! Ready to shine bright for you! ✨")
            return  # Exit early to avoid further processing

        elif event.message.message.lower() == "stop":
            bot_active = False
            await event.reply("🌟 Oh no! Twinkle will miss you! Don't forget to call me back to sparkle again! 🌈")
            return  # Exit early to avoid further processing

        # If the bot is active, generate replies
        if bot_active:

            # Try to get the sender's username or first name
            sender = await event.get_sender()
            user_name = sender.username or sender.first_name
            
            # Check if there's a custom reply for this user
            custom_message = custom_replies.get(event.sender_id, None)
            
            # Choose reply: custom message > AI-generated reply > default reply
            if custom_message:
                reply_message = custom_message
            else:
                # Use AI to generate a response if no custom reply is found
                reply_message = await get_ai_reply(event.message.message, user_name)

            # Reply to the sender
            await event.reply(reply_message)
            print(f"Replied to user: {event.sender_id} with message: {reply_message}")

async def main():
    # Connect to Telegram
    await client.start(PHONE_NUMBER)
    print("🌟 Twinkle is now awake and ready to spread joy! Let’s make the magic happen! 🌈")

    # Send a message to yourself indicating the bot has started
    me = await client.get_me()
    await client.send_message(me.id, "🌟 Twinkle is now awake and ready to spread joy! Let’s make the magic happen! 🌈")
    print("Sent startup message to myself")

# Run the client and listen for messages
with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
