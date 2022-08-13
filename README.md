# Python-Flask-Forum-Project

Staj Başvuru sürecimde geliştirmiş olduğum python projesi

Projenin Yapabildikleri:
    1) Login ve Register sayfaları mevcut
    2) Register olan kişinin şifreleri şifreli şekilde tutuluyor.
    3) Herkes bir konu başlığı ve başlığa ait içerik girebilir.
    4) İsteyen üyeler açılan başlıklara yorum yapabilir.
    5) Yapılan yorumları sadece yorumu yapan kişi veya moderator silebilir/düzenleyebilir.
    6) Açılan başlıkları sadece o başlığı açan kişi yorumlara kapatabilir.
    7) Her üyenin kendi profil sayfası mevcut.
    8) Her üye profil sayfasını editleyebiliyor.
    9) Her üye profil sayfasında açtığı başlıkları görebiliyor.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

Install and update using pip:
```
$ pip install -U Flask
```

### Running the project

If you can't run it is my fault :).
You can check the Heroku link: * [Heroku](https://python-project-flask.herokuapp.com/)

You can log in with the nickname and password below for trial purposes.

Nickname:moderator
Password:12345

```
1) ../Python-Flask-Forum-Project> cd flaskr

2) flask init-db

3) 
    set FLASK_APP=__init__.py
    $env:FLASK_APP = "__init__.py"
    flask run

    Runnig on http://127.0.0.1:5000 (Press CTRL+C to quit)
```
### Links

* [Documentation](https://flask.palletsprojects.com/en/2.1.x/) - Flask Documentations