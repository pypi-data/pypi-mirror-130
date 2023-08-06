# O mnie
Jeżdżę do czterech światów od zimy 2020.
Znany jako: Frasiu, Justin Biber, Kuba, Filon... A od turnusu masterskiego w zimę 2022 jako *Filon Async*.
Jestem wiernym fanem psora Adonisa.

# O projekcie
Pewnego razu tak sobie wchodząc na fotorelację, żeby pooglądać sobie zdjęcia z turnusu, zobaczyłem, że już po załadowaniu strony wyświetla się `pobieranie zdjęć`.
Stwierdziłem więc, że zdjęcia muszą nie być wbudowane w stronę, tylko pobierane skąd indziej.

Otworzyłem devtool-sy i zobaczyłem, że wysyłane jest dodatkowe zapytanie na `quatromondisapi.azurewebsites.net`...
A więc odpaliłem sobie nowego tab-a na https://quatromondisapi.azurewebsites.net/ a tam co? SWAGGER XDD
Po prostu mają swagger-a otwartego. Nawet z przyciskami `Try it out!`

Że na wyższym poziomie umiem tylko python-a, to sobie tak po prostu zacząłem robić w python-ie wrapper do Quatromondis API.
Moi rodzice teraz myślą, że hackuję, no ale cóż...

Wszystkie zapytania POST, nie będą na razie testowane przeze mnie, bo nie chcę na prawdę wysyłać fałszywych zamówień książki, rezerwacji turnusów itp. bo one są rozpatrywane przez rzeczywistych ludzi, a to im będzie przeszkadzać w pracy. 
Mam zupełnie zero nadziei, że ktoś kiedykolwiek zainteresuje się tym projektem.
Jeszcze mniej, że będzie to osoba, która prześle swoje zamówienie/rezerwacje przez tę bibliotekę, tylko po to, by pomóc w projekcie.

POST /api/ParentsZone/Apply\
To już w ogóle jest poważne zapytanie.
W swagger-ze nawet nie ma udokumentowanych danych, które trzeba wysłać.
Z kodu strony domyślam się tylko, że są przesyłane w formie forma (haha).
To nie zmienia faktu, że metoda najprawdopodobniej nigdy nie będzie zaimplementowana, właśnie przez brak możliwości testowania.

