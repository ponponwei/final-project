import random
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image 

# https://www.youtube.com/watch?v=8QTsK1aVMI0&t=1133s - used as a guide on how to go about creating the game in the shell form
# Used to Create All the Cards - https://stackoverflow.com/questions/41970795/what-is-the-best-way-to-create-a-deck-of-cards/41970851
# How to use classes with functions, __init__, __str__, (sel)f - https://www.youtube.com/watch?v=wfcWRAxRVBA
# how to use tKinter: https://realpython.com/python-gui-tkinter/
# File with 52 Cards - https://boardgames.stackexchange.com/questions/51426/where-can-i-download-high-quality-images-of-poker-cards (names of cards were changed to match code)
# How to pip install PIL https://pillow.readthedocs.io/en/stable/installation.html
# How to get started with building a GUI with TKinter: https://www.youtube.com/watch?v=jE-SpRI3K5g

playing = True # We will use gloabal logic to coninuosly play the game

suits = ('Spades', 'Clubs', 'Hearts', 'Diamonds')
names = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
values = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10}

class individualCardCreator:
    def __init__ (self, suit, name):
        self.suit = suit
        self.name = name
    
    def __str__ (self):
        return self.name + ' of ' + self.suit

class Deck:                             # Creates a deck 
    def __init__(self):
        self.deck = []                  # Initializes deck list
        for suit in suits:
            for suitNumb in names:
                self.deck.append(individualCardCreator(suit, suitNumb))
    
    def shuffle(self):
        random.shuffle(self.deck)       # Shuffles deck
    def deal(self):
        dealt_card = self.deck.pop()    # Picks a card from the deck, and removes it
        return dealt_card               # Returns picked card

class Hand:
    def __init__(self):
        self.cards = []                 # Creats the hand
        self.value = 0                  # Initializes the hand value
        self.aces = 0                   # Need to account for aces b/c troublesome

    def add_card(self, card):           # adds card to the player's or dealer's hand
        self.cards.append(card)
        self.value += values[card.name]
        if card.name == 'Ace':
            self.aces += 1

    def ace_adjust(self):
        while self.value > 21 and self.aces:
            self.value -= 10            # Accounts for Ace counting as 11, or 1 when the hand total is over 21
            self.aces -=1               # Removes the count of ace after it is accounted for once, this allows for the loop to run twice just in case there is a senario of double aces


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.ace_adjust()

def HoS(deck, hand):
    global playing                        # https://www.geeksforgeeks.org/global-keyword-in-python/

    while True:
        HorS = input("\nHit or Stand? (Enter 'h' to hit or 's' to stand) ")
        
        if HorS[0].lower() == 'h':
            hit(deck, hand)
        elif HorS[0].lower() == 's':
            print("You have chosen to stand. The deal will play his turn now.")
            playing = False                     # Ends global 'True' on play, everything is now automatic
        else:
            print("Invalid input. Try again!")
            continue
        break                                   # https://www.tutorialspoint.com/python/python_loop_control.htm

def hidden(player, dealer):
    print("\nDealer's Hand: ")
    print(" <card hidden>")
    print("", dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')

def shown(player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

class Bank:
    def __init__(self):
        self.total = 1000
        self.bet = 0
    
    def betW(self):
        self.total += self.bet

    def betL(self):
        self.total -= self.bet

def wager(cash):
    while True:
        try:
            cash.bet = int(input("How much money would you like to wager? (Enter dollar amount) "))
        except ValueError:                      # https://www.journaldev.com/33500/python-valueerror-exception-handling-examples#:~:text=Python%20ValueError%20is%20raised%20when,precise%20exception%20such%20as%20IndexError.
            print("Invalid input. Please enter the amount of money you would like to bet: ")
        else:
            if cash.bet > cash.total:
                print("Your bet cannot exceed: $1000!")
            else:
                break


# Game Situations

def playerL(player, dealer, cash):         # Player Wins
    print("PLAYER LOSES!")
    cash.betL()

def playerW(player, dealer, cash):          # Player Loses
    print("PLAYER WINS!")
    cash.betW()

def dealerW(player, dealer, cash):          # Dealer Wins
    print("DEALER WINS!")
    cash.betL()

def dealerL(player, dealer, cash):         # Dealer Loses
    print("DEALER LOSES!")
    cash.betW()

def tie(player, dealer):                        # Tie
    print("Player and Dealer tie!")

# Game
while True:
    print("WELCOME TO BLACK JACK!")
    print("Bank Amount: $1000")

    #----------------------------------------------------------------------------------------------
    root = tk.Tk()
    root.title("Black Jack")

    canvas = tk.Canvas(root, height=900, width=1200, bg="#263D42")

    canvas.create_text(600, 37, text="Black Jack", fill="white", font=('Helvetica 25 bold'))
    canvas.create_text(600, 125, text="Dealer's Hand", fill="white", font=('Helvetica 15 bold'))
    canvas.create_text(600, 525, text="Player's Hand", fill="white", font=('Helvetica 15 bold'))
    canvas.pack()

    middle = tk.Frame(root, bg="white")
    middle.place(width=800, height=15, x=200, y=450)
    canvas.pack()
    #----------------------------------------------------------------------------------------------

    deck = Deck()                       # Creates a deck with 52 cards
    deck.shuffle()                      #Shuffles a 52 card deck

    playerH = Hand()                    # Creates a player hand
    dealerH = Hand()                    # Creates a dealer hand
    
    playerH.add_card(deck.deal())       # 1st Player Card
    playerH.add_card(deck.deal())       # 2nd Player Card

    dealerH.add_card(deck.deal())       # 1st Dealer Card
    dealerH.add_card(deck.deal())       # 2nd Dealer Card
    
    player_bank = Bank()                # Creates a bank for the player with an intial amount of $1000

    wager(player_bank)                  # Allows for a way to take in wager

    hidden(playerH, dealerH)            # Prints hands, 1 of dealer card is hidden


    while playing:
        HoS(deck, playerH)
        hidden(playerH, dealerH)

        if playerH.value > 21:
            playerL(playerH, dealerH, player_bank)
            break

    if playerH.value <= 21:
        
        while dealerH.value < 17:
            hit(deck, dealerH)
        shown(playerH, dealerH)

        if dealerH.value > 21:
            dealerL(playerH, dealerH, player_bank)


        elif dealerH.value > playerH.value:
            dealerW(playerH, dealerH, player_bank)


        elif dealerH.value < playerH.value:
            playerW(playerH, dealerH, player_bank)

        if playerH.value > 21:
            playerL(playerH, dealerH, player_bank)

    print("\nPlayer's bank: ", player_bank.total)
    print("\nThank you for playing!")
    
    aP = 0
    imgs = {}                           # To create new variable names within loops: https://stackoverflow.com/questions/36767496/creating-multiple-variables-during-each-iteration-of-for-loop-and-executing-tk-c
    imgs_r = {}
    imgs_n = {}
    
    for i in list(playerH.cards):
        name = "img" + str(aP)
        i = str(i)
        imgs[name] = Image.open(i+".png")                                   # How to get image from file and put onto GUI: https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python
        imgs_r[name] = imgs[name].resize((130,195), Image.ANTIALIAS)
        imgs_n[name] = ImageTk.PhotoImage(imgs_r[name])
        canvas.create_image((215+160*aP),597, anchor=NW, image=imgs_n[name])
        aP = aP + 1
    
    dimgs = {}
    dimgs_r = {}
    dimgs_n = {}
    dP = 0
    for z in list(dealerH.cards):
        name = "dimg" + str(dP)
        z = str(z)
        dimgs[name] = Image.open(z+".png")
        dimgs_r[name] = dimgs[name].resize((130,195), Image.ANTIALIAS)
        dimgs_n[name] = ImageTk.PhotoImage(dimgs_r[name])
        canvas.create_image((215+160*dP),197, anchor=NW, image=dimgs_n[name])
        dP = dP + 1
    
    root = mainloop()
    
    break 