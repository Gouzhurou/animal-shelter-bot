"""Модуль содержит константы для меню пользователя"""

class UserButtons():
    """Класс содержит константы для кнопок меню пользователя"""
    VIEW_ABOUT_US = 'О нас'
    VIEW_ADDRESS = 'Наш адрес'
    VIEW_OPENING_HOURS = 'Часы работы'
    VIEW_VISIT_SHELTER = 'Посетить приют'
    VIEW_HELP_ANIMALS = 'Помочь животным'
    VIEW_WHAT_SHELTER_NEEDS = 'Что нужно приюту.'
    VIEW_BECOME_A_VOLUNTEER = 'Стать волонтером'
    VIEW_URGENT_HELP = 'Срочно помочь'
    VIEW_ANIMALS_CATALOG = 'Хочу посмотреть каталог животных приюта'
    VIEW_ANIMAL_QUESTION = 'Хочу задать вопрос о животном приюта'
    VIEW_ORDER_DELIVERY = 'Заказать доставку в приют'
    VIEW_GIVE_ANIMAL = 'Отдать животное в приют'
    VIEW_TAKE_ANIMAL = 'Забрать животное домой'
    VIEW_BECOME_A_GUARDIAN = 'Стать опекуном для животного'
    VIEW_SING_UP_TOUR = 'Записаться на экскурсию'
    VIEW_WORK_AT_SHELTER = 'Хочу работать в приюте'
    VIEW_SOCIAL_MEDIA = 'Посмотреть соцсети'
    VIEW_REPORTS = 'Посмотреть отчеты'
    VIEW_ASK_QUESTION = 'Задать вопрос'
    VIEW_BUSINESS_HELP = 'У меня собственный бизнес, хочу помогать благотворительной организации'
    VIEW_FLYER = ('хочу скачать, распечатать или разместить у себя в соцсетях листовку приюта, '
                  'логотип приюта, '
                  'изображение QR кода для сбора пожертвования')
    VIEW_QUESTION_TO_DIRECTOR = 'Задать вопрос руководителю'
    VIEW_REVIEW = 'Хочу оставить отзыв о приюте'
    VIEW_GIFT = 'Хочу получить подарок'
    VIEW_NEXT_PAGE_BUTTON = 'Следующая страница'
    VIEW_PREV_PAGE_BUTTON = 'Предыдущая страница'


class UserMessages():
    """Класс содержит константы для сообщений меню пользователя"""
    ABOUT_US = ('Мы с 2016 года помогаем  бездомным животным, которые оказались в беде.\n'
                '\n'
                'Мы негосударственная организация, поэтому сами находим деньги на работу'
                'наших проектов: собираем пожертвования, ищем спонсоров, гранты, субсидии.\n'
                '\n'
                'Всю свою работу мы осуществляем на территории собственного приюта для животных.\n'
                'Мы оказываем помощь травмированным и больным бездомным животным, '
                'проводим льготные массовые стерилизации и '
                'вакцинации, ищем новые семьи для наших подопечных, проводим уроки доброты. '
                'Помогаем другим приютам и кураторам.\n'
                '\n'
                'На попечении более 900 животных\n'
                '\n'
                'Строим Центр Помощи Животным.\n'
                '\n'
                'Придерживаемся принципов 5 свобод животных.')
    ADDRESS = ('г. Санкт-Петербург\n'
               'м. Кировский Завод\n'
               'Автовская ул., 31, лит. И')
    OPENING_HOURS = 'Ответ : Ежедневно с 10.00-22.00'
    VISIT_SHELTER = ('Ответ: Посетить приют можно:\n'
                     '- Среда и четверг: с 18:00 до 20:00\n'
                     '- Суббота и воскресенье: с 17:00 до 20:00')
    HELP_ANIMALS = 'Ссылка на сайт на страницу сборов'
    WHAT_SHELTER_NEEDS = 'PLACEHOLDER'
    BECOME_A_VOLUNTEER = ('Для того, чтобы стать волонтером "Преданного Сердца" надо '
                          'либо связаться с руководством\n'
                          'по тел. 8 (921) 953-09-18, \n'
                          'либо написать письмо на электронный адрес '
                          'predannoe.serdce.spb@gmail.com\n')
    URGENT_HELP = 'PLACEHOLDER'
    ANIMALS_CATALOG = ('Каталоги наших животных можно посмотреть:\n'
                       '- На сайте: *link*\n'
                       '- В группе ВК: *link*')
    ANIMAL_QUESTION = 'Вопрос о животном приюте можно задать по телефону 8921 953-09-18'
    ORDER_DELIVERY = ('	Ответ: Заказать доставку в приют можно несколькими способами:\n'
                      '\n'
                      '1. Озон\n'
                      '- Доставка на адрес приюта: ул.Автовская 31И\n'
                      '- Время: ежедневно с 10:00 до 22:00\n'
                      '- Контакт: +7 (952) 209-39-51 (Инна Петровна)\n'
                      '\n'
                      '2. Пункт выдачи Озон\n'
                      '- Адрес: ул. Маршала Говорова д.8, лит.А\n'
                      '- Получатель: Алиева Инна\n'
                      '- Требуется: выслать штрихкод для получения\n'
                      '- Телефон: +7 (952) 209-39-51\n'
                      '\n'
                      '3. Другие магазины\n'
                      '- Доставка на адрес приюта: ул.Автовская 31И\n'
                      '- Время: ежедневно с 10:00 до 22:00\n'
                      '- Контакт: +7 (952) 209-39-51 (Инна Алиева)')
    GIVE_ANIMAL = ('Для того, чтобы отдать животное в приют, '
                   'нужно (используйте один из вариантов):\n'
                   '1. Написать письмо на почту организации: predannoe.serdce.spb@gmail.com\n'
                   '2. Позвонить по телефону ☎ +7 (921) 554-05-64 с 18:00 '
                   'до 20:00 ежедневно\n')
    TAKE_ANIMAL = ('Для того, чтобы забрать животное домой, надо заполнить '
                   'анкету будущего владельца *link*')
    BECOME_A_GUARDIAN = ('Если вы хотите взять котика на попечение - '
                         'вы можете выбрать любого котика из каталога либо на сайте *link*\n '
                         'либо в нашей группе ВК *link*\n'
                         'Анкета попечителя *link*\n'
                         'Подробнее о попечительской программе можно узнать в нашей '
                         'группе ВК *link* по ссылке:')
    SING_UP_TOUR = ('Правила посещения приюта "Преданное Сердце"\n'
                    '🎫 1. Купить билет: Timepad *link*\n'
                    '📞 2. Согласовать визит: 8 (952) 209-39-51')
    WORK_AT_SHELTER = ('Для того, чтобы узнать об актуальных вакансиях в приюте, нужно:\n'
                       '- Позвонить директору Авласевич Наталии Владимировне по тел. '
                       '8 (921) 953-09-18\n'
                       '- Или написать на почту организации: predannoe.serdce.spb@gmail.com\n')
    SOCIAL_MEDIA = ('Наши соцсети:\n'
                    '🌐 Сайт: *link* \n'
                    '📱 ВКонтакте: *link* \n'
                    '📨 Телеграм: *link* \n'
                    '👥 Одноклассники: *link* \n')
    REPORTS = 'Отчеты организации можно посмотреть на сайте *link*'
    ASK_QUESTION = 'PLACEHOLDER'
    BUSINESS_HELP = ('Файл с презентацией для партнеров\n'
                     '• Менеджер по работе с корпоративными партнерами: 📞 8 (921) 953-09-18')
    FLYER = 'PLACEHOLDER'
    QUESTION_TO_DIRECTOR = ('Директор благотворительной организации "Преданное Сердце" '
                            'Авласевич Наталия Владимировна\n'
                            'тел. 8921 953-09-18\n'
                            'электронная почта организации: predannoe.serdce.spb@gmail.com')
    REVIEW = 'Оставить отзыв *link*'
    GIFT = 'PLACEHOLDER'
