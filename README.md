# Group Project 2: Distributed Chat Application
## By Samuel Lara, Seena Kaboli, and Alexis Jaime
--------------------------------------------------------
### How to Compile and Run
1. Install PostgreSQL
   On your local machine, download PostgreSQL via the following link: https://www.postgresql.org/download/
   The installation process differs on each OS, but make sure to keep the default settings of the database port
   number and ip address. This is typically 'localhost' and 5432 respectively. Additionally, keep note of your
   password, it will be needed to connect to the database.
2. Enter your shell and navigate to the directory with the source code.
3. Install Python Dependencies
   Install the required dependencies using the following command:
   run pip install -r requirements.txt
4. Set Up Database
   Run the setup script setup_db.sh to create the necessary database for the application.
   Ensure the script has executable permissions by running
   chmod +x setup_db.sh
   Then, execute the script:
   ./setup_db.sh
5. Run the Application
   Launch the main application by running the following command,
   replacing "PASSWORD" with your chosen database password as done in step 1:
   python main.py "PASSWORD"
6. Within the console application, follow the login/sign-up process to begin chatting with other peers in the network
7. Repeat steps 5 & 6 in order to sign-up/log in as another peer, so that you try the chatting process as shown in the video
8. Exit the Application:
   Press ctrl+c in each respective terminal to close the chat application.
