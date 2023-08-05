# -*- coding: utf-8 -*-
class IdCard:
    def __init__(self, id, name, birth, nationality, sex, hometown, address, expires):
        self.id = id
        self.name = name
        self.birth = birth
        self.nationality = nationality
        self.sex = sex
        self.hometown = hometown
        self.address = address
        self.expires = expires

    def print_idCard(self):
        print("Số CMND: " + self.id)
        print("Họ tên: " + self.name)
        print("Ngày sinh: " + self.birth)
        print("Quốc tịch: " + self.nationality)
        print("Giới tính: " + self.sex)
        print("Quê quán: " + self.hometown)
        print("Địa chỉ thường trú: " + self.address)
        print("Có giá trị đến: " + self.expires)
