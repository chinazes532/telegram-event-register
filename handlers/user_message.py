from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
import keyboards as kb
from database import insert_user, insert_zayavka, get_event, get_accepted_count

import sqlite3 as sq


async def create_db():
    print("База данных создана!")

    global db, cur
    db = sq.connect('zayavka.db')
    cur = db.cursor()


router = Router()

class Register(StatesGroup):
    full_name = State()
    date_age = State()
    rider_exp = State()
    skate = State()
    helmet = State()
    deffender = State()
    parents_name = State()
    parents_contact = State()

@router.message(CommandStart())
async def bot_start(message: Message):
    await insert_user(user_id=message.from_user.id, username=message.from_user.username)
    await message.answer_photo(photo='AgACAgIAAxkBAAIBP2Z68ES9b3L8CEafEwPVL_Duw36vAAJn3zEbSnLZS7fVxE31ZYZpAQADAgADeQADNQQ',
                               caption='<b>Социальная скейт-школа приветствует Вас на регистрации в нашем боте!</b>',
                               parse_mode='HTML')
    await message.answer('<b>Выберите мероприятие:</b>',
                         reply_markup=await kb.all_events_cb(),
                         parse_mode='HTML')
    for admin_id in ADMIN_ID:
        if admin_id == message.from_user.id:
            await message.answer('Вы авторизовались как администратор!',
                                 reply_markup=kb.admin_menu)


@router.callback_query(F.data.startswith('event_'))
async def event(callback: CallbackQuery):
    await callback.message.delete()
    event_id = int(callback.data.split('_')[1])
    event = await get_event(event_id)
    await callback.message.answer_photo(photo=f'{event[1]}',
                                        caption=f'<b>{event[2]}</b>\n\n{event[3]}',
                                        parse_mode='HTML',
                                        reply_markup=await kb.register_cb(event_id))


@router.callback_query(F.data.startswith('eventregister_'))
async def register(callback: CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split('_')[1])
    await state.update_data(event_id=event_id)
    event = await get_event(event_id)
    accepted_count = await get_accepted_count(event_id)
    if accepted_count == event[4]:
        await callback.message.answer("Регистрация закрыта!")
    else:
        await callback.message.delete()
        await callback.message.answer("Для регистрации введите ваше ФИО:",
                                      reply_markup=kb.user_cancel)
        await state.set_state(Register.full_name)

@router.message(Register.full_name)
async def name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Укажите вашу дату рожденя в формате: <code>ДД.ММ.ГГГГ</code>:",
                         parse_mode='HTML',
                         reply_markup=kb.user_cancel)
    await state.set_state(Register.date_age)

@router.message(Register.date_age)
async def age(message: Message, state: FSMContext, bot: Bot):
    if len(message.text) == 10:
        await state.update_data(date_age=message.text)
        await message.answer("Расскажите про ваш стаж катания.\n"
                             "Есть ли у Вас опыт катания, пробовали ли Вы стоять на скейтборде?",
                             reply_markup=kb.user_cancel)
        await state.set_state(Register.rider_exp)
    else:
        await message.reply("Необходимо ввести дату рождения в формате: <code>ДД.ММ.ГГГГ</code>:",
                             parse_mode='HTML',
                             reply_markup=kb.user_cancel)

@router.message(Register.rider_exp)
async def exp(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await state.update_data(rider_exp=message.text)
        await message.answer("Есть ли у вас свой скейтборд?",
                             reply_markup=kb.skate)
        await state.set_state(Register.skate)
    else:
        await message.reply("Расскажите про ваш стаж катания более подробно",
                             reply_markup=kb.user_cancel)

@router.callback_query(Register.skate, F.data == 'skate_yes')
async def skate(callback: CallbackQuery, state: FSMContext):
    await state.update_data(skate='Да')
    await callback.message.delete()
    await callback.message.answer("Есть ли у вас шлем?",
                                  reply_markup=kb.helmet)
    await state.set_state(Register.helmet)

@router.callback_query(Register.skate, F.data == 'skate_no')
async def no_skate(callback: CallbackQuery, state: FSMContext):
    await state.update_data(skate='Нет')
    await callback.message.delete()
    await callback.message.answer("Есть ли у вас шлем?",
                                  reply_markup=kb.helmet)
    await state.set_state(Register.helmet)


@router.callback_query(Register.helmet, F.data == 'helmet_yes')
async def helmet(callback: CallbackQuery, state: FSMContext):
    await state.update_data(helmet='Да')
    await callback.message.delete()
    await callback.message.answer("Есть ли у вас своя защита?",
                                  reply_markup=kb.deffender)
    await state.set_state(Register.deffender)

@router.callback_query(Register.helmet, F.data == 'helmet_no')
async def no_helmet(callback: CallbackQuery, state: FSMContext):
    await state.update_data(helmet='Нет')
    await callback.message.delete()
    await callback.message.answer("Есть ли у вас своя защита?",
                                  reply_markup=kb.deffender)
    await state.set_state(Register.deffender)


@router.callback_query(Register.deffender, F.data == 'deffender_yes')
async def deffender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(deffender='Да')
    await callback.message.delete()
    await callback.message.answer("Укажите ФИО родителя:",
                                  reply_markup=kb.user_cancel)
    await state.set_state(Register.parents_name)

@router.callback_query(Register.deffender, F.data == 'deffender_no')
async def no_deffender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(deffender='Нет')
    await callback.message.delete()
    await callback.message.answer("Укажите ФИО родителя:",
                                  reply_markup=kb.user_cancel)
    await state.set_state(Register.parents_name)


@router.message(Register.parents_name)
async def parents_name(message: Message, state: FSMContext):
    await state.update_data(parents_name=message.text)
    await message.answer("Укажите контакты родителя:",
                         reply_markup=kb.user_cancel)
    await state.set_state(Register.parents_contact)


@router.message(Register.parents_contact)
async def parents_contact(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(parents_contact=message.text)
    data = await state.get_data()
    full_name = data['full_name']
    date_age = data['date_age']
    rider_exp = data['rider_exp']
    skate = data['skate']
    helmet = data['helmet']
    deffender = data['deffender']
    parents_name = data['parents_name']
    parents_contact = data['parents_contact']
    event_id = data['event_id']
    event = await get_event(event_id)
    await message.answer(f"Вы успешно зарегистрировались на мероприятие <b>{event[2]}</b>!\nВаша регистрация находится на модерации, ожидайте обратной связи!",
                         parse_mode='HTML')
    await insert_zayavka(full_name,
                         date_age,
                         rider_exp,
                         skate,
                         helmet,
                         deffender,
                         parents_name,
                         parents_contact,
                         event_id)
    db = sq.connect('zayavka.db')
    cur = db.cursor()
    zayavka_id = cur.execute("SELECT zayavka_id FROM zayavka WHERE full_name = ? AND date_age = ? AND event_id = ? AND parents_name = ? AND parents_contact = ? AND skate = ? AND helmet = ? AND deffender = ?",
                             (data['full_name'], data['date_age'], data['event_id'], data['parents_name'], data['parents_contact'], data['skate'], data['helmet'], data['deffender'])).fetchone()[0]
    for admin in ADMIN_ID:
        await bot.send_message(chat_id=admin,
                               text=f"<b>Новая регистрация на {event[2]}</b>\n\n"
                                    f"<b>ФИО:</b> {full_name}\n"
                                    f"<b>Дата рождения:</b> {date_age}\n"
                                    f"<b>Стаж катания:</b> {rider_exp}\n"
                                    f"<b>Наличие скейта:</b> {skate}\n"
                                    f"<b>Наличие шлема:</b> {helmet}\n"
                                    f"<b>Наличие защиты:</b> {deffender}\n"
                                    f"<b>ФИО родителя:</b> {parents_name}\n"
                                    f"<b>Контакты родителя:</b> {parents_contact}\n",
                               parse_mode='HTML',
                               reply_markup=await kb.check_register(user_id=message.from_user.id,
                                                                    zayavka_id=zayavka_id,
                                                                    event_id=data['event_id']))

    await state.clear()


@router.callback_query(F.data == 'user_cancel')
async def user_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Действие отменено!\n"
                                  "Вы вернулись в меню.Нажмите на /start")
    await state.clear()