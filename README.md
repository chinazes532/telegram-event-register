# telegram event register

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

<h1>Предыстория</h1>

У Федерации скейтбординга России есть свой проект, который направлен на социализацию подростков и улучшению их навыков катания, он называется "Социальная Скейт Школа".
Социальная Скейт Школа проводит открытые тренировки в различных скейт-парках и чтобы попасть на тренировку нужно зарегистрироваться.
Раньше у них была регистрация по почте, но я предложил им идею регистраии в виде телеграм чат-бота, потому что у Социальной Скейт Школы есть свой канал в телеграме, в котором сидит основная аудитория.

<h1>Принцип работы</h1>

В боте есть админ-панель, в которой можно добавлять/редактировать/удалять мероприятия. 
Администратор вводит заголовок тренировки, описание и ограничение регистраций.
Пользователь при переходе в меню видит клавиатуру с кнопками, на которых заголовки тренировок.
При регистрации пользователь указывает ФИО, дату рождения, контакты родителей, свой опыт в катании, наличие скейта и защиты, далее эта заявка отправляется всем админам бота с кнопками <b>"Принять"</b> и <b>"Отклонить"</b>.

Если админ принимает регистрацию, то она сохраняется в Excel таблицу (для каждого события автомитачески создается своя таблица).
При отклонении заявку необходимо указать причину.
Во всех случаях пользователь получает обратную связь с определенной информацией.

<h1>Установка и запуск</h1>

Для установки потребуется: 
<ol>
    <li>Python 3.9 и выше</li>
    <li>Выбрать в главном меню "Get from VCS" и вставить данную ссылку: <code>https://github.com/chinazes532/telegram-event-register.git</code></li>
    <li>Установить нужные зависиомсти, при помощи: <code>pip install -r requirements.txt</code></li>
    <li>Запустите скрипт при помощи <code>python3 main.py</code></li>
</ol>


