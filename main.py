import random
from tkinter import *
import pandas

# Constants
BACKGROUND_COLOR = "#B1DDC6"
CARD_WIDTH = 800
CARD_HEIGHT = 526

# Globals
currentCard = {}

# ---------------------------- DATA RETRIEVAL ------------------------------- #
data = pandas.read_csv("data/french_words.csv")

wordsToLearn = data.to_dict(orient='records')


# ---------------------------- Function Definition ------------------------------- #
def flipCard():
    canvas.itemconfig(card, image=cardBack)
    canvas.itemconfig(cardTitle, text="English", fill="white")
    canvas.itemconfig(cardWord, text=currentCard["English"], fill="white")
    return


def correctButton():
    if len(wordsToLearn) > 0:
        wordsToLearn.remove(currentCard)
        nextCard()
    if len(wordsToLearn) == 0:
        canvas.itemconfig(cardTitle, text="Congrats")
        canvas.itemconfig(cardWord, text="No more cards!")
    return


def nextCard():
    global currentCard, flipTimer

    window.after_cancel(flipTimer)

    if len(wordsToLearn) > 0:
        currentCard = random.choice(wordsToLearn)
        canvas.itemconfig(cardTitle, text="French", fill="black")
        canvas.itemconfig(cardWord, text=currentCard["French"], fill="black")
        canvas.itemconfig(card, image=cardFront)
        flipTimer = window.after(3000, func=flipCard)
    return

# ---------------------------- UI SETUP ------------------------------- #


# Window
window = Tk()
window.title("Flashy French Learning")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flipTimer = window.after(3000, func=flipCard)

# Images
cardFront = PhotoImage(file="images/card_front.png")
cardBack = PhotoImage(file="images/card_back.png")
correctImage = PhotoImage(file="images/right.png")
wrongImage = PhotoImage(file="images/wrong.png")

# Canvas
# Make the card as a canvas, so we can layer the text on top of it
canvas = Canvas(width=CARD_WIDTH, height=CARD_HEIGHT)
card = canvas.create_image(CARD_WIDTH/2, CARD_HEIGHT/2, image=cardFront)
cardTitle = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
cardWord = canvas.create_text(400, CARD_HEIGHT/2, text="", font=("Arial", 68, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)


# Buttons
correctButton = Button(image=correctImage, bd=0, highlightthickness=0, command=correctButton)
correctButton.grid(column=1, row=1)

wrongButton = Button(image=wrongImage, bd=0, highlightthickness=0, command=nextCard)
wrongButton.grid(column=0, row=1)

nextCard()
window.mainloop()
