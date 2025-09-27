from abc import ABC, abstractmethod


class ApiHH(ABC):  # pragma: no cover
    """Базовый класс, для подключения к api HeadHunters"""

    @abstractmethod
    def __init__(self, employers_id: list): ...

    @abstractmethod
    def _connect_to_api(self) -> bool: ...

    @abstractmethod
    def get_employers(self) -> str | list: ...

    @abstractmethod
    def get_vacancies(self) -> str | list: ...


class FunctionsBD(ABC):  # pragma: no cover
    """Базовый класс, для работы с базой данных"""

    @abstractmethod
    def __init__(self, db_name: str, params: dict):
        pass

    @abstractmethod
    def create_bd(self): ...

    @abstractmethod
    def create_table_in_bd(self, table_name: str, column: list): ...

    @abstractmethod
    def fill_table_data(self, table_name: str, data: list): ...

    @abstractmethod
    def get_companies_and_vacancies_count(self): ...

    @abstractmethod
    def get_all_vacancies(self): ...

    @abstractmethod
    def get_avg_salary(self): ...

    @abstractmethod
    def get_vacancies_with_higher_salary(self): ...

    @abstractmethod
    def get_vacancies_with_keyword(self, search_words: list): ...
