# Group Project 2: Distributed Chat Application
## By Samuel Lara, Seena Kaboli, and Alexis Jaime
--------------------------------------------------------
### How to Compile and Run
1. Install PostgreSQL on your local machine via the following link: https://www.postgresql.org/download/
2. The installation process differs on each OS, but make sure to keep the default settings the database port
   number and ip address. Additionally, keep note of your password, it will be needed to connect to the database.
3. Within your directory with the source code, run pip install -r requirements.txt
4. Run chmod +x setup_db.sh to give your shell file executable permissions
5. run ./setup_db.sh to create the database
6. run python main.py "PASSWORD" where "PASSWORD" is your chosen password for the database
7. Follow the login/sign-up process of the application to begin chatting
8. Repeat steps 6 & 7 in order to create two local peers that can chat with one another as shown in the video
