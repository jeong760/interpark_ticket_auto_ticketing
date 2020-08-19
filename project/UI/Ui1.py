import time
import string
import random
from apscheduler.schedulers import background as b
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers import interval as i
from PyQt5.QtWidgets import QPushButton, qApp, QAction, QMainWindow, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from project.bs import TK
import requests


class Ui1(QMainWindow):
    global sched

    def __init__(self):
        super().__init__()
        self.btn = QPushButton('예매시작', self)
        self.btn2 = QPushButton('예약예매시작', self)
        self.btn3 = QPushButton('예약예매스탑', self)
        self.cnt_txtline = QLineEdit(self)
        self.cnt_lbl1 = QLabel(self)
        self.cnt_lbl = QLabel(self)
        self.ch_txtline = QLineEdit(self)
        self.ch_lbl2 = QLabel(self)
        self.gu_txtline = QLineEdit(self)
        self.gu_lbl2 = QLabel(self)
        self.gu_lbl = QLabel(self)
        self.m_txtline = QLineEdit(self)
        self.h_txtline = QLineEdit(self)
        self.d_txtline = QLineEdit(self)
        self.M_txtline = QLineEdit(self)
        self.y_txtline = QLineEdit(self)
        self.ymd_lbl5 = QLabel(self)
        self.ymd_lbl4 = QLabel(self)
        self.ymd_lbl3 = QLabel(self)
        self.ymd_lbl2 = QLabel(self)
        self.ymd_lbl1 = QLabel(self)
        self.ymd_lbl = QLabel(self)
        self.id_lbl = QLabel(self)
        self.pw_lbl = QLabel(self)
        self.id_txtline = QLineEdit(self)
        self.pw_txtline = QLineEdit(self)
        self.GoodsCode_txtline = QLineEdit(self)
        self.eh_txtline = QLineEdit(self)
        self.em_txtline = QLineEdit(self)
        self.initUI()

    def initUI(self):
        # 메뉴 안에 끄기
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # 상단 메뉴가 등장!?
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        # 라벨
        GoodsCode_lbl = QLabel(self)
        GoodsCode_lbl.move(60, 130)
        GoodsCode_lbl.setText("GoodsCode")
        # 텍스트라인
        self.GoodsCode_txtline.move(150, 130)
        self.GoodsCode_txtline.setStatusTip('상품번호')

        # 라벨
        self.ymd_lbl.move(60, 200)
        self.ymd_lbl.setText("년월일시")
        self.ymd_lbl1.move(250, 200)
        self.ymd_lbl1.setText("년")

        self.ymd_lbl2.move(370, 200)
        self.ymd_lbl2.setText("월")

        self.ymd_lbl3.move(500, 200)
        self.ymd_lbl3.setText("일")

        self.ymd_lbl4.move(620, 200)
        self.ymd_lbl4.setText("시")

        self.ymd_lbl5.move(750, 200)
        self.ymd_lbl5.setText("분")

        # 텍스트라인
        self.y_txtline.move(150, 200)
        self.y_txtline.setStatusTip('년')

        self.M_txtline.move(270, 200)
        self.M_txtline.setStatusTip('월')

        self.d_txtline.move(400, 200)
        self.d_txtline.setStatusTip('일')

        self.h_txtline.move(520, 200)
        self.h_txtline.setStatusTip('시')

        self.m_txtline.move(640, 200)
        self.m_txtline.setStatusTip('분')

        # 라벨
        self.gu_lbl.move(60, 250)
        self.gu_lbl.setText("좌석")
        self.gu_lbl2.move(250, 250)
        self.gu_lbl2.setText("구역")
        # 텍스트라인
        self.gu_txtline.move(150, 250)
        self.gu_txtline.setStatusTip('구역')

        # 라벨
        self.ch_lbl2.move(380, 250)
        self.ch_lbl2.setText("석")
        # 텍스트라인
        self.ch_txtline.move(280, 250)
        self.ch_txtline.setStatusTip('석')

        # 라벨
        self.cnt_lbl.move(60, 300)
        self.cnt_lbl.setText("명")
        self.cnt_lbl1.move(250, 300)
        self.cnt_lbl1.setText("명")
        # 텍스트라인
        self.cnt_txtline.move(150, 300)
        self.cnt_txtline.setStatusTip('명')

        # 라벨
        self.id_lbl.move(60, 350)
        self.id_lbl.setText("ID")
        # 텍스트라인
        self.id_txtline.move(150, 350)
        self.id_txtline.setStatusTip('id')

        self.pw_lbl.move(260, 350)
        self.pw_lbl.setText("PW")
        # 텍스트라인
        self.pw_txtline.move(280, 350)
        self.pw_txtline.setStatusTip('pw')

        # 예약시간
        hm_lbl = QLabel(self)
        hm_lbl.move(60, 400)
        hm_lbl.setText("예약시간")
        # 텍스트라인
        self.eh_txtline.move(150, 400)
        self.eh_txtline.setStatusTip('시')
        self.em_txtline.move(300, 400)
        self.em_txtline.setStatusTip('분')

        # 버튼
        self.btn.move(50, 50)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.start_Ticketing)
        # 끄기 btn.clicked.connect(QCoreApplication.instance().quit)

        self.btn2.move(60, 450)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.clicked.connect(self.start_e_Ticketing)

        self.btn3.move(60, 500)
        self.btn3.resize(self.btn2.sizeHint())
        self.btn3.clicked.connect(self.stop_e_Ticketing)

        # 상태바
        self.statusBar()

        # 윈도우 생성
        self.setWindowTitle('티켓이 하고싶은데 너무 어려운것')
        self.setGeometry(500, 200, 800, 600)  # 가로위치, 세로위치, 가로길이, 세로길이
        self.show()

    def start_Ticketing(self):
        try:
            print("그냥 티넷 예매")

            tk = TK.TK()
            tk.open_window()
            tk.login(self.id_txtline.text(), self.pw_txtline.text())

            tk.location_page(self.GoodsCode_txtline.text(), self.y_txtline.text(), self.M_txtline.text(),
                             self.d_txtline.text(), self.h_txtline.text(), self.m_txtline.text(),
                             self.gu_txtline.text(), self.ch_txtline.text(), self.cnt_txtline.text())

            while tk.iszha():
                tk.location_page(self.GoodsCode_txtline.text(), self.y_txtline.text(), self.M_txtline.text(),
                                 self.d_txtline.text(), self.h_txtline.text(), self.m_txtline.text(),
                                 self.gu_txtline.text(), self.ch_txtline.text(), self.cnt_txtline.text())
        except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            print('예외가 발생했습니다.', e)

    def start_Ticketing2(self):
        global sched, tk2
        try:
            random_string = "".join([random.choice(string.ascii_letters) for _ in range(10)])
            print(random_string)
            res = requests.get('https://ticket.interpark.com/' + random_string + 'asp')
            headers = res.headers.get('Date').split(' ')
            hmd = headers[4].split(':')
            print(headers)
            h = int(hmd[0]) + 9
            if str(h) == self.eh_txtline.text() and hmd[1] == self.em_txtline.text():
                print("예약중단" + str(sched.state))
                sched.pause()
                print(sched.state)
                tk2.location_page(self.GoodsCode_txtline.text(), self.y_txtline.text(), self.M_txtline.text(),
                                  self.d_txtline.text(), self.h_txtline.text(), self.m_txtline.text(),
                                  self.gu_txtline.text(), self.ch_txtline.text(), self.cnt_txtline.text())

                while tk2.iszha():
                    tk2.location_page(self.GoodsCode_txtline.text(), self.y_txtline.text(), self.M_txtline.text(),
                                      self.d_txtline.text(), self.h_txtline.text(), self.m_txtline.text(),
                                      self.gu_txtline.text(), self.ch_txtline.text(), self.cnt_txtline.text())
                sched.shutdown()
        except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            print('예외가 발생했습니다.', e)
        finally:
            res.close()

    def start_e_Ticketing(self):
        global sched, tk2
        try:
            print("예약 시작")
            tk2 = TK.TK()
            tk2.open_window()
            tk2.login(self.id_txtline.text(), self.pw_txtline.text())

            sched = b.BackgroundScheduler()
            trigger = OrTrigger([
                # c.CronTrigger(hour=self.eh_txtline.text(), minute=self.em_txtline.text())
                i.IntervalTrigger(seconds=0.5)
            ])

            sched.add_job(self.start_Ticketing2, trigger)
            sched.start()
        except Exception as e:
            print('예외 맨', e)

    def stop_e_Ticketing(self):
        global sched
        try:
            sched.shutdown()
            print("예약중단" + str(sched.state))
        except Exception as e:
            print('예외 맨2', e)
