import json
from random import randint
from copy import deepcopy
from PyQt5 import QtWidgets
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.uic import loadUiType

const_drugs = {"Кокаин": [7000, 0], "Крэк": [7000, 0], "Экстези": [2000, 0], "Гашиш": [1600, 0], "Героин": [5000, 0],
               "Айс": [2000, 0], "Мефедрон": [400, 0], "ЛСД": [800, 0], "Мандрак": [1000, 0], "Морфий": [2200, 0],
               "Грибы": [370, 0], "Опиум": [1200, 0], "Ангельская пыль": [600, 0], "Кактус": [800, 0],
               "Марихуана": [900, 0], "Кетамин": [1300, 0], "Метамфетамин": [1000, 0]}
data = {"balance": 3000,
        "inventory": {},
        "drugs": {"Кокаин": [0, 0], "Крэк": [0, 0], "Экстези": [0, 0], "Гашиш": [0, 0], "Героин": [0, 0],
                  "Айс": [0, 0], "Мефедрон": [0, 0], "ЛСД": [0, 0], "Мандрак": [0, 0], "Морфий": [0, 0],
                  "Грибы": [0, 0], "Опиум": [0, 0], "Ангельская пыль": [0, 0], "Кактус": [0, 0],
                  "Марихуана": [0, 0], "Кетамин": [0, 0], "Метамфетамин": [0, 0]},
        "city": "New York",
        "capacity": 10,
        "city_prices": {"New York": deepcopy(const_drugs),
                        "Boston": deepcopy(const_drugs),
                        "Moscow": deepcopy(const_drugs)}}


def data_save():
    global data
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)


def data_load():
    global data
    with open("data.json", "r") as read_file:
        data = json.load(read_file)


def update():
    print("update")
    for i in data["city_prices"]:
        for k in data["city_prices"][i]:
            if data["city_prices"][i][k][0] * 2 < const_drugs[k][0]:
                data["city_prices"][i][k][0] += int(randint(1, 100) / 500 * const_drugs[k][0])
            elif data["city_prices"][i][k][0] > const_drugs[k][0] * 1.5:
                data["city_prices"][i][k][0] -= int(randint(1, 100) / 500 * const_drugs[k][0])
            else:
                if rand_bool(50):
                    data["city_prices"][i][k][0] += int(randint(1, 100) / 500 * const_drugs[k][0])
                else:
                    data["city_prices"][i][k][0] -= int(randint(1, 100) / 500 * const_drugs[k][0])
    for k in const_drugs:
        data["city_prices"][data["city"]][k][1] = randint(data["capacity"] // 4, data["capacity"] * 2)
    ex.update_info()


def rand_bool(chance):
    if chance <= randint(0, 99):
        return True
    else:
        return False


def buy(count, name):
    if data["city_prices"][data["city"]][name][1] < count:
        print("На улицах столько товара нет")
    elif data["city_prices"][data["city"]][name][0] * count > data["balance"]:
        print("Столько денег у меня нет")
    elif count + sum([i[0] for i in list(data["drugs"].values())]) > data["capacity"]:
        print("Инвентарь полон")
    else:
        data["city_prices"][data["city"]][name][1] -= count
        data["balance"] -= data["city_prices"][data["city"]][name][0] * count
        if data["drugs"][name][0]:
            data["drugs"][name][1] = int(data["drugs"][name][1] / data["drugs"][name][0]
                                         + data["city_prices"][data["city"]][name][0]) // 2
        else:
            data["drugs"][name][1] = data["city_prices"][data["city"]][name][0]
        data["drugs"][name][0] += count
    ex.update_info()


def sell(count, name):
    if data["drugs"][name][0] < count:
        print("У меня нет столько товара")
    else:
        data["drugs"][name][0] -= count
        data["balance"] += count * data["city_prices"][data["city"]][name][0]
        data["city_prices"][data["city"]][name][1] += count
    ex.update_info()


app = QApplication(sys.argv)
main_class, base_class = loadUiType('main.ui')


class MainWin(QMainWindow, main_class):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setupUi(self)
        self.balance.display(data["balance"])
        self.prices.setRowCount(len(const_drugs))
        self.prices.setColumnCount(3)
        self.prices.setHorizontalHeaderLabels(('Название', 'Количество', 'Цена'))
        print([data["drugs"][i][0] != 0 for i in data["drugs"]].count(True))
        self.inventory.setRowCount([data["drugs"][i][0] != 0 for i in data["drugs"]].count(True))
        self.inventory.setColumnCount(3)
        self.inventory.setHorizontalHeaderLabels(('Название', 'Количество', 'Цена'))
        self.wait.clicked.connect(lambda x: update())

    def update_info(self):
        temp = 0
        for i in data["city_prices"][data["city"]]:
            self.prices.setItem(temp, 0, QTableWidgetItem(i))
            self.prices.setItem(temp, 1, QTableWidgetItem(str(data["city_prices"][data["city"]][i][1])))
            self.prices.setItem(temp, 2, QTableWidgetItem(str(data["city_prices"][data["city"]][i][0])))
            temp += 1
        self.inventory.setRowCount([data["drugs"][i][0] != 0 for i in data["drugs"]].count(True))
        temp = 0
        print(data["drugs"])
        for i in data["drugs"]:
            if data["drugs"][i][0] != 0:
                self.inventory.setItem(temp, 0, QTableWidgetItem(i))
                self.inventory.setItem(temp, 1, QTableWidgetItem(str(data["drugs"][i][1])))
                self.inventory.setItem(temp, 2, QTableWidgetItem(str(data["drugs"][i][0])))
                temp += 1
        self.balance.display(data["balance"])


ex = MainWin()
update()
buy(1, "ЛСД")
buy(1, "Мефедрон")
ex.show()
sys.exit(app.exec_())

while True:
    cmd = input()
    if cmd == "balance":
        print(data["balance"])
    elif cmd == "prices":
        print(data["city_prices"][data["city"]])
    elif cmd == "inventory":
        print(data["drugs"])
    elif "buy" in cmd:
        cmd = cmd.split(" ")
        buy(int(cmd[1]), cmd[2])
    elif "sell" in cmd:
        cmd = cmd.split(" ")
        sell(int(cmd[1]), cmd[2])
    elif cmd == "wait":
        update()
    else:
        pass
