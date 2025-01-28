import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from src.database_commander import DatabaseCommander  # Veritabanı sorguları için DatabaseCommander sınıfını import edin

# E-posta gönderim fonksiyonu
def send_email(subject, recipient, body, smtp_server, smtp_port, sender_email, sender_password):
    """E-posta gönderimi için genel bir fonksiyon."""
    try:
        # MIME yapısını oluştur
        msg = MIMEMultipart()
        msg['Cocktail Machine'] = sender_email  # Gönderen e-posta adresi
        msg['admin'] = recipient  # Alıcı e-posta adresi
        msg['subject'] = subject  # E-posta başlığı

        # E-posta gövdesini ekle
        msg.attach(MIMEText(body, 'plain'))

        # SMTP sunucusuna bağlan ve e-posta gönder
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Bağlantıyı şifrele
            server.login(sender_email, sender_password)  # E-posta hesabına giriş
            server.sendmail(sender_email, recipient, msg.as_string())  # E-postayı gönder
            print("E-posta başarıyla gönderildi!")
    except Exception as e:
        print(f"E-posta gönderimi başarısız oldu: {e}")


# Şişe doluluk seviyesini kontrol etme ve boş şişeler varsa e-posta gönderme fonksiyonu
def check_and_notify_empty_bottles():
    """Boş şişeleri kontrol et ve varsa e-posta gönder."""
    db_commander = DatabaseCommander()
    empty_bottles = db_commander.get_empty_bottles()  # Veritabanından boş şişeleri al

    if empty_bottles:
        # Boş şişe bilgilerini formatla
        email_body = "The following bottles are empty:\n\n"
        email_body += "Bottle Number\t\tName\t\tFill Level\n\n"
        email_body += "-" * 40 + "\n"
        for bottle_num, name, fill_level in empty_bottles:
            email_body += f"{bottle_num}\t\t\t{name}\t\t{fill_level}\n"

        # E-posta bilgilerini ayarla
        subject = "Alert: Empty Bottles Detected"
        recipient = "esmapasaoglu7@gmail.com"  # Alıcı e-posta adresi
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "1esmapasaoglu@gmail.com"  # Gönderen e-posta adresi
        sender_password = "lzbu nczj jsbb lecj"  # Uygulama şifresi

        # E-postayı gönder
        send_email(subject, recipient, email_body, smtp_server, smtp_port, sender_email, sender_password)
        print("Boş şişeler hakkında uyarı e-postası gönderildi.")
    else:
        print("Tüm şişeler dolu, e-posta gönderimi gerekmedi.")


# Zamanlayıcı fonksiyonu: 24 saatte bir boş şişeleri kontrol eder
def periodic_check():
    """Her 24 saatte bir boş şişeleri kontrol eder."""
    check_and_notify_empty_bottles()  # Boş şişeleri kontrol et ve e-posta gönder
    # 24 saat (86400 saniye) sonra yeniden çalıştır
    threading.Timer(86400, periodic_check).start()  # Zamanlayıcıyı başlat

# Zamanlayıcıyı başlatmak için bu fonksiyonu çağırın
periodic_check()  # Uygulama başlatıldığında zamanlayıcıyı başlat
