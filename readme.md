# ATS Recruitment BE built using Django & sqlite

I'd build REST API server for basic ATS for recruiters.

Here Candidates can create their application form, Recruiter can shortlist or reject the candidate form. Also I'd used JWT Login Authentication system.

## Recruiter Login: -

#### username:  recruiter1@gmail.com
#### password: Recruiter@123#


Here recruiters can filter/search for specific candidates based on expected salary, age, years of exp more than, phone number, email or name. Also I'd created one Name search API that has a relevance based sorting.

## Steps to run the code (in Windows): 

1.  Firstly clone the repo and create virtual environment by command: - **python -m venv env**
2.  Then activate the virtual environment: - **.//env//Scripts//activate**
3.  Change the directory to **recruitmentbe** : - **cd recruitmentbe**
4.  Install the required packages available in **requirements.txt** file: - **pip install -r requirements.txt**
5.  Now finally run the code and test API's in Postman: - **python manage.py runserver**
