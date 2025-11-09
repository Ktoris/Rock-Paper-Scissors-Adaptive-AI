import streamlit as st
import game_logic

st.set_page_config(page_title="Rock Paper Scissors AI", layout="wide")

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.last_result = None
    st.session_state.last_ai_move = None
    st.session_state.last_player_move = None

st.markdown("""
<style>
    .big-emoji {
        font-size: 120px;
        text-align: center;
        margin: 20px;
    }
    .result-text {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    .win-text { color: #28a745; }
    .lose-text { color: #dc3545; }
    .tie-text { color: #ffc107; }
    .strategy-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #e7f3ff;
        margin: 10px 0;
    }
    .score-display {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
    .player-icon {
        font-size: 60px;
        text-align: center;
        margin: 10px 0;
    }
    .move-display {
        font-size: 80px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


st.title("🎮 Rock Paper Scissors AI")
st.markdown("### Play against an adaptive AI that learns your patterns!")

st.sidebar.header("📊 Strategy Performance")
if st.session_state.game_started:
    scores = game_logic.strategy_scores
    for strategy_name in ['strategy_1', 'strategy_4', 'random']:
        if len(scores[strategy_name]) > 0:
            total = sum(scores[strategy_name])
            st.sidebar.metric(
                label=f"{strategy_name.replace('_', ' ').title()}",
                value=f"{total:+d}",
                delta=f"Last {len(scores[strategy_name])} games"
            )
        else:
            st.sidebar.metric(
                label=f"{strategy_name.replace('_', ' ').title()}",
                value="0"
            )
else:
    st.sidebar.info("Strategy scores will appear after playing a few rounds")

st.sidebar.markdown("---")
st.sidebar.header("🎯 Current Strategy")

if st.session_state.game_started and game_logic.last_strategy_used:
    strategy_display = game_logic.last_strategy_used.replace('_', ' ').title()
    cycle_detected = game_logic.cycle_detected_last_turn

    if cycle_detected or game_logic.last_strategy_used == 'cycle':
        st.sidebar.markdown("**🔄 Cycle Detection**")
    else:
        st.sidebar.markdown(f"**{strategy_display}**")
else:
    st.sidebar.markdown("*No strategy yet*")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Game", use_container_width=True):
    game_logic.reset_game()
    st.session_state.game_started = False
    st.session_state.last_result = None
    st.session_state.last_ai_move = None
    st.session_state.last_player_move = None
    st.rerun()

move_emoji = {"R": "🪨", "P": "📄", "S": "✂️"}

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("<div class='player-icon'>🦲</div>", unsafe_allow_html=True)
    if st.session_state.last_player_move:
        st.markdown(f"<div class='move-display'>{move_emoji[st.session_state.last_player_move]}</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<div class='move-display'>❓</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-display'>{game_logic.player_score}</div>", unsafe_allow_html=True)

with col2:
    if st.session_state.last_result:
        result_text = st.session_state.last_result
        if result_text == "win":
            st.markdown("<div class='result-text lose-text'>AI WINS!</div>", unsafe_allow_html=True)
        elif result_text == "loss":
            st.markdown("<div class='result-text win-text'>YOU WIN!</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-text tie-text'>TIE!</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-text' style='color: #666;'>VS</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='player-icon'>🤖</div>", unsafe_allow_html=True)
    if st.session_state.last_ai_move:
        st.markdown(f"<div class='move-display'>{move_emoji[st.session_state.last_ai_move]}</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<div class='move-display'>❓</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-display'>{game_logic.ai_score}</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Make Your Move")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪨", use_container_width=True, key="rock", help="Rock"):
        result = game_logic.play_turn("R")
        st.session_state.game_started = True
        st.session_state.last_result = result['result']
        st.session_state.last_ai_move = result['computer_play']
        st.session_state.last_player_move = "R"
        st.rerun()
    st.markdown("<h2 style='text-align: center;'>Rock</h2>", unsafe_allow_html=True)

with col2:
    if st.button("📄", use_container_width=True, key="paper", help="Paper"):
        result = game_logic.play_turn("P")
        st.session_state.game_started = True
        st.session_state.last_result = result['result']
        st.session_state.last_ai_move = result['computer_play']
        st.session_state.last_player_move = "P"
        st.rerun()
    st.markdown("<h2 style='text-align: center;'>Paper</h2>", unsafe_allow_html=True)

with col3:
    if st.button("✂️", use_container_width=True, key="scissors", help="Scissors"):
        result = game_logic.play_turn("S")
        st.session_state.game_started = True
        st.session_state.last_result = result['result']
        st.session_state.last_ai_move = result['computer_play']
        st.session_state.last_player_move = "S"
        st.rerun()
    st.markdown("<h2 style='text-align: center;'>Scissors</h2>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
**How it works:**
- The AI uses multiple strategies 
- It tracks the performance for strategies and picks the best one
- If a pattern is detected it exploits it until the pattern switches
- The best performing strategy is automatically selected
""")