from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import (get_user, get_zayavka, get_events, get_event, delete_event, edit_event_photo, edit_event_desc, edit_event_name,
                      delete_zayavka_all, get_rejects, edit_event_count)


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Админ-панель")
        ]
    ], resize_keyboard=True
)

register_url = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Зарегистрироваться", url="https://t.me/zayavkichinazes_bobot")
        ]
    ]
)

user_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена", callback_data="user_cancel")
        ]
    ]
)

admin_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена", callback_data="admin_cancel")
        ]
    ]
)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Записи", callback_data="get_excel")
        ],
        [
            InlineKeyboardButton(text="Создать мероприятие", callback_data="add_event")
        ],
        [
            InlineKeyboardButton(text="Редактировать мероприятие", callback_data="all_events")
        ],
        [
            InlineKeyboardButton(text="Список отклонений", callback_data="reject_list")
        ]
    ]
)

ad_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="admin_back")
        ]
    ]
)

async def check_register(user_id, zayavka_id, event_id):
    user = await get_user(user_id)
    zayavka = await get_zayavka(zayavka_id)
    event = await get_event(event_id)
    kb = InlineKeyboardBuilder()
    if user and zayavka and event:
        kb.add(InlineKeyboardButton(text="✅Принять", callback_data=f"accept_register_{zayavka_id}_{user_id}_{event_id}"))
        kb.add(InlineKeyboardButton(text="❌Отклонить", callback_data=f"decline_register_{zayavka_id}_{user_id}_{event_id}"))
    return kb.as_markup()

async def all_events_cb():
    events = await get_events()
    kb = InlineKeyboardBuilder()
    for event in events:
        kb.add(InlineKeyboardButton(text=f'{event[2]}', callback_data=f"event_{event[0]}"))
    return kb.as_markup()

async def all_events_admin_ex_cb():
    events = await get_events()
    kb = InlineKeyboardBuilder()
    for event in events:
        kb.add(InlineKeyboardButton(text=f'{event[2]}', callback_data=f"eventadminsec_{event[0]}"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="admin_back"))
    return kb.as_markup()

async def all_events_admin_cb():
    events = await get_events()
    kb = InlineKeyboardBuilder()
    for event in events:
        kb.row(InlineKeyboardButton(text=f'{event[2]}', callback_data=f"eventadmin_{event[0]}"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="admin_back"))
    return kb.as_markup()

async def register_cb(event_id):
    event = await get_event(event_id)
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=f'Зарегистрироваться', callback_data=f"eventregister_{event[0]}"))
    return kb.as_markup()

async def delete_event_cb(event_id):
    kb = InlineKeyboardBuilder()
    event = await get_event(event_id)
    kb.button(text=f"❌Удалить", callback_data=f'delete_{event_id}')
    await edit_event_name(event_id, f"{event[2]}")
    kb.button(text=f"Редактировать название", callback_data=f'edit_name_{event_id}')
    await edit_event_desc(event_id, f"{event[3]}")
    kb.button(text=f"Редактировать описание", callback_data=f'edit_description_{event_id}')
    await edit_event_photo(event_id, f"{event[1]}")
    kb.button(text=f"Редактировать фото", callback_data=f'edit_photo_{event_id}')
    await edit_event_count(event_id, f"{event[4]}")
    kb.button(text=f"Редактировать ограничение", callback_data=f'edit_count_{event_id}')
    kb.adjust(1)
    kb.row(InlineKeyboardButton(text='🔙Назад', callback_data='admin_back'))
    return kb.as_markup()

async def reject_list_admin_cb():
    rejects = await get_rejects()
    kb = InlineKeyboardBuilder()
    for reject in rejects:
        kb.row(InlineKeyboardButton(text=f'{reject[1]}', callback_data=f"rejectadmin_{reject[0]}"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="admin_back"))
    return kb.as_markup()

skate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="skate_yes"),
            InlineKeyboardButton(text="Нет", callback_data="skate_no")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="user_cancel")
        ]
    ]
)

helmet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="helmet_yes"),
            InlineKeyboardButton(text="Нет", callback_data="helmet_no")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="user_cancel")
        ]
    ]
)

deffender = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="deffender_yes"),
            InlineKeyboardButton(text="Нет", callback_data="deffender_no")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="user_cancel")
        ]
    ]
)

links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Связаться с администратором для уточнения информации.", url="https://t.me/stmnkvc")
        ]
    ]
)