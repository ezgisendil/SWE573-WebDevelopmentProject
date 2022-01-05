# SWE573-WebDevelopmentProject
![](https://github.com/ezgisl/SWE573-WebDevelopmentProject/blob/main/images/logo.png)

Repository for Software Development Practice course

Visit [Wiki](https://github.com/ezgisl/SWE573-WebDevelopmentProject/wiki) page for project details.

[Project Code](https://github.com/ezgisl/SWE573-WebDevelopmentProject/tree/master) is available in master branch.

## How to install and run the project

```bash
git clone https://github.com/ezgisl/SWE573-WebDevelopmentProject.git

python -m venv venv

cd venv

.\Scripts\activate

cd..

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```
## How to run on Docker

```
docker-compose up --build
```