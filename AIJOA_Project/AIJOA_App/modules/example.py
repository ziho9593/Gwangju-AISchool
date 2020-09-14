from AIJOA_App.modules import gspeech
import time
# from AIJOA_App.session import search # 이 부분이 메뉴 선택 or 추가, 기타 등등 기능들이 추가되어야되는 부분


def main():
    # 음성인식 활성화
    # 카드결제, QR code, pay등이 인식이되면
    # 그 신호와 동시에 음성 인식이 활성화 되어 주문을 받음
    # 처음에는 위와 같이 생각했었으나
    # 물체감지 센서로 거리를 조정해서 손을 인식시키는 방법이 좋을꺼 같음
    # 꼭 손이 아니라 센서 앞에 일정 거리 가까이 물체가 인식되면 음성인식 활성화


    gsp = gspeech.Gspeech()

    while True:
        # 말하면 음성인식되는 순간 stt에다가 문자열 형태로 담는다
        stt = gsp.getText()

        # 들어온 문자가 어떤거냐에 따라 분기 작성
        if stt is None:
            break
        else:
            if ('그만' in stt):
                break
            else:
                return (stt)
                # search(stt)
        # print(stt)
        time.sleep(0.01)

        # # '그만'의 위치를 고민해 봐야될꺼 같음
        # # 지금은 '그만'을 했는데 그만을 써칭하고 나서 break되고 있음
        # if ('그만' in stt):
        #     break


# main()

# response:
# results {
#   alternatives {transcript: "\352\267\270\353\247\214"}
#   stability: 0.009999999776482582
#   result_end_time {seconds: 5 nanos: 340000000}
# }
#
# response:
# results {
#   alternatives {transcript: "\352\267\270\353\247\214" confidence: 0.9236595630645752}
#   is_final: true
#   result_end_time {seconds: 5 nanos: 730000000}
# }
