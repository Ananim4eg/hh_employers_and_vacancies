from config import config
from src.api_client import HeadHunterAPI
from src.bd_services import DBManager

def main():
    employers_id_list = [1163045, 105699, 640043, 1758776, 93051, 9112940, 147219, 917409, 4376451, 3151617]

    hh_api = HeadHunterAPI(employers_id_list)

    db_emp_and_vac = DBManager('employers_and_vacancies', config())

    print("Приветствуем в программе отслеживания вакансий для заданных организаций.\n")
    print("Идет формирование данных...")

    # Создание базы данных
    db_emp_and_vac.create_bd()

    # Создание таблицы employers
    db_emp_and_vac.create_table_in_bd(
        'employers',
        ['employer_id INT PRIMARY KEY', 'employer_name VARCHAR UNIQUE NOT NULL', 'open_vacancies INT NOT NULL']
    )

    # Создание базы данных vacancies
    db_emp_and_vac.create_table_in_bd(
        'vacancies',
        [
            'vacancy_id INT PRIMARY KEY',
            'vacancy_name VARCHAR NOT NULL',
            'employer_name VARCHAR REFERENCES employers(employer_name) NOT NULL',
            'salary INT NOT NULL',
            'url_vacancy text NOT NULL'
        ]
    )

    # Заполнение таблицы employers данными
    db_emp_and_vac.fill_table_data(
        'employers',
        hh_api.get_employers()
    )

    # Заполнение таблицы vacancies данными
    db_emp_and_vac.fill_table_data(
        'vacancies',
        hh_api.get_vacancies()
    )
    print("Данные сформированы!")

    while True:
        user_choice = input(
                "\nВыберите необходимый пункт.\n"
                "1. Вывести список всех компаний и количество вакансий у каждой компании.\n"
                "2. Вывести список всех вакансий.\n"
                "3. Вывести среднюю зарплату по вакансиям.\n"
                "4. Вывести список всех вакансий, у которых зарплата выше средней. \n"
                "5. Поиск вакансий по ключевым словам. \n"
                "6. Выход\n"
                "Ввод: "
        )

        if user_choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Не найден выбранный пункт. Пожалуйста, повторите выбор.")
            continue
        elif user_choice == "1":
            db_emp_and_vac.get_companies_and_vacancies_count()
            continue
        elif user_choice == "2":
            db_emp_and_vac.get_all_vacancies()
            continue
        elif user_choice == "3":
            db_emp_and_vac.get_avg_salary()
            continue
        elif user_choice == "4":
            db_emp_and_vac.get_vacancies_with_higher_salary()
            continue
        elif user_choice == "5":
            words_list = input("Введите слова для поиска через запятую: ").split(',')
            db_emp_and_vac.get_vacancies_with_keyword(words_list)
            continue
        elif user_choice == "6":
            print("\nРабота программы завершена!")
            break

if __name__ == "__main__":
    main()
