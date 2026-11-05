# print("what's the best CMS?") #namayesh soal karbar
# print("A:wordpress")# namayesh gozineha
# print("B:Joomla")# daryaft javab az karbar
# print("C:Drupal")#namayesh dorost o ghalat boodan
# print("B:Headless")
from rich.console import Console
import random
console = Console()

questions=[
    ("what's the bestCMS?",["A wordpress","B:Joomla","C:Drupal","D: headless"],"A"),
    ("what's the best programming language ?",["A Python","B:JavaScript","C:Java","D:C++ "],"A"),
    ("what's the best database ?",["A:MySQL ","B:PostgreSQL","C:MonoDB","D:SQL "],"B"),

                            
]

def show_menu():
    while True:
        user_input=input("Do you want to start the quiz?").strip().lower()
        if user_input=="yes":
            return True
        elif user_input=="no":
            console. print("exiting the quiz.Goodbye!",style="yellow on black")
            return False
        else:
            console.print("invalid input.please enter'yes' or'no'.",style="red on white")
def play_quiz(player_name):

    score=0
    user_correct=0
    BONUS=10
    PENALTY=3
    used_change=False
    player_questions=questions.copy()
    for i in range(len(player_questions)):
        if not used_change and i<len(player_questions)-1:
            while True:
                change=input("do you want to changethis question?(yes/no):").strip().lower()
                if change=="yes":
                    new_index=random.choice(range(i+1,len(player_questions)))
                    player_questions[i],player_questions[new_index]=(player_questions[new_index],player_questions[i])
                    used_change=True
                    print("Question changed!")
                    break
                elif change=="no":
                    break
                else:
                    print("please enter yes or no.")
    question,options,correct_answer =player_questions[i]
    print(question)
    for option in options:
        print(option)
        user_answer=str(input("Your choice:").strip().upper())
        if user_answer==correct_answer:
            print("Correct")
            score+=BONUS
            user_correct+=1
        else:
            print("Incorrect")
            score-=PENALTY
    return score,user_correct
def show_results(score,user_correct):
    print(f"Your final score is:{score}")
    print(f"Your answer{user_correct}question correctly.")
    print(f"Percentage:{user_correct/len(questions)*100}")
while True:
    if show_menu():
        number_of_players=int(input("Enter number of players:"))
        for i in range(number_of_players):
            player_name=input("Enter player name:")
            score,user_correct=play_quiz(player_name)
            show_results(score,user_correct)
    else:
        break
