from datetime import datetime
from typing import Union
from pydantic import BaseModel, field_validator


class Passport(BaseModel):
    """
    Модель паспорта.
    """

    passport_series: str
    passport_number: str
    passport_issued_by: str
    passport_issued_on: str
    full_name: str
    date_of_birth: str

    @field_validator('passport_issued_on', 'date_of_birth', mode="before")
    def validate_date_format(cls, value):
        """
        Валидатор для проверки формата даты.

        :param value: Значение даты.
        :return: Верное значение даты.
        :raises ValueError: Если формат даты неверный.
        """
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return value
        except ValueError:
            raise ValueError('Неверный формат даты. Пожалуйста, используйте формат dd.mm.yyyy.')

    @field_validator('full_name')
    def capitalize_full_name(cls, value):
        """
        Преобразует поле full_name так, чтобы каждое слово начиналось с заглавной буквы.

        :param value: Значение поля full_name.
        :return: Преобразованное значение поля full_name.
        """
        return ' '.join(word.capitalize() for word in value.split())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RecognitionResult(BaseModel):
    status: str
    result: Union[str, Passport]
