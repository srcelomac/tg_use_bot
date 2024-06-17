import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
import string
import sqlite3
import math
import keyboard
from handlers import start, main_menu
import os


conn = sqlite3.connect('tasks.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Tasks (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER, task_id INTEGER, words TEXT, answers TEXT)')
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect('stats.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Stats (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER UNIQUE, rights INTEGER DEFAULT 0, wrongs INTEGER DEFAULT 0)')
conn.commit()
cur.close()
conn.close()

task_id = 0

task_4 = [
    ['аэропорты', 'аэропОрты'],
    ['банты', 'бАнты'],
    ['бороду', 'бОроду'],
    ['бухгалтеров', 'бухгАлтеров'],
    ['вероисповедание', 'вероисповЕдание'],
    ['водопровод', 'водопровОд'],
    ['газопровод', 'газопровОд'],
    ['гражданство', 'граждАнство'],
    ['дефис', 'дефИс'],
    ['дешевизна', 'дешевИзна'],
    ['диспансер', 'диспансЕр'],
    ['договорённость', 'договорЁнность'],
    ['документ', 'докумЕнт'],
    ['досуг', 'досУг'],
    ['еретик', 'еретИк'],
    ['жалюзи', 'жалюзИ'],
    ['значимость', 'знАчимость'],
    ['иксы', 'Иксы'],
    ['каталог', 'каталОг'],
    ['квартал', 'квартАл'],
    ['километр', 'киломЕтр'],
    ['конусов', 'кОнусов'],
    ['корысть', 'корЫсть'],
    ['краны', 'крАны'],
    ['кремень, кремня', 'кремЕнь, кремнЯ'],
    ['лекторов', 'лЕкторов'],
    ['локтя, локтей', 'лОктя, локтЕй'],
    ['лыжня', 'лыжнЯ'],
    ['местностей', 'мЕстностей'],
    ['намерение', 'намЕрение'],
    ['нарост', 'нарОст'],
    ['недруг', 'нЕдруг'],
    ['недуг', 'недУг'],
    ['некролог', 'некролОг'],
    ['ненависть', 'нЕнависть'],
    ['нефтепровод', 'нефтепровОд'],
    ['новостей', 'новостЕй'],
    ['ногтя, ногтей', 'нОгтя, ногтЕй'],
    ['отзыв (о книге)', 'Отзыв'],
    ['отзыв (посла из страны)', 'отзЫв'],
    ['отрочество', 'Отрочество'],
    ['партер', 'партЕр'],
    ['портфель', 'портфЕль'],
    ['поручни', 'пОручни'],
    ['приданое', 'придАное'],
    ['призыв', 'призЫв'],
    ['свёкла', 'свЁкла'],
    ['сироты', 'сирОты'],
    ['созыв', 'созЫв'],
    ['сосредоточение', 'сосредотОчение'],
    ['средства', 'срЕдства'],
    ['статуя', 'стАтуя'],
    ['столяр', 'столЯр'],
    ['таможня', 'тамОжня'],
    ['торты', 'тОрт'],
    ['туфля', 'тУфля'],
    ['цемент', 'цемЕнт'],
    ['центнер', 'цЕнтнер'],
    ['цепочка', 'цепОчка'],
    ['шарфы', 'шАрфы'],
    ['шофер', 'шофЁр'],
    ['эксперт', 'экспЕрт'],
    ['верна, верный', 'вернА, вЕрный'],
    ['значимый', 'знАчимый'],
    ['красивее', 'КрасИвее'],
    ['кухонный', 'кУхонный'],
    ['ловка, ловкий', 'ловкА, лОвкий'],
    ['мозаичный', 'мозаИчный'],
    ['оптовый', 'оптОвый'],
    ['прозорливый', 'прозорлИвый'],
    ['сливовый', 'слИвовый'],
    ['брала, брать', 'бралА, брАть'],
    ['бралась, браться', 'бралАсь, брАться'],
    ['взяла', 'взялА'],
    ['взялась, взяться', 'взялАсь, взЯться'],
    ['влилась, влиться', 'влилАсь, влИться'],
    ['ворвалась, ворваться', 'ворвалАсь, ворвАться'],
    ['воспринять', 'воспринЯть'],
    ['воссоздала', 'воссоздалА'],
    ['вручит', 'вручИт'],
    ['гнала', 'гналА'],
    ['гналась', 'гналАсь'],
    ['добрала', 'добралА'],
    ['добралась', 'добралАсь'],
    ['дождалась', 'дождалАсь'],
    ['дозвонится', 'дозвонИтся'],
    ['дозировать', 'дозИровать'],
    ['ждала', 'ждалА'],
    ['жилось', 'жилОсь'],
    ['закупорить', 'закУпорить'],
    ['занять, занял, заняла, заняли', 'занЯть, зАнял, занялА, зАняли'],
    ['заперла', 'заперлА'],
    ['запломбировать', 'запломбировАть'],
    ['защемит', 'защемИт'],
    ['звала', 'звалА'],
    ['звонит', 'звонИт'],
    ['кашлянуть', 'кАшлянуть'],
    ['клала', 'клАла'],
    ['клеить', 'клЕить'],
    ['кралась', 'крАлась'],
    ['кровоточить', 'кровоточИть'],
    ['лгала', 'лгалА'],
    ['лила', 'лИлА'],
    ['лилась', 'лИлась'],
    ['наврала', 'навралА'],
    ['наделит', 'наделИт'],
    ['надорвалась', 'надорвалАсь'],
    ['назвалась', 'назвалАсь'],
    ['накренится', 'накренИтся'],
    ['налила', 'налилА'],
    ['нарвала', 'нарвалА'],
    ['начать, начал, начала, начали', 'начАть, нАчал, началА, нАчали'],
    ['обзвонит', 'обзвонИт'],
    ['облегчить, облегчит', 'облегчИть, облегчИт'],
    ['облилась', 'облилАсь'],
    ['обнялась', 'обнялАсь'],
    ['обогнала', 'обогналА'],
    ['ободрала', 'ободралА'],
    ['ободрить, ободрит', 'ободрИть, ободрИт'],
    ['ободриться, ободрится', 'ободрИться, ободрИтся'],
    ['обострить', 'обострИть'],
    ['одолжить, одолжит', 'одолжИть, одолжИт'],
    ['озлобить', 'озлОбить'],
    ['оклеить', 'оклЕить'],
    ['окружит', 'окружИт'],
    ['опошлить', 'опОшлить'],
    ['Осведомиться, осведомится', 'освЕдомиться, освЕдомится'],
    ['отбыла', 'отбылА'],
    ['отдала', 'отдалА'],
    ['откупорить', 'откУпорить'],
    ['отозвала', 'отозвалА'],
    ['отозвалась', 'отозвалАсь'],
    ['перезвонит', 'перезвонИт'],
    ['перелила', 'перелилА'],
    ['плодоносить', 'плодоносИть'],
    ['пломбировать', 'пломбировАть'],
    ['повторит', 'повторИт'],
    ['позвала', 'позвалА'],
    ['позвонит', 'позвонИт'],
    ['полила', 'полилА'],
    ['положить, положил', 'положИть, положИл'],
    ['понять, поняла', 'понЯть, понялА'],
    ['послала', 'послАла'],
    ['прибыть, прибыл, прибыла, прибыли', 'прибЫть, прИбыл, прибылА, прИбыли'],
    ['принять, принял, приняла, приняли', 'принЯть, прИнял, принялА, прИняли'],
    ['рвала', 'рвалА'],
    ['сверлит', 'сверлИт'],
    ['сняла', 'снялА'],
    ['соврала', 'совралА'],
    ['создала', 'создалА'],
    ['сорвала', 'сорвалА'],
    ['сорит', 'сорИт'],
    ['убрала', 'убралА'],
    ['углубить', 'углубИть'],
    ['укрепит', 'укрепИт'],
    ['черпать', 'чЕрпать'],
    ['щемит', 'щемИт'],
    ['щёлкать', 'щЁлкать'],
    ['довезённый', 'довезЁнный'],
    ['загнутый', 'зАгнутый'],
    ['занятый, занята', 'зАнятый, занятА'],
    ['запертый', 'зАпертый'],
    ['заселённый, заселена', 'заселЁнный, заселенА'],
    ['кормящий', 'кормЯщий'],
    ['кровоточащий', 'кровоточАщий'],
    ['наживший', 'нажИвший'],
    ['наливший', 'налИвший'],
    ['нанявшийся', 'нанЯвшийся'],
    ['начавший', 'начАвший'],
    ['начатый', 'нАчатый'],
    ['низведённый', 'низведЁнный'],
    ['облегчённый', 'облегчЁнный'],
    ['ободрённый', 'ободрЁнный'],
    ['обострённый', 'обострЁнный'],
    ['отключённый', 'отключЁнный'],
    ['повторённый', 'повторЁнный'],
    ['поделённый', 'поделЁнный'],
    ['понявший', 'понЯвший'],
    ['принятый, принята', 'прИнятый, принятА'],
    ['приручённый', 'приручЁнный'],
    ['проживший', 'прожИвший'],
    ['снята', 'снятА'],
    ['согнутый', 'сОгнутый'],
    ['углублённый', 'углублЁнный'],
    ['закупорив', 'закУпорив'],
    ['начав', 'начАв'],
    ['начавшись', 'начАвшись'],
    ['отдав', 'отдАв'],
    ['подняв', 'поднЯв'],
    ['поняв', 'понЯв'],
    ['прибыв', 'прибЫв'],
    ['создав', 'создАв'],
    ['вовремя', 'вОвремя'],
    ['доверху', 'дОверху'],
    ['донельзя', 'донЕльзя'],
    ['донизу', 'дОнизу'],
    ['досуха', 'дОсуха'],
    ['засветло', 'зАсветло'],
    ['затемно', 'зАтемно'],
    ['красивее', 'красИвее'],
    ['надолго', 'надОлго'],
    ['ненадолго', 'ненадОлго']
]

tasks_common = [[['беспр_кословный', 'беспрекословный'], ['пр_клонный', 'преклонный'], ['пр_лестный', 'прелестный'], ['пр_небречь', 'пренебречь'], ['пр_небрежение', 'пренебрежение'], ['знаки пр_пинания', 'знаки препинания'], ['пр_пираться', 'препираться'], ['пр_пона', 'препона'], ['пр_поднести', 'преподнести'], ['пр_пятствие', 'препятствие'], ['пр_рекаться', 'пререкаться'], ['пр_рогатива', 'прерогатива'], ['пр_возносить', 'превозносить'], ['пр_зидент', 'президент'], ['пр_зидиум', 'президиум'], ['пр_следовать', 'преследовать'], ['пр_тензия', 'претензия'], ['пр_успеть', 'преуспеть'], ['пр_возмочь', 'превозмочь'], ['пр_амбула', 'преамбула'], ['пр_одолеть', 'преодолеть'], ['пр_стол', 'престол'], ['пр_мьера', 'премьера'], ['пр_взойти', 'превзойти'], ['пр_имущество', 'преимущество'], ['пр_возносить', 'превозносить'], ['пр_зентация', 'презентация'], ['пр_зентовать', 'презентовать'], ['пр_йскурант', 'прейскурант'], ['пр_людия', 'прелюдия'], ['пр_миальный', 'премиальный'], ['пр_мьера', 'премьера'], ['пр_валировать', 'превалировать'], ['пр_парат', 'препарат'], ['пр_сечь', 'пресечь'], ['пр_смыкаться', 'пресмыкаться'], ['пр_словутый', 'пресловутый'], ['пр_небрежительный', 'пренебрежительный'], ['пр_стиж', 'престиж'], ['пр_тендент', 'претендент'], ['пр_ткновение', 'преткновение'], ['воспр_пятствовать', 'воспрепятствовать'], ['непр_ложная (истина)', 'непреложная (истина)'], ['времяпр_провождение', 'времяпрепровождение'], ['пр_даваться мечтаниям', 'предаваться мечтаниям'], ['пр_клонять колени в храме', 'преклонять колени в храме'], ['пр_льщать', 'прельщать'], ['пр_подобный', 'преподобный'], ['пр_цедент', 'прецедент'], ['пр_грешение', 'прегрешение'], ['беспр_дельный', 'беспредельный'], ['беспр_станный', 'беспрестанный'], ['пр_фектура', 'префектура'], ['пр_людия', 'прелюдия'], ['пр_людно', 'прилюдно'], ['пр_баутка', 'прибаутка'], ['пр_бор', 'прибор'], ['пр_вереда', 'привереда'], ['пр_видение', 'привидение'], ['пр_вычка', 'привычка'], ['пр_годный', 'пригодный'], ['пр_дирчивый', 'придирчивый'], ['пр_вилегия', 'привилегия'], ['пр_гожий', 'пригожий'], ['пр_страстие', 'пристрастие'], ['пр_красы', 'прикрасы'], ['пр_верженец', 'приверженец'], ['пр_оритет', 'приоритет'], ['пр_ключение', 'приключение'], ['пр_скорбный', 'прискорбный'], ['пр_тязание', 'притязание'], ['пр_чудливый', 'причудливый'], ['пр_лежный', 'прилежный'], ['пр_говор', 'приговор'], ['без пр_крас', 'без прикрас'], ['беспр_страстный', 'беспристрастный'], ['пр_сяга', 'присяга'], ['пр_митивный', 'примитивный'], ['пр_ветливый', 'приветливый'], ['пр_вивка', 'прививка'], ['пр_влекательный', 'привлекательный'], ['пр_норовиться', 'приноровиться'], ['пр_чина', 'причина'], ['пр_язнь', 'приязнь'], ['непр_личный', 'неприличный'], ['непр_хотливый', 'неприхотливый'], ['пр_близительно', 'приблизительно'], ['пр_емлемый', 'приемлемый'], ['непр_емлемый', 'неприемлемый'], ['пр_каз', 'приказ'], ['пр_урочить', 'приурочить'], ['пр_ватный', 'приватный'], ['непр_ступная (крепость)', 'неприступная'], ['супер_яхта', 'суперъяхта'], ['из_ян', 'изъян'], ['ин_екция', 'инъекция'], ['под_есаул', 'подъесаул'], ['ад_ютант', 'адъютант'], ['неот_емлемый', 'неотъемлемый'], ['аб_юрация', 'абъюрация'], ['диз_юнкция', 'дизъюнкция'], ['кон_юнктивит', 'конъюнктивит'], ['кон_ектура', 'конъектура'], ['пан_европейский', 'панъевропейский'], ['транс_европейский', 'трансъевропейский'], ['фельд_егерь', 'фельдъегерь'], ['под_ячий', 'подьячий'], ['п_едестал', 'пьедестал'], ['ар_ергард', 'арьергард'], ['порт_ера', 'портьера'], ['пр_бывать (находиться)', 'пребывать'], ['пр_бывать (пр_езжать)', 'прибывать'], ['пр_емник (наследник)', 'преемник'], ['пр_емник (радиоаппарат)', 'приемник'], ['пр_зирать (ненавидеть)', 'презирать'], ['пр_зирать (заботиться)', 'призирать'], ['пр_ступить (нарушить)', 'преступить'], ['пр_ступить (начать)', 'приступить'], ['пр_творить (осуществить)', 'претворить'], ['пр_творить (закрыть)', 'притворить'], ['пр_дать (изменить)', 'предать'], ['пр_дать (добавить усилить)', 'придать'], ['пр_дел (конец)', 'предел'], ['пр_дел (пр_стройка)', 'придел'], ['пр_ходящее (временное)', 'преходящее'], ['пр_ходящий (тот кто пр_ходит)', 'приходящий'], ['пр_клоняться (уважать)', 'преклоняться'], ['приклоняться (наклониться)', 'приклоняться'], ['пр_вратный (неправильно истолковали)', 'превратный'], ['пр_вратник (тот который охраняет ворота)', 'привратник'], ['непр_ложный (тот который нельзя переделать)', 'непреложный'], ['пр_ложение (добавление)', 'приложение'], ['пр_терпеть (ся) (пр_выкнуть)', 'притерпеть'], ['пр_терпеть (пережить)', 'претерпеть']],
                [],
                [],
                [],
                [],
                [],
                []]

tasks_new_common = [[['беспр_кословный', 'е'], ['пр_клонный', 'е'], ['пр_лестный', 'е'], ['пр_небречь', 'е'], ['пр_небрежение', 'е'], ['знаки пр_пинания', 'е'], ['пр_пираться', 'е'], ['пр_пона', 'е'], ['пр_поднести', 'е'], ['пр_пятствие', 'е'], ['пр_рекаться', 'е'], ['пр_рогатива', 'е'], ['пр_возносить', 'е'], ['пр_зидент', 'е'], ['пр_зидиум', 'е'], ['пр_следовать', 'е'], ['пр_тензия', 'е'], ['пр_успеть', 'е'], ['пр_возмочь', 'е'], ['пр_амбула', 'е'], ['пр_одолеть', 'е'], ['пр_стол', 'е'], ['пр_мьера', 'е'], ['пр_взойти', 'е'], ['пр_имущество', 'е'], ['пр_возносить', 'е'], ['пр_зентация', 'е'], ['пр_зентовать', 'е'], ['пр_йскурант', 'е'], ['пр_людия', 'е'], ['пр_миальный', 'е'], ['пр_мьера', 'е'], ['пр_валировать', 'е'], ['пр_парат', 'е'], ['пр_сечь', 'е'], ['пр_смыкаться', 'е'], ['пр_словутый', 'е'], ['пр_небрежительный', 'е'], ['пр_стиж', 'е'], ['пр_тендент', 'е'], ['пр_ткновение', 'е'], ['воспр_пятствовать', 'е'], ['непр_ложная (истина)', 'е'], ['времяпр_провождение', 'е'], ['пр_даваться мечтаниям', 'е'], ['пр_клонять (колени в храме)', 'е'], ['пр_льщать', 'е'], ['пр_подобный', 'е'], ['пр_цедент', 'е'], ['пр_грешение', 'е'], ['беспр_дельный', 'е'], ['беспр_станный', 'е'], ['пр_фектура', 'е'], ['пр_людия', 'е'], ['пр_людно', 'и'], ['пр_баутка', 'и'], ['пр_бор', 'и'], ['пр_вереда', 'и'], ['пр_видение', 'и'], ['пр_вычка', 'и'], ['пр_годный', 'и'], ['пр_дирчивый', 'и'], ['пр_вилегия', 'и'], ['пр_гожий', 'и'], ['пр_страстие', 'и'], ['пр_красы', 'и'], ['пр_верженец', 'и'], ['пр_оритет', 'и'], ['пр_ключение', 'и'], ['пр_скорбный', 'и'], ['пр_тязание', 'и'], ['пр_чудливый', 'и'], ['пр_лежный', 'и'], ['пр_говор', 'и'], ['без пр_крас', 'и'], ['беспр_страстный', 'и'], ['пр_сяга', 'и'], ['пр_митивный', 'и'], ['пр_ветливый', 'и'], ['пр_вивка', 'и'], ['пр_влекательный', 'и'], ['пр_норовиться', 'и'], ['пр_чина', 'и'], ['пр_язнь', 'и'], ['непр_личный', 'и'], ['непр_хотливый', 'и'], ['пр_близительно', 'и'], ['пр_емлемый', 'и'], ['непр_емлемый', 'и'], ['пр_каз', 'и'], ['пр_урочить', 'и'], ['пр_ватный', 'и'], ['непр_ступная (крепость)', 'и'], ['супер_яхта', 'ъ'], ['из_ян', 'ъ'], ['ин_екция', 'ъ'], ['под_есаул', 'ъ'], ['ад_ютант', 'ъ'], ['неот_емлемый', 'ъ'], ['аб_юрация', 'ъ'], ['диз_юнкция', 'ъ'], ['кон_юнктивит', 'ъ'], ['кон_ектура', 'ъ'], ['пан_европейский', 'ъ'], ['транс_европейский', 'ъ'], ['фельд_егерь', 'ъ'], ['под_ячий', 'ь'], ['п_едестал', 'ь'], ['ар_ергард', 'ь'], ['порт_ера', 'ь'], ['пр_бывать (находиться)', 'е'], ['пр_бывать (пр_езжать)', 'и'], ['пр_емник (наследник)', 'е'], ['пр_емник (радиоаппарат)', 'и'], ['пр_зирать (ненавидеть)', 'е'], ['пр_зирать (заботиться)', 'и'], ['пр_ступить (нарушить)', 'е'], ['пр_ступить (начать)', 'и'], ['пр_творить (осуществить)', 'е'], ['пр_творить (закрыть)', 'и'], ['пр_дать (изменить)', 'е'], ['пр_дать (добавить усилить)', 'и'], ['пр_дел (конец)', 'е'], ['пр_дел (пр_стройка)', 'и'], ['пр_ходящее (временное)', 'е'], ['пр_ходящий (тот кто пр_ходит)', 'и'], ['пр_клоняться (уважать)', 'е'], ['приклоняться (наклониться)', 'я'], ['пр_вратный (неправильно истолковали)', 'е'], ['пр_вратник (тот который охраняет ворота)', 'и'], ['непр_ложный (тот который нельзя переделать)', 'е'], ['пр_ложение (добавление)', 'и'], ['пр_терпеть (ся) (пр_выкнуть)', 'и'], ['пр_терпеть (пережить)', 'е']],
                [],
                [],
                [['брезж_щий', 'у'], ['внемл_щий', 'ю'], ['всклокоч_нный', 'е'], ['выровн_нный', 'е'], ['движ_мый', 'и'], ['муч_мый', 'и'], ['дремл_щий', 'ю'], ['кле_щий', 'я'], ['колебл_щийся', 'ю'], ['колыш_щийся', 'у'], ['мел_щий (кофе)', 'ю'], ['обрыз_нный', 'е'], ['незыбл_мый', 'е'], ['немысл_мый', 'и'], ['неотъемл_мый', 'е'], ['тащ_щий', 'а'], ['приемл_мый', 'е'], ['стел_щий (стелить)', 'ю'], ['пыш_щий (здоровьем)', 'у']],
                [],
                [],
                [['назва_ый брат', 'н'], ['посаже_ый отец', 'н'], ['смышле_ый ребенок', 'н'], ['прида_ое невесты', 'н'], ['проще_ое воскресенье', 'н'], ['конче_ый человек', 'н'], ['варе_ик', 'н'], ['труже_ик', 'н'], ['муче_ик', 'н'], ['масле_ица', 'н'], ['гости_ый', 'н'], ['подли_ый', 'нн'], ['недюжи_ый', 'нн'], ['преда_ый', 'нн'], ['исти_ый', 'нн'], ['ветря_ая мельница', 'н'], ['ветре_ый человек', 'н'], ['ветре_о', 'н'], ['безветре_ый день', 'нн'], ['поисти_е', 'н'], ['нежда_ый', 'нн'], ['нечая_ый', 'нн'], ['неожида_ый', 'нн'], ['медле_ый', 'нн'], ['жела_ый', 'нн'], ['виде_ый', 'нн'], ['нежда_ый', 'нн'], ['негада_ый', 'нн'], ['невида_ый', 'нн'], ['неслыха_ый', 'нн'], ['жема_ый', 'нн'], ['свяще_ый', 'нн'], ['обеща_ый', 'нн'], ['отчая_ый', 'нн'], ['чека_ый', 'нн']]]


def diff_letters(a, b):
    return sum(a[i] != b[i] for i in range(min(len(a), len(b))))


'''
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Hi, {message.from_user.first_name}", reply_markup=keyboard.start_kb)

vars = ["Тренировка", "тренировка", "Моя статистика", "моя статистика", "Добавить слово", "добавить слово"]
@dp.message(F.text == ["Тренировка", "Моя статистика"])
async def on_click(message: Message):
    print(message.text)
'''

'''
@dp.message(Command("/start"))
async def start(message: Message):
    await message.answer(f"Hi, {message.from_user.first_name}", reply_markup=keyboard.start_kb_kb)
    try:
        #await message.answer(f"Hi, {message.from_user.first_name}", reply_markup=keyboard.main_kb)
        markup = keyboard.start_kb
        await message.answer(f"Привет, {message.from_user.first_name}!\nЗдесь ты можешь попрактиковаться в орфографии для ЕГЭ.\nДля управления используй встроенную или обычную клавиатуру", reply_markup=markup)
        conn = sqlite3.connect('stats.db')
        cur = conn.cursor()
        cur.execute(f'SELECT COUNT (*) from Stats where user_id = {message.chat.id}')
        tmp = str(cur.fetchall()[0])
        tmp = tmp.replace('(', '')
        tmp = tmp.replace(')', '')
        tmp = tmp.replace("'", '')
        tmp = tmp.replace(',', '')
        #print(tmp)
        cnt = int(tmp)
        if (cnt == 0):
            cur.execute('INSERT INTO Stats (user_id, rights, wrongs) VALUES (?, ?, ?)',
                        (message.chat.id, 0, 0))
        conn.commit()
        cur.close()
        conn.close()
        #bot.register_next_step_handler(message, on_click)
    except Exception as exp:
        print("ERROR start", exp)

@dp.message(Command("Тренировка", "тренировка", "Моя статистика", "моя статистика", "Добавить слово", "добавить слово"))
async def on_click(message):
    try:
        #print(message.text)
        if message.text.strip() == 'Тренировка' or message.text.lower() == "тренировка":
            markup = keyboard.training_kb
            await message.answer(f'Каким заданием хочешь заняться?', reply_markup=markup)
            #bot.register_next_step_handler(message, on_click_task)
        elif message.text.strip() == 'Моя статистика' or message.text.lower() == 'моя статистика':
            conn = sqlite3.connect('stats.db')
            cur = conn.cursor()
            sqlite_select_query = f"""SELECT rights from Stats where user_id = {message.chat.id}"""
            cur.execute(sqlite_select_query)
            right = str(cur.fetchall()[0])
            sqlite_select_query = f"""SELECT wrongs from Stats where user_id = {message.chat.id}"""
            cur.execute(sqlite_select_query)
            wrong = str(cur.fetchall()[0])
            right = right.replace('(', '')
            right = right.replace(')', '')
            right = right.replace("'", '')
            right = right.replace(',', '')
            wrong = wrong.replace('(', '')
            wrong = wrong.replace(')', '')
            wrong = wrong.replace("'", '')
            wrong = wrong.replace(',', '')
            #print(right)
            #print(wrong)
            cor = int(right)
            uncor = int(wrong)
            cur.close()
            conn.close()
            #if (cor+uncor == 0):
            #    bot.send_message(message.chat.id, "Ты пока не выполнил ни одного задания :(")
            #else:
            #    bot.send_message(message.chat.id,
            #                 f'Ты сделал верно {cor} из {cor + uncor} заданий ({math.ceil(cor/(cor+uncor)*100)}%). Что-то ещё?')
            #bot.register_next_step_handler(message, on_click)
        elif message.text.strip() == 'Добавить слово' or message.text.lower() == 'добавить слово':
            markup = keyboard.training_kb
            #bot.send_message(message.chat.id, f'В какое задание хочешь добавить слово?', reply_markup=markup)
            #bot.register_next_step_handler(message, on_click_task_add)
    except Exception as exp:
        print("ERROR on_click", exp)
'''

async def main():
    tg_token = os.environ["tg_token"]
    bot = Bot(str(tg_token))
    dp = Dispatcher()

    dp.include_routers(main_menu.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
