import json
from fpdf import FPDF


class CustomPDF(FPDF):
    def header(self):
        self.set_fill_color(40, 40, 40)
        self.rect(0, 0, self.w, self.h, 'F')

    def footer(self):
        pass


def create_pdf(name):
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=0)

    font_path = 'fonts/Bold.ttf'  # замени на свой путь
    pdf.add_font('CustomFont', '', font_path, uni=True)

    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 111, 255)
    white = (255, 255, 255)

    with open(f'{name}.json', 'r', encoding='utf-8') as f:
        file = json.load(f)
        for i in file['entries']:
            i['content'] = i['content'].replace('\n    ', ' ')
            i['content'] = i['content'].replace('     ', '')
            i['content'] = i['content'].replace('    ', '')
        data = [(entry['role'], entry['content']) for entry in file['entries']]

    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    line_height = 8

    for title, text in data:
        needed_height = line_height * (1.5 + 3)  # заголовок 1.5 линии + 3 строки текста
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
        else:
            pdf.set_text_color(*yellow)
        pdf.set_font('CustomFont', size=28)
        pdf.cell(0, line_height * 1.5, title, ln=True, align="C")

        pdf.set_text_color(*white)
        pdf.set_font('CustomFont', size=22)
        pdf.multi_cell(0, line_height, text.strip())

    pdf.output('ПРАВИЛА' + '.pdf')
    print(f"PDF создан: {name}")


create_pdf('kyb')
