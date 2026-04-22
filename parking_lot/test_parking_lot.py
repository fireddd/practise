from parking_lot.enums.VehicleType import VehicleType
from parking_lot.models.BikeParkingSpot import BikeParkingSpot
from parking_lot.models.CarParkingSpot import CarParkingSpot
from parking_lot.models.TruckParkingSpot import TruckParkingSpot
from parking_lot.models.ParkingFloor import ParkingFloor
from parking_lot.service.ParkingFloorService import ParkingFloorService
from parking_lot.service.ParkingLotService import ParkingLotService
from parking_lot.parkingstrategy.ParkingStrategy import ClosestParkingFloor


def build_parking_lot():
    floor1_spots = [BikeParkingSpot("b1"), BikeParkingSpot("b2"), CarParkingSpot("c1"), TruckParkingSpot("t1")]
    floor2_spots = [BikeParkingSpot("b3"), CarParkingSpot("c2"), CarParkingSpot("c3"), TruckParkingSpot("t2")]
    pf1 = ParkingFloor(floor1_spots, "F1")
    pf2 = ParkingFloor(floor2_spots, "F2")
    pfs1 = ParkingFloorService(pf1)
    pfs2 = ParkingFloorService(pf2)
    lot = ParkingLotService([pfs1, pfs2], ClosestParkingFloor(), "LOT1")
    return lot, pfs1, pfs2


def test_park_returns_ticket():
    lot, _, _ = build_parking_lot()
    ticket = lot.park(VehicleType.CAR)
    assert ticket is not None
    assert ticket.parking_lot_id == "LOT1"
    assert ticket.ticket_id is not None
    print("PASS: test_park_returns_ticket")


def test_park_occupies_spot():
    lot, _, _ = build_parking_lot()
    free_before = len(lot.get_parking_free_spots())
    lot.park(VehicleType.CAR)
    free_after = len(lot.get_parking_free_spots())
    assert free_after == free_before - 1
    print("PASS: test_park_occupies_spot")


def test_unpark_frees_spot():
    lot, _, _ = build_parking_lot()
    ticket = lot.park(VehicleType.CAR)
    free_before = len(lot.get_parking_free_spots())
    lot.unpark(ticket)
    free_after = len(lot.get_parking_free_spots())
    assert free_after == free_before + 1
    print("PASS: test_unpark_frees_spot")


def test_park_then_unpark_restores_state():
    lot, _, _ = build_parking_lot()
    total = len(lot.get_parking_free_spots())
    ticket = lot.park(VehicleType.BIKE)
    lot.unpark(ticket)
    assert len(lot.get_parking_free_spots()) == total
    assert len(lot.get_parking_occupied_spots()) == 0
    print("PASS: test_park_then_unpark_restores_state")


def test_closest_floor_strategy():
    lot, pfs1, pfs2 = build_parking_lot()
    ticket = lot.park(VehicleType.TRUCK)
    assert ticket.floor_number == "F1"
    assert len(pfs1.get_parking_occupied_spots()) == 1
    assert len(pfs2.get_parking_occupied_spots()) == 0
    print("PASS: test_closest_floor_strategy")


def test_closest_floor_overflows_to_second():
    lot, pfs1, pfs2 = build_parking_lot()
    lot.park(VehicleType.TRUCK)
    ticket2 = lot.park(VehicleType.TRUCK)
    assert ticket2.floor_number == "F2"
    assert len(pfs1.get_parking_occupied_spots()) == 1
    assert len(pfs2.get_parking_occupied_spots()) == 1
    print("PASS: test_closest_floor_overflows_to_second")


def test_no_spots_raises():
    lot, _, _ = build_parking_lot()
    lot.park(VehicleType.TRUCK)
    lot.park(VehicleType.TRUCK)
    try:
        lot.park(VehicleType.TRUCK)
        assert False, "Should have raised"
    except ValueError:
        pass
    print("PASS: test_no_spots_raises")


def test_get_free_spots_by_vehicle_type():
    lot, _, _ = build_parking_lot()
    free_cars = lot.get_parking_free_spots_by_vehicle_type(VehicleType.CAR)
    assert len(free_cars) == 3
    lot.park(VehicleType.CAR)
    free_cars = lot.get_parking_free_spots_by_vehicle_type(VehicleType.CAR)
    assert len(free_cars) == 2
    print("PASS: test_get_free_spots_by_vehicle_type")


def test_get_occupied_spots_by_vehicle_type():
    lot, _, _ = build_parking_lot()
    assert len(lot.get_parking_occupied_spots_by_vehicle_type(VehicleType.BIKE)) == 0
    lot.park(VehicleType.BIKE)
    lot.park(VehicleType.BIKE)
    assert len(lot.get_parking_occupied_spots_by_vehicle_type(VehicleType.BIKE)) == 2
    assert len(lot.get_parking_occupied_spots_by_vehicle_type(VehicleType.CAR)) == 0
    print("PASS: test_get_occupied_spots_by_vehicle_type")


def test_ticket_persisted_in_dao():
    lot, _, _ = build_parking_lot()
    ticket = lot.park(VehicleType.CAR)
    retrieved = lot.ticket_dao.get_ticket(ticket.ticket_id)
    assert retrieved is ticket
    assert len(list(lot.ticket_dao.get_all_tickets())) == 1
    print("PASS: test_ticket_persisted_in_dao")


def test_multiple_parks_multiple_tickets():
    lot, _, _ = build_parking_lot()
    t1 = lot.park(VehicleType.BIKE)
    t2 = lot.park(VehicleType.CAR)
    t3 = lot.park(VehicleType.TRUCK)
    assert t1.ticket_id != t2.ticket_id != t3.ticket_id
    assert len(list(lot.ticket_dao.get_all_tickets())) == 3
    print("PASS: test_multiple_parks_multiple_tickets")


def test_different_vehicle_types_dont_interfere():
    lot, _, _ = build_parking_lot()
    lot.park(VehicleType.TRUCK)
    lot.park(VehicleType.TRUCK)
    free_bikes = lot.get_parking_free_spots_by_vehicle_type(VehicleType.BIKE)
    free_cars = lot.get_parking_free_spots_by_vehicle_type(VehicleType.CAR)
    assert len(free_bikes) == 3
    assert len(free_cars) == 3
    print("PASS: test_different_vehicle_types_dont_interfere")


def test_floor_service_park_unpark():
    floor = ParkingFloor([CarParkingSpot("c1"), CarParkingSpot("c2")], "F1")
    service = ParkingFloorService(floor)
    assert len(service.get_parking_free_spots()) == 2
    spot = service.park(VehicleType.CAR)
    assert len(service.get_parking_free_spots()) == 1
    assert len(service.get_parking_occupied_spots()) == 1
    service.unpark(spot.parking_id)
    assert len(service.get_parking_free_spots()) == 2
    assert len(service.get_parking_occupied_spots()) == 0
    print("PASS: test_floor_service_park_unpark")


if __name__ == '__main__':
    test_park_returns_ticket()
    test_park_occupies_spot()
    test_unpark_frees_spot()
    test_park_then_unpark_restores_state()
    test_closest_floor_strategy()
    test_closest_floor_overflows_to_second()
    test_no_spots_raises()
    test_get_free_spots_by_vehicle_type()
    test_get_occupied_spots_by_vehicle_type()
    test_ticket_persisted_in_dao()
    test_multiple_parks_multiple_tickets()
    test_different_vehicle_types_dont_interfere()
    test_floor_service_park_unpark()
    print("\nAll tests passed!")
