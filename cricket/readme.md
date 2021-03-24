#step 1

#create directory
cd Desktop
 
Desktop$ mkdir cricketmatch
Enter cricketmatch directory
cd cricketmatch

#step2

#install create Virtual Enviorment type below command
 
first install Virtual Enviorment

#install
 sudo pip3 install virtualenv 

#create virtual Envoriment

virtualenv -p python3.8 myenv

# now pull project
 
$cricketmatch git pull origin 

# now active Enviorment

source myenv/bin/active

#after active looks

(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch$ 

#now go project dir
(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch$ cd cricket

(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch/cricket$

#install requerments
(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch/cricket$ pip install -r requirements.text


# makemigrations

(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch/cricket$ python manage.py makemigrations


#migrate command 

(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch/cricket$ python manage.py migrate

#after migrate

# create superuser
(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch/cricket$ python manage.py createsuperuser

# import database backup

(myenv) arvind@arvind-Lenovo:~/Desktop/cricketmatch/cricket$ python manage.py loaddata cricket.json


# for bulk team and player creation script wriiten in  GetTeams view function 

if you need bulk team and player creation script  please uncomment and use it,

#note we are considering 
 i am considering number of player per team is 10

   

# working flow 

 menu 
 Teams click list for all team
 Matches click for random match between two team
 
 








 









 


 
 
 


 

