from django.shortcuts import redirect, render
import requests

# Create your views here.

def first(request):
    session_id = request.session.session_key
    request.session['data'] = []
    return redirect('home/')

def home(request):
    session_id = request.session.session_key
    return render(request, 'home.html')

def cart(request):
    if request.method == "POST":
        session_id = request.session.session_key
        balhyo = request.POST['balhyo']
        hyang = request.POST['hyang']
        num = request.POST['num']
        image = request.POST['image']
        name = request.POST['name']
        time = request.POST['time']
        phone = request.POST['phone']
        data = {
            "balhyo" : balhyo,
            "hyang" : hyang,
            "num": num,
            "image":image,
            "name": name,
            "time": time,
            "phone": phone,
            "id": session_id
        }
        request.session['data'].append(data)
    return render(request, 'cart.html' ,{"data":request.session['data']})

def kakao_pay(request):
    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "4cac6618fb4a521801d73c5c0a3ab8a9",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        data = request.session['data']
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "mybrew",    # 유저 아이디
            "item_name": 'mybrew',        # 구매 물품 이름
            "quantity": '1',                # 구매 물품 수량
            "total_amount": '2000',        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": "http://127.0.0.1:8000/approval",
            "cancel_url": "http://127.0.0.1:8000/cart",
            "fail_url": "http://127.0.0.1:8000/cart",
        }

        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)
    return redirect('approval')

def approval(request):
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "4cac6618fb4a521801d73c5c0a3ab8a9",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",     # 주문번호
        "partner_user_id": "mybrew",    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    print("확인",res.json())
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    return render(request, 'approval.html', context)