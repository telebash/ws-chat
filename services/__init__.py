import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()
prompt = ''
with open('prompt.txt') as f:
    prompt = f.read()


class Messages(Enum):
    START_MESSAGE_1 = '''
Привет!👋  Я Telegram-бот для SMM услуг.

🤖 Мои возможности:

/create_post - ✍🏻 Создание постов с помощью ИИ. От вас - ниша и тема, от меня - оригинальный текст и подходящее изображение.

/create_theme - 💡Подбор идей. У меня есть неисчерпаемая база для тем постов и сторис.

/create_image - 🖼️ Создание изображений. От вас - описание, от меня - оригинальная картинка. Возможность выбрать разный стиль.

/create_content_plan - 📅 Создание контент плана на месяц.

Давайте создавать уникальный контент вместе!🤖

/help - инструкция по использованию бота
/feedback - сообщить о проблеме

'''  # noqa

    START_MESSAGE_2 = '↙️↙️↙️ Все мои возможности есть в меню. Они доступны тебе БЕСПЛАТНО 7 дней!!!, а дальше решишь, оставаться активным пользователем при небольшой оплате 50000KZT/мес или пока посидеть, послушать🙂. Скидка ранним участникам 60% (20000KZT/мес)' # noqa

    POST_THEME_MESSAGE = '*Выберите тему для поста* 📜: \n (Тип: _{type}_) \n\n {themes}'

    WAIT_MESSAGE = 'Подождите пожалуйста, я подбираю темы для поста ... 🔎'

    CHOOSE_TYPE = 'Выберите какой тип поста вы хотите написать:'

    WAIT_CALLBACK_MESSAGE = 'Подождите пожалуйста, я создаю пост, это может занять некоторое время ...📜'

    WAIT_CALLBACK_MESSAGE_FOR_CONTENT_PLAN = 'Подождите пожалуйста, я создаю контент план, это может занять некоторое время ...📜'

    WAIT_CALLBACK_MESSAGE_FOR_IMAGE = 'Подождите пожалуйста, я создаю изображение ... 🖼️'

    WAIT_CALLBACK_MESSAGE_FOR_TEXT = 'Подождите пожалуйста, я создаю текст для поста ... 📜'

    CHOOSE_CUSTOM_NICHE_MESSAGE = 'Напишите свой вариант для нишы ↩️'

    NICHE_NOT_FOUND_MESSAGE = 'Пожалуйста, в начале расскажите нам больше о вашем бизнесе. Выберите нишу по команде /niches'

    NICHE_CHOSEN = '''Ниша выбрана.

Теперь вы можете:

/create_post - ✍🏻 Создать пост с помощью ИИ. От вас - тема, от меня - оригинальный текст и подходящее изображение.

/create_theme - 💡Подбор идей. У меня есть неисчерпаемая база для тем постов и сторис.
    '''

    CHOOSE_CUSTOM_THEME_MESSAGE = 'Напишите свой вариант темы  ↩️'
    CHOOSE_CUSTOM_IMAGE_PROMPT_MESSAGE = ' Пришлите описание изображения, которое нужно создать.   ↩️'

    REGENERATE_IMAGE = 'Хотите сгенерировать новое изображение?'

    CHOOSE_CONTENT_PLAN_MESSAGE = 'Напишите количество постов в неделю ↩️'

    PAYMENT_MESSAGE = '''
🗓<b>Тарифный план</b>: BasicBoost
В тарифный план входит:
    1. Посты
    2. Изображения
    3. Вопросы

<b>Информация</b>:
    -Цена: 20 000 KZT
    -Период: 1 месяц

<b>После оформления подписки вам станут доступны</b>:
    - Посты
    - Изображения
    - Вопросы

ℹ️ Оплачивая попдписку, вы принимаете условия <a href="https://www.smm.art/privacy/pay.pdf">Публичной оферты</a>
    '''
    # PAYMENT_DESCRIPTION = '''Оплачивая попдписку, вы принимаете условия <a href="https://www.smm.art/privacy/pay.pdf">Публичной оферты</a>'''
    PAYMENT_SUCCESS = "*Платеж на сумму {amount} {currency} прошел успешно!!!*"

    QUESTIONS_ANSWER_MESSAGE = '*Пожалуйста ответьте на несколько вопросов* 📜:\n*Создаю вопросы ...*'

    QUESTIONS_MESSAGE = "*{question}*"

    PROMOCODE_MESSAGE = "Вы хотите купить подписку. У вас есть промокод? Если да, введите его. Если нет, нажмите 'Продолжить без промокода'."

    ERROR_MESSAGE = """Ты не нажал никакую команду 🥴
Всё, что я умею, ты найдешь в меню↙️↙️↙️
                """

    HELP = """
🛠Как пользоваться чат-ботом SMMart?

⚙️ Запустите бота командой /start.

⚙️ В меню чата выберите команду /niches, чтобы задать нишу вашего бренда.

Если в предложенном ботом списке отсутствует ваша сфера деятельности, выберите пункт «Написать свой вариант» и задайте нишу самостоятельно (наберите текстовый ответ на сообщение бота).

⚙️ После выбора ниши через меню бота выберите команду /create_post, чтобы сгенерировать готовый пост на нужную вам тему (наберите текстовый ответ на сообщение бота).

⚙️ Если вам нужна помощь с идеями для постов, через меню бота выберите команду /create_theme.

Далее из предложенного списка выберите тип контента — и SMMart сгенерирует подборку из 10 тем для постов.

Просто выберите порядковый номер темы, чтобы сгенерировать по ней готовый пост.

⚙️ Если вас не устраивает получившийся пост или список идей, вы можете запросить у SMMart новый вариант через команды выпадающего меню «Получить другой текст» или «Получить другие темы».

⚙️ Иногда бот задаёт уточняющие вопросы, чтобы генерировать более точные и релевантные ответы, которые идеально соответствуют потребностям вашего бизнеса. Пожалуйста, ответьте на них, чтобы получить максимально персонализированный контент.

💡 Для быстрой навигации между доступными командами пользуйтесь меню чат-бота.
"""

    FEEDBACK_TEXT = '''
Есть проблемы, пожелания, идеи или любые вопросы?

Пиши их прямо в чат *ОДНИМ ТЕКСТОМ* прямо сейчас.

Их прочитает ральный человек 😊

'''

    NOTIFY_FOR_FREE_USE_DAYS = """Так-так 🕒

Напоминаем: осталось всего {day} {day_name}, чтобы воспользоваться бесплатной неделей безлимита на SMMart. 

Не упусти шанс создать уникальные посты для своих подписчиков, используя все преимущества нашего обновлённого чат-бота. 

Твори, экспериментируй, прокачай свои навыки SMM до максимума 😎👌
"""

    NOTIFY_FOR_EXPIRED_SUBSCRIPTION = """Упс… У вас закончилась подписка

Для того, чтобы продолжить пользоваться ботом, выберите удобный для вас тариф, перейдя по кнопке /buy_subscription:

🎯1 день - всего лишь 2,000 тенге (да-да, как стоимость одного кофе в Старбакс)
🎯1 неделя - 10,000 тенге (или как за поход в кино вдвоем)
🎯1 месяц - 20,000 тенге (выгода этого весьма очевидна 😉)
"""

    NOTIFY_FOR_EXPIRED_FREE_DAYS = """Упс… У вас закончился бесплатный период🥺

Для того, чтобы продолжить пользоваться ботом, выберите удобный для вас тариф, перейдя по кнопке /buy_subscription:

🎯1 день - всего лишь 2,000 тенге (да-да, как стоимость одного кофе в Старбакс)
🎯1 неделя - 10,000 тенге (или как за поход в кино вдвоем)
🎯1 месяц - 20,000 тенге (выгода этого весьма очевидна 😉)
"""


class ChatPrompts(Enum):
    CONTENT_PLAN = os.getenv('CONTENT_PLAN')
    POST_THEME = os.getenv('POST_THEME')
    CREATE_POST = os.getenv('CREATE_POST')
    CREATE_PROMPT = prompt
    CREATE_IMAGE = os.getenv('CREATE_IMAGE')
    CLARIFICATION_PROMPT = '''
        «Вы в роли менеджера социальных сетей для «{niche_name}». Я дам вам название поста на русском языке. Ваша задача просто сказать «Готово», если у вас достаточно информации, чтобы написать содержательный пост в Instagram из 100 слов по заголовку поста. Если у вас недостаточно информации для содержательного сообщения, вы должны ответить «У меня есть вопросы». Заголовок поста: «{title}»"
    '''  # noqa
    LIST_OF_QUESTIONS = "Дайте мне список ваших вопросов, каждый на новой строке"


class ImageStyles(Enum):
    THREED_MODEL = "3d-model"
    ANALOG_FILM = "analog-film"
    ANIME = "anime"
    CINEMATIC = "cinematic"
    COMIC_BOOK = "comic-book"
    DIGITAL_ART = "digital-art"
    ENHANCE = "enhance"
    FANTASY_ART = "fantasy-art"
    ISOMETRIC = "isometric"
    LINE_ART = "line-art"
    LOW_POLY = "low-poly"
    # MODELING_COMPOUND = "modeling-compound"  # Пока не нашел промпты для этого стиля
    NEON_PUNK = "neon-punk"
    ORIGAMI = "origami"
    PHOTOGRAPHIC = "photographic"
    PIXEL_ART = "pixel-art"
    # TILE_TEXTURE = "tile-texture"  # Пока не нашел промпты для этого стиля


IMAGES_STYLES_REPLICATE = {
    "3d-model": {
        "prompt": "professional 3d model {prompt}. octane render, highly detailed, volumetric, dramatic lighting",
        "negative_prompt": "ugly, deformed, noisy, low poly, blurry, painting"
    },
    "analog-film": {
        "prompt": "analog film photo {prompt}. faded film, desaturated, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured"
    },
    "anime": {
        "prompt": "anime artwork {prompt}. anime style, key visual, vibrant, studio anime, highly detailed",
        "negative_prompt": "photo, deformed, black and white, realism, disfigured, low contrast"
    },
    "cinematic": {
        "prompt": "cinematic film still {}. shallow depth of field, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured"
    },
    "comic-book": {
        "prompt": "comic {prompt}. graphic illustration, comic art, graphic novel art, vibrant, highly detailed",
        "negative_prompt": "photograph, deformed, glitch, noisy, realistic, stock photo"
    },
    "digital-art": {
        "prompt": "concept art {prompt}. digital artwork, illustrative, painterly, matte painting, highly detailed",
        "negative_prompt": "photo, photorealistic, realism, ugly"
    },
    "enhance": {
        "prompt": "breathtaking {prompt}. award-winning, professional, highly detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, distorted, grainy"
    },
    "fantasy-art": {
        "name": "fantasy-art",
        "prompt": "ethereal fantasy concept art of  {prompt}. magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
        "negative_prompt": "photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white"
    },
    "isometric": {
        "prompt": "isometric style {prompt}. vibrant, beautiful, crisp, detailed, ultra detailed, intricate",
        "negative_prompt": "deformed, mutated, ugly, disfigured, blur, blurry, noise, noisy, realistic, photographic"
    },
    "line-art": {
        "prompt": "line art drawing {prompt}. professional, sleek, modern, minimalist, graphic, line art, vector graphics",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, blurry, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, mutated, realism, realistic, impressionism, expressionism, oil, acrylic"
    },
    "low-poly": {
        "prompt": "low-poly style {prompt}. low-poly game art, polygon mesh, jagged, blocky, wireframe edges, centered composition",
        "negative_prompt": "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo"
    },
    "neon-punk": {
        "prompt": "neonpunk style {prompt}. cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured"
    },
    "origami": {
        "prompt": "origami style {prompt}. paper art, pleated paper, folded, origami art, pleats, cut and fold, centered composition",
        "negative_prompt": "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo"
    },
    "photographic": {
        "prompt": "cinematic photo {prompt}. 35mm photograph, film, bokeh, professional, 4k, highly detailed",
        "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly"
    },
    "pixel-art": {
        "prompt": "pixel-art {prompt}. low-res, blocky, pixel art style, 8-bit graphics",
        "negative_prompt": "sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic"
    }
}


class LikePostTypes(Enum):
    LIKE = ("👍", "like_post")
    DISLIKE = ("👎", "dislike_post")


class TextSize(Enum):
    BIG_TEXT = ("Хочу больше текста", "more_text")
    SMALL_TEXT = ("Хочу меньше текста", "less_text")


class LikeImageTypes(Enum):
    LIKE = ("👍", "like_image")
    DISLIKE = ("👎", "dislike_image")


class TextStyles(Enum):
    SCIENTIFIC = "Научный стиль"
    OFFICIAL_BUSINESS = "Официально-деловой стиль"
    PUBLICISTIC = "Публицистический стиль"
    COLLOQUIAL = "Разговорный стиль"
    ARTISTIC = "Художественный стиль"


class PaymentTarifs(Enum):
    DAY = ("1 День-2000 KZT", "2000")
    WEEK = ("Неделя-10000 KZT", "10000")
    MONTH = ("Месяц-20000 KZT", "20000")


class Resolutions(Enum):
    X2 = "1024x1024"
    INST_900 = "1344x768"
    INST_600 = "768x1344"


class ChatEnum(str, Enum):
    POSTS = "POSTS"
    IMAGES = "IMAGES"
    THEMES = "THEMES"


class MessageTypeEnum(str, Enum):
    TEXT = "TEXT"
    POST = "POST"
    IMAGE = "IMAGE"
    THEME = "THEME"


class SenderEnum(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
