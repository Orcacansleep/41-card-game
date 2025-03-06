import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.face_value = min(value, 10)  # As, J, Q, K bernilai 10
        
        # Format nama file kartu
        value_str = str(value).zfill(2)
        suit_str = suit.lower() 
        self.image_path = f"./cards/card_{suit_str}_{value_str}.png"
        
        # Khusus untuk kartu As (value 1)
        if value == 1:
            self.image_path = f"./cards/card_{suit_str}_01.png"
        # Khusus untuk kartu Jack (11), Queen (12), King (13)
        elif value == 11:
            self.image_path = f"./cards/card_{suit_str}_11.png"
        elif value == 12:
            self.image_path = f"./cards/card_{suit_str}_12.png"
        elif value == 13:
            self.image_path = f"./cards/card_{suit_str}_13.png"

class Game41:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game 41")
        
        # Initialize deck
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.values = list(range(1, 14))
        self.deck = []
        self.create_deck()
        
        # Players
        self.players = ['Player South', 'Player East', 'Player North', 'Player West']
        self.current_player = 0
        self.hands = {player: [] for player in self.players}
        
        # Game state
        self.discard_pile = []
        self.draw_pile = self.deck.copy()
        random.shuffle(self.draw_pile)
        self.selected_card_index = None
        self.game_over = False
        
        # Computer labels dictionary
        self.computer_labels = {}
        
        # GUI elements
        self.setup_gui()
        self.deal_initial_cards()
    
    def create_deck(self):
        for suit in self.suits:
            for value in self.values:
                self.deck.append(Card(suit, value))
    
    def setup_gui(self):
        # Main container
        self.main_container = tk.Frame(self.window)
        self.main_container.pack(expand=True, fill='both')
        self.window.geometry("800x600")
        # Create grid layout
        for i in range(3):
            self.main_container.grid_rowconfigure(i, weight=1)
            self.main_container.grid_columnconfigure(i, weight=1)
        
        # North player (Computer 2)
        self.north_frame = tk.Frame(self.main_container)
        self.north_frame.grid(row=0, column=1)
        self.setup_player_area('Player North', self.north_frame, 'horizontal')
        
        # West player (Computer 3)
        self.west_frame = tk.Frame(self.main_container)
        self.west_frame.grid(row=1, column=0)
        self.setup_player_area('Player West', self.west_frame, 'vertical')
        
        # East player (Computer 1)
        self.east_frame = tk.Frame(self.main_container)
        self.east_frame.grid(row=1, column=2)
        self.setup_player_area('Player East', self.east_frame, 'vertical')
        
        # Center area
        self.center_frame = tk.Frame(self.main_container)
        self.center_frame.grid(row=1, column=1)
        self.setup_center_area()
        
        # South player (Human)
        self.south_frame = tk.Frame(self.main_container)
        self.south_frame.grid(row=2, column=1)
        self.setup_player_area('Player South', self.south_frame, 'horizontal')
        
        # Controls for human player
        self.controls_frame = tk.Frame(self.south_frame)
        self.controls_frame.pack(pady=10)
        
        self.draw_button = tk.Button(self.controls_frame, text="Draw Card", command=self.draw_card)
        self.draw_button.pack(side=tk.LEFT, padx=5)
        
        self.discard_button = tk.Button(self.controls_frame, text="Discard Card", 
                                      command=self.discard_card, state=tk.DISABLED)
        self.discard_button.pack(side=tk.LEFT, padx=5)

    def setup_center_area(self):
        # Status display
        self.status_label = tk.Label(self.center_frame, text="Your turn", 
                                   font=('Arial', 12, 'bold'))
        self.status_label.pack(pady=10)
        
        # Score display
        self.score_label = tk.Label(self.center_frame, text="", 
                                  font=('Arial', 10))
        self.score_label.pack(pady=5)
        
        # Piles frame
        piles_frame = tk.Frame(self.center_frame)
        piles_frame.pack(pady=20)
        
        # Draw pile
        draw_frame = tk.Frame(piles_frame)
        draw_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(draw_frame, text="Draw Pile", font=('Arial', 10)).pack()
        self.draw_pile_label = tk.Label(draw_frame)
        self.draw_pile_label.pack()
        # Tambahkan label untuk jumlah kartu
        self.draw_pile_count = tk.Label(draw_frame, text="", font=('Arial', 10))
        self.draw_pile_count.pack()
        
        # Discard pile
        discard_frame = tk.Frame(piles_frame)
        discard_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(discard_frame, text="Discard Pile", font=('Arial', 10)).pack()
        self.discard_pile_label = tk.Label(discard_frame)
        self.discard_pile_label.pack()
    
    def setup_player_area(self, player, frame, orientation):
        # Player label
        label = tk.Label(frame, text=player, font=('Arial', 12, 'bold'))
        label.pack(pady=5)
        
        # Cards frame
        cards_frame = tk.Frame(frame)
        cards_frame.pack(pady=5)
        
        # Initialize card labels
        self.computer_labels[player] = []
        
        # Create card placeholders
        for _ in range(4):
            card_label = tk.Label(cards_frame)
            if orientation == 'vertical':
                card_label.pack(pady=2)
            else:
                card_label.pack(side=tk.LEFT, padx=2)
            self.computer_labels[player].append(card_label)
    
    def load_card_image(self, card):
        try:
            # Untuk kartu back/tertutup
            if card.suit == 'Back':
                image = Image.open("cards/card_back.png")
            else:
                image = Image.open(card.image_path)
            # Ukuran kartu diperkecil menjadi 50x68 (rasio yang sama)
            image = image.resize((60, 68))
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading card image: {card.image_path}")
            print(f"Error message: {str(e)}")
            return None
    
    def deal_initial_cards(self):
        # Deal 4 cards to each player
        for player in self.players:
            for _ in range(4):
                card = self.draw_pile.pop()
                self.hands[player].append(card)
        
        # Show cards
        self.update_player_hand()
        self.update_computer_hands()
        
        # Start discard pile
        first_card = self.draw_pile.pop()
        self.discard_pile.append(first_card)
        self.update_piles()
        self.update_scores()
    
    def update_player_hand(self):
        player = 'Player South'  # Human player
        current_cards = len(self.hands[player])
        
        # Ensure we have enough labels
        while len(self.computer_labels[player]) < current_cards:
            new_label = tk.Label(self.computer_labels[player][0].master)
            new_label.pack(side=tk.LEFT, padx=2)
            self.computer_labels[player].append(new_label)
        
        # Update all card labels
        for i in range(len(self.computer_labels[player])):
            if i < current_cards:
                card = self.hands[player][i]
                card_image = self.load_card_image(card)
                
                if card_image:
                    self.computer_labels[player][i].configure(image=card_image)
                    self.computer_labels[player][i].image = card_image
                    
                    # Highlight selected card
                    if i == self.selected_card_index:
                        self.computer_labels[player][i].configure(relief=tk.RAISED, borderwidth=2)
                    else:
                        self.computer_labels[player][i].configure(relief=tk.FLAT, borderwidth=0)
                        
                    self.computer_labels[player][i].bind('<Button-1>', 
                        lambda e, idx=i: self.select_card(idx))
            else:
                # Hide unused labels
                self.computer_labels[player][i].configure(image='')
                self.computer_labels[player][i].unbind('<Button-1>')
    
    def update_computer_hands(self):
        card_back = self.load_card_image(Card('Back', 0))
        if card_back:
            for player in ['Player North', 'Player East', 'Player West']:
                for label in self.computer_labels[player]:
                    label.configure(image=card_back)
                    label.image = card_back
    
    def update_piles(self):
        # Update draw pile
        if self.draw_pile:
            card_back = self.load_card_image(Card('Back', 0))
            if card_back:
                self.draw_pile_label.configure(image=card_back)
                self.draw_pile_label.image = card_back
                # Update draw pile count
                self.draw_pile_count.configure(text=f"Cards remaining: {len(self.draw_pile)}")
        else:
            self.draw_pile_label.configure(image='')
            self.draw_pile_count.configure(text="No cards remaining")
                
        # Update discard pile
        if self.discard_pile:
            top_card = self.discard_pile[-1]
            card_image = self.load_card_image(top_card)
            if card_image:
                self.discard_pile_label.configure(image=card_image)
                self.discard_pile_label.image = card_image

    def draw_card(self):
        if self.current_player == 0 and not self.game_over:  # Player's turn
            if self.draw_pile:
                card = self.draw_pile.pop()
                self.hands['Player South'].append(card)
                
                # Update all displays
                self.update_player_hand()
                self.update_piles()
                self.update_scores()
                
                # Update button states
                self.discard_button.configure(state=tk.NORMAL)
                self.draw_button.configure(state=tk.DISABLED)
    
    def discard_card(self):
        if self.selected_card_index is not None and not self.game_over:
            # Add selected card to discard pile
            discarded_card = self.hands['Player South'].pop(self.selected_card_index)
            self.discard_pile.append(discarded_card)
            
            # Reset selection
            self.selected_card_index = None
            
            # Update displays
            self.update_player_hand()
            self.update_piles()
            self.update_scores()
            
            # Update button states
            self.discard_button.configure(state=tk.DISABLED)
            self.draw_button.configure(state=tk.DISABLED)
            
            # Check for game end
            if len(self.draw_pile) == 0:
                self.end_game()
                return
            
            # Move to next player's turn
            self.current_player = (self.current_player + 1) % 4
            self.status_label.configure(text=f"{self.players[self.current_player]}'s turn")
            
            # Handle next turn
            if self.current_player != 0:
                self.window.after(1000, self.computer_turn)
            else:
                self.draw_button.configure(state=tk.NORMAL)

    def select_card(self, card_index):
        if not self.game_over and self.current_player == 0:
            self.selected_card_index = card_index
            self.update_player_hand()
            if len(self.hands['Player South']) > 4:  # Can only discard if we have more than 4 cards
                self.discard_button.configure(state=tk.NORMAL)
    
    def calculate_score(self, hand):
        # Calculate score for a hand
        suits_sum = {}
        for card in hand:
            if card.suit not in suits_sum:
                suits_sum[card.suit] = 0
            suits_sum[card.suit] += card.face_value
        return max(suits_sum.values()) if suits_sum else 0
    
    def update_scores(self):
        score_text = "Scores:\n"
        for player in self.players:
            score = self.calculate_score(self.hands[player])
            player_name = player.replace('Player ', '')  # Remove 'Player ' prefix
            score_text += f"{player_name}: {score}\n"
        self.score_label.configure(text=score_text)
    
    def computer_turn(self):
        if self.game_over:
            return
            
        current_computer = self.players[self.current_player]
        computer_hand = self.hands[current_computer]
        
        # Simulate thinking time
        self.window.after(1000, lambda: self.computer_draw_card(current_computer))
    
    def computer_draw_card(self, computer):
        # Draw a card
        if self.draw_pile:
            new_card = self.draw_pile.pop()
            self.hands[computer].append(new_card)
            self.update_piles()
            self.update_scores()
            
            # Simulate thinking time before discarding
            self.window.after(1000, lambda: self.computer_discard_card(computer))
    
    def computer_discard_card(self, computer):
        # Simple AI: Keep cards that contribute to the highest suit sum
        hand = self.hands[computer]
        suits_sum = {}
        card_contributions = {}
        
        # Calculate current contribution of each card
        for i, card in enumerate(hand):
            if card.suit not in suits_sum:
                suits_sum[card.suit] = 0
            suits_sum[card.suit] += card.face_value
            card_contributions[i] = card.face_value
            
        # Find the card that contributes least to winning
        worst_card_index = max(range(len(hand)), 
                             key=lambda i: min(card_contributions[i], 
                                             suits_sum[hand[i].suit] - card_contributions[i]))
        
        # Discard the worst card
        discarded_card = hand.pop(worst_card_index)
        self.discard_pile.append(discarded_card)
        self.update_piles()
        self.update_scores()
        
        # Check for game end
        if len(self.draw_pile) == 0:
            self.end_game()
            return
            
        # Move to next player
        self.current_player = (self.current_player + 1) % 4
        self.status_label.configure(text=f"{self.players[self.current_player]}'s turn")
        
        if self.current_player == 0:
            self.draw_button.configure(state=tk.NORMAL)
        else:
            self.window.after(1000, self.computer_turn)
    def end_game(self):
        self.game_over = True
        winners, max_score = self.check_winner()
        
        # Prepare winner message
        if len(winners) == 1:
            message = f"Game Over!\n{winners[0]} wins with score {max_score}!"
        else:
            message = f"Game Over!\nTie between {', '.join(winners)} with score {max_score}!"
            
        # Show game over message
        self.status_label.configure(text=message)
        messagebox.showinfo("Game Over", message)
        
        # Disable buttons
        self.draw_button.configure(state=tk.DISABLED)
        self.discard_button.configure(state=tk.DISABLED)
        
    def check_winner(self):
        # Check if anyone has won
        scores = {}
        for player in self.players:
            scores[player] = self.calculate_score(self.hands[player])
        
        max_score = max(scores.values())
        winners = [player for player, score in scores.items() if score == max_score]
        
        return winners, max_score
        
    def run(self):
        self.window.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = Game41()
    game.run()