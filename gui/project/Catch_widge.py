import json
import time

from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets
from utils.demo import get_data_from_tcp
import threading
import pandas as pd
from utils.demo import predict


class Catch_widge(QWidget):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.setWindowTitle('抓取数据')
        self.setFixedSize(300, 200)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_begin = QtWidgets.QPushButton('开始')

        self.btn_end = QtWidgets.QPushButton('关闭并保存')
        self.label = QLabel('抓取数据')
        self.btn_predict = QtWidgets.QPushButton('预测')

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.btn_begin, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.btn_end, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_predict, 2, 1, 1, 1)

        self.btn_begin.clicked.connect(self.get_csv)
        self.btn_end.clicked.connect(self.end)
        self.btn_predict.clicked.connect(self.predict)
        self.btn_end.setEnabled(False)
        self.btn_predict.setEnabled(False)
        self.flag = 1

        print(self.btn_begin.size())

    def end(self):
        self.flag = 0

        self.btn_begin.setEnabled(True)
        self.btn_begin.setText('开始')
        QtWidgets.QMessageBox.information(self.btn_end, '提示', '保存', QMessageBox.Ok)
        # self.btn_predict.setEnabled(True)
        self.btn_end.setEnabled(False)

    def begin(self):
        self.flag = 1
        self.btn_predict.setEnabled(False)
        time_start = time.time()
        data = get_data_from_tcp(self.ip, 10003)

        columns = [i for i in data.__dict__.keys()]
        values = [i for i in data.__dict__.values()]
        self.df = pd.DataFrame(columns=columns, data=[values])
        self.btn_begin.setText('正在采集...')
        self.btn_begin.setEnabled(False)
        self.btn_end.setEnabled(True)

        while True:
            # if time.time() > time_start + 60:
            #     self.btn_predict.setEnabled(True)

            if self.flag == 1:
                try:
                    data = get_data_from_tcp(self.ip, 10003)
                    r = data.__dict__
                    self.df = self.df.append(r, ignore_index=True)
                except Exception as e:
                    print(e)
                    continue

            else:
                y_hat = predict(self.df)
                self.df['health'] = y_hat
                self.df.to_csv(r['robot_id'] + '_' + str(time.time()) + '.csv')
                self.btn_predict.setEnabled(True)

                break

    def get_csv(self):
        t = threading.Thread(target=self.begin, name='t')
        t.start()

    def predict(self):
        total_count = self.df.shape[0]
        health_count = self.df[self.df['health'] == 1].shape[0]
        broken_count = total_count - health_count
        message = '采集数据 %d 条,预测为:健康%d条,不健康%d条(当前仅预测2关节)' % (total_count,health_count,broken_count)
        QtWidgets.QMessageBox.information(self.btn_end, '提示', message, QMessageBox.Ok)
        print('predict')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建窗口
    window = Catch_widge('192.168.1.105')

    window.show()

    sys.exit(app.exec_())
