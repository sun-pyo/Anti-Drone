#-*-coding:utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time
from pyfcm import FCMNotification

class fcm:

    # 파이어베이스 콘솔에서 얻어 온 API키를 넣어 줌
    push_service = FCMNotification(api_key="AAAAX5SpFgc:APA91bG2YQo1PojdmVVmxg30fWhS_JQl4djqn43rilA4pWpNvvIxlwYZRQEKG0-a__EePQvkL9w7xkHEoF2P_o9spUC04r_CPLF4DE5vUOBKqgQYC6G4KgNT9aML2RGe4hzaOmmOa1iv")

    def __init__(self, mToken):
        #클라우드 메세징 서버키 토큰 
        self.mToken = mToken

    #Settings 일반 웹API키 
    '''
    여기서는 지정된 토큰 1개만 넣어서 사용함. 
    좀 더 확장할려면 토큰을 앱으로 부터 받거나 앱서버 DB에서 가져와서 다수의 토큰에 알림을 발송 할 수도 있음.
    '''
    def sendMessage(self):
        registration_id = self.mToken
        data_message = {
            "body" : " Drone WARNING 알수 없는 드론이 나타났습니다."
        } 

        #data payload만 보내야 안드로이드 앱에서 백그라운드/포그라운드 두가지 상황에서 onMessageReceived()가 실행됨
        result = self.push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
        print(result)