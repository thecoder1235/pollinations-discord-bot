import requests,urllib.parse  # API'ye HTTP istekleri göndermek için requests kütüphanesini içe aktarma
class ImgAPI:
    def download_image(self,prompt):
        # download_image işlevinin tanımlanması.
        # Bu işlev tek bir parametre alır: prompt.
        # prompt, oluşturulacak görüntünün metin açıklamasıdır.
        prompt = urllib.parse.quote(prompt)

        url = f"https://image.pollinations.ai/prompt/{prompt}"
        # İstek URL'sini oluşturma.
        # "prompt" değişkeninin değeri URL'ye eklenir.
        # Bu, resim oluşturma hizmetine erişmek için kullandığımız adrestir.

        response = requests.get(url)
        # Sunucuya bir GET isteği gönderiliyor.
        # Sunucu yanıt olarak resim verilerini döndürmelidir.

        with open('generated_image.jpg', 'wb') as file:
            # generated_image.jpg dosyasını bayt yazma modunda açılıyor.
            # Görüntü düz metin değil, ikili veri olduğu için wb modu gereklidir.

            file.write(response.content)
            # Sunucu yanıtının içeriğini dosyaya yazma.
            # response.content, görüntünün baytlarını içerir.

        print('Resim kaydedildi!')
        # Kullanıcının programın bittiğini anlaması için konsola bir mesaj yazdırma.
if __name__ == "__main__":
    api = ImgAPI()
    api.download_image("a cat sitting on a windowsill, looking outside at the rain")
# İşlevi çağırıp komut istemini işlevin içine aktarıyoruz.
# Çalıştırıldıktan sonra program isteği gönderecek ve görüntüyü bir dosyaya kaydedecektir.