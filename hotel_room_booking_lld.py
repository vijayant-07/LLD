class Booking:
    def __init__(self, hotel_id, room, start_date, end_date):
        self.hotel_id = hotel_id
        self.room = room
        self.start_date = start_date
        self.end_date = end_date

    def check_overlap(self, start_date, end_date):
        if start_date > self.end_date:
            return False
        elif end_date < self.start_date:
            return False
        else:
            return True

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.bookings = []

    def get_bookings(self):
        return self.bookings

    def make_booking(self, hotel_id, start_date, end_date):
        new_booking = Booking(hotel_id, self, start_date, end_date)
        self.bookings.append(new_booking)


class Hotel:
    def __init__(self, hotel_id, num_rooms):
        self.hotel_id = hotel_id
        self.rooms = [Room(i) for i in range(num_rooms)]

    def get_available_rooms(self, start_date, end_date):
        result = []
        for room in self.rooms:
            overlap = any(booking.check_overlap(start_date, end_date) for booking in room.get_bookings())
            if not overlap:
                result.append(room)
        return result


class BookingManager:
    def __init__(self, hotel):
        self.hotel = hotel

    def search_rooms(self, start_date, end_date):
        return self.hotel.get_available_rooms(start_date, end_date)

    def make_booking(self, room, start_date, end_date):
        if room not in self.hotel.get_available_rooms(start_date, end_date):
            return "Invalid Room Selected"
        else:
            room.make_booking(self.hotel.hotel_id, start_date, end_date)
            return f"Room with ID {room.room_id} is booked"


hotel = Hotel("1", 5)
booking_manager = BookingManager(hotel)

print("Available rooms before booking:")
list_of_rooms = booking_manager.search_rooms(0, 10)
print([room.room_id for room in list_of_rooms])

print("\nBooking one room...")
booking_manager.make_booking(list_of_rooms[0], 0, 10)

print("\nAvailable rooms after booking:")
list_of_rooms = booking_manager.search_rooms(0, 10)
print([room.room_id for room in list_of_rooms])