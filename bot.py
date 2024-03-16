# -*- coding: utf-8 -*-
import telebot, logging, json
from telebot import types, util
from logging.handlers import RotatingFileHandler
from pymongo.mongo_client import MongoClient

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# RotatingFileHandler
max_log_size_mb = 5  # Set your desired maximum log size in megabytes
handler = RotatingFileHandler('bot.log', maxBytes=max_log_size_mb * 1024 * 1024, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

bot = telebot.TeleBot("6561574428:AAHv-wwOsFCDYEcNXFY8xPqxeUlkpldQHn0")

uri = "mongodb+srv://hani:hh123456hh@cluster0.ona8wkd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Create "Permissions" database
db = client.permissions # Permissions is the name of the database

# Create "CGManaging" database
db2 = client.managing


""" # Create the collections
db.create_collection("owner_collection")
db.create_collection("admin_collection")
db.create_collection("user_collection")
db2.create_collection("channel_collection")
db2.create_collection("group_collection") """

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Create a schema for owner that contains a full name and username and chat id of the owner
owner_schema = {
    "full_name": str,
    "username": str,
    "chat_id": int
}
# Create a schema for admins that contains a full name and username and chat id of the admin
admin_schema = {
    "full_name": str,
    "username": str,
    "chat_id": int
}
# Create a schema for users that contains a full name and username and chat id of the user
user_schema = {
    "full_name": str,
    "username": str,
    "chat_id": int,
    "total": int
}
# Create a schema for channels that contains a full name and username and chat id of the channel
channel_schema = {
    "full_name": str,
    "username": str,
    "chat_id": int
}
# Create a schema for groups that contains a full name and username and chat id of the group
group_schema = {
    "full_name": str,
    "username": str,
    "chat_id": int
}

# Define the collections for owner, admins, users, channels, and groups
owner_collection = client.permissions.owner_collection

admin_collection = client.permissions.admin_collection

user_collection = client.permissions.user_collection

channel_collection = client.managing.channel_collection

group_collection = client.managing.group_collection

# Create a function to get the owner information from the database
def get_owner():
    return owner_collection.find_one()

# Create a function to get the admin information from the database
def get_admin():
    return admin_collection.find_one()

# Create a function to get the user information from the database
def get_user():
    return user_collection.find_one()

# Create a function to get the channel information from the database
def get_channel():
    return channel_collection.find_one()

# Create a function to get the group information from the database
def get_group():
    return group_collection.find_one()

# Create a function to save the owner information to the database
def save_owner(full_name, username, chat_id):
    owner_info = {
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id
    }
    owner_existed = owner_collection.find_one({"chat_id": chat_id}) is not None
    
    if owner_existed:
        owner_collection.update_one({"chat_id": chat_id}, {"$set": owner_info})
        
    else:
        owner_collection.insert_one(owner_info)

# Create a function to save the admin information to the database
def save_admin(full_name, username, chat_id):
    admin_info = {
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id
    }
    admin_existed = admin_collection.find_one({"chat_id": chat_id}) is not None
    owner = get_owner()
    chat_id = owner['chat_id']
    
    if admin_existed:
        admin_collection.update_one({"chat_id": chat_id}, {"$set": admin_info})
        bot.send_message(chat_id, f"Admin {full_name} (@{username}) updated successfully.")
    
    else:
        admin_collection.insert_one(admin_info)
        bot.send_message(chat_id, f"Admin {full_name} (@{username}) added successfully.")

# Create a function to save the user information to the database
def save_user(full_name, username, chat_id, total_users):
    user_info = {
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id,
        "total_users": total_users
    }
    user_existed = user_collection.find_one({"chat_id": chat_id}) is not None
    
    if user_existed:
        user_collection.update_one({"chat_id": chat_id}, {"$set": {"full_name": full_name, "username": username}})
        
    else:
        user_collection.insert_one(user_info)
        # Send message to owner when a new member joined

        # Get owner from collection
        owner = get_owner()
        logging.info(owner)
        user = get_user()
        logging.info(user)
        
        # Get chat ID from owner document
        chat_id = owner['chat_id']
        if chat_id != user['chat_id']:
            bot.send_message(chat_id, f"🔥 New member:\n\n👤 <b>{full_name}</b>\n\nTotal users: {total_users}", parse_mode='HTML' )
        

# Create a function to save the channel information to the database
def save_channel(full_name, username, chat_id):
    channel_info = {
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id
    }
    channel_existed = channel_collection.find_one({"chat_id": chat_id}) is not None
    
    if channel_existed:
        channel_collection.update_one({"chat_id": chat_id}, {"$set": channel_info})
        
    else:
        channel_collection.insert_one(channel_info)

# Create a function to save the group information to the database
def save_group(full_name, username, chat_id):
    group_info = {
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id
    }
    group_existed = group_collection.find_one({"chat_id": chat_id}) is not None
    
    if group_existed:
        group_collection.update_one({"chat_id": chat_id}, {"$set": group_info})
        
    else:
        group_collection.insert_one(group_info)
    

# Starts the bot code
try:
    logging.info("Bot is working!")

    #Welcome Message
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        if message.chat.type == "private":
            
            # User's informations
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name 
            if last_name:
                full_name = first_name + " " + last_name
            else:
                full_name = first_name
            
            username = message.from_user.username
            chat_id = message.chat.id
            
            # Set owner if it's the first user and there is one owner only
            if owner_collection.count_documents({}) == 0:
                save_owner(full_name, username, chat_id)
                bot.send_message(message.chat.id, f"Welcome <b>{full_name}</b>\nYou are my owner from now on", parse_mode='HTML')

            else:
                # Counting the number of the users
                total_users = user_collection.count_documents({}) + 1
                
                # Save the user info in the database
                save_user(full_name, username, chat_id, total_users)

                bot.send_message(message.chat.id, "هلا بالغالي")
        else:
            bot_username = bot.get_me().username
            if f"@{bot_username}" in message.text:
                bot.reply_to(message, "أهلا بكم في بوت الدعم الرجاء طرح مشكلتكم بشكل واضح ,لن نتأخر في الرد🌹.")

    #Admins control
    @bot.message_handler(commands=['admin'])
    def show_request_list(message):
        user_id = message.from_user.id

        # Check if the user is owner
        owner = get_owner()
        if user_id != owner['chat_id']:
            bot.reply_to(message, "Only the owner is allowed to use this command.")
            return

        bot.send_message(message.chat.id, "مرحبا بك في القائمة التعريفية للمشرفين:\n\n/ssettings - للتحكم بالقناة المراد النشر إليها\n\n/admins - أمر التحكم بالمشرفين خاص بالمالك\n\n/su - أمر الرسائل الجماعية خاص بالمالك\n\n/sc - أمر إرسال رسائل للقناة\n\n/userprofile - أمر للحصول على حساب مستخدم من رقم المعرف الخاص به")

    #Admins commands list
    @bot.message_handler(commands=['admins'])
    def admin_command(message):
        user_id = message.from_user.id
        
        # Check if the user is an admin
        owner = get_owner()
        if user_id != owner['chat_id']:
            bot.reply_to(message, "Only the owner is allowed to use this command.")
            return

        # Initial message with inline keyboard
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        add_admin_button = types.InlineKeyboardButton("Add Admin 🥷🏼", callback_data='add_admin')
        remove_admin_button = types.InlineKeyboardButton("Remove Admin ✖️", callback_data='remove_admin')
        show_admins_button = types.InlineKeyboardButton("Show Admins 📝", callback_data='show_admins')
        keyboard.add(add_admin_button, remove_admin_button, show_admins_button)

        bot.send_message(message.chat.id, "📊 Admins Control Panel:", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data == 'show_admins')
    def show_admins_callback(call):
        # Add a "Back" button
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_admin_menu')
        keyboard.add(back_button)

        # Get all admins info from the collection and send them as a message to the chat
        if admin_collection.count_documents({}) > 0:
            admin = admin_collection.find_one()
            admins = admin_collection.find()
            bot.edit_message_text("Admins:\n\n" + "- " + "\n\n- ".join([f"{admin['full_name']} (@{admin['username']})" for admin in admins]), call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')
        else:
            # There is no admins
            bot.send_message(call.message.chat.id, "There are no admins.")


        
    @bot.callback_query_handler(func=lambda call: call.data == 'add_admin')
    def add_admin_callback(call):
        # Add a "Back" button
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_admin_menu')
        keyboard.add(back_button)

        bot.edit_message_text("⏩ Forward a message from the user you want to add as an admin.", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

        # Set the next state to handle the forwarded message
        bot.register_next_step_handler(call.message, process_admin_forwarded_message)


    def process_admin_forwarded_message(message):
        # Check if message.forward_from exists and has necessary attributes
        if message.forward_from and hasattr(message.forward_from, 'id') and hasattr(message.forward_from, 'first_name'):
            # Extract user information from the forwarded message
            user_id = message.forward_from.id
            username = message.forward_from.username
            full_name = (
                f"{message.forward_from.first_name} {message.forward_from.last_name}"
                if message.forward_from.last_name
                else message.forward_from.first_name
            )

            save_admin(full_name, username, user_id)
            return
        else:
            bot.send_message(
                message.chat.id, "Error: The forwarded message doesn't contain valid user information. Make sure the account is not hidden."
            )



        # Ask the user to retry by setting the next step handler again
        bot.register_next_step_handler(message, process_admin_forwarded_message_retry)


    def process_admin_forwarded_message_retry(message):
        # Retry the same process to handle the forwarded message
        process_admin_forwarded_message(message)

    #Back Button
    @bot.callback_query_handler(func=lambda call: call.data == 'back_to_admin_menu')
    def back_to_admin_menu_callback(call):
        # End the waiting for the forwarded message
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        # Initial message with inline keyboard
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        add_admin_button = types.InlineKeyboardButton("Add Admin 🥷🏼", callback_data='add_admin')
        remove_admin_button = types.InlineKeyboardButton("Remove Admin ✖️", callback_data='remove_admin')
        show_admins_button = types.InlineKeyboardButton("Show Admins 📝", callback_data='show_admins')
        keyboard.add(add_admin_button, remove_admin_button, show_admins_button)

        bot.edit_message_text("📊 Admins Control Panel:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('remove_admin'))
    def remove_admin_callback(call):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        admins = admin_collection.find()
        admin = admin_collection.find_one()
        for admin in admins:
            button = types.InlineKeyboardButton(f"{admin['full_name']}", callback_data=f'remove_confirm_{admin["chat_id"]}')
            keyboard.add(button)


        # Add a "Back" button
        back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_admin_menu')
        keyboard.add(back_button)

        bot.edit_message_text("Select an admin to remove:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('remove_confirm_'))
    def remove_admin_decision_callback(call):
        admin_id = int(call.data.split('remove_confirm_')[1])
        fullname = admin_collection.find_one({'chat_id': admin_id})['full_name']
        username = admin_collection.find_one({'chat_id': admin_id})['username']
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        yes_button = types.InlineKeyboardButton("Yes ✅", callback_data=f'remove_yes_{admin_id}')
        back_button = types.InlineKeyboardButton("Back 🔙", callback_data=f'remove_back_{admin_id}')  # Add a Back button
        keyboard.add(yes_button, back_button)

        bot.edit_message_text(
            f"Are you sure you want to remove this admin:\n\nName: <b>{fullname}</b>\nUsername: @{username}\nUserID: <code>{admin_id}</code>\n\nThis action can't be undone ?",
            call.message.chat.id,
            call.message.message_id, parse_mode='HTML', reply_markup=keyboard
        )

    # Add a new callback handler for the "Back" button
    @bot.callback_query_handler(func=lambda call: call.data.startswith('remove_back_'))
    def remove_admin_back_callback(call):
        # Edit the message to show the "Select an admin ID to remove:" message
        remove_admin_callback(call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('remove_yes_'))
    def remove_admin_decision_callback(call):
        parts = call.data.split('_')

        # Check if there are enough parts to unpack
        if len(parts) >= 3:
            action, admin_id = parts[1], int(parts[2])  # Correct the unpacking

            if action == 'yes':
                # If the callback was yes, remove the admin from admin collection
                if admin_collection.find_one({'chat_id': admin_id}):
                    admin_collection.delete_one({'chat_id': admin_id})
                    bot.send_message(call.message.chat.id, f"Admin with ID {admin_id} removed successfully.")
                else:
                    bot.send_message(call.message.chat.id, f"Admin with ID {admin_id} not found.")
            elif action == 'back':
                remove_admin_callback(call)  # Go back to the "Select an admin ID to remove:" message
        else:
            bot.send_message(call.message.chat.id, "Invalid action data.")

    bot.infinity_polling()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")
    