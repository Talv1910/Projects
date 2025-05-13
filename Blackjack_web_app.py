import streamlit as st
import random

# Function to deal a card
def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

# Calculate score
def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack
    if sum(cards) > 21 and 11 in cards:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

# Game result
def final_result(user_score, computer_score):
    if user_score > 21:
        return "You went over. You lose 😞"
    elif computer_score > 21:
        return "Computer went over. You win 🎉"
    elif user_score == computer_score:
        return "It's a draw 🤝"
    elif user_score == 0:
        return "Blackjack! You win 🂡🎉"
    elif computer_score == 0:
        return "Computer has Blackjack! You lose 😞"
    elif user_score > computer_score:
        return "You win 🎉"
    else:
        return "You lose 😞"

# Start of Streamlit app
st.title("🃏 Blackjack Game")
st.write("Play Blackjack right in your browser!")

# Initialize session state
if "user_cards" not in st.session_state:
    st.session_state.user_cards = []
    st.session_state.computer_cards = []
    st.session_state.game_over = False

# New game
if st.button("Start New Game"):
    st.session_state.user_cards = [deal_card(), deal_card()]
    st.session_state.computer_cards = [deal_card(), deal_card()]
    st.session_state.game_over = False

# Show cards
if st.session_state.user_cards:
    user_score = calculate_score(st.session_state.user_cards)
    comp_first = st.session_state.computer_cards[0]

    st.write(f"**Your cards:** {st.session_state.user_cards}  | **Score:** {user_score}")
    st.write(f"**Computer's first card:** {comp_first}")

    # If not game over
    if not st.session_state.game_over:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hit"):
                st.session_state.user_cards.append(deal_card())
                if calculate_score(st.session_state.user_cards) > 21:
                    st.session_state.game_over = True
        with col2:
            if st.button("Stand"):
                st.session_state.game_over = True

# After game ends
if st.session_state.game_over and st.session_state.user_cards:
    user_score = calculate_score(st.session_state.user_cards)
    computer_cards = st.session_state.computer_cards

    # Computer plays
    while calculate_score(computer_cards) != 0 and calculate_score(computer_cards) < 17:
        computer_cards.append(deal_card())

    computer_score = calculate_score(computer_cards)

    st.write(f"**Your final hand:** {st.session_state.user_cards} | **Final score:** {user_score}")
    st.write(f"**Computer's hand:** {computer_cards} | **Final score:** {computer_score}")

    result = final_result(user_score, computer_score)
    st.success(result)
