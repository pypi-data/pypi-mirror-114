# -*- coding: utf-8 -*-
class DrivingLicense:
    def __init__(self, id, name, birth, nationality, address, classOfDL, expires):
        self.id = id
        self.name = name
        self.birth = birth
        self.nationality = nationality
        self.address = address
        self.classOfDL = classOfDL
        self.expires = expires

    def print_DrivingLicense(self):
        print("Số: " + self.id)
        print("Họ tên: " + self.name)
        print("Ngày sinh: " + self.birth)
        print("Quốc tịch: " + self.nationality)
        print("Nơi cư trú: " + self.address)
        print("Hạng: " + self.classOfDL)
        print("Có giá trị đến: " + self.expires)
