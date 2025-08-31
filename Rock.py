"""
Rock, Paper, Scissors Game
-------------------------------------------

How to play:
1.You will play against the computer.
2.On each round, type Rock, Paper, or Scissors (case-insensitive).
3.The computer will randomly choose as well.
4. The winner is decided by the standard rules:
    Rock beats Scissors
    Scissors beats Paper
    Paper beats Rock
- Type 'exit' anytime to quit the game.

Nirattay Biswas
"""
import random

#choices available

choices=["rock","paper","scissors"]

def menu():
    print("\nWelcome to Rock,Paper,Scissors!")
    print("Rules: Rock beats Scissors, Scissors beats Paper, Paper beats Rock.")
    print("Play Rock, Paper, or Scissors.")
    print("Type 'exit' to quit anytime.\n")

ASCII_ART = {
    "rock": """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",
    "paper": """
         ___
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""",
    "scissors": """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""
}

def player():
    while(True):
     ch=input("Your choice:").strip().lower()
     if(ch=="exit"):
       return ch
     if(ch in choices):
       return ch
     else:
      print("Invalid input.PLease enter Rock, Paper, or Scissors.")

def computer():
    return random.choice(choices)
    

def determine_winner(playerc,computerc):
 if(playerc==computerc):
   return "tie"
 elif ((playerc == "rock" and computerc == "scissors") or
        (playerc== "scissors" and computerc == "paper") or
        (playerc == "paper" and computerc == "rock")):
     return "player"
 else:
    return "computer"
  
def play_game():
   
 wins=losses=ties=0

 menu()
 while(True):
     ply=player()
     if(ply=="exit"):
          break
     comp=computer()

     print("\nYou choose")
     print(ASCII_ART[ply])
     print("Computer chose:")
     print(ASCII_ART[comp])
    
     result=determine_winner(ply,comp)

     if result == "tie":
            print(" It's a tie!")
            ties += 1
     elif result == "player":
            print("You win this round!")
            wins += 1
     else:
            print("Computer wins this round!")
            losses += 1
     print(f"Score---> Wins: {wins}, Losses: {losses}, Ties: {ties}\n")
 print("\nThanks for playing Rock, Paper, Scissors!")
 print(f"Score → Wins: {wins}, Losses: {losses}, Ties: {ties}\n")
 if wins > losses:
        print("  Winner: You!")
 elif wins < losses:
        print(" Winner: Computer!")
 else:
        print(" Its a tie !")

if __name__ == "__main__":
    play_game()

