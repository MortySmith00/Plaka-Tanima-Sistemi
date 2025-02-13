# **Plaka Tanıma ve Araç Bilgi Sistemi**

Bu proje, Python ve SQLite veritabanı kullanılarak geliştirilmiş bir plaka tanıma ve araç bilgi sistemidir. Sistem, araç plakalarını otomatik olarak tanıyarak, araç ve sürücü bilgilerini görüntülemenizi sağlar. Ayrıca, geçmiş plaka kayıtlarını ve giriş-çıkış bilgilerini takip edebilirsiniz. Bu proje, gümrük kapıları, fabrikalar veya otopark girişleri gibi yerlerde giriş-çıkışların güvenliğini artırmak, kayıt tutmak ve güvenlik görevlisinin işini kolaylaştırmak amacıyla hazırlanmıştır.

## **Proje Fotoğrafları**
Proje fotoğrafları, **Proje Ekran Alıntıları** klasöründe bulunmaktadır.

![Proje Görseli](https://github.com/MortySmith00/Plaka-Tanima-Sistemi/blob/main/Proje%20Ekran%20Alıntıları/img3.png)

![Proje Görseli2](https://github.com/MortySmith00/Plaka-Tanima-Sistemi/blob/main/Proje%20Ekran%20Alıntıları/img4.PNG)

## **Özellikler**

1. **Plaka Tanıma**
   - Gerçek zamanlı olarak kamera üzerinden araç plakalarını tanır.
   - Tanınan plakaları veritabanına kaydeder ve daha önce kaydedilmiş plakaları kontrol eder.
   
2. **Araç ve Sürücü Bilgilerini Görüntüleme**
   - Tanınan plakaya ait araç ve sürücü bilgilerini görüntüler.
   - Araç modeli, yük türü, sigorta bilgileri, sürücü adı, kimlik bilgileri gibi detayları içerir.
   
3. **Geçmiş Plaka Kayıtları**
   - Daha önce tanınan plakaların kayıtlarını listeler.
   - Her plakanın ne zaman tanındığı bilgisini içerir.

5. **Güvenlik Görevlisi Giriş Kaydı**
   - Sisteme güvenlik görevlilerinin giriş saatleri kaydedilir.
   - Her güvenlik görevlisinin ne zaman göreve başladığı ve ne zaman görevden ayrıldığı bilgileri tutulur.
   - Güvenlik görevlilerinin vardiya takipleri yapılabilir. 

4. **Bariyer Kontrolü**
   - Tanınan plakaya göre bariyerin açılmasını simüle eder.
   - Bariyer açıldığında kullanıcıya bilgi mesajı gösterir.
