import sqlite3
import random
import bcrypt
#connect to database
conn = sqlite3.connect('quizapp.db')

#create a cursor
cursor = conn.cursor()

def register_user(username, password):
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users_tbl (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()


def authenticate_user(username, password):
    cursor.execute("SELECT password FROM users_tbl WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        hashed_password = result[0]
        # Check if the entered password matches the hashed password
        if bcrypt.checkpw(password.encode(), hashed_password):
            return True
    return False

def register_user():
    # Prompt the user to enter a username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Insert the username and hashed password into the database
    cursor.execute("INSERT INTO users_tbl (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

# Example usage:
register_user()


asked_questions = []

def fetch_random_question():
    while True:
        cursor.execute("SELECT * FROM quiz_tbl ORDER BY RANDOM() LIMIT 1")
        question = cursor.fetchone()
        question_id = question[0]
        if question_id not in asked_questions:
            asked_questions.append(question_id)
            return question
    

def run_quiz():
    score = 0
    total_questions = 10  # Number of questions to ask
    for i in range(total_questions):
        print(f"Question {i+1}:")
        question = fetch_random_question()
        print(question[0])  # Print the question
        options = question[1:5]  # Extract options from the fetched question
        correct_answer = question[5]  # Correct answer text
        
        # Print options
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
    
        
        # Check user answer
        if user_answer_str == correct_answer:
            print("Correct!")
            score += 1
        else:
            print("Incorrect!")
            print(f"Correct answer is: {correct_answer}")
        print()
        
    percentage_score = (score / total_questions) * 100
    return percentage_score

percentage_score = run_quiz()
print("Quiz completed! Your score is:", f"{percentage_score}%")
conn.close()
