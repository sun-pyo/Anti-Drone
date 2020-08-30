#-*-coding:utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time
from pyfcm import FCMNotification

cred = credentials.Certificate('drone-detection-js-firebase-adminsdk-4xh9r-3ba93b9ccd.json')
# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('firestore-1add2-firebase-adminsdk-7vjg4-6c20413010.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# 파이어베이스 콘솔에서 얻어 온 API키를 넣어 줌
push_service = FCMNotification(api_key="AAAAX5SpFgc:APA91bG2YQo1PojdmVVmxg30fWhS_JQl4djqn43rilA4pWpNvvIxlwYZRQEKG0-a__EePQvkL9w7xkHEoF2P_o9spUC04r_CPLF4DE5vUOBKqgQYC6G4KgNT9aML2RGe4hzaOmmOa1iv")
#Settings 일반 웹API키 
'''
여기서는 지정된 토큰 1개만 넣어서 사용함. 
좀 더 확장할려면 토큰을 앱으로 부터 받거나 앱서버 DB에서 가져와서 다수의 토큰에 알림을 발송 할 수도 있음.
'''
#클라우드 메세징 서버키 토큰 
mToken = "dM4Tyq6_QiaWGRT3rvgMx5:APA91bERqNtgqXwNeuRUCM7ZryDSVZGbAxhKQVuMnBw0V6y4482TZJD0Kw9XCASEUGQu3D-Q0LNVciZ73vQpm2Cd9Jt6HEM-hp51b0dkmZ2je0eIlw5WaQf10tjXpxezHB0twkD00GP8" #안드로이드스튜디오에서 토큰얻어서 넣기 
mToken1 = "fVXVBOI7Th-9FHCks5fVab:APA91bHCwiTR4s-cvKln-_RyaZlg60BPj6MB8T9V1sAFmmQY9oaaRER7ZNLiXARY_DjGd_CFdwnuxv7L_GwkTQ3lT62DCHvn-BIsrw-lO97Fjnbxf1H0TMOgGa2kxx_yJEZFT5ia4YT5"
nth = 0
def sendMessage():

    global nth
    nth += 1
    registration_id = mToken
    registration_id1 = mToken1

    data_message = {
        "body" : " Drone WARNING 알수 없는 드론이 " + str(nth)+"번 나타났습니다."
    }
    
    #data payload만 보내야 안드로이드 앱에서 백그라운드/포그라운드 두가지 상황에서 onMessageReceived()가 실행됨
    result = push_service.single_device_data_message(registration_id=registration_id1, data_message=data_message)
    print(result)

def _main():
    dnum=0
    while True:
        doc_ref_drone = db.collection(u'robot').document(u'sky')
        dic = doc_ref_drone.get().to_dict()
        current = int(dic['Num_of_drone'])
        if dnum != current:
            dnum = current
            if dnum != 0:
                print(current)
                print('sending')
                sendMessage()

if __name__ == "__main__":
	_main()