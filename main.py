import pickle
from collections import UserDict
from datetime import datetime, timedelta

# Базовий клас для полів
class Field:
    def __init__(self, value):
        self._value = None
        self.validate(value)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate_value(new_value)
        self.validate(new_value)
        self._value = new_value

    def validate_value(self, value):
        pass  

    def validate(self, value):
        pass  

    def __str__(self):
        return str(self.value)

# Клас для зберігання номера телефону
class Phone(Field):
    def validate_value(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен складатися лише з 10 цифр.")

    def validate(self, value):
        super().validate(value)
        self.validate_value(value)

# Клас для зберігання дня народження
class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Невірний формат дня народження. Повинно бути у форматі YYYY-MM-DD.")

# Клас для зберігання імені
class Name(Field):
    def validate_value(self, value):
        if not value.isalpha():
            raise ValueError("Name повинен складатися лише з літер.")

# Клас для представлення контакту
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        old_phone = self.find_phone(old_phone_number)
        if old_phone:
            old_phone.value = new_phone_number
        else:
            raise ValueError(f"Номер телефону {old_phone_number} не знайдено.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
        return (next_birthday - today).days

    def __str__(self):
        return f"Ім'я контакту: {self.name.value}, телефони: {'; '.join(str(p) for p in self.phones)}, " \
               f"день народження: {self.birthday.value if self.birthday else 'Немає'}"

# Клас для представлення адресної книги
class AddressBook(UserDict):
    def __init__(self, file_path='address_book.pkl'):
        super().__init__()
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def add_record(self, record):
        self.data[record.name.value] = record
        self.save_data()

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            self.save_data()

    def search(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
        return results

    def find(self, name):
        return self.data.get(name)