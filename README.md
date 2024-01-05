# Fake CSV Service 📎

The Fake CSV Service project aims to create an online platform using Python and Django for generating CSV files with fake (dummy) data. The application allows users to log in, create custom data schemas with various data types, and generate CSV files based on those schemas. The project utilizes Django's generic views for user authentication/registration and Celery for data generation.

## ⚙️ Installing using GitHub

Linux/MacOS:

```shell
git clone https://github.com/denys-source/fake-csv-service/
cd fake-csv-service/
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Windows:
```shell
git clone https://github.com/denys-source/fake-csv-service/
cd fake-csv-service/
python venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🐳 Running with docker

Docker should be installed
```shell
sudo docker-compose up --build
```

## 📍 Features

- **User Authentication and Registration:** Users can register new accounts and log in with a username and password.
- **Data Schema Management:** Users can create multiple data schemas with names and columns of specified data types.
- **Flexible Schema Building:** Users can create data schemas with any number of columns, each having a specified data type, name, and order.
- **CSV Generation:** Enable users to input the number of records and use Celery to generate CSV files with fake data, saving the result in the "media" directory.
- **Interface and Status Labels:** Display colored labels indicating each dataset's status (processing/ready/failed).

## ✅ Demo

![image](https://github.com/denys-source/fake-csv-service/assets/72623693/b6305769-5e51-420b-81ea-17af67fe4aa7)

![image](https://github.com/denys-source/fake-csv-service/assets/72623693/f55fb656-3fc4-44d1-a5db-5d17a5abc726)

![image](https://github.com/denys-source/fake-csv-service/assets/72623693/7fb507ed-3b1b-43d5-a271-ae5cbbcb571a)

![image](https://github.com/denys-source/fake-csv-service/assets/72623693/af863994-407d-405d-b22d-5aef9ce92d60)

![image](https://github.com/denys-source/fake-csv-service/assets/72623693/d224344a-9531-452b-87e4-bfdbeeb661ec)
