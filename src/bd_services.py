import psycopg2
from psycopg2.errors import InvalidCatalogName

from src.base_classes import FunctionsBD


class DBManager(FunctionsBD):
    """Класс для работы с базой данных"""

    def __init__(self, db_name: str, params: dict):
        """Создает объект класса"""
        self.__db_name = db_name
        self.__params = params

    def create_bd(self) -> None:
        """Создает базу данных"""

        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"DROP DATABASE {self.__db_name}")
        except InvalidCatalogName:
            print("Ошибка при удалении указанной базы. База данных не найдена.")
        cur.execute(f"CREATE DATABASE {self.__db_name}")

        cur.close()
        conn.close()

    def create_table_in_bd(self, table_name: str, column: list) -> None:
        """Создает таблицу в базе данных"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(f"""CREATE TABLE {table_name} ({','.join(column)})""")

        conn.commit()
        conn.close()

    def fill_table_data(self, table_name: str, data: list) -> None:
        """Наполняет таблицу данными"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            query = f"""
             SELECT column_name
             FROM information_schema.columns
             WHERE table_name = '{table_name}'
             ORDER BY ordinal_position;
            """

            cur.execute(query)
            columns_name = [row[0] for row in cur.fetchall()]

        with conn.cursor() as cur:
            for next_data in data:
                cur.execute(
                    f"""
                    INSERT INTO {table_name} ({','.join(columns_name)})
                    VALUES ({','.join(['%s'] * len(columns_name))})
                    """,
                    next_data,
                )

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self) -> None:
        """Получает список всех компаний и количество вакансий у каждой компании"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT employer_name, open_vacancies FROM employers
                INNER JOIN vacancies USING(employer_name)
                """
            )

            rows = cur.fetchall()
        conn.close()

        for row in rows:
            print(f"Компания {row[0]}, открытых вакансий - {row[1]} шт.")

    def get_all_vacancies(self) -> None:
        """Получает список всех вакансий"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, employer_name, salary, url_vacancy FROM employers
                INNER JOIN vacancies USING(employer_name)
                """
            )

            rows = cur.fetchall()

        conn.close()

        for row in rows:
            print(
                f"Название вакансии <{row[0]}>, название организации <{row[1]}>, "
                f"з/п - {row[2]}, ссылка на вакансию - {row[3]}"
            )

    def get_avg_salary(self) -> None:
        """Получает среднюю зарплату по вакансиям"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary) from vacancies""")

            result = cur.fetchall()

        conn.close()

        print(round(result[0][0], 0))

    def get_vacancies_with_higher_salary(self) -> None:
        """Получает список всех вакансий, у которых зарплата выше средней"""
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, employer_name, salary, url_vacancy from employers
                INNER JOIN vacancies USING(employer_name)
                WHERE salary > (SELECT AVG(salary) from vacancies)
                """
            )

            rows = cur.fetchall()

        conn.close()

        for row in rows:
            print(
                f"Название вакансии <{row[0]}>, название организации <{row[1]}>, "
                f"з/п - {row[2]}, ссылка на вакансию - {row[3]}"
            )

    def get_vacancies_with_keyword(self, search_words: list) -> None:
        """Получает список всех вакансий, в названии которых содержатся переданные слова"""
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        for word in search_words:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name, employer_name, salary, url_vacancy from employers
                    INNER JOIN vacancies USING(employer_name)
                    WHERE vacancy_name LIKE '%{word.strip()}%'
                    """
                )

                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(
                            f"Название вакансии <{row[0]}>, название организации <{row[1]}>, "
                            f"з/п - {row[2]}, ссылка на вакансию - {row[3]}"
                        )
        conn.close()
