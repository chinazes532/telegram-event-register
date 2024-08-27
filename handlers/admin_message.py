from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.types.input_file import FSInputFile

from config import ADMIN_ID
import keyboards as kb
from database import (delete_zayavka, create_db, insert_event, get_event,
                      delete_event, edit_event_photo, edit_event_desc, edit_event_name, delete_zayavka_all, insert_zayavka,
                      insert_accepted, get_zayavka, insert_rejected, get_reject, edit_event_count, get_accept, delete_zayavka)

import sqlite3 as sq
import pandas as pd

router = Router()

class Reject(StatesGroup):
    reason = State()

class AddEvent(StatesGroup):
    event_name = State()
    event_description = State()
    event_photo = State()
    event_count = State()

    new_event_name = State()
    new_event_description = State()
    new_event_photo = State()
    new_event_count = State()


@router.message(F.text == 'Админ-панель')
async def admin_panel(message: Message):
    for admin_id in ADMIN_ID:
        if admin_id == message.from_user.id:
            await message.answer('Добро пожаловать в админ-панель!\n'
                                 'Выберите действие:',
                                 reply_markup=kb.admin_panel)


@router.callback_query(F.data == 'get_excel')
async def get_all_exel_asa(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите контест',
                                        reply_markup=await kb.all_events_admin_ex_cb())

@router.callback_query(F.data.startswith('eventadminsec_'))
async def event_admin(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    event_id = int(callback.data.split('_')[1])
    event = await get_event(event_id)
    global db, cur
    db = sq.connect('zayavka.db')
    cur = db.cursor()
    query = f"SELECT * FROM accepted WHERE event_id = {event_id}"
    df = pd.read_sql_query(query, db)

    # Запись данных в Excel файл
    df.to_excel(f'{event[2]}.xlsx', index=False)

    await callback.message.answer_document(FSInputFile(f'{event[2]}.xlsx'),
                                           caption=f'Список заявок на <b>{event[2]}</b>',
                                           reply_markup=kb.ad_back,
                                           parse_mode='HTML')
    db.close()


@router.callback_query(F.data == 'admin_back')
async def admin_back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Вы вернулись в меню.",
                                  reply_markup=kb.admin_panel)

@router.callback_query(F.data.startswith('accept_register_'))
async def accept_register(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split('_')[3])
    zayavka_id = int(callback.data.split('_')[2])
    event_id = int(callback.data.split('_')[4])
    event = await get_event(event_id)
    accept = await get_accept(zayavka_id)
    zayavka = await get_zayavka(zayavka_id)
    if not accept:
        await callback.message.delete()
        await bot.send_message(chat_id=user_id,
                               text=f"Ваша регистрация на мероприятие <b>{event[2]}</b> принята!\n"
                                    f"Ждем Вас!",
                               parse_mode='HTML')
        await callback.message.answer("Вы приняли заявку",
                                      reply_markup=kb.admin_menu)
        await insert_accepted(zayavka_id=zayavka_id,
                              full_name=zayavka[1],
                              date_age=zayavka[2],
                              rider_exp=zayavka[3],
                              skate=zayavka[4],
                              helmet=zayavka[5],
                              deffender=zayavka[6],
                              parents_name=zayavka[7],
                              parents_contact=zayavka[8],
                              event_id=event_id)
    else:
        await callback.message.delete()
        await callback.message.answer("Другой администратор уже рассмотрел заявку!")


@router.callback_query(F.data.startswith('decline_register_'))
async def decline_register(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = int(callback.data.split('_')[3])
    zayavka_id = int(callback.data.split('_')[2])
    event_id = int(callback.data.split('_')[4])
    zayavka = await get_zayavka(zayavka_id)
    reject = await get_reject(zayavka_id)
    if not reject:
        await callback.message.delete()
        await state.update_data(zayavka_id=zayavka_id)
        await state.update_data(user_id=user_id)
        await state.update_data(event_id=event_id)
        data = await state.get_data()
        zayavka_id = data['zayavka_id']
        user_id = data['user_id']
        event_id = data['event_id']
        await callback.message.answer('Напишите причину отклонения:',
                                      reply_markup=kb.admin_cancel)
        await state.set_state(Reject.reason)
    else:
        await callback.message.delete()
        await callback.message.answer("Другой администратор уже рассмотрел заявку!")
        await state.clear()



@router.message(Reject.reason)
async def reason(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    zayavka_id = data['zayavka_id']
    user_id = data['user_id']
    event_id = data['event_id']
    event = await get_event(event_id)
    await bot.send_message(chat_id=user_id,
                           text=f"Ваша заявка отклонена в связи с причиной: <b>{message.text}</b>",
                           parse_mode='HTML',
                           reply_markup=kb.links)
    zayavka = await get_zayavka(zayavka_id)
    await insert_rejected(zayavka_id=zayavka_id,
                          full_name=zayavka[1],
                          date_age=zayavka[2],
                          rider_exp=zayavka[3],
                          skate=zayavka[4],
                          helmet=zayavka[5],
                         deffender=zayavka[6],
                          parents_name=zayavka[7],
                          parents_contact=zayavka[8],
                          event_id=event_id,
                          reason=message.text)
    await message.answer("Вы отклонили заявку",
                         reply_markup=kb.admin_menu)
    await state.clear()

@router.callback_query(F.data == 'add_event')
async def add_event(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Напишите название мероприятия:",
                                  reply_markup=kb.admin_cancel)
    await state.set_state(AddEvent.event_name)

@router.message(AddEvent.event_name)
async def event_name(message: Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await message.answer("Напишите описание мероприятия:",
                          reply_markup=kb.admin_cancel)
    await state.set_state(AddEvent.event_description)

@router.message(AddEvent.event_description)
async def event_description(message: Message, state: FSMContext):
    await state.update_data(event_description=message.text)
    await message.answer("Отправьте фото мероприятия:",
                          reply_markup=kb.admin_cancel)
    await state.set_state(AddEvent.event_photo)

@router.message(AddEvent.event_photo)
async def event_photo(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        await state.update_data(event_photo=message.photo[-1].file_id)
        await message.answer("Фото успешно добавлено!\n"
                             "Введите максимальное количество людей на мероприятии:",
                              reply_markup=kb.admin_cancel)
        await state.set_state(AddEvent.event_count)

    else:
        await message.answer("Отправьте фото мероприятия:",
                              reply_markup=kb.admin_cancel)


@router.message(AddEvent.event_count)
async def event_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(event_count=message.text)
        event = await state.get_data()
        await insert_event(event_name=event['event_name'],
                        event_description=event['event_description'],
                        event_photo=event['event_photo'],
                        event_count=event['event_count'])
        await message.answer("Мероприятие успешно добавлено!\n\nВы вернулись в админ-меню!",
                              reply_markup=kb.admin_panel)
        await state.clear()
    else:
        await message.answer("Колличество людей на мероприятии должно быть числом!\n"
                             "Повторите попытку!",
                              reply_markup=kb.admin_cancel)

@router.callback_query(F.data == 'all_events')
async def all_events(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Текущие контесты",
                                  reply_markup=await kb.all_events_admin_cb())

@router.callback_query(F.data.startswith('eventadmin_'))
async def event_admin(callback: CallbackQuery):
    await callback.message.delete()
    event_id = int(callback.data.split('_')[1])
    event = await get_event(event_id)
    await callback.message.answer_photo(photo=f'{event[1]}',
                                        caption=f'<b>{event[2]}</b>\n\n{event[3]}\n\nОграничение регистраций: {event[4]}',
                                        parse_mode='HTML',
                                        reply_markup=await kb.delete_event_cb(event_id))

@router.callback_query(F.data.startswith("delete_"))
async def delete_contest(callback: CallbackQuery):
    await callback.message.delete()
    event_id = int(callback.data.split("_")[1])
    await delete_event(event_id)
    await delete_zayavka_all(event_id)
    await delete_zayavka(event_id)
    await callback.message.answer("Контест был успешно удален!\n\nВы вернулись в админ-меню!",
                                  reply_markup=kb.admin_panel)

@router.callback_query(F.data.startswith("edit_name_"))
async def edit_event_name_router(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    event_id = int(callback.data.split("_")[2])
    await state.set_state(AddEvent.new_event_name.state)
    await state.update_data(event_id=event_id)
    await callback.message.answer("Напишите новое название контеста",
                                  reply_markup=kb.admin_cancel)

@router.message(AddEvent.new_event_name)
async def edit_product_name(message: Message, state: FSMContext):
    event_id = await state.get_data()
    event_id = event_id.get("event_id")
    await edit_event_name(event_id, message.text)
    await message.answer("Название успешно изменено!",
                          reply_markup=kb.admin_panel)
    await state.clear()

@router.callback_query(F.data.startswith("edit_description_"))
async def edit_event_description_router(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    event_id = int(callback.data.split("_")[2])
    await state.set_state(AddEvent.new_event_description.state)
    await state.update_data(event_id=event_id)
    await callback.message.answer("Напишите новое описание контеста",
                                  reply_markup=kb.admin_cancel)

@router.message(AddEvent.new_event_description)
async def edit_product_description(message: Message, state: FSMContext):
    event_id = await state.get_data()
    event_id = event_id.get("event_id")
    await edit_event_desc(event_id, message.text)
    await message.answer("Описание успешно изменено!",
                          reply_markup=kb.admin_panel)
    await state.clear()

@router.callback_query(F.data.startswith("edit_photo_"))
async def edit_event_photo_router(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    event_id = int(callback.data.split("_")[2])
    await state.set_state(AddEvent.new_event_photo.state)
    await state.update_data(event_id=event_id)
    await callback.message.answer("Отправьте новое фото контеста",
                                  reply_markup=kb.admin_cancel)

@router.message(AddEvent.new_event_photo)
async def edit_product_photo(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(event_photo=message.photo[-1].file_id)
        event_id = await state.get_data()
        event_id = event_id.get("event_id")
        await edit_event_photo(event_id, message.photo[-1].file_id)
        await message.answer("Фото успешно изменено!",
                              reply_markup=kb.admin_panel)
        await state.clear()
    else:
        await message.answer("Отправьте фото контеста:",
                              reply_markup=kb.admin_cancel)

@router.callback_query(F.data.startswith("edit_count_"))
async def edit_event_count_router(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    event_id = int(callback.data.split("_")[2])
    await state.set_state(AddEvent.new_event_count.state)
    await state.update_data(event_id=event_id)
    await callback.message.answer("Напишите новое ограничение регистрации",
                                  reply_markup=kb.admin_cancel)

@router.message(AddEvent.new_event_count)
async def edit_product_count(message: Message, state: FSMContext):
    event_id = await state.get_data()
    event_id = event_id.get("event_id")
    await edit_event_count(event_id, message.text)
    await message.answer("Ограничение регистрации успешно изменено!",
                          reply_markup=kb.admin_panel)
    await state.clear()

@router.callback_query(F.data == 'reject_list')
async def reject_list(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Текущие отклоненные заявки",
                                  reply_markup=await kb.reject_list_admin_cb())

@router.callback_query(F.data.startswith('rejectadmin_'))
async def rejectadmin(callback: CallbackQuery):
    await callback.message.delete()
    reject_id = int(callback.data.split('_')[1])
    reject = await get_reject(reject_id)
    await callback.message.answer(f'<b>Отклоненная заявка №{reject[0]}\n\n</b>'
                                  f'<b>ФИО:</b> {reject[1]}\n'
                                  f'<b>Дата рождения:</b> {reject[2]}\n'
                                  f'<b>Стаж катания:</b> {reject[3]}\n'
                                  f'<b>Наличие скейта:</b> {reject[4]}\n'
                                  f'<b>Наличие шлема:</b> {reject[5]}\n'
                                  f'<b>Наличие защиты:</b> {reject[6]}\n'
                                  f'<b>ФИО родителей:</b> {reject[7]}\n'
                                  f'<b>Контакты родителей:</b> {reject[8]}\n'
                                  f'<b>Причина отклонения заявки:</b> {reject[10]}',
                                  reply_markup=kb.ad_back,
                                  parse_mode='HTML')


@router.callback_query(F.data == 'admin_back')
async def admin_back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Вы вернулись в меню.",
                                  reply_markup=kb.admin_menu)

@router.callback_query(F.data == 'admin_cancel')
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Действие отменено!\n"
                                  "Вы вернулись в меню.",
                                  reply_markup=kb.admin_panel)
    await state.clear()



