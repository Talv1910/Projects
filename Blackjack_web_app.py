import streamlit as st
import random

logo = r"""
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ / 
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   <  
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if sum(cards) > 21 and 11 in cards:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def final_score(u_score, c_score):
    if u_score > 21:
        return "You went over. You lose 😞"
    elif c_score > 21:
        return "Computer went over. You win 🎉"
    elif u_score == c_score:
        return "Draw 🤝"
    elif u_score == 0:
        return "Blackjack! You win 🂡🎉"
    elif c_score == 0:
        return "Computer has Blackjack! You lose 😞"
    elif u_score > c_score:
        return "You win 🎉"
    else:
        return "You lose 😞"

# Initialize state
if "user_cards" not in st.session_state:
    st.session_state.user_cards = []
    st.session_state.computer_cards = []
    st.session_state.game_over = False
    st.session_state.show_result = False
    st.session_state.hit = False

st.title("🃏 Blackjack")
st.text(logo)

# Start new game
if st.button("🔁 Start New Game"):
    st.session_state.user_cards = [deal_card(), deal_card()]
    st.session_state.computer_cards = [deal_card(), deal_card()]
    st.session_state.game_over = False
    st.session_state.show_result = False
    st.session_state.hit = False

# Show current state
if st.session_state.user_cards:
    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)

    st.write(f"**Your cards:** {st.session_state.user_cards} | **Score:** {user_score}")
    st.write(f"**Computer's first card:** {st.session_state.computer_cards[0]}")

    if not st.session_state.game_over:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🃏 Hit"):
                st.session_state.hit = True
        with col2:
            if st.button("✋ Stand"):
                st.session_state.game_over = True
                st.session_state.show_result = True

    # Process "Hit" action
    if st.session_state.hit:
        st.session_state.user_cards.append(deal_card())
        st.session_state.hit = False
        if calculate_score(st.session_state.user_cards) > 21:
            st.session_state.game_over = True
            st.session_state.show_result = True

# After game ends
if st.session_state.game_over and st.session_state.show_result:
    while calculate_score(st.session_state.computer_cards) != 0 and calculate_score(st.session_state.computer_cards) < 17:
        st.session_state.computer_cards.append(deal_card())

    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)

    st.write("---")
    st.write(f"**Your final hand:** {st.session_state.user_cards} | Score: {user_score}")
    st.write(f"**Computer's final hand:** {st.session_state.computer_cards} | Score: {computer_score}")
    st.success(final_score(user_score, computer_score))
