from datetime import datetime

from pydantic import BaseModel, validator


class Passport(BaseModel):
    name: str
    middle_name: str
    surname: str
    gender: str
    birth_date: str
    birth_place: str
    number: str
    issued_by: str
    issue_date: str
    subdivision: str

    @validator('birth_date', 'issue_date')
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError as e:
            logger.error(
                'Ошибка: Неверный формат даты. Значение:',
                f' {value}. Ожидаемый формат: дд.мм.гггг')
            raise e
        return value
