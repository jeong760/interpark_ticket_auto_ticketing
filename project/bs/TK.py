import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


class TK:

    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.level = ""
        self.p_cnt = ""
        self.zone = ""
        print("드라이버 시작혀")

    def open_window(self):
        # setup Driver|Chrome : 크롬드라이버를 사용하는 driver 생성
        self.driver = webdriver.Chrome('./chromedriver.exe')
        # 사이즈조절
        self.driver.set_window_size(1400, 1000)
        self.driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')

    def login(self, inId, inPw):
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
        userId = self.driver.find_element(By.ID, 'userId')
        userId.send_keys(inId)
        userPwd = self.driver.find_element(By.ID, "userPwd")
        userPwd.send_keys(inPw)
        userPwd.send_keys(Keys.ENTER)

    def location_page2(self, goodsCode):
        self.driver.get('http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=' + goodsCode)

    def location_page(self, wantYear, wantMonth, wantDate, hour, min_, gu, ch, people):
        self.driver.find_element(By.XPATH, "//div[@class='tk_dt_btn_TArea']/a").click()

        # 예매하기 눌러서 팝업창이 뜨면 포커스를 새창으로 바꿔준다
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get_window_position(self.driver.window_handles[1])

        # 혹시 예매안내가 뜨면 꺼버린다릿
        ticketingInfo_check = self.check_exists_by_element(By.XPATH, "//div[@class='layerWrap']/div[@class='titleArea']/a[@class='closeBtn']")

        if ticketingInfo_check:
            self.driver.find_element(By.XPATH, "//div[@class='layerWrap']/div[@class='titleArea']/a[@class='closeBtn']").click()

        # 날짜 아이프레임
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='contL']/iframe[@id='ifrmBookStep']"))

        # 월 체크
        calHead = self.driver.find_elements(By.XPATH, "//div[@class='calHead']/div[@class='month']/span")
        year_month = calHead[1].find_elements(By.XPATH, "//em")
        year = year_month[0].text  # 년
        month = year_month[1].text  # 월

        yearC = int(wantYear) - int(year)
        monthC = int(wantMonth) - int(month)

        s = yearC * 12 + monthC
        i = 0
        if s > 0:
            while i < s:
                calHead[2].click()
                i = i + 1
                calHead = self.driver.find_elements(By.XPATH, "//div[@class='calHead']/div[@class='month']/span")
        elif s < 0:
            while i < s:
                calHead[0].click()
                i = i - 1
                calHead = self.driver.find_elements(By.XPATH, "//div[@class='calHead']/div[@class='month']/span")

        # 선택 가능한 날짜 모두 불러오기
        CellPlayDate = self.driver.find_elements(By.NAME, "CellPlayDate")

        for cell in CellPlayDate:
            if cell.text == wantDate:
                cell.click()
                break

        # 시간클릭하기 전에 시간 클릭버튼이 활성화 되기를 기다렸다 움직여라잉
        time_li = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.ID, "CellPlaySeq"))
        )

        hour_min = hour + "시 " + min_ + "분"

        for li in time_li:
            if li.text == hour_min:
                li.click()
                break

        # 원래 팝업 프레임으로 돌아가기
        self.driver.switch_to.default_content()

        # 다음
        next = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='contR']/div[@class='buy_info']/p[@id='LargeNextBtn']/a/img"))
        )
        next[0].click()

        # 캡챠 레이아웃이 있는지 없는지 체크를 해보자꾸나아
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"))
        capchaLayer_check = self.check_exists_by_element(By.XPATH, "//div[@id='divRecaptcha']")

        # 자동예매 방지 문자열  나오면 일단 5초를 기다리거라
        if capchaLayer_check:
            time.sleep(5)
            print("정지를 5초동안 하고 있을것잉!")

        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='seatL']/iframe[@id='ifrmSeatDetail']"))

        self.zone = gu
        self.level = ch
        self.p_cnt = people

        self.f5_man()

    def f5_man(self):
        cnt = 0
        yul_cnt = 0
        try:
            seat_check = self.driver.find_element(By.CSS_SELECTOR, "img.stySeat")
            seat_title = seat_check.get_attribute('title')
            b = seat_title.split('-')

            if '구역' in b[1]:
                if b[1][b[1].find('역') + 1] == ' ':
                    zone_seat_return = self.seat_title_checking1
                else:
                    zone_seat_return = self.seat_title_checking2
            elif '블럭' in b[1]:
                zone_seat_return = self.seat_title_checking3
            else:
                c = re.compile('[0-9]')
                if c.match(b[1]):
                    zone_seat_return = self.seat_title_checking4
                else:
                    zone_seat_return = self.seat_title_checking5

            # 좌석 선택
            w_check = False
            while yul_cnt < 20:
                yul_cnt = yul_cnt + 1
                gooyuk = zone_seat_return(yul_cnt)
                imgs = self.driver.find_elements(By.CSS_SELECTOR, "img.stySeat" + gooyuk)

                for i in imgs:
                    i.click()
                    cnt = cnt + 1
                    if cnt == int(self.p_cnt):
                        w_check = True
                        break

                if w_check:
                    break

            # 원래 팝업 프레임으로 돌아가기
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"))
            # 다음 버튼 클릭
            self.driver.find_element(By.XPATH, "//div[@class='seatR']/div[@class='inner']/div[@class='btnWrap']/a/img").click()

            if self.iszha():
                self.f5_man2()
        except:
            print("에러 발생 하였는걸요")
            self.f5_man2()
        finally:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.get_window_position(self.driver.window_handles[0])

    def f5_man2(self):
        # 원래 팝업 프레임으로 돌아가기
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"))
        self.driver.find_element(By.XPATH, "//div[@class='seatR']/div[@class='inner']/div[@class='btnWrap']/p[@class='fl_r']/a/img").click()
        # 좌석 프레임으로 돌려버리깃
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='seatL']/iframe[@id='ifrmSeatDetail']"))
        self.f5_man()

    def check_exists_by_element(self, by, name):
        try:
            print("노드가 있는지 체크를 해주세요 제발요")
            self.driver.find_element(by, name)
        except NoSuchElementException:
            print("노드가 없는 것이다.")
            return False
        return True

    def iszha(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            print("뭐가 되었던간에 팝업창은 안나왔다는거지")
            return False
        return True

    def ticket_select(self):
        # 티켓갯수? 선택
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='contL']/iframe[@id='ifrmBookStep']"))

        select = Select(self.driver.find_element(By.XPATH, "//select[@name='SeatCount']"))

        select.select_by_index((len(select.options) - 1))

    def seat_title_checking1(self, seat):
        return "[title*='" + self.level + "석'][title*='" + self.zone + "구역 " + str(seat) + "열']"

    def seat_title_checking2(self, seat):
        return "[title*='" + self.level + "석'][title*='" + self.zone + "구역" + str(seat) + "열']"

    def seat_title_checking3(self, seat):
        return "[title*='" + self.level + "석']title*='" + self.zone + "블럭" + str(seat) + "열']"

    def seat_title_checking4(self, seat):
        return "[title*='" + self.level + "석']title*='-" + str(seat) + "열']"

    def seat_title_checking5(self, seat):
        return "[title*='" + self.level + "석']title*='-" + chr(64 + seat) + "열']"
