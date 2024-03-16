# -*- coding: utf-8 -*-
import telebot, logging, json
from telebot import types, util
from logging.handlers import RotatingFileHandler

bot = telebot.TeleBot("6137336827:AAExYT6TMaL3u2pKtpnYSucJU6zAbJ4h6nQ")

# Starts the bot code
try:
  
  # Existing logging configuration
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

  # RotatingFileHandler
  max_log_size_mb = 5  # Set your desired maximum log size in megabytes
  handler = RotatingFileHandler('bot.log', maxBytes=max_log_size_mb * 1024 * 1024, backupCount=1)
  handler.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  logging.getLogger().addHandler(handler)
  
  # Load channel username from file
  try:
    with open('channel_username.json', 'r') as chuser_file:
        CHANNEL_USERNAME = json.load(chuser_file).get('channel_username', [])
  except FileNotFoundError:
    CHANNEL_USERNAME = []
  
  # Save channel username to file
  def save_owner_id_to_file():
    with open('channel_username.json', 'w') as chuser_file:
        json.dump({'channel_username': CHANNEL_USERNAME}, chuser_file, indent=4)
  
  # Read from the log file
  try:
    with open('bot.log', 'r') as log_file:
        log_contents = log_file.read()
        logging.info(f'Read from log file:\n{log_contents}')
  except FileNotFoundError:
    logging.warning('Log file not found.')
  
  # Write to the log file
  try:
    with open('bot.log', 'a') as log_file:
        log_file.write('New log entry: This is a write operation.\n')
        logging.info('Write to log file: New log entry added.')
  except FileNotFoundError:
    logging.error('Log file not found. Unable to write.')

  # Load owner ID from file
  try:
    with open('owner_id.json', 'r') as owner_file:
        OWNER_ID = json.load(owner_file).get('owner_id', [])
  except FileNotFoundError:
    OWNER_ID = []

  # Save owner ID to file
  def save_owner_id_to_file():
    with open('owner_id.json', 'w') as owner_file:
        json.dump({'owner_id': OWNER_ID}, owner_file, indent=4)

  # Load admin info from file
  try:
    with open('admin_ids.json', 'r') as admin_file:
        admin_data = json.load(admin_file).get('admin_info', {})
        ADMIN_INFO = {admin.get('full_name'): [admin.get('full_name'), admin.get('username'), admin.get('id')] for admin in admin_data}
  except (FileNotFoundError, json.JSONDecodeError):
    ADMIN_INFO = {}

  # Save admin info to file
  def save_admin_info_to_file():
    admin_data = [{'full_name': user_data[0], 'username': user_data[1], 'id': user_data[2]} for user_data in ADMIN_INFO.values()]
    with open('admin_ids.json', 'w') as admin_file:
        json.dump({'admin_info': admin_data}, admin_file, indent=4)

  # Load chat IDs from file
  try:
    with open('chat_ids.json', 'r') as file:
        CHAT_IDS = json.load(file)
  except FileNotFoundError:
    CHAT_IDS = []

  # Save chat IDs to file
  def save_chat_ids_to_file():
    with open('chat_ids.json', 'w') as file:
        json.dump(CHAT_IDS, file, indent=4)

#   # Load Game Requests from file
#   try:
#     with open('game_requests.json', 'r') as file:
#         GAME_REQUESTS = json.load(file)
#   except FileNotFoundError:
#     pass
# 
#   # Save Games Requests to file
#   def save_requests_to_file():
#     with open('game_requests.json', 'w') as file:
#         json.dump(GAME_REQUESTS, file, indent=4)

  logging.info("Bot is working!")
  
  #Welcome Message
  @bot.message_handler(commands=['start'])
  def send_welcome(message):
    if message.chat.type == "private":
        chat_id = message.chat.id
        if chat_id not in CHAT_IDS:
            CHAT_IDS.append(chat_id)
            save_chat_ids_to_file()

        bot.reply_to(message, "أهلا بكم في بوت الدعم الرجاء طرح مشكلتكم بشكل واضح ,لن نتأخر في الرد🌹.")
        bot.send_message(message.chat.id, "تفضل")
    else:
        bot_username = bot.get_me().username
        if f"@{bot_username}" in message.text:
            bot.reply_to(message, "أهلا بكم في بوت الدعم الرجاء طرح مشكلتكم بشكل واضح ,لن نتأخر في الرد🌹.")

  # To show the user profile by its id if possible
  @bot.message_handler(commands=['userprofile'])
  def send_user_link(message):
    user_id = message.from_user.id

    # Check if the user is an admin
    if user_id not in OWNER_ID:
        bot.reply_to(message, "Only the owner is allowed to use this command.")
        return

    bot.reply_to(message, "Please send the user ID you want to generate a link for.")

    # Set the next state to handle the forwarded message
    bot.register_next_step_handler(message, process_user_id)

  def process_user_id(message):
    try:
        # Check if the message contains a valid user ID
        user_id = int(message.text)

        # Generate the user link in the message text
        user_link = f"[Click here to view user](tg://user?id={user_id})"

        # Reply with the generated user link
        bot.reply_to(message, user_link, parse_mode='Markdown')
    except ValueError:
        bot.reply_to(message, "Invalid user ID. Please provide a valid numerical user ID.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
  
  @bot.message_handler(commands=['ssettings'])
  def send_sertinga(message):
    user_id = message.from_user.id
    # Check if the user is the owner
    if user_id not in OWNER_ID:
        bot.reply_to(message, "Only the owner is allowed to use this command.")
    else:
        # Set sending settings
        # Initial message with inline keyboard
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        channel_username_button = types.InlineKeyboardButton("Set channel username", callback_data='set_channel_username')
        show_channel_button = types.InlineKeyboardButton("Show channel", callback_data='show_channel')
        keyboard.add(channel_username_button, show_channel_button)
        
        bot.send_message(message.chat.id, "Channel Setting", reply_markup=keyboard)
  
  @bot.callback_query_handler(func=lambda call: call.data == 'set_channel_username')
  def set_channel_username_callback(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu')
    keyboard.add(back_button)
  
    bot.edit_message_text("Send your channel username", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')
  
    # Set the next state to handle the channel username message
    bot.register_next_step_handler(call.message, process_channel_username)
    
  def process_channel_username(message):
    try:
        if message.text.startswith('@'):
            # Open the channel_username.json file and save the username given in the message
            with open('channel_username.json', 'w') as file:
                data = {'channel_username': message.text}  # Remove the '@' from the username
                json.dump(data, file)
            # Confirm successful set
            bot.send_message(message.chat.id, f"Channel username set to {message.text}")
        else:
            bot.send_message(message.chat.id, "Wrong format:\nPlease provide a valid username.")
    except Exception as e:
        # Show error message to the user 
        bot.send_message(message.chat.id, f"Error: {str(e)}")
  
  @bot.callback_query_handler(func=lambda call: call.data == 'show_channel')
  def show_channel_callback(call):
    try:
        # Load channel username from file
        with open('channel_username.json', 'r') as chuser_file:
            channel_username = json.load(chuser_file).get('channel_username', None)
  
        if channel_username:
            # Add a back button to go back
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu')
            keyboard.add(back_button)
            
            # Display the channel username
            bot.edit_message_text(f"Channel username: {channel_username}", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
  
        else:
            bot.send_message(call.message.chat.id, "Channel username not set.")
  
    except Exception as e:
        # Show error message to the user
        bot.send_message(call.message.chat.id, f"Error: {str(e)}")
  
  @bot.callback_query_handler(func=lambda call: call.data == 'back_to_main_menu')
  def back_to_main_menu_callback(call):
    # End the waiting for the forwarded message
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
  
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    channel_username_button = types.InlineKeyboardButton("Set channel username", callback_data='set_channel_username')
    show_channel_button = types.InlineKeyboardButton("Show channel", callback_data='show_channel')
    keyboard.add(channel_username_button, show_channel_button)
  
    bot.edit_message_text("Channel Settings", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
  
  # Handler for the sending to channels command
  @bot.message_handler(commands=['sc'])
  def send_channel(message):
      user_id = message.from_user.id
      # Check if the user is the owner
      if user_id not in OWNER_ID:
          bot.reply_to(message, "Only the owner is allowed to use this command.")
      else:
          # Set the user's state to waiting for input
          bot.register_next_step_handler(message, process_button_data)
  
          # Ask the owner for button data
          bot.send_message(message.chat.id, "Please provide the message and the button data as a text message in the following format:\n\nButton Name - URL\nMessage Text")
  
  def process_button_data(message):
    try:
        if '-' in message.text:
            button_data_str, button_description = map(str.strip, message.text.split('\n', 1))
            button_data_list = [button.strip().split() for button in button_data_str.split('-')]
  
            inline_keyboard = types.InlineKeyboardMarkup()
  
            for i in range(0, len(button_data_list), 2):
                row_buttons = button_data_list[i:i + 2]
                row = [types.InlineKeyboardButton(text=name, url=url) for name, url in row_buttons]
                inline_keyboard.row(*row)
  
            # Load channel ID from file
            try:
                with open('channel_username.json', 'r') as chuser_file:
                    channel_username = json.load(chuser_file).get('channel_username', None)
  
                if channel_username:
                    # Send message to the channel with inline keyboard
                    bot.send_message(channel_username, button_description, reply_markup=inline_keyboard)
  
                    bot.send_message(message.chat.id, "Button data sent to the channel. You can now add more buttons.")
  
                else:
                    bot.send_message(message.chat.id, "Channel ID not found. Make sure the channel is set.")
            except FileNotFoundError:
                bot.send_message(message.chat.id, "Channel ID file not found. Make sure the channel is set.")
  
        else:
            bot.send_message(message.chat.id, "Invalid format. Please provide button data as 'Button1 Name URL - Button2 Name URL - ...'")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")
  
  #Send messages to the bot subscribers
  @bot.message_handler(commands=['su'])
  def send_message_to_all(message):
    user_id = message.from_user.id
  
    # Check if the user is an admin
    if user_id not in OWNER_ID:
        bot.reply_to(message, "Only admins are allowed to use this command.")
        return
  
    try:
        # Extract the message content
        message_content = message.text.split('/su ', 1)[1]
  
        # Send the message to all stored chat IDs
        for chat_id in CHAT_IDS:
            try:
                bot.send_message(chat_id, message_content)
            except telebot.apihelper.ApiTelegramException as e:
                if e.error_code == 403:
                    if "Forbidden: user is deactivated" in e.description:
                        logging.warning(f"Skipping deactivated user with chat_id: {chat_id}")
                    elif "Forbidden: bot was blocked by the user" in e.description:
                        logging.warning(f"Bot was blocked by user with chat_id: {chat_id}")
                    else:
                        raise
  
        bot.reply_to(message, f"Message sent to {len(CHAT_IDS) - 1} chats.")
    except IndexError:
        bot.reply_to(message, "Please provide a message content after the /su command.")
  
  # GroupSilencer
  @bot.message_handler(content_types=['new_chat_members'])
  def delete_join_message(m):
    try:
        bot.delete_message(m.chat.id, m.message_id)
    except:
        if m.new_chat_member.id != bot.get_me().id:
            bot.send_message(m.chat.id, "Please make me an admin to remove the join and leave messages in this group!")
        else:
            bot.send_message(m.chat.id, "Hi! I am your trusty GroupSilencer Bot! Thanks for adding me! To use me, make me an admin, and I will be able to delete all the pesky notifications when a member joins or leaves the group!")

#   @bot.message_handler(func=lambda message: message.text and message.text.startswith("#request "))
#   def handle_game_request(message):
#     game_name = message.text.split("#request ")[1].strip()
#     user_id = message.from_user.id
#     user_name = f"{message.from_user.first_name} {message.from_user.last_name}" if message.from_user.last_name else message.from_user.first_name
#     chat_id = message.chat.id
#     if game_name in GAME_REQUESTS:
#         for existing_user_id, existing_chat_id, _ in GAME_REQUESTS.get(game_name, []):
#             if existing_user_id == user_id and existing_chat_id == chat_id:
#                 bot.reply_to(message, f"Your request for '{game_name}' has already been submitted.")
#                 return
#     if game_name not in GAME_REQUESTS:
#         GAME_REQUESTS[game_name] = [(user_id, chat_id, user_name)]
#     else:
#         GAME_REQUESTS[game_name].append((user_id, chat_id, user_name))
#     reply_message = f"Your request for '{game_name}' has been submitted!"
#     bot.reply_to(message, reply_message, parse_mode='Markdown')
#     save_requests_to_file()
# 
#   @bot.message_handler(commands=['reqlist'])
#   def show_request_list(message):
#     user_id = message.from_user.id
# 
#     # Check if the user is an admin
#     if user_id not in OWNER_ID and user_id not in [admin_data[2] for admin_data in ADMIN_INFO.values()]:
#         bot.reply_to(message, "Only admins are allowed to use this command.")
#         return
# 
#     if not GAME_REQUESTS:
#         bot.send_message(message.chat.id, 'There are no requests at this time.')
#     else:
#         keyboard = types.InlineKeyboardMarkup(row_width=1)
#         for game_name in GAME_REQUESTS:
#             button = types.InlineKeyboardButton(game_name, callback_data=f'show_{game_name}')
#             keyboard.add(button)
#         bot.send_message(message.chat.id, 'Game Requests:', reply_markup=keyboard)
#         
#   # Members Request List
#   @bot.message_handler(commands=['request'])
#   def view_requested_games(message):
#     if not GAME_REQUESTS:
#         bot.send_message(message.chat.id, 'لايوجد طلبات قيد الانتظار في الوقت الحالي.')
#     else:
#         # Enumerate and sort the requested games based on game names
#         sorted_games = sorted(enumerate(GAME_REQUESTS.items(), start=1), key=lambda x: x[0])
# 
#         # Display the sorted list with numbers
#         response_text = "\n".join([f"{number}- {game} : {len(users)} requests" for number, (game, users) in sorted_games])
#         bot.send_message(message.chat.id, f'قائمة الألعاب قيد الانتظار:\n{response_text}')

  #Admins control
  @bot.message_handler(commands=['admin'])
  def show_request_list(message):
    user_id = message.from_user.id

    # Check if the user is an admin
    if user_id not in OWNER_ID and user_id not in [admin_data[2] for admin_data in ADMIN_INFO.values()]:
        bot.reply_to(message, "Only admins are allowed to use this command.")
        return

    bot.send_message(message.chat.id, "مرحبا بك في القائمة التعريفية للمشرفين:\n\n/ssettings - للتحكم بالقناة المراد النشر إليها\n\n/admins - أمر التحكم بالمشرفين خاص بالمالك\n\n/su - أمر الرسائل الجماعية خاص بالمالك\n\n/sc - أمر إرسال رسائل للقناة\n\n/userprofile - أمر للحصول على حساب مستخدم من رقم المعرف الخاص به")
    
  #Admins commands list
  @bot.message_handler(commands=['admins'])
  def admin_command(message):
    user_id = message.from_user.id
     # Check if the user is an admin
    if user_id not in OWNER_ID:
        bot.reply_to(message, "Only the owner is allowed to use this command.")
        return
 
    # Initial message with inline keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    add_admin_button = types.InlineKeyboardButton("Add Admin 🥷🏼", callback_data='add_admin')
    remove_admin_button = types.InlineKeyboardButton("Remove Admin ✖️", callback_data='remove_admin')
    show_admins_button = types.InlineKeyboardButton("Show Admins 📝", callback_data='show_admins')
    keyboard.add(add_admin_button, remove_admin_button, show_admins_button)
    
    bot.send_message(message.chat.id, "Admins", reply_markup=keyboard)

  @bot.callback_query_handler(func=lambda call: call.data == 'show_admins')
  def show_admins_callback(call):
    try:
        with open('admin_ids.json', 'r') as admin_file:
            admin_data = json.load(admin_file).get('admin_info', [])

            if not admin_data:
                bot.send_message(call.message.chat.id, 'No admins found.')
            else:
                admins_list = "\n".join([f"Fullname: {admin.get('full_name')}\nUsername: @{admin.get('username')}\nID: {admin.get('id')}\n"
                                         for admin in admin_data])
                bot.send_message(call.message.chat.id, f'Admins:\n{admins_list}')
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, 'Admins file not found.')
    except json.JSONDecodeError:
        bot.send_message(call.message.chat.id, 'Error decoding admin_ids.json. Please check the file format.')
    except Exception as e:
        bot.send_message(call.message.chat.id, f'An error occurred: {str(e)}')
        
  @bot.callback_query_handler(func=lambda call: call.data == 'add_admin')
  def add_admin_callback(call):
    # Add a "Back" button
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_admin_menu')
    keyboard.add(back_button)

    bot.edit_message_text("Forward a message from the user you want to add as an admin.", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

    # Set the next state to handle the forwarded message
    bot.register_next_step_handler(call.message, process_admin_forwarded_message)


  def process_admin_forwarded_message(message):
    try:
        # Check if message.forward_from exists and has necessary attributes
        if message.forward_from and hasattr(message.forward_from, 'id') and hasattr(message.forward_from, 'first_name'):
            # Extract user information from the forwarded message
            user_id = message.forward_from.id
            full_name = (
                f"{message.forward_from.first_name} {message.forward_from.last_name}"
                if message.forward_from.last_name
                else message.forward_from.first_name
            )
            username = message.forward_from.username

            # Check if the full name already exists in ADMIN_INFO
            if full_name in ADMIN_INFO:
                # Update the existing entry
                ADMIN_INFO[full_name] = [full_name, username, user_id]
            else:
                # Add a new entry
                ADMIN_INFO[full_name] = [full_name, username, user_id]

            save_admin_info_to_file()

            bot.send_message(
                message.chat.id, f"Admin {full_name} (@{username}) added successfully."
            )
        else:
            bot.send_message(
                message.chat.id, "Error: The forwarded message doesn't contain valid user information. Make sure the account is not hidden."
            )

    except AttributeError as e:
        logging.error(f"Error processing forwarded message: {e}")

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

    bot.edit_message_text("Admins", call.message.chat.id, call.message.message_id, reply_markup=keyboard)


  @bot.callback_query_handler(func=lambda call: call.data.startswith('remove_admin'))
  def remove_admin_callback(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for admin_name, (_, _, admin_id) in ADMIN_INFO.items():
        button = types.InlineKeyboardButton(f"{admin_name} - ID: {admin_id}", callback_data=f'remove_confirm_{admin_id}')
        keyboard.add(button)

    # Add a "Back" button
    back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_admin_menu')
    keyboard.add(back_button)

    bot.edit_message_text("Select an admin to remove:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    bot.edit_message_text("Select an admin ID to remove:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

  @bot.callback_query_handler(func=lambda call: call.data.startswith('remove_confirm_'))
  def remove_admin_decision_callback(call):
    admin_id = int(call.data.split('remove_confirm_')[1])
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    yes_button = types.InlineKeyboardButton("Yes ✅", callback_data=f'remove_yes_{admin_id}')
    back_button = types.InlineKeyboardButton("Back 🔙", callback_data=f'remove_back_{admin_id}')  # Add a Back button
    keyboard.add(yes_button, back_button)

    bot.edit_message_text(
        f"Are you sure you want to remove admin with ID {admin_id}?",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
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
            if admin_id in [admin_data[2] for admin_data in ADMIN_INFO.values()]:
                admins_to_remove = [key for key, admin_data in ADMIN_INFO.items() if admin_data[2] == admin_id]
                for key in admins_to_remove:
                    del ADMIN_INFO[key]
                save_admin_info_to_file()
                bot.send_message(call.message.chat.id, f"Admin with ID {admin_id} removed successfully.")
            else:
                bot.send_message(call.message.chat.id, f"Admin with ID {admin_id} not found.")
        elif action == 'back':
            remove_admin_callback(call)  # Go back to the "Select an admin ID to remove:" message
    else:
        bot.send_message(call.message.chat.id, "Invalid action data.")

#   @bot.callback_query_handler(func=lambda call: call.data.startswith('show_'))
#   def show_game_info(call):
#     game_name = call.data.split('show_')[1]
#     users_list = ', '.join(
#         f"[{user_name}](tg://user?id={user_id})" for user_id, _, user_name in GAME_REQUESTS.get(game_name, []))
# 
#     # Log information
#     logging.info(f'Showing game info for {game_name}')
# 
#     # Create inline buttons for options, including a "Back" buttons
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(types.InlineKeyboardButton('Back to List 🔙', callback_data='back_to_list'),
#              types.InlineKeyboardButton('Delete Request 🗑', callback_data=f'delete_{game_name}'))
# 
#     bot.edit_message_text(
#         f'Who requested {game_name}:\n{users_list}',
#         call.message.chat.id,
#         call.message.message_id,
#         reply_markup=keyboard,
#         parse_mode='Markdown'
#     )
# 
#   @bot.callback_query_handler(func=lambda call: call.data == 'back_to_list')
#   def back_to_list_callback(call):
#     # Log information
#     logging.info('Going back to the request list')
# 
#     # Create inline buttons for the updated request list
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     for updated_game_name in GAME_REQUESTS:
#         button = types.InlineKeyboardButton(updated_game_name, callback_data=f'show_{updated_game_name}')
#         keyboard.add(button)
# 
#     # Edit the original message to show the updated request list with inline buttons
#     bot.edit_message_text(
#         'Game Requests:',
#         call.message.chat.id,
#         call.message.message_id,
#         reply_markup=keyboard,
#     )
# 
#     # Log information about editing the message
#     logging.info('Edited the message to show the request list')
# 
#   @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
#   def button_callback(call):
#     action, game_name = call.data.split('_')
#     
#     # Log information
#     logging.info(f'Deleted {game_name} request') 
#     
#     original_message_id = call.message.message_id
#     original_chat_id = call.message.chat.id
# 
#     if action == 'delete':
#         del GAME_REQUESTS[game_name]
#         save_requests_to_file()
# 
#         # Check if there are remaining requests
#         if not GAME_REQUESTS:
#             # If no requests, send the appropriate message
#             bot.edit_message_text(
#                 'There is no requests at this time.',
#                 original_chat_id,
#                 original_message_id
#             )
#         else:
#             # Create inline buttons for the updated request list
#             keyboard = types.InlineKeyboardMarkup(row_width=1)
#             for updated_game_name in GAME_REQUESTS:
#                 button = types.InlineKeyboardButton(updated_game_name, callback_data=f'show_{updated_game_name}')
#                 keyboard.add(button)
# 
#             # Edit the original message to show the updated request list with inline buttons
#             bot.edit_message_text(
#                 'Game Requests:',
#                 original_chat_id,
#                 original_message_id,
#                 reply_markup=keyboard,
#             )
# 
#         # Log information about editing the message
#         logging.info('Edited the message to show the request list')

  bot.infinity_polling()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")
