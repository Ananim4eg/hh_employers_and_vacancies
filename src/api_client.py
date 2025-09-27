import requests

from src.base_classes import ApiHH


class HeadHunterAPI(ApiHH):
    """Получает вакансии с API HeadHunter"""

    def __init__(self, employers_id: list):
        """Создает объект класса"""
        self.__employers_id = employers_id

    def _connect_to_api(self) -> bool:
        """Проверяет доступность api сервиса"""

        url = "https://api.hh.ru/vacancies"

        response = requests.get(url)

        if response.status_code == 200:
            return True

        else:
            return False

    def get_employers(self) -> str | list:
        """Получает информацию о выбранных работодателях"""

        if not self._connect_to_api():
            return "Ошибка при подключении к сервису"

        result = []

        for id_number in self.__employers_id:
            url = f"https://api.hh.ru/employers/{id_number}"

            response = requests.get(url)
            employer = response.json()

            if employer:
                next_employer = [
                    employer.get("id"),
                    employer.get("name"),
                    employer.get("open_vacancies"),
                ]

                result.append(next_employer)

        return result

    def get_vacancies(self) -> str | list:
        """Получает список вакансий по заданным работодателям"""

        if not self._connect_to_api():
            return "Ошибка при подключении к сервису"
        page = 0
        result = []

        url = "https://api.hh.ru/vacancies"

        while page < 20:

            params = {"employer_id": self.__employers_id, "per_page": 100, "page": page}

            response = requests.get(url, params=params)
            vacancies = response.json()

            if vacancies.get("items"):
                for vacancy in vacancies.get("items"):
                    if (
                        vacancy.get("salary") is None
                        or vacancy.get("salary").get("from") is None
                    ):
                        salary = 0
                    else:
                        salary = vacancy["salary"]["from"]

                    result.append(
                        [
                            vacancy["id"],
                            vacancy["name"],
                            vacancy["employer"]["name"],
                            salary,
                            vacancy["alternate_url"],
                        ]
                    )
            else:
                page += 1
                continue

            page += 1

        if not result:
            return "Подходящих вакансий не найдено"

        return result
