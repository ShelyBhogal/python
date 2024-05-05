import tkinter
import random

# Function to load card images

def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    extension = 'png'
    
    for suit in suits:
        # Go through number cards 1-10
        for card in range(1, 11):
            filepath = 'data/cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=filepath)
            card_images.append((card, image))
            
        # Go through face cards
        for card in face_cards:
            filepath = 'data/cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=filepath)
            card_images.append((10, image))
            

# Function to deal cards

def deal_card(frame):
    # Pop off next card from top of the deck
    next_card = deck.pop(0)
    # Add to the back of the deck (so cards don't run out)
    deck.append(next_card)
    # Add image to a label widget and pack into frame
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # Return face value
    return next_card


# Function to calculate total of hand (all cards in hand)

def score_hand(hand):
    # Only one Ace can be 11, which reduces to 1 if hand goes over 21
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
            
        score += card_value
        
        # Check if hand is bust and if there is ace
        if score > 21 and ace:
            score -= 10
            ace = False
            
    return score


# Function to deal card for dealer and add up score

def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)
    
    player_score = score_hand(player_hand)
    
    if player_score > 21:
        result_text.set("Dealer Wins")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player Wins!!")
    elif dealer_score > player_score:
        result_text.set("Dealer Wins")
    else:
        result_text.set("DRAW")
    

# Function to deal card for player and add up score

def deal_player():
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    
    if player_score > 21:
        result_text.set("Dealer Wins")
    

# Function to clear cards and reset hands (start new game)

def new_game():
    # Access global variables to modify
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    
    # Destroy dealer/player card frames and re-create them
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)
    
    # Reset text in results label
    result_text.set("")
    
    # Reset lists to store dealer and player scores
    dealer_hand = []
    player_hand = []
    
    # To keep game going
    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()
    

# Function to shuffle deck (you can't include parameter in command argument)

def shuffle():
    random.shuffle(deck)
    

# Function to start playing

def play():
    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()
    
    main_window.mainloop()
    


# ------------------------------------- END OF FUNCTIONS ----------------------------------------------
    

# ---- MAIN PROGRAM (executed no matter what)
main_window = tkinter.Tk()

main_window.title("Black Jack")
main_window.geometry('640x480')
main_window.configure(background='green')

# ---- ADD LABEL FOR RESULT TEXT
result_text = tkinter.StringVar()
result = tkinter.Label(main_window, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

# --- ADD FRAME FOR CARDS
card_frame = tkinter.Frame(main_window, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

# ---- ADD FRAME FOR DEALER CARDS WITH LABEL TO CARD FRAME
dealer_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text="Dealer", background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)

dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

# ---- ADD FRAME FOR PLAYER CARDS WITH LABEL TO CARD FRAME
player_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text="Player", background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)

player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

# ---- ADD FRAME FOR CARD BUTTONS
button_frame = tkinter.Frame(main_window)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

# ---- ADD BUTTONS TO BUTTON FRAME
dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text="Shuffle",  command=shuffle)
shuffle_button.grid(row=0, column=3)

# ---- LOAD CARD PNG IMAGES
cards = []
load_images(cards)

# Create new deck of cards and shuffle
deck = list(cards)
shuffle()

# Initialize lists to store dealer and player scores
dealer_hand = []
player_hand = []

# MODULE FUNCTION TO BE IMPORTED FOR USE

if __name__ == "__main__":
    play()
    
