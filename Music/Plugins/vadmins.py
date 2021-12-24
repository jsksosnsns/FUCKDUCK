from pyogram import Client, filters
 from pyrogram.types import (
     callbackQuery,
     InlineKeyboardButton,
     InlineKeyboardMarkup,
     messages,
 )

 from Music import app
 from Music.MusicUtilities.tgcallsrun.music import pytgcalls as call_py

 from Music.MusicUtilities.helpers.decorators import authorized_users_only
 from Music.MusicUtilities.helpers.filters import command
 from Music.MusicUtilities.tgcallsrun.queues import QUEUE, clear_queue
 from Music.MusicUtilities.tgcallsrun.video import skip_current_song, skip_item


 bttn = InlineKeyboardMarkup(
     [[InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data="cbmenu")]]
 )


 bcl = InlineKeyboardMarkup([[InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="cls")]])


 @Client.on_callback_query(filters.regex("cbmenu"))
 async def cbmenu(_, query: CallbackQuery):
     if query.message.sender_chat:
         return await query.answer(
             "You are **Anonymous Admin** !\n\n» back to user account from admin rights."
         )
     a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
     if not a.can_manage_voice_chats:
         return await query.answer(
             "💡 Only admins with voice chat manage permission can tap this button!",
             show_alert=True,
         )
     await query.edit_message_text(
         f"⚙️ **Settings from** {query.message.chat.title}\n\nII : Pause Streaming\n▷ : Continue Streaming\n🔇 : Mute Assistant\n🔊 : Unmute Assistant\n▢ : Stop Streaming"  ,
         reply_markup=InlineKeyboardMarkup(
             [
                 [
                     InlineKeyboardButton("▢", callback_data="cbstop"),
                     InlineKeyboardButton("II", callback_data="cbpause"),
                     InlineKeyboardButton("▷", callback_data="cbresume"),
                 ],
                 [
                     InlineKeyboardButton("🔇", callback_data="cbmute"),
                     InlineKeyboardButton("🔊", callback_data="cbunmute"),
                 ],
                 [InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="cls")],
             ]
         ),
     )


 @Client.on_callback_query(filters.regex("cls"))
 async def close(_, query: CallbackQuery):
     a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
     if not a.can_manage_voice_chats:
         return await query.answer(
             "💡 Only admins with voice chat manage permission can tap this button!",
             show_alert=True,
         )
     await query.message.delete()


 @app.on_message(command(["vskip"]) & filters.group)
 @authorized_users_only
 async def skip(client, m: Message):

     keyboard = InlineKeyboardMarkup(
         [
             [
                 InlineKeyboardButton(text="ᴍᴇɴᴜ", callback_data="cbmenu"),
             ]
         ]
     )

     chat_id = m.chat.id
     if len(m.command) < 2:
         op = await skip_current_song(chat_id)
         ifop == 0:
             await m.reply("❌ Nothing is playing")
         elif op == 1:
             await m.reply(
                 "✅ __Queue__ **empty.**\n\n**• Assistant left voice chat**"
             )
         elif op == 2:
             await m.reply(
                 "🗑️ **Clearing the Queue**\n\n**• Assistant leaves voice chat**"
             )
         else:
             await m.reply(
                 f"""
 ️ **Plays next {op[2]}**

 **Name:** [{op[0]}]({op[1]})
 **On request:** {m.from_user.mention()}
 """,
                 disable_web_page_preview=True,
                 reply_markup=keyboard,
             )
     else:
         skip = m.text.split(None, 1)[1]
         OP = "🗑 **Song removed from queue:**"
         if chat_id in QUEUE:
             items = [int(x) for x in skip.split(" ") if x.isdigit()]
             items.sort(reverse=True)
             for x in items:
                 if x == 0:
                     pass
                 else:
                     hm = await skip_item(chat_id, x)
                     if hm == 0:
                         pass
                     else:
                         OP = OP + "\n" + f"**#{x}** - {hm}"
             await m.reply(OP)


 @app.on_message(command(["vstop"]) & filters.group)
 @authorized_users_only
 async def stop(client, m: Message):
     chat_id = m.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.leave_group_call(chat_id)
             clear_queue(chat_id)
             await m.reply("✅ **Stream has ended.**")
         except Exception as e:
             await m.reply(f"**Error:**\n\n`{e}`")
     else:
         await m.reply("❌ **Not in stream**")


 @app.on_message(command(["vpause"]) & filters.group)
 @authorized_users_only
 async def pause(client, m: Message):
     chat_id = m.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.pause_stream(chat_id)
             await m.reply(
                 "II **Video is paused.**\n\n• **To resume video, use Command** » /vresume"
             )
         except Exception as e:
             await m.reply(f"**Error:**\n\n`{e}`")
     else:
         await m.reply("❌ **Not in stream**")


 @app.on_message(command(["vresume"]) & filters.group)
 @authorized_users_only
 async def resume(client, m: Message):
     chat_id = m.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.resume_stream(chat_id)
             await m.reply(
                 "▷ **Video resumes.**\n\n• **To pause the video, use Command** » /vpause"
             )
         except Exception as e:
             await m.reply(f"**Error:**\n\n`{e}`")
     else:
         await m.reply("❌ **Not in stream**")


 @app.on_message(command(["vmute"]) & filters.group)
 @authorized_users_only
 async def mute(client, m: Message):
     chat_id = m.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.mute_stream(chat_id)
             await m.reply(
                 "🔇 **Assistant is muted.**\n\n• **To activate Assistant voice, use Command**\n» /vunmute"
             )
         except Exception as e:
             await m.reply(f"**Error:**\n\n`{e}`")
     else:
         await m.reply("❌ **Not in stream**")


 @app.on_message(command(["vunmute"]) & filters.group)
 @authorized_users_only
 async def unmute(client, m: Message):
     chat_id = m.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.unmute_stream(chat_id)
             await m.reply(
                 "🔊 **Assistant enabled.**\n\n• **To disable user bots, use Command**\n» /vmute"
             )
         except Exception as e:
             await m.reply(f"**Error:**\n\n`{e}`")
     else:
         await m.reply("❌ **Not in stream**")


 @Client.on_callback_query(filters.regex("cbpause"))
 async def cbpause(_, query: CallbackQuery):
     if query.message.sender_chat:
         return await query.answer(
             "You are **Anonymous Admin** !\n\n» back to user account from admin rights."
         )
     a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
     if not a.can_manage_voice_chats:
         return await query.answer(
             "💡 Only admins with voice chat manage permission can tap this button!",
             show_alert=True,
         )
     chat_id = query.message.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.pause_stream(chat_id)
             await query.edit_message_text("II Stream has been paused", reply_markup=bttn)
         except Exception as e:
             await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
     else:
         await query.answer("❌ Nothing is streaming", show_alert=True)


 @Client.on_callback_query(filters.regex("cbresume"))
 async def cbresume(_, query: CallbackQuery):
     if query.message.sender_chat:
         return await query.answer(
             "You are **Anonymous Admin** !\n\n» back to user account from admin rights."
         )
     a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
     if not a.can_manage_voice_chats:
         return await query.answer(
             "💡 Only admins with voice chat manage permission can tap this button!",
             show_alert=True,
         )
     chat_id = query.message.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.resume_stream(chat_id)
             await query.edit_message_text(
                 "▷ Streaming has resumed", reply_markup=bttn
             )
         except Exception as e:
             await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
     else:
         await query.answer("❌ Nothing is streaming", show_alert=True)


 @Client.on_callback_query(filters.regex("cbstop"))
 async def cbstop(_, query: CallbackQuery):
     if query.message.sender_chat:
         return await query.answer(
             "You are **Anonymous Admin** !\n\n» back to user account from admin rights."
         )
     a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
     if not a.can_manage_voice_chats:
         return await query.answer(
             "💡 Only admins with voice chat manage permission can tap this button!",
             show_alert=True,
         )
     chat_id = query.message.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.leave_group_call(chat_id)
             clear_queue(chat_id)
             await query.edit_message_text(
                 "✅ **Stream has ended**", reply_markup=bcl
             )
         except Exception as e:
             await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
     else:
         await query.answer("❌ Nothing is streaming", show_alert=True)


 @Client.on_callback_query(filters.regex("cbmute"))
 async def cbmute(_, query: CallbackQuery):
     if query.message.sender_chat:
         return await query.answer(
             "You are **Anonymous Admin** !\n\n» back to user account from admin rights."
         )
     a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
     if not a.can_manage_voice_chats:
         return await query.answer(
             "💡 Only admins with voice chat manage permission can tap this button!",
             show_alert=True,
         )
     chat_id = query.message.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.mute_stream(chat_id)
             await query.edit_message_text(
                 "🔇 Assistant successfully shut down", reply_markup=bttn
             )
         except Exception as e:
             await query.edit_message_text(f"***Error:**\n\n`{e}`", reply_markup=bcl)
     else:
         await query.answer("❌ Nothing is streaming", show_alert=True)


 @Client.on_callback_query(filters.regex("cbunmute"))
 async def cbunmute(_, query: CallbackQuery):
     if query.message.sender_chat:
         return await query.answer(
             "You are **Anonymous Admin** !\n\n» back to user account from admin rights."
         )
     a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
     if not a.can_manage_voice_chats:
         return await query.answer(
             "💡 Only admins with voice chat manage permission can tap this button!",
             show_alert=True,
         )
     chat_id = query.message.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.unmute_stream(chat_id)
             await query.edit_message_text(
                 "🔊 Assistant sounded successfully", reply_markup=bttn
             )
         except Exception as e:
             await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
     else:
         await query.answer("❌ Nothing is streaming", show_alert=True)


 @app.on_message(command(["volume", "vol"])))
 @authorized_users_only
 async def change_volume(client, m: Message):
     range = m.command[1]
     chat_id = m.chat.id
     if chat_id in QUEUE:
         try:
             await call_py.change_volume_call(chat_id, volume=int(range))
             await m.reply(f"✅ **Volume set to** `{range}`%")
         except Exception as e:
             await m.reply(f"**Error:**\n\n`{e}`")
     else:
         await m.reply("❌ **Not in stream**")