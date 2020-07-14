# 1주일 내용 4문제로 복습

# 1. 파이썬 조건문을 활용하여 장발장은 빵을 못먹게 하기
# - 실행 예시 : "장발장 차례 입니다, 빵을 드릴 수 없습니다."
# - 실행 예시 : "홍길동 차례 입니다, 빵을 하나 드리겠습니다."

people = ['홍길동', '성진', '심청이', '장발장', '심봉사']

for person in people:
    if person == "장발장":
        print('장발장 차례 입니다, 빵을 드릴 수 없습니다.')
    else:
        print(f'{person} 차례 입니다, 빵을 하나 드리겠습니다.')

# --------------------------------------------------------

# 2. 1번 문제의 구현된 부분을 함수로 바꾸기
# - 조건 : 입력값(사람 한 명씩) 을 받아서 빵을 먹으면 안되는 사람이면 0을, 먹어도 되면 1을 반환하기
# - 실행 예시 : "홍길동은 빵을 먹을 수 있는 사람 입니다."
# - 실행 예시 : "장발장은 빵을 먹을 수 없는 사람 입니다."
# 반복문을 활용하여 5 명 전원 다 출력 할 것
def can_eat_bread(person):
    if person == "장발장":
        print(f'{person}은 빵을 먹을 수 없는 사람입니다.')
        return 0
    else:
        print(f'{person}은 빵을 먹을 수 있는 사람입니다.')
        return 1

for person in people:
    can_eat_bread(person)
        
# --------------------------------------------------------

# 3. 지역변수와 전역변수 이해하기

# 아래의 코드는 num_stamp 라는 전역변수를 함수 내에서 global 명령을 통해 수정가능하게 억지로 만든상태이다.
# 하지만, 함수의 기능과 본질을 생각하면 아래의 예시는 굉장히 바람직하지 못하다!
# global 명령은 안쓰는 것이 좋다!
# 그렇다면, global 명령을 사용하지 않고 아래의 로직을 함수의 입력값과 반환값을 활용하여 수정해보기!


num_stamp = 0  # 쿠폰 스탬프가 찍힌 횟수 (전역변수)

def stamp(num_stamp):
    """쿠폰 스탬프가 찍힌 횟수를 증가시키고, 화면에 출력한다."""
    # global num_stamp           # num_stamp는 전역변수다
    num_stamp = num_stamp + 1  # 오류가 발생하지 않는다 (global 안쓰면 오류 발생함)
    return num_stamp

num_stamp = stamp(num_stamp)  
print(num_stamp)    # 화면에 1이 출력된다
num_stamp = stamp(num_stamp)
print(num_stamp)    # 화면에 2가 출력된다


# --------------------------------------------------------

# 4. 클래스 이용하기
# 요구사항
# - 교통수단 클래스 만들기 (속성 : 이름, 가격, 출발시간, 도착시간 / 기능 : 출발시간, 도착시간 보기)
# - 비행기 클래스 만들기
# 속성 : 이름, 가격, 출발시간, 도착시간, 수하물 가능여부
# 기능 : 출발시간, 도착시간 보기, 수하물 맡기기(수하물이 가능하면 "수하물을 맡겼습니다!"출력, 불가능하면 "이 비행기는 수하물을 못맡깁니다!" 출력)
# - 기차 클래스 만들기
# 속성 : 이름, 가격, 출발시간, 도착시간, 좌석등급
# 기능 : 출발시간, 도착시간 보기, 좌석등급 보기

# 클래스를 상속을 활용해서 효율적으로 만들어 볼것! (메소드 오버라이딩)
# 두 개 이상의 인스턴스를 비행기, 기차 각각 만들어 볼것

class Vehicle():
    def __init__(self, name, price, start, arrive):
        self.name = name
        self.price = price
        self.start = start
        self.arrive = arrive
    
    def show_time(self):
        print(f'출발 시간은 {self.start}입니다.')
        print(f'도착 시간은 {self.arrive}입니다.')

class Airplane(Vehicle):
    def __init__(self, name, price, start, arrive, baggage):
        super().__init__(name, price, start, arrive)
        self.baggage = baggage
    
    def can_baggage(self):
        if self.baggage == True:
            print('수하물을 맡겼습니다!')
        else:
            print('이 비행기는 수하물을 못맡깁니다!')
    
class Train(Vehicle):
    def __init__(self, name, price, start, arrive, grade):
        super().__init__(name, price, start, arrive)
        self.grade = grade
    
    def show_grade(self):
        print(self.grade)


# test
asiana = Airplane('A777', 170000, '07:00', '11:00', True)
korean = Airplane('B888', 350000, '10:00', '19:00', False)

asiana.show_time()
korean.can_baggage()

KTX = Train('1호차', 30000, '09:00', '12:00', '2등석')
SRT = Train('7호차', 60000, '12:00', '13:00', '1등석')

KTX.show_time()
SRT.show_grade()


# --------------------------------------------------------