from parking_lot.enums.VehicleType import VehicleType
from parking_lot.models.BikeParkingSpot import BikeParkingSpot
from parking_lot.models.CarParkingSpot import CarParkingSpot
from parking_lot.models.ParkingFloor import ParkingFloor
from parking_lot.models.TruckParkingSpot import TruckParkingSpot
from parking_lot.parkingstrategy.ParkingStrategy import ClosestParkingFloor
from parking_lot.service.ParkingFloorService import ParkingFloorService
from parking_lot.service.ParkingLotService import ParkingLotService

if __name__ == '__main__':
    parking_spots = []
    bikeparking_spot1 = BikeParkingSpot("b1")
    bikeparking_spot2 = BikeParkingSpot("b2")
    bikeparking_spot3 = BikeParkingSpot("b3")
    carparking_spot1 = CarParkingSpot("c1")
    carparking_spot2 = CarParkingSpot("c2")
    truckparking_spot1 = TruckParkingSpot("t1")
    parking_spots.append(bikeparking_spot1)
    parking_spots.append(bikeparking_spot2)
    parking_spots.append(bikeparking_spot3)
    parking_spots.append(carparking_spot1)
    parking_spots.append(carparking_spot2)
    parking_spots.append(truckparking_spot1)
    parking_spots2 = []
    bikeparking_spot12 = BikeParkingSpot("b12")
    bikeparking_spot22 = BikeParkingSpot("b22")
    bikeparking_spot32 = BikeParkingSpot("b32")
    carparking_spot12 = CarParkingSpot("c12")
    carparking_spot22 = CarParkingSpot("c22")
    truckparking_spot12 = TruckParkingSpot("t12")
    parking_spots2.append(bikeparking_spot12)
    parking_spots2.append(bikeparking_spot22)
    parking_spots2.append(bikeparking_spot32)
    parking_spots2.append(carparking_spot12)
    parking_spots2.append(carparking_spot22)
    parking_spots2.append(truckparking_spot12)
    pf1 = ParkingFloor(parking_spots, "ParkingFloor1")
    pf2 = ParkingFloor(parking_spots2, "ParkingFloor2")
    pfs1 = ParkingFloorService(pf1)
    pfs2 = ParkingFloorService(pf2)
    # listpks = []
    # listpks.append(pf1)
    # listpks.append(pf2)
    listpfs = [pfs1, pfs2]
    # parking_lot = ParkingLotService(listpks)
    parking_lot = ParkingLotService(listpfs, ClosestParkingFloor(), "ParkingLotid1")
    parking_lot.park(VehicleType.TRUCK)
    # curr = pf.park(VehicleType.TRUCK)
    print(pfs1.get_parking_free_spots())
    print(pfs1.get_parking_occupied_spots())
    print(parking_lot.get_parking_free_spots())
    print(parking_lot.get_parking_occupied_spots())
    parking_lot.park(VehicleType.TRUCK)
    print(parking_lot.get_parking_free_spots())
    print(parking_lot.get_parking_occupied_spots())
    print(pfs2.get_parking_free_spots())
    print(pfs2.get_parking_occupied_spots())
    print(parking_lot.ticket_dao.tickets)
    # pf.unpark(curr.parking_id)
    # print(pf.get_parking_free_spots())
    # print(pf.get_parking_occupied_spots())
    # pf.park(VehicleType.TRUCK)
    # print(pf.get_parking_free_spots())
    # print(pf.get_parking_occupied_spots())


