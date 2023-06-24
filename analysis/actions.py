from analysis.amplitude import amp, logger


async def send_and_log(event_name, id, event_properties=None, user_properties=None):
    try:
        await amp.log(id, event_name,
                      event_properties=event_properties,
                      user_properties=user_properties)
        logger.info(f"id: {id},\n"
                    f"event_name: {event_name},\n"
                    f"event_properties: {event_properties},\n"
                    f"user_properties: {user_properties}\n")
    except Exception as error:
        logger.error(f"Error: {error}")


async def amplitude_get_char_data(user_id, char_id):
    event_name = "Web site backend get created bot data settings"
    event_properties = {"character_id": char_id}
    user_properties = {"user_id": user_id}
    await send_and_log(event_name, user_id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def amplitude_char_data_insert(user_id, char_id):
    event_name = "Web site backend INSERT INTO db created bot data "
    event_properties = {"character_id": char_id}
    user_properties = {"user_id": user_id}
    await send_and_log(event_name, user_id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def amplitude_press_publick_bots_button(user_id):
    event_name = "User press public_bots button"
    user_properties = {"user_id": user_id}
    await send_and_log(event_name, user_id,
                       user_properties=user_properties)


async def amplitude_event_message(user_id, event_name: str):
    user_properties = {"user_id": user_id}
    await send_and_log(event_name, user_id,
                       user_properties=user_properties)


async def amplitude_site_loaded(user_id, event_name: str,
                                site_tab: str, bg_color: str,
                                text_color: str,
                                hint_color: str,
                                link_color: str,
                                button_color: str,
                                backgound_color: str):
    user_properties = {"user_id": user_id}
    event_properties = {"site_tab": site_tab,
                        "theme": bg_color,
                        "text_color": text_color,
                        "hint_color": hint_color,
                        "link_color": link_color,
                        "button_color": button_color,
                        "backgound_color": backgound_color}
    await send_and_log(event_name, user_id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def amplitude_user_not_found(user_id):
    event_name = """User not found when change
    character for user_id Stage 6 onboarding
    """
    user_properties = {"user_id": user_id}
    await send_and_log(event_name, user_id,
                       user_properties=user_properties)


async def amplitude_choose_char_msg(user_id, char_id):
    event_name = "User chose a character from available bots (Stage 6 onboarding)"
    event_properties = {"character_id": char_id}
    user_properties = {"user_id": user_id}
    await send_and_log(event_name, user_id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def amplitude_error(user_id,
                          event_name="error"):
    if event_name != "error":
        event_name = "error_" + event_name
    event_properties = {"error": event_name}
    user_properties = {"user_id": user_id}
    await send_and_log(event_name, user_id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def amplitude_answer_saved_to_db(message, answer):
    event_name = "Response saved to database"
    event_properties = {"message_answer": answer}
    user_properties = {"username": message.from_user.username,
                       "first_name": message.from_user.first_name,
                       "last_name": message.from_user.last_name}
    await send_and_log(event_name, message.from_user.id,
                       event_properties=event_properties,
                       user_properties=user_properties)
