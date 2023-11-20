import pandas as pd
from flet import *
import flet as ft
import Library_tools as lt
import time


def main(page: ft.Page):
    def good_banner():
        """
        Отображает баннер с сообщением об успешном выполнении операции.
        """
        def close_banner(e):
            page.banner.open = False
            page.update()

        bt = ft.TextButton(on_click=close_banner)

        page.banner = ft.Banner(
            leading=ft.Icon(ft.icons.DONE, color=ft.colors.GREEN, size=40),
            content=ft.Text(
                "Изменения успешно сохранены!"
            ),
            actions=[
                bt,
            ],
        )

        page.banner.open = True
        page.update()

        for i in range(5, 0, -1):
            bt.text = f'скрыть ({i})'
            page.update()
            time.sleep(1)

        page.banner.open = False
        page.update()

    def bad_banner(message):
        """
        Отображает баннер с сообщением об ошибке выполнения операции.

        Args:
        - message (str): Сообщение об ошибке.
        """
        def close_banner(e):
            page.banner.open = False
            page.update()

        bt = ft.TextButton(on_click=close_banner)

        page.banner = ft.Banner(
            leading=ft.Icon(ft.icons.CANCEL, color=ft.colors.RED, size=40),
            content=ft.Text(
                f"{message}"
            ),
            actions=[
                bt,
            ],
        )

        page.banner.open = True
        page.update()

        for i in range(5, 0, -1):
            bt.text = f'скрыть ({i})'
            page.update()
            time.sleep(1)

        page.banner.open = False
        page.update()

    def page_report():
        """
        Возвращает интерфейс для генерации различных отчетов о состоянии библиотеки.
        """
        def button_clicked(e):

            def alert_dialog_table_2columns(text1, text2, table):
                dlg = ft.AlertDialog(

                    title=Column([Column([ft.Text(text1)]),
                                  Column([ft.DataTable(

                                      columns=[
                                          ft.DataColumn(ft.Text(table.columns[0])),
                                          ft.DataColumn(ft.Text(table.columns[1]))]
                                      ,
                                      rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(i)) for i in n]) for n in
                                            table.values]

                                  ), ], height=400, scroll=True),
                                  Column([ft.Text(text2)])])
                )
                page.dialog = dlg
                dlg.open = True
                page.update()

            def alert_dialog_table_7columns(text1, text2, table):
                dlg = ft.AlertDialog(

                    title=Column([Column([ft.Text(text1)]),
                                  Column([ft.DataTable(

                                      columns=[
                                          ft.DataColumn(ft.Text(table.columns[0])),
                                          ft.DataColumn(ft.Text(table.columns[1])),
                                          ft.DataColumn(ft.Text(table.columns[2])),
                                          ft.DataColumn(ft.Text(table.columns[3])),
                                          ft.DataColumn(ft.Text(table.columns[4])),
                                          ft.DataColumn(ft.Text(table.columns[5])),
                                          ft.DataColumn(ft.Text(table.columns[6]))
                                      ]
                                      ,
                                      rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(i)) for i in n]) for n in
                                            table.values]

                                  ), ], height=400, scroll=True),
                                  Column([ft.Text(text2)])])
                )
                page.dialog = dlg
                dlg.open = True
                page.update()

            def alert_dialog_table_3columns(text1, text2, table):
                dlg = ft.AlertDialog(

                    title=Column([Column([ft.Text(text1)]),
                                  Column([ft.DataTable(

                                      columns=[
                                          ft.DataColumn(ft.Text(table.columns[0])),
                                          ft.DataColumn(ft.Text(table.columns[1])),
                                          ft.DataColumn(ft.Text(table.columns[2]))]
                                      ,
                                      rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(i)) for i in n]) for n in
                                            table.values]

                                  ), ], height=400, scroll=True),
                                  Column([ft.Text(text2)])])
                )
                page.dialog = dlg
                dlg.open = True
                page.update()

            def alert_dialog_text(text):

                dlg = ft.AlertDialog(
                    title=ft.Text(f"{text}"),
                )
                page.dialog = dlg
                dlg.open = True
                page.update()

            value = dd.value

            if value == '1':
                number = lt.count('books')
                alert_dialog_text(f'Всего книг в библиотеке {number}')

            elif value == '2':
                number = lt.count('readers')
                alert_dialog_text(f'Всего читателей в библиотеке {number}')

            elif value == '3':
                table = lt.counting_all_readers()
                if type(table) == pd.DataFrame:
                    alert_dialog_table_3columns('Читателей, которые брали книги\nв библиотеке',
                                                f"Всего книг было взято: {table['book_summury'].sum()}", table)
                else:
                    bad_banner(table)

            elif value == '4':
                table = lt.counting_book_hand()
                if type(table) == pd.DataFrame:
                    alert_dialog_table_3columns('Читатели, которые не вернули\nкниги в библиотеку',
                                                f"Всего книг на руках: {table['book_summury'].sum()}", table)
                else:
                    bad_banner(table)

            elif value == '5':
                table = lt.last_visit_library()
                if type(table) == pd.DataFrame:
                    alert_dialog_table_3columns('Дата крайнего посещения\nбиблиотеки',
                                                f"", table)
                else:
                    bad_banner(table)

            elif value == '6':
                table = lt.popular_author()
                if type(table) == pd.DataFrame:
                    alert_dialog_table_3columns('Самые популярные авторы\n',
                                                f"", table)
                else:
                    bad_banner(table)

            elif value == '7':
                table = lt.popular_genre()
                if type(table) == pd.DataFrame:
                    alert_dialog_table_2columns('Самые популярные жанры\n',
                                                f"", table)
                else:
                    bad_banner(table)

            elif value == '8':
                table = lt.popular_genre_readers()
                if type(table) == pd.DataFrame:
                    alert_dialog_table_3columns('Самый популярный жанр по читателям\n',
                                                f"", table)
                else:
                    bad_banner(table)

            else:
                table = lt.overdue_borrowers()
                if type(table) == pd.DataFrame:
                    alert_dialog_table_7columns('Отчет о читателях, которые не сдали книгу вовремя',
                                                f"Отчет сохранен в корневой папке проекта 'overdue_borrowers.csv'", table)
                else:
                    bad_banner(table)

        menu = {1: 'Количество книг в библиотеке',
                2: 'Количество читателей',
                3: 'Сколько книг брал каждый читатель за все время',
                4: 'Сколько книг сейчас находится на руках у каждого читателя',
                5: 'Дата последнего посещения читателем библиотеки',
                6: 'Самый читаемый автор',
                7: 'Самый предпочитаемые читателями жанры по убыванию',
                8: 'Любимый жанр каждого читателя',
                9: 'Отчет о читателях, которые не сдали книгу вовремя'}
        b = ft.ElevatedButton(text="Сформировать отчет", on_click=button_clicked)
        dd = ft.Dropdown(
            options=[ft.dropdown.Option(k, v) for k, v in menu.items()],
        )

        return ft.Column(controls=[dd, b])

    def page_rent():
        """
        Возвращает интерфейс для аренды и возврата книг читателями.
        """
        tb_rent_book1 = ft.TextField(label="Введите ID читателя", border="underline")
        tb_rent_book2 = ft.TextField(label="Введите ID книги", border="underline")
        tb_rent_book3 = ft.TextField(label="Введите дату выдачи книги (%Y-%m-%d)", border="underline")
        tb_rent_book4 = ft.TextField(label="Введите планируемую дату возврата книги (%Y-%m-%d)", border="underline")
        tb_rent_book5 = ft.TextField(label="Введите дату возврата книги (%Y-%m-%d)", border="underline")

        def rent_book(e):
            id_reader = tb_rent_book1.value
            id_book = tb_rent_book2.value
            taken_date = tb_rent_book3.value
            planned_return_date = tb_rent_book4.value

            if id_book and id_reader and taken_date and planned_return_date:
                flag, message = lt.rent_book(id_reader, id_book, taken_date, planned_return_date)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        def return_book(e):
            id_book = tb_rent_book2.value
            return_date = tb_rent_book5.value

            if id_book and return_date:
                flag, message = lt.return_book(id_book, return_date)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        return ft.Tabs(
            selected_index=1,
            animation_duration=500,
            tabs=[
                ft.Tab(
                    text="Арендовать книгу",
                    content=Column([
                        ft.Container(
                            content=tb_rent_book1, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_rent_book2, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_rent_book3, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_rent_book4, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=rent_book),
                            alignment=ft.alignment.center_right,
                        ), ]),
                ),
                ft.Tab(
                    text="Оформить возврат книги",
                    content=Column([
                        ft.Container(
                            content=tb_rent_book2, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_rent_book5, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=return_book),
                            alignment=ft.alignment.center_right,
                        ), ]),
                ),
            ],
            expand=1,
        )

    def page_books():
        """
        Возвращает интерфейс для добавления, редактирования и удаления информации о книгах в библиотеке.
        """
        tb_add_book1 = ft.TextField(label="Введите ФИО автора", border="underline")
        tb_add_book2 = ft.TextField(label="Введите название книги", border="underline")
        tb_add_book3 = ft.TextField(label="Введите жанр книги", border="underline")

        tb_edit_book1 = ft.TextField(label="Введите ID книги", border="underline")
        tb_edit_book2 = ft.TextField(label="Введите старое или обновленное ФИО автора", border="underline")
        tb_edit_book3 = ft.TextField(label="Введите старое или обновленное название книги", border="underline")
        tb_edit_book4 = ft.TextField(label="Введите старый или обновленный жанр книги", border="underline")

        def add_book(e):
            author = tb_add_book1.value
            name = tb_add_book2.value
            genre = tb_add_book3.value

            if author and name and genre:
                flag, message = lt.add_book(author, name, genre)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        def edit_book(e):
            id_book = tb_edit_book1.value
            author = tb_edit_book2.value
            name = tb_edit_book3.value
            genre = tb_edit_book4.value

            if author and name and genre and id_book:
                flag, message = lt.edit_book(id_book, author, name, genre)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        def deleted_book(e):
            id_book = tb_edit_book1.value

            if id_book:
                flag, message = lt.deleted_book(id_book)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        return ft.Tabs(
            selected_index=1,
            animation_duration=500,
            tabs=[
                ft.Tab(
                    text="Добавить книгу",
                    content=Column([
                        ft.Container(
                            content=tb_add_book1, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_add_book2, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_add_book3, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=add_book),
                            alignment=ft.alignment.center_right,
                        ), ])
                ),
                ft.Tab(
                    text="Редактировать книгу",
                    content=Column([
                        ft.Container(
                            content=tb_edit_book1, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_edit_book2, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_edit_book3, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_edit_book4, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=edit_book),
                            alignment=ft.alignment.center_right,
                        ), ]),
                ),
                ft.Tab(
                    text="Удалить книгу",
                    content=Column([
                        ft.Container(
                            content=tb_edit_book1, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=deleted_book),
                            alignment=ft.alignment.center_right,
                        ), ]),
                ),

            ],
            expand=1,
        )

    def page_readers():
        """
        Возвращает интерфейс для добавления, редактирования и удаления информации о читателях библиотеки.
        """
        tb_add_reader1 = ft.TextField(label="Введите ФИО читателя", border="underline")

        tb_edit_reader1 = ft.TextField(label="Введите ID читателя", border="underline")
        tb_edit_reader2 = ft.TextField(label="Введите обновленное ФИО читателя", border="underline")

        def add_reader(e):
            reader = tb_add_reader1.value

            if reader:
                flag, message = lt.add_reader(reader)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        def edit_reader(e):
            id_reader = tb_edit_reader1.value
            name_reader = tb_edit_reader2.value

            if id_reader and name_reader:
                flag, message = lt.edit_reader(id_reader, name_reader)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        def deleted_reader(e):
            id_reader = tb_edit_reader1.value

            if id_reader:
                flag, message = lt.deleted_reader(id_reader)
                if flag:
                    good_banner()
                else:
                    bad_banner(message)
                page.update()

        return ft.Tabs(
            selected_index=1,
            animation_duration=500,
            tabs=[
                ft.Tab(
                    text="Добавить читателя",
                    content=Column([
                        ft.Container(
                            content=tb_add_reader1, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=add_reader),
                            alignment=ft.alignment.center_right,
                        ), ]),
                ),
                ft.Tab(
                    text="Редактировать информацию о читателе",
                    content=Column([
                        ft.Container(
                            content=tb_edit_reader1, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=tb_edit_reader2, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=edit_reader),
                            alignment=ft.alignment.center_right,
                        ), ]),
                ),
                ft.Tab(
                    text="Удалить информацию о читателе",
                    content=Column([
                        ft.Container(
                            content=tb_edit_reader1, alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text="ОК", on_click=deleted_reader),
                            alignment=ft.alignment.center_right,
                        ),
                    ]),
                )
            ],
            expand=1,
        )

    t = ft.Tabs(
        selected_index=1,
        animation_duration=500,

        tabs=[
            ft.Tab(
                text="Читатели",
                content=ft.Container(
                    page_readers()
                )
                ,
            ),
            ft.Tab(
                text="Книги",
                content=ft.Container(
                    page_books()
                ),
            ),
            ft.Tab(
                text="Аренда книг",
                content=ft.Container(
                    page_rent()
                ),
            ),
            ft.Tab(
                text="Отчеты",
                content=ft.Container(
                    page_report()
                )
            )
        ],
        expand=1
    )

    page.add(t)


lt.create_table_db()
ft.app(target=main)
