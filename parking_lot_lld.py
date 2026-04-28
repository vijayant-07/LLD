from abc import ABC, abstractmethod
from enum import Enum
import time


class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3


class SpotType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Vehicle(ABC):
    def __init__(self, number: str):
        self.number = number

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def can_fit_in(self, spot) -> bool:
        pass


class Bike(Vehicle):
    def get_type(self):
        return VehicleType.BIKE

    def can_fit_in(self, spot):
        return True


class Car(Vehicle):
    def get_type(self):
        return VehicleType.CAR

    def can_fit_in(self, spot):
        return spot.spot_type in [SpotType.MEDIUM, SpotType.LARGE]


class Truck(Vehicle):
    def get_type(self):
        return VehicleType.TRUCK

    def can_fit_in(self, spot):
        return spot.spot_type == SpotType.LARGE



class ParkingSpot:
    def __init__(self, spot_id: int, spot_type: SpotType, price: float):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.price = price
        self.is_occupied = False

    def assign_vehicle(self):
        self.is_occupied = True

    def remove_vehicle(self):
        self.is_occupied = False



class SpotAllocationStrategy(ABC):
    @abstractmethod
    def find_spot(self, spots, vehicle):
        pass


class DefaultSpotAllocationStrategy(SpotAllocationStrategy):
    def find_spot(self, spots, vehicle):
        for spot in spots:
            if not spot.is_occupied and vehicle.can_fit_in(spot):
                return spot
        return None



class Ticket:
    def __init__(self, ticket_id, vehicle, spot, entry_time):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = entry_time
        self.exit_time = None
        self.amount = None



class FeeCalculator:
    def calculate(self, ticket: Ticket):
        duration = ticket.exit_time - ticket.entry_time
        return duration * ticket.spot.price



class ParkingLot:
    def __init__(self, spots, strategy, fee_calculator):
        self.spots = spots
        self.strategy = strategy
        self.fee_calculator = fee_calculator
        self.active_tickets = {}
        self.ticket_counter = 0

    def park_vehicle(self, vehicle):
        spot = self.strategy.find_spot(self.spots, vehicle)

        if not spot:
            raise Exception("No available spot")

        spot.assign_vehicle()

        self.ticket_counter += 1
        ticket = Ticket(
            self.ticket_counter,
            vehicle,
            spot,
            entry_time=time.time()
        )

        self.active_tickets[ticket.ticket_id] = ticket
        return ticket

    def unpark_vehicle(self, ticket_id):
        ticket = self.active_tickets.get(ticket_id)

        if not ticket:
            raise Exception("Invalid ticket")

        ticket.exit_time = time.time()

        amount = self.fee_calculator.calculate(ticket)
        ticket.amount = amount

        ticket.spot.remove_vehicle()
        del self.active_tickets[ticket_id]

        return amount


if __name__ == "__main__":
    spots = [
        ParkingSpot(1, SpotType.SMALL, 10),
        ParkingSpot(2, SpotType.MEDIUM, 20),
        ParkingSpot(3, SpotType.LARGE, 30),
    ]

    strategy = DefaultSpotAllocationStrategy()
    fee_calculator = FeeCalculator()

    parking_lot = ParkingLot(spots, strategy, fee_calculator)

    vehicle = Car("KA-01-1234")

    ticket = parking_lot.park_vehicle(vehicle)
    print(f"Vehicle parked. Ticket ID: {ticket.ticket_id}")

    time.sleep(2)

    amount = parking_lot.unpark_vehicle(ticket.ticket_id)
    print(f"Parking fee: {amount}")