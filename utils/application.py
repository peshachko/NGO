#!/usr/bin/env python
"""Handle membership application.

Note
-----
Requires: ``sudo dnf install pdftk-java`` and ``pip install pymupdf``

"""

import argparse
import subprocess
from datetime import datetime

import pymupdf

# Initial text that I can customize later.
INITIAL_MAIL = """Здравей {name}!

Радвам се, че искаш да бъдеш Пешачко -- {welcome_cap}.

Нашата инициатива е начин на себеизразяване, тя не е по задължение, така че участвай в нея
по начин, който ти пасва. Няма очаквания за резултати :)

Стремим се да сме отворено сдружение и цялата ни документация, уеб страница,
счетоводство и дискусии за проекти (и за това как да се развиваме) е достъпна за всеки в
GitHub (https://github.com/peshachko). Ако имаш желание да участваш в дискусията там, но
не си {sure} как да го направиш, кажи и ще се опитам да ти помогна.

Разбира се имаме и групи във Фейсбук, Инстаграм и Вайбър, но те са с по-различна
насоченост.

Моля те потвърди, че си {received} този мейл, и че ти си ни {sent} заявлението за
членство (което съм прикачил попълнено и от нас).

Поздрави,
Димитър
"""


def get_gender_variants(gender="f"):
    f = gender == "f"
    variants = dict(
        welcome="добре дошла" if f else "добре дошъл",
        familiar="запозната" if f else "запознат",
        received="получила" if f else "получил",
        sent="изпратила" if f else "изпратил",
        sure="сигурна" if f else "сигурен",
    )

    variants.update(
        {key + "_cap": value.capitalize() for key, value in variants.items()}
    )
    return variants


def parse_args():
    parser = argparse.ArgumentParser(description="Handle the application form.")

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        required=True,
    )

    show_parser = subparsers.add_parser(
        "show",
        help="Extract form fields from a PDF membership application.",
    )
    show_parser.add_argument("filename", help="Path to the PDF file")
    show_parser.set_defaults(func=show_form_data)

    fill_parser = subparsers.add_parser(
        "fill",
        help="Fill membership application.",
    )
    fill_parser.add_argument("filename", help="Path to the PDF file")
    fill_parser.add_argument(
        "-g",
        "--gender",
        choices=["f", "m"],
        default="f",
        help="Gender of applicant.",
    )
    fill_parser.add_argument(
        "-m",
        dest="email",
        action="store_true",
        help="Generate initial mail",
    )
    fill_parser.set_defaults(func=fill_application)

    return parser.parse_args()


def fill_application(args):
    doc = pymupdf.open(args.filename)

    first_page = doc[0]
    widgets = {w.field_name: w for w in first_page.widgets()}
    email = widgets["email"].field_value
    first_name = widgets["name"].field_value.split()[0]

    gender_variants = get_gender_variants(args.gender)
    welcome = gender_variants["welcome"]

    widgets["decision"].field_value = f"{first_name}, {welcome} в Пешачко!"
    widgets["decision-date"].field_value = datetime.today().strftime("%d/%m/%Y")
    widgets["representative"].field_value = "Димитър @ Пешачко"

    # it is better to update all fields so that the fonts are the same
    for name in [
        "name",
        "email",
        "date",
        "decision",
        "decision-date",
        "representative",
    ]:
        widgets[name].update()

    doc.save(f"build/{email}.pdf")

    if args.email:
        with open("build/email.txt", "w") as h:
            h.write(INITIAL_MAIL.format(name=first_name, **gender_variants))


# FIXME: probably I should use pymupdf (as in fill_application) instead of pdftk
def extract_form_data(pdf_path):
    result = subprocess.run(
        ["pdftk", pdf_path, "dump_data_fields_utf8"],
        capture_output=True,
        text=True,
    )

    fields = {}
    current_name = None

    for line in result.stdout.splitlines():
        if line.startswith("FieldName:"):
            current_name = line.split(":", 1)[1].strip()
        elif line.startswith("FieldValue:") and current_name is not None:
            fields[current_name] = line.split(":", 1)[1].strip()

    return fields


def show_form_data(args):
    data = extract_form_data(args.filename)
    for key, value in data.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    args = parse_args()
    args.func(args)
