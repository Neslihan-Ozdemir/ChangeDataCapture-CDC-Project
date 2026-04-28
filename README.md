# Change Data Capture (CDC) – SQL’den NoSQL’e Veri Aktarımı Projesi

Bu projede bir ilişkisel veritabanında (SQL) oluşturulan tablolar üzerinde INSERT, UPDATE,
DELETE işlemlerini gerçekleştirerek bu değişiklikleri uygulama katmanında yakalayarak bir NoSQL
veritabanına (MongoDB) aktarılmıştır.Böylece Change Data Capture (CDC) mekanizmasının basit bir
prototipi geliştirilmiştir.

**Kullanılan Teknolojiler:**
-SQL DB: MySQL
-NoSQL DB: MongoDB
-Programlama Dili: Python

**CDC Yaklaşımı ve Kullanılan Yöntem**
Projede Change Data Capture (CDC) yaklaşımı kullanılarak MySQL veritabanında gerçekleşen veri
değişiklikleri izlenmiştir. Orders ve Customers tablosuüzerinde tanımlanan triggerlar sayesinde
INSERT, UPDATE ve DELETE işlemleri anında Orders_log ve Customer_log tablosuna
kaydedilmiştir.
Log kayıtlarının MongoDB’ye aktarımı Python dili ile gerçekleştirilmiştir. Uygulama, belirli
aralıklarla Orders_log , Customers_log tablosunu kontrol ederek henüz aktarılmamış kayıtları tespit
etmekte ve bu kayıtları MongoDB’deki changes koleksiyonuna belge formatında aktarmaktadır.
Aktarım işlemi tamamlandıktan sonra ilgili log kayıtları MySQL tarafında transferred = 1 olarak
güncellenmekte, böylece aynı verinin tekrar aktarılması engellenmektedir. Bu yöntem ile gecikmenin
az olduğu,izlenebilir ve güvenilir bir CDC sistemi oluşturulmuştur.



