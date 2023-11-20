import sqlite3
from typing import List
from datetime import datetime
import pandas as pd

db_path = 'library.db'


def check_table_db(c: sqlite3.Cursor, table_name: str) -> bool:
    """
    Проверяет наличие таблицы в базе данных.

    Args:
    - c (sqlite3.Cursor): Курсор для выполнения запросов к базе данных.
    - table_name (str): Название таблицы для проверки наличия.

    Returns:
    - bool: Возвращает True, если таблица существует в базе данных, иначе возвращает False.
    """

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    table_exists = c.fetchone()

    if not table_exists:
        return True

    return False


def record_table_db(c: sqlite3.Cursor, table_name: str, data: List[tuple]) -> None:
    """
    Вставляет записи в таблицу базы данных SQLite.

    Args:
    - c (sqlite3.Cursor): Курсор для выполнения запросов к базе данных.
    - table_name (str): Название таблицы, в которую будут вставлены записи.
    - data (List[tuple]): Список кортежей, содержащих данные для вставки в таблицу.

    Returns:
    - None
    """
    for record in data:
        placeholders = ', '.join('?' * len(record))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        c.execute(query, record)


def create_table_db() -> None:
    """
    Создает таблицы в базе данных SQLite и заполняет их тестовыми данными.


    Returns:
    - None

    Description:
    Функция create_table_db создает таблицы authors,
    books, readers и return_book в этой базе данных, если они еще не существуют. Каждая таблица создается
    с заданными полями (id и другие) с использованием SQL-запросов из словаря table_create.

    Затем функция заполняет каждую из созданных таблиц тестовыми данными из словаря test_data. Каждая
    таблица имеет предварительно определенные строки с данными, соответствующими структуре таблицы.
    """
    table_create = {
        'authors': '''
        CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL);
        ''',
        'books': '''
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        name_book VARCHAR(255) NOT NULL,
        genre VARCHAR(255) NOT NULL,
        author_id INT REFERENCES authors(id),
        availability VARCHAR(255) NOT NULL
        );
        ''',
        'readers': '''
        CREATE TABLE IF NOT EXISTS readers (
        id INTEGER PRIMARY KEY, 
        name_reader VARCHAR(255) NOT NULL);
        ''',
        'return_book': '''
        CREATE TABLE IF NOT EXISTS return_book (
        id INTEGER PRIMARY KEY, 
        book_id INT REFERENCES books(id), 
        reader_id INT REFERENCES readers(id), 
        data_taken DATE NOT NULL, 
        data_return DATE, 
        planned_return_date DATE NOT NULL
        );
        '''

    }

    test_data = {
        'authors': [
            (1, 'Leo Tolstoy'),
            (2, 'Jane Austen'),
            (3, 'Fyodor Dostoevsky'),
            (4, 'Charles Dickens'),
            (5, 'Mark Twain'),
            (6, 'Agatha Christie'),
            (7, 'J.K. Rowling'),
            (8, 'Ernest Hemingway'),
            (9, 'Gabriel Garcia Marquez'),
            (10, 'Virginia Woolf')
        ],
        'books': [
            (1, 'War and Peace', 'роман', 1, 'Available'),
            (2, 'Anna Karenina', 'роман', 1, 'Available'),
            (3, 'Pride and Prejudice', 'роман', 2, 'Not available'),
            (4, 'Crime and Punishment', 'триллер', 3, 'Available'),
            (5, 'Great Expectations', 'роман', 4, 'Available'),
            (6, 'The Adventures of Tom Sawyer', 'приключения', 5, 'Not available'),
            (7, 'Murder on the Orient Express', 'детектив', 6, 'Available'),
            (8, 'Harry Potter and the Philosopher\'s Stone', 'фэнтези', 7, 'Not available'),
            (9, 'The Old Man and the Sea', 'роман', 8, 'Available'),
            (10, 'One Hundred Years of Solitude', 'магический реализм', 9, 'Available'),
            (11, 'To the Lighthouse', 'роман', 10, 'Not available'),
            (12, 'The Great Gatsby', 'роман', 8, 'Available')
        ],
        'readers': [
            (1, 'John Doe'),
            (2, 'Jane Smith'),
            (3, 'Alice Johnson'),
            (4, 'David Brown'),
            (5, 'Emily Wilson'),
            (6, 'Michael Davis'),
            (7, 'Sophia Miller'),
            (8, 'William Garcia'),
            (9, 'Olivia Martinez'),
            (11, 'Daniel Lopez'),
        ],
        'return_book': [
            (1, 1, 1, '2023-11-15', '2023-12-05', '2023-12-10'),
            (2, 2, 2, '2023-11-10', '2023-11-28', '2023-12-01'),
            (3, 3, 3, '2023-11-20', None, '2023-12-05'),
            (4, 4, 4, '2023-11-25', '2023-12-10', '2023-12-15'),
            (5, 5, 5, '2023-11-18', None, '2023-12-08'),
            (6, 6, 6, '2023-11-22', '2023-12-05', '2023-12-12'),
            (7, 7, 7, '2023-11-30', None, '2023-12-15'),
            (8, 8, 8, '2023-11-28', '2023-12-10', '2023-12-20'),
            (9, 1, 2, '2023-11-20', '2023-12-02', '2023-12-10'),
            (10, 3, 5, '2023-11-18', None, '2023-12-10'),
            (11, 2, 6, '2023-11-23', '2023-12-05', '2023-12-12'),
            (12, 4, 9, '2023-11-28', '2023-12-10', '2023-12-20'),
            (13, 5, 3, '2023-12-01', None, '2023-12-12'),
            (14, 6, 1, '2023-12-05', '2023-12-23', '2023-12-22'),
            (15, 7, 10, '2023-12-10', '2023-12-25', '2024-01-05'),
        ]
    }

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        for key, value in table_create.items():
            if check_table_db(cursor, key):
                cursor.execute(value)
                data = test_data[key]
                record_table_db(cursor, key, data)

        conn.commit()


def check_author(c: sqlite3.Cursor, author_name: str) -> int:
    """
        Проверяет наличие автора в базе данных.

        Args:
        - c (sqlite3.Cursor): Объект курсора для выполнения запросов к базе данных.
        - author_name (str): Имя автора для проверки.

        Returns:
        - int: ID автора. Если автор не найден, создает запись об авторе и возвращает его ID.
    """

    c.execute("SELECT * FROM authors WHERE name = ?", (author_name,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        c.execute("SELECT * FROM authors WHERE name = ?", (author_name,))
        row = c.fetchone()
    id_authors = row[0]
    return id_authors


def add_book(author: str, name: str, genre: str) -> tuple:
    """
    Добавляет книгу в базу данных.

    Args:
    - author (str): ФИО автора книги.
    - name (str): Название книги.
    - genre (str): Жанр книги.

    Returns:
    tuple: Кортеж из двух элементов. Первый элемент представляет собой булевое значение:
             True, если редактирование прошло успешно, False в противном случае.
             Второй элемент - пустая строка в случае успеха (если редактирование прошло успешно),
             либо содержит объект исключения, возникшего во время выполнения операции редактирования.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            author = check_author(cursor, author)

            cursor.execute(
                """INSERT INTO books (name_book, genre, author_id, availability) 
                VALUES (?, ?, ?, 'Available')""", (
                    name, genre, author))

            conn.commit()
        return True, ''

    except Exception as ex:
        return False, ex


def edit_book(id_book: str, author: str, name: str, genre: str, availability: str = 'Available') -> tuple:
    """
    Редактирует информацию о книге в базе данных.

    Args:
    - id_book (str): Уникальный идентификатор книги в базе данных.
    - author (str): Имя автора книги.
    - name (str): Название книги.
    - genre (str): Жанр книги.

    Returns:
    - tuple: Кортеж из двух элементов. Первый элемент представляет собой булевое значение:
             True, если редактирование прошло успешно, False в противном случае.
             Второй элемент - пустая строка в случае успеха (если редактирование прошло успешно),
             либо содержит объект исключения, возникшего во время выполнения операции редактирования.
    """
    try:
        id_book = int(id_book)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM books WHERE id = ?""", (id_book,))
            row = cursor.fetchone()
            if row:
                author = check_author(cursor, author)
                cursor.execute(
                    """UPDATE books SET name_book = ?, author_id = ?, genre = ?, availability = ? WHERE id = ?""",
                    (name, author, genre, id_book, availability))
                conn.commit()

            else:
                raise ValueError('Книга с указанным ID не существует')

        return True, ''

    except Exception as ex:
        return False, ex


def deleted_book(id_book: str) -> tuple:
    """
        Удаляет информацию о книге в базе данных.

        Args:
        - id_book (str): Уникальный идентификатор книги в базе данных.

        Returns:
        - tuple: Кортеж из двух элементов. Первый элемент представляет собой булевое значение:
                 True, если удаление прошло успешно, False в противном случае.
                 Второй элемент - пустая строка в случае успеха (если удаление прошло успешно),
                 либо содержит объект исключения, возникшего во время выполнения операции удаления.
        """
    try:
        id_book = int(id_book)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM books WHERE id = ?""", (id_book,))
            row = cursor.fetchone()

            if row:
                cursor.execute("""DELETE FROM books WHERE id = ?""", (id_book,))
                conn.commit()

            else:
                raise ValueError('Книгa с указанным ID не существует')

        return True, ''

    except Exception as ex:
        return False, ex


def add_reader(name_reader: str) -> tuple:
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO readers (name_reader) 
                VALUES (?)""", (name_reader,))

            conn.commit()
        return True, ''

    except Exception as ex:
        return False, ex


def edit_reader(id_reader, name_reader) -> tuple:
    try:
        id_reader = int(id_reader)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM readers WHERE id = ?""", (id_reader,))
            row = cursor.fetchone()
            if row:
                cursor.execute("""UPDATE readers SET name_reader = ? WHERE id = ?""", (name_reader, id_reader))
                conn.commit()

            else:
                raise ValueError('Читателя с указанным ID не существует')

        return True, ''

    except Exception as ex:
        return False, ex


def deleted_reader(id_reader: str) -> tuple:
    """
        Удаляет информацию о читателе в базе данных.

        Args:
        - id_reader (str): Уникальный идентификатор читателя в базе данных.

        Returns:
        - tuple: Кортеж из двух элементов. Первый элемент представляет собой булевое значение:
                 True, если удаление прошло успешно, False в противном случае.
                 Второй элемент - пустая строка в случае успеха (если удаление прошло успешно),
                 либо содержит объект исключения, возникшего во время выполнения операции удаления.
        """
    try:
        id_reader = int(id_reader)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM readers WHERE id = ?""", (id_reader,))
            row = cursor.fetchone()

            if row:
                cursor.execute("""DELETE FROM readers WHERE id = ?""", (id_reader,))
                conn.commit()

            else:
                raise ValueError('Информация о человеке с указанным ID не существует')

        return True, ''

    except Exception as ex:
        return False, ex


def rent_book(id_reader: str, id_book: str, data_taken: str, planned_return_date: str) -> tuple:
    """
    Арендует книгу читателю.

    Args:
    - id_reader (str): Уникальный идентификатор читателя в базе данных.
    - id_book (str): Уникальный идентификатор книги в базе данных (в виде строки).
    - data_taken (str): Дата взятия книги в формате "%Y-%m-%d".
    - planned_return_date (str): Планируемая дата возврата книги в формате "%Y-%m-%d".

    Returns:
    - tuple: Кортеж из двух элементов. Первый элемент представляет собой булевое значение:
             True, если операция аренды прошла успешно, False в противном случае.
             Второй элемент - пустая строка в случае успеха (если операция прошла успешно),
             либо содержит объект исключения, возникшего во время выполнения операции аренды.
    """
    try:
        id_book = int(id_book)
        id_reader = int(id_reader)
        if datetime.strptime(data_taken, "%Y-%m-%d") and datetime.strptime(planned_return_date, "%Y-%m-%d"):
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT availability FROM books WHERE id = ?""", (id_book,))
                row = cursor.fetchone()
                if row:
                    if row[0] == 'Not available':
                        raise ValueError('Книга не доступна для выдачи')

                    else:
                        cursor = conn.cursor()
                        cursor.execute("""SELECT * FROM readers WHERE id = ?""", (id_reader,))
                        row = cursor.fetchone()
                        if row:
                            cursor.execute("""
                                        INSERT INTO return_book (book_id, reader_id, data_taken, planned_return_date) VALUES (?, ?, ?, ?);
                                        """, (id_book, id_reader, data_taken, planned_return_date))

                            cursor.execute("""
                                        UPDATE books SET availability = ? WHERE id = ?;
                                        """, ('Not available', id_book))
                            conn.commit()
                        else:
                            raise ValueError('Читателя с указанным ID не существует')
                else:
                    raise ValueError('Книга с указанным ID не существует')
        else:
            raise ValueError('Некорректна указана дата ("%Y-%m-%d")')

        return True, ''

    except Exception as ex:
        return False, ex


def return_book(id_book: str, date_return: str) -> tuple:
    """
    Возвращает книгу обратно в библиотеку.

    Args:
    - id_book (str): Уникальный идентификатор книги в базе данных.
    - data_return (str): Дата возврата книги в формате "%Y-%m-%d".

    Returns:
    - tuple: Кортеж из двух элементов. Первый элемент представляет собой булевое значение:
             True, если операция возврата прошла успешно, False в противном случае.
             Второй элемент - пустая строка в случае успеха (если операция прошла успешно),
             либо содержит объект исключения, возникшего во время выполнения операции возврата.
    """
    try:
        id_book = int(id_book)

        if datetime.strptime(date_return, "%Y-%m-%d"):
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM books WHERE id = ?""", (id_book,))
                row = cursor.fetchone()
                if row:
                    cursor.execute("""
                                UPDATE return_book SET data_return = ? WHERE book_id = ? AND data_return IS NULL;
                                """, (date_return, id_book))

                    cursor.execute("""
                                UPDATE books SET availability = ? WHERE id = ?;
                                """, ('Аvailable', id_book))
                    conn.commit()
                else:
                    raise ValueError('Книга с указанным ID не существует')
        else:
            raise ValueError('Некорректна указана дата ("%Y-%m-%d")')

        return True, ''

    except Exception as ex:
        return False, ex


def count(name_table: str) -> int:
    """
    Выполняет запрос для подсчета количества строк в указанной таблице.

    Args:
    - table_name (str): Имя таблицы, в которой нужно подсчитать количество строк.

    Returns:
    - int: Количество строк в указанной таблице.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT COUNT(*) FROM {name_table}""")
        number = cursor.fetchone()[0]

    return number


def counting_all_readers() -> pd.DataFrame:
    """
    Выполняет запрос к базе данных для подсчета количества взятых книг каждым читателем.

    Returns:
    - pd.DataFrame: DataFrame с информацией о читателях и количестве взятых ими книг.
    Возвращаемые столбцы: 'reader_id' (ID читателя), 'name_reader' (имя читателя), 'book_summary' (общее количество книг).
    """
    query = """
            SELECT r.reader_id, c.name_reader, COUNT(*) AS book_summury
            FROM readers AS c
            JOIN return_book AS r ON c.id = r.reader_id
            GROUP BY r.reader_id, c.name_reader
            """
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df.sort_values('book_summury', ascending=False)
    except Exception as ex:
        pass


def counting_book_hand() -> pd.DataFrame:
    """
    Выполняет запрос к базе данных для подсчета количества книг, которые читатели в настоящее время держат у себя.

    Returns:
    - pd.DataFrame: DataFrame с информацией о читателях и количестве книг, которые они в настоящее время держат у себя.
    Возвращаемые столбцы: 'reader_id' (ID читателя), 'name_reader' (имя читателя), 'book_summary' (общее количество книг).
    """
    query = """
            SELECT r.reader_id, c.name_reader, COUNT(*) AS book_summury
            FROM readers AS c
            JOIN return_book AS r ON c.id = r.reader_id
            WHERE r.data_return IS NULL
            GROUP BY r.reader_id, c.name_reader
            """
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df.sort_values('book_summury', ascending=False)
    except Exception as ex:
        pass


def last_visit_library() -> pd.DataFrame:
    """
    Выполняет запрос к базе данных для определения последнего посещения библиотеки читателями.

    Returns:
    - pd.DataFrame: DataFrame с информацией о читателях и дате их последнего посещения библиотеки.
    Возвращаемые столбцы: 'reader_id' (ID читателя), 'name_reader' (имя читателя), 'last_visit_date' (дата последнего посещения).
    """
    query = """
               SELECT r.reader_id, c.name_reader, MAX(COALESCE(r.data_return, r.data_taken)) AS last_visit_date
               FROM readers AS c
               JOIN return_book AS r ON c.id = r.reader_id
               GROUP BY r.reader_id, c.name_reader
               """

    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df.sort_values('name_reader')
    except Exception as ex:
        pass


def popular_author() -> pd.DataFrame:
    """
    Возвращает DataFrame с информацией о пяти самых популярных авторах по числу арендованных их книг.

    Returns:
    - pd.DataFrame: DataFrame с информацией о пяти самых популярных авторах и количестве арендованных их книг.
    Столбцы: 'id' (ID автора), 'author_name' (имя автора), 'books_borrowed' (общее количество арендованных книг).
    """
    query = """
                    SELECT a.id, a.name AS author_name, COUNT(*) AS books_borrowed
                    FROM authors AS a
                    JOIN books AS b ON a.id = b.author_id
                    JOIN return_book AS r ON b.id = r.book_id
                    GROUP BY a.id, a.name
                    ORDER BY COUNT(*) DESC
                    LIMIT 5;
            """
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as ex:
        print(ex)
        pass


def popular_genre() -> pd.DataFrame:
    """
    Возвращает DataFrame с информацией о пяти самых популярных жанрах по числу арендованных книг.

    Returns:
    - pd.DataFrame: DataFrame с информацией о пяти самых популярных жанрах и количестве арендованных книг каждого жанра.
    Столбцы: 'genre' (жанр), 'borrow_count' (общее количество арендованных книг данного жанра).
    """
    query = """
            SELECT b.genre, COUNT(*) AS borrow_count
            FROM return_book AS r
            JOIN books AS b ON r.book_id = b.id
            GROUP BY b.genre
            ORDER BY COUNT(*) DESC
            LIMIT 5;
            """
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as ex:
        print(ex)
        pass


def popular_genre_readers() -> pd.DataFrame:
    """
    Возвращает DataFrame с информацией о читателях и их любимых жанрах книг.

    Returns:
    - pd.DataFrame: DataFrame с информацией о читателях и их предпочитаемом жанре, который они арендуют чаще всего.
    Столбцы: 'reader_id' (ID читателя), 'reader_name' (имя читателя), 'favorite_genre' (предпочитаемый жанр),
    'borrow_count' (общее количество арендованных книг этого жанра).
    """

    query = """
            SELECT sub.reader_id, sub.reader_name, sub.favorite_genre, sub.borrow_count
            FROM (
                -- Подзапрос для выбора всех жанров для каждого читателя и подсчета количества арендованных книг для каждого жанра
                SELECT r.reader_id, c.name_reader AS reader_name, b.genre AS favorite_genre, COUNT(*) AS borrow_count
                FROM readers AS c
                JOIN return_book AS r ON c.id = r.reader_id
                JOIN books AS b ON r.book_id = b.id
                GROUP BY r.reader_id, c.name_reader, b.genre
            ) AS sub
            JOIN (
                -- Подзапрос для выбора максимального количества арендованных книг для каждого читателя
                SELECT reader_id, MAX(borrow_count) AS max_borrow_count
                FROM (
                    -- Подзапрос для подсчета количества арендованных книг для каждого читателя и жанра
                    SELECT r.reader_id, b.genre, COUNT(*) AS borrow_count
                    FROM readers AS c
                    JOIN return_book AS r ON c.id = r.reader_id
                    JOIN books AS b ON r.book_id = b.id
                    GROUP BY r.reader_id, b.genre
                ) AS counts
                GROUP BY reader_id
            ) AS max_counts
            ON sub.reader_id = max_counts.reader_id AND sub.borrow_count = max_counts.max_borrow_count;
    """

    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as ex:
        pass


def overdue_borrowers() -> pd.DataFrame:
    """
    Возвращает информацию о читателях, у которых есть просроченные книги на основе данных из базы данных.

    Returns:
    - pd.DataFrame: DataFrame с информацией о читателях, арендовавших книги, которые просрочены по сроку возврата.
    Столбцы: 'reader_id' (ID читателя), 'reader_name' (имя читателя), 'book_title' (название просроченной книги),
    'author_name' (имя автора), 'data_taken' (дата взятия книги), 'data_return' (дата возврата книги),
    'planned_return_date' (планируемая дата возврата).
    """
    query = """
            SELECT r.reader_id, c.name_reader AS reader_name, b.name_book AS book_title, a.name AS author_name, r.data_taken, r.data_return, r.planned_return_date
            FROM readers AS c
            JOIN return_book AS r ON c.id = r.reader_id
            JOIN books AS b ON r.book_id = b.id
            JOIN authors AS a ON b.author_id = a.id
            WHERE r.data_return > r.planned_return_date;

    """
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        df.to_csv('overdue_borrowers.csv', sep=';', index=False)
        return df
    except Exception as ex:
        return ex


