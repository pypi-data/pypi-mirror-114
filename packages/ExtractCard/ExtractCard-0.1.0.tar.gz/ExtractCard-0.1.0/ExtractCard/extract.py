# -*- coding: utf-8 -*-
import cv2
import numpy as np
from ExtractCard.processing import proc_img
from PIL import Image
from ExtractCard.idCard_class import *
from ExtractCard.drivingLicense_class import *
from ExtractCard.studentCard_class import *
from ExtractCard.classify import *


def single_pic_proc(image_file):
    image = np.array(Image.open(image_file).convert("RGB"))  # chuyển ảnh xám
    # nhận dạng, gọi hàm proc_img của module processing
    result, image_framed = proc_img(image)
    return result, image_framed  # trả về


# Hàm xử lí ảnh trả về ảnh đã vẽ khung và kết quả nhận dạng


def show_img(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Hàm hiển thị ảnh


def print_list_text(list_img):
    for text in list_img:
        print("TEXT OUTPUT:" + text)


# Hàm in danh sách kết quả


def output_proc(results):  # xử lí kết quả đầu ra
    id = " "
    name = " "
    birth = " "
    nationality = " "
    sex = " "
    hometown = " "
    address = " "
    classOfDL = " "
    major = " "
    faculty = " "
    course = " "
    expires = " "

    if classify(results) == 1:
        card = IdCard(id, name, birth, nationality, sex, hometown, address, expires)
        card = output_proc_idCard(results)
        card.print_idCard()
    if classify(results) == 2:
        card = DrivingLicense(id, name, birth, nationality, address, classOfDL, expires)
        card = output_proc_drivingLicense(results)  # phân loại
        card.print_DrivingLicense()
    if classify(results) == 3:
        card = StudentCard(name, id, major, faculty, course)
        card = output_proc_studentCard(results)
        card.print_StudentCard()


def extract(img):
    # Hàm trả về là kết quả dạng array và img đã đóng khung
    results, image_framed = single_pic_proc(img)
    output_proc(results)
