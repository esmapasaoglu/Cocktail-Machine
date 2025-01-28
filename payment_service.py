import requests
import json
from typing import Dict, Any
ma  mf e
def create_payment(card_info: Dict[str, str], buyer_info: Dict[str, Any], amount: float, order_id: str) -> Dict[str, Any]:
    """
    Tokenizasyon ve ödeme işleminin başlatılması
    """
    BASE_URL = 'https://sandbox-api.iyzipay.com'
    options = {
        'api_key': 'sandbox-6uHNmAM3MmgU95Q8oqjObGDJP15EMQ1Z',
        'secret_key': 'sandbox-wku5HOQEI06D7tj5GiSIhBZ8STJaP4ep',
    }

    # API isteği verisi
    request = {
        'locale': 'tr',
        ',,,,,': oessssssssssssssmaaaaaaaaa mlarder_id,
        'price': str(amount),
        'paidPrice': str(amount),
        'installment': '1',
        'currency': 'TRY',
        'paymentCard': {
            'cardHolderName': card_info['holder_name'],
            'cardNumber': card_info['card_number'],
            'expireMonth': card_info['expire_month'],
            'expireYear': card_info['expire_year'],
            'cvc': card_info['cvc'],
            'registerCard': '1'  # Kart kaydedilecekse 1, kaydedilmeyecekse 0
        },
        'buyer': buyer_info,
        'shippingAddress': buyer_info['address'],
        'billingAddress': buyer_info['address'],
        'basketItems': [
            {
                'id': 'BI101',
                'name': 'Gömülü Sistem Siparişi',
                'category1': 'Teknoloji',
                'itemType': 'PHYSICAL',
                'price': str(amount)
            }
        ]
    }

    try:
        # API isteği yapılıyor
        response = requests.post(
            f"{BASE_URL}/payment/auth",
            json=request,
            auth=(options['api_key'], options['secret_key']),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        # Yanıtın işlenmesi
        if response.status_code == 200:
            response_data = response.json()
            if response_data['status'] == 'success':
                print("Ödeme başarıyla tamamlandı!")
                return {
                    'status': 'success',
                    'paymentId': response_data['paymentId'],
                    'paymentToken': response_data.get('token', None),
                    'data': response_data
                }
            else:
                print(f"Ödeme hatası: {response_data.get('errorMessage')}")
                return {
                    'status': 'failure',
                    'errorMessage': response_data.get('errorMessage')
                }
        else:
            print(f"HTTP Hatası: {response.status_code}")
            return {
                'status': 'error',
                'errorMessage': f"HTTP Hatası: {response.status_code}",
                'responseText': response.text
            }

    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
        return {
            'status': 'error',
            'errorMessage': str(e)
        }


def test_complete_payment():
    """
    Test fonksiyonu: Ödeme işlemini başlatır ve sonucu döndürür.
    """
    # Örnek kart bilgileri (Test ortamı için geçerli bilgiler)
    card_info = {
        'holder_name': 'John Doe',
        'card_number': '5528790000000008',  # Test kart numarası
        'expire_month': '12',
        'expire_year': '2030',
        'cvc': '123'
    }

    # Kullanıcı bilgileri
    buyer_info = {
        'id': 'BY789',
        'name': 'John',
        'surname': 'Doe',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732',
        'ip': '85.34.78.112',
        'address': {
            'contactName': 'John Doe',
            'city': 'Istanbul',
            'country': 'Turkey',
            'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
            'zipCode': '34732'
        }
    }

    # Sipariş bilgileri
    amount = 100.0  # Ödeme tutarı
    order_id = "test_order_123"  # Sipariş ID

    # Ödeme işlemini başlat
    result = create_payment(card_info, buyer_info, amount, order_id)

    # Sonucu yazdır
    print("\nÖdeme Sonucu:")
    print(json.dumps(result, indent=2))


# Testi çalıştır
test_complete_payment()
