import json
from datetime import date

GUEST_ID_KEY = "name"
CHECK_IN_KEY = "check-in"
CHECK_OUT_KEY = "check-out"

class Guest:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    @property
    def check_in(self):
        return date.fromisoformat(self.__getattribute__(CHECK_IN_KEY))

    @property
    def check_out(self):
        return date.fromisoformat(self.__getattribute__(CHECK_OUT_KEY))

class Hotel:
    def __init__(self, max_capacity):
        self.guest_list = list()
        self.max_capacity = max_capacity

    def add_guest(self, guest: Guest)  -> None:
        self.guest_list.append(guest)

    def check_capacity(self) -> bool:
        events = list()
        for guest in self.guest_list:
            events.append((guest.check_in, 1))
            events.append((guest.check_out, -1))
        events.sort()

        current_guest_quantity = 0
        for _, delta in events:
            current_guest_quantity += delta
            if current_guest_quantity > self.max_capacity:
                return False
        return True

if __name__ == "__main__":
    max_capacity = int(input())
    guest_quantity = int(input())
    hotel = Hotel(max_capacity)

    for _ in range(guest_quantity):
        guest = Guest(**json.loads(input()))
        hotel.add_guest(guest)

    print(hotel.check_capacity())
