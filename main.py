import json
import subprocess

from fpdf import FPDF


class CustomPDF(FPDF):
    def header(self):
        self.set_fill_color(40, 40, 40)
        self.rect(0, 0, self.w, self.h, 'F')

    def footer(self):
        pass


def public():
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "update"])
    subprocess.run(["git", "push"])
    print("Правила опубликованы!")


def create_pdf(name):
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=0)

    font_path = 'fonts/Bold.ttf'  # замени на свой путь
    pdf.add_font('CustomFont', '', font_path, uni=True)

    yellow = (255, 255, 0)
    red = (255, 79, 58)
    green = (140, 255, 0)
    blue = (0, 111, 255)
    orange = (255, 155, 0)
    white = (255, 255, 255)

    with open(f'{name}.json', 'r', encoding='utf-8') as f:
        file = json.load(f)
        data = [(entry['role'], entry['content']) for entry in file['entries']]

    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    for title, text in data:
        needed_height = 8 * (1.5 + 13)  # размер пустоты для новой страницы
        current_y = pdf.get_y()
        if current_y + needed_height > pdf.page_break_trigger:
            pdf.add_page()
        if name == 'kyb':
            if title in ['']:
                pdf.add_page()
        if title in ["Ищейка", "Адвокат", "Мафия", "Маньяк", "Картель", "Оборотень", 'Стукач', 'Сектант',
                     'Мафиози', 'Одиночки', 'Крёстный отец', 'Вор', 'Потрошитель', 'Аферист', 'Якудза',
                     'Мафия и картель', 'Преступники', 'Любовница', 'Босс', 'Дон', 'Отравитель', 'Революционер',
                     'Зомби', 'Консильери', 'Минер', 'Берсерк']:
            pdf.set_text_color(*red)
        elif title in ['Детектив', 'Сыщик и Патрульный', 'Супермирный']:
            pdf.set_text_color(*blue)
        elif title in ['Золотая минута', 'Переголосование', 'Вскрытие роли','Рейтинг']:
            pdf.set_text_color(*yellow)
        elif title in ['Что нового:']:
            pdf.set_text_color(*blue)
        else:
            pdf.set_text_color(*green)

        # ─── Заголовок ────────────────────────────────────────────────────────────
        pdf.set_font('CustomFont', size=28)
        pdf.multi_cell(0, 16, title, align="C")

        # ─── Картинка ────────────────────────────────────────────────────────────
        images = True
        if images:
            menu_images = {'Главное меню': '1',
                            'Управление игрой': '2',
                            'Режимы раздачи ролей': '4',
                            'Окно знакомства': '6',
                            'Окно ночного выбора': '7',
                            'Окно результата ночи': '9',
                            'Окно результата голосования': '10',
                            'Отмена результата ночи или голосования': '11',
                            'Рейтинговая система': '12'}
            if title in menu_images:
                img_path = f'images/{menu_images[title]}.jpg'
                text_width = pdf.w - pdf.l_margin - pdf.r_margin
                pdf.image(img_path, x=pdf.l_margin, w=text_width)
                pdf.ln(5)
                if menu_images[title] in ['2', '4', '7']:
                    img_path = f'images/{int(menu_images[title]) + 1}.jpg'
                    text_width = pdf.w - pdf.l_margin - pdf.r_margin
                    pdf.image(img_path, x=pdf.l_margin, w=text_width)
                    pdf.ln(5)

            roles_images = {
                "Вор": 'thief',
                "Маньяк": 'maniac',
                "Агент": 'agent',
                "Адвокат": 'advocate',
                "Мафия": 'mafia',
                "Картель": 'cartel',
                "Якудза": 'yakuza',
                'Стукач': 'slanderer',
                "Красотка": 'fucker',
                'Телохранитель': 'bodyguard',
                "Доктор": 'doc',
                "Детектив": 'cop',
                "Сыщик": 'finder',
                "Патрульный": 'patrol',
                "Сыщик и Патрульный": 'finder',
                "Журналист": 'aferist',
                "Мститель": 'avenger',
                "Оборотень": 'werewolf',
                "Везунчик": 'lucker',
                "Экстрасенс": 'ekstrasens',
                'Судья': 'judge',
                'Сектант': 'sect',
                'Дон': 'don',
                'Отравитель': 'poisoner',
                'Супермирный': 'superman',
                'Близнецы': 'twins',
                'Зомби': 'zombie',
                'Зеркало': 'glass',
                'Консильери': 'consigliere',
                'Минер': 'bomber',
                'Лидер': 'leader',
                'Оратор': 'speaker',
                'Берсерк': 'berserk',
                'Провокатор': 'provocator'}
            if title in roles_images:
                img1_path = f'images/roles/{roles_images[title]}1.png'
                img2_path = f'images/roles/{roles_images[title]}2.png'
                page_height = pdf.h - pdf.t_margin
                img_height = page_height / 3
                img_width = (pdf.w - pdf.l_margin - pdf.r_margin - 5) / 2
                y = pdf.get_y()
                pdf.image(img1_path, x=pdf.l_margin, y=y, w=img_width, h=img_height)
                pdf.image(img2_path, x=pdf.l_margin + img_width + 5, y=y, w=img_width, h=img_height)

                pdf.set_y(y + img_height + 5)

        # ─── Текст ────────────────────────────────────────────────────────────────
        pdf.set_text_color(*white)
        pdf.set_font('CustomFont', size=22)
        pdf.multi_cell(0, 9, text.strip(), align="L")

    pdf.output('ПРАВИЛА' + '.pdf')
    print(f"PDF создан: {name}")


create_pdf('kyb')
public()
