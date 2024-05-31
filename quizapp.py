import sqlite3
import datetime

# Connection to database "quizapp.db"
conn = sqlite3.connect('quizapp.db') 

# Create a cursor
cursor = conn.cursor()

# User registration function: user input username and password and store to users_tbl table
def register_user(username, password):
    # Check if the username already exists
    cursor.execute("SELECT COUNT(*) FROM users_tbl WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    if count > 0:
        print("Username already exists. Please choose a different username.")
        return
    
    # If the username doesn't exist, insert the new user
    cursor.execute("INSERT INTO users_tbl (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    # Only print "User registered successfully." if a new user was successfully inserted
    if cursor.rowcount > 0:
        print("User registered successfully.")

# Login authentication function: check if username and password are in the users_tbl table
def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users_tbl WHERE username = ? AND password = ?", (username, password))
    if cursor.fetchone():
        return True
    return False

# Function to make sure that question is randomly selected and not repeated
def fetch_random_question():
    while True:
        cursor.execute("SELECT * FROM quiz_tbl ORDER BY RANDOM() LIMIT 1")
        question = cursor.fetchone()
        question_id = question[0]
        if question_id not in asked_questions:
            asked_questions.append(question_id)
            return question
asked_questions = []

# Function to run the quiz application
def run_quiz(username):
    score = 0
    total_questions = 10  # Number of questions to ask.
    for i in range(total_questions):
        print(f"Question {i+1}:")
        question = fetch_random_question()
        print(question[0])  # Print the question
        options = question[1:5]  # Extract options from the fetched question
        correct_answer = question[5]  # Correct answer text
        
        # Print each question
        for idx, option in enumerate(options, start=1):
            print(f"{idx}. {option}")  # Print each option
        
        # Input validation loop
        while True:
            user_input = input("Enter your answer (1-4): ")
            if user_input.isdigit():
                user_answer_index = int(user_input)
                if 1 <= user_answer_index <= 4:
                    user_answer_str = options[user_answer_index - 1]
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")
            else:
                print("Invalid input. Please enter a number between 1 and 4.")
    
        # Validate user answer.
        if user_answer_str == correct_answer:
            print("Correct!")
            score += 1
        else:
            print("Incorrect!")
            print(f"Correct answer is: {correct_answer}")
        print()
        
    percentage_score = (score / total_questions) * 100 # Score computation
    
    # Log quiz summary
    log_quiz_summary(username, percentage_score)
    return percentage_score

# Function to log quiz summary
def log_quiz_summary(username, percentage_score):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("quiz_summary.txt", "a") as file:
        file.write(f"Username: {username}, Score: {percentage_score}%, Time: {current_time}\n")

# Quiz application index where user will be asked to register, login or exit. 
def index():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice:[1, 2, 3] ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            register_user(username, password)
            # print("User registered successfully!")
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authenticate_user(username, password):
                print("Login successful!")
                percentage_score = run_quiz(username) # Run the quiz application after successful login
                print("Quiz completed! Your score is:", f"{percentage_score}%")
                
            else:
                print("Invalid username or password.")
        elif choice == '3':
            exit()
        else:
            print("Invalid choice. Please enter a valid option.")



if __name__ == "__main__":
    index()
    conn.close()
