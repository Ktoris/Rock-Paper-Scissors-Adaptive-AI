import random
from collections import Counter, deque

# Global state variables
history = []
max_results = 15
lost = deque(maxlen=max_results)
after_lost = deque(maxlen=max_results)
won = deque(maxlen=max_results)
after_won = deque(maxlen=max_results)
tie = deque(maxlen=max_results)
after_tie = deque(maxlen=max_results)
current_state = ""
cycle_length = 6
winloss = 10

strategy_scores = {
    'strategy_1': deque(maxlen=winloss),
    'strategy_4': deque(maxlen=winloss),
    'random': deque(maxlen=winloss)
}

last_strategy_used = None
cycle_detected_last_turn = False
cycle_just_failed = False
player_score = 0
ai_score = 0


def reset_game():
    """Reset all game state variables"""
    global history, lost, after_lost, won, after_won, tie, after_tie
    global current_state, strategy_scores, last_strategy_used
    global cycle_detected_last_turn, cycle_just_failed, player_score, ai_score

    history = []
    lost = deque(maxlen=max_results)
    after_lost = deque(maxlen=max_results)
    won = deque(maxlen=max_results)
    after_won = deque(maxlen=max_results)
    tie = deque(maxlen=max_results)
    after_tie = deque(maxlen=max_results)
    current_state = ""
    strategy_scores = {
        'strategy_1': deque(maxlen=winloss),
        'strategy_4': deque(maxlen=winloss),
        'random': deque(maxlen=winloss)
    }
    last_strategy_used = None
    cycle_detected_last_turn = False
    cycle_just_failed = False
    player_score = 0
    ai_score = 0


def get_strategy_total(strategy_name):
    scores = strategy_scores[strategy_name]
    if len(scores) == 0:
        return 0
    return sum(scores)


def get_best_strategy():
    best_strategy = None
    best_score = float('-inf')

    for strategy_name, scores in strategy_scores.items():
        if len(scores) > 0:
            total = sum(scores)
            if total > best_score:
                best_score = total
                best_strategy = strategy_name

    return best_strategy if best_strategy else 'random'


def evaluate_move(ai_move, player_move):
    if ai_move == player_move:
        return 'tie'
    elif (ai_move == "P" and player_move == "R") or (ai_move == "S" and player_move == "P") or (
            ai_move == "R" and player_move == "S"):
        return 'win'
    else:
        return 'loss'


def record_result(strategy_name, result):
    score_map = {'win': 1, 'tie': 0, 'loss': -1}
    strategy_scores[strategy_name].append(score_map[result])


def calculate():
    lost_respective_r = []
    lost_respective_p = []
    lost_respective_s = []
    for i in range(len(lost)):
        if lost[i] == "R":
            lost_respective_r.append(after_lost[i])
        elif lost[i] == "P":
            lost_respective_p.append(after_lost[i])
        elif lost[i] == "S":
            lost_respective_s.append(after_lost[i])

    won_respective_r = []
    won_respective_p = []
    won_respective_s = []
    for i in range(len(won)):
        if won[i] == "R":
            won_respective_r.append(after_won[i])
        elif won[i] == "P":
            won_respective_p.append(after_won[i])
        elif won[i] == "S":
            won_respective_s.append(after_won[i])

    tie_respective_r = []
    tie_respective_p = []
    tie_respective_s = []
    for i in range(len(tie)):
        if tie[i] == "R":
            tie_respective_r.append(after_tie[i])
        elif tie[i] == "P":
            tie_respective_p.append(after_tie[i])
        elif tie[i] == "S":
            tie_respective_s.append(after_tie[i])
    return lost_respective_r, lost_respective_p, lost_respective_s, tie_respective_r, tie_respective_p, tie_respective_s, won_respective_r, won_respective_p, won_respective_s


def counter_move(move):
    if move == "R":
        return "P"
    elif move == "P":
        return "S"
    elif move == "S":
        return "R"
    else:
        return random.choice(["R", "P", "S"])


def strategy_1():
    global lost_respective_r, lost_respective_p, lost_respective_s
    global tie_respective_r, tie_respective_p, tie_respective_s
    global won_respective_r, won_respective_p, won_respective_s

    previous_player_move = history[-1] if len(history) >= 1 else None

    if current_state == "Lost":
        if previous_player_move == "R":
            if lost_respective_r:
                computer_play = counter_move(Counter(lost_respective_r).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])
        elif previous_player_move == "P":
            if lost_respective_p:
                computer_play = counter_move(Counter(lost_respective_p).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])
        else:
            if lost_respective_s:
                computer_play = counter_move(Counter(lost_respective_s).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])

    elif current_state == "Won":
        if previous_player_move == "R":
            if won_respective_r:
                computer_play = counter_move(Counter(won_respective_r).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])
        elif previous_player_move == "P":
            if won_respective_p:
                computer_play = counter_move(Counter(won_respective_p).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])
        else:
            if won_respective_s:
                computer_play = counter_move(Counter(won_respective_s).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])

    else:
        if previous_player_move == "R":
            if tie_respective_r:
                computer_play = counter_move(Counter(tie_respective_r).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])
        elif previous_player_move == "P":
            if tie_respective_p:
                computer_play = counter_move(Counter(tie_respective_p).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])
        else:
            if tie_respective_s:
                computer_play = counter_move(Counter(tie_respective_s).most_common(1)[0][0])
            else:
                computer_play = random.choice(["R", "P", "S"])
    return computer_play


def detect_cycle(hist):
    for cycle_len in range(min(cycle_length, len(hist) // 2), 1, -1):
        recent = hist[-cycle_len:]
        previous = hist[-2 * cycle_len:-cycle_len]

        if recent == previous:
            cycle_start_index = 0
            for start in range(len(hist) - 2 * cycle_len + 1):
                matches = True
                for pos in range(start, len(hist)):
                    expected_move = hist[start + (pos - start) % cycle_len]
                    if hist[pos] != expected_move:
                        matches = False
                        break

                if matches:
                    cycle_start_index = start
                    break

            actual_cycle = hist[cycle_start_index:cycle_start_index + cycle_len]
            return actual_cycle, cycle_start_index

    return None, None


def predict_next(hist):
    cycle, cycle_start = detect_cycle(hist)
    if cycle:
        position_in_cycle = (len(hist) - cycle_start) % len(cycle)
        predicted = cycle[position_in_cycle]
        return predicted
    else:
        return None


def strategy_4():
    previous_player_move = history[-1] if len(history) >= 1 else None

    if current_state == "Won":
        s4_play = counter_move(previous_player_move)
    elif current_state == "Lost":
        s4_play = previous_player_move
    else:
        s4_play = random.choice(["R", "S", "P"])
    return s4_play


def get_random_move():
    return random.choice(["R", "P", "S"])


def play_turn(player_move):
    """
    Process one turn of the game
    Returns: dict with game state information
    """
    global current_state, last_strategy_used, cycle_just_failed
    global player_score, ai_score
    global lost_respective_r, lost_respective_p, lost_respective_s
    global tie_respective_r, tie_respective_p, tie_respective_s
    global won_respective_r, won_respective_p, won_respective_s

    previous_player_move = history[-1] if len(history) >= 1 else None

    # Update tracking deques
    if current_state == "Lost":
        lost.append(previous_player_move)
        after_lost.append(player_move)
    elif current_state == "Won":
        won.append(previous_player_move)
        after_won.append(player_move)
    elif current_state == "Tie":
        tie.append(previous_player_move)
        after_tie.append(player_move)

    # Simulate all strategies
    simulated_moves = {}
    if previous_player_move:
        (lost_respective_r, lost_respective_p, lost_respective_s,
         tie_respective_r, tie_respective_p, tie_respective_s,
         won_respective_r, won_respective_p, won_respective_s) = calculate()

        simulated_moves['strategy_1'] = strategy_1()
        simulated_moves['strategy_4'] = strategy_4()
        simulated_moves['random'] = get_random_move()

        for strategy_name, move in simulated_moves.items():
            result = evaluate_move(move, player_move)
            record_result(strategy_name, result)

    # Select strategy
    if cycle_just_failed:
        predicted_player_move = None
        cycle_just_failed = False
    else:
        predicted_player_move = predict_next(history)

    strategy_info = {}
    if predicted_player_move:
        computer_play = counter_move(predicted_player_move)
        strategy_used = 'cycle'
        strategy_info['cycle_detected'] = True
        strategy_info['predicted_cycle'] = predicted_player_move
    else:
        strategy_info['cycle_detected'] = False
        if previous_player_move:
            best_strategy = get_best_strategy()
            strategy_info['best_strategy'] = best_strategy

            if best_strategy == 'strategy_1':
                lost_respective_r, lost_respective_p, lost_respective_s, \
                    tie_respective_r, tie_respective_p, tie_respective_s, \
                    won_respective_r, won_respective_p, won_respective_s = calculate()
                computer_play = strategy_1()
                strategy_used = 'strategy_1'
            elif best_strategy == 'strategy_4':
                computer_play = strategy_4()
                strategy_used = 'strategy_4'
            else:
                computer_play = random.choice(["R", "P", "S"])
                strategy_used = 'random'
        else:
            computer_play = random.choice(["R", "P", "S"])
            strategy_used = 'random'
            strategy_info['best_strategy'] = 'random'

    last_strategy_used = strategy_used
    history.append(player_move)

    # Evaluate result
    result = None
    if player_move == "R":
        if computer_play == "R":
            current_state = "Tie"
            result = 'tie'
        elif computer_play == "P":
            current_state = "Lost"
            ai_score += 1
            result = 'win'
        else:
            current_state = "Won"
            player_score += 1
            result = 'loss'
    elif player_move == "P":
        if computer_play == "P":
            current_state = "Tie"
            result = 'tie'
        elif computer_play == "R":
            player_score += 1
            current_state = "Won"
            result = 'loss'
        else:
            current_state = "Lost"
            ai_score += 1
            result = 'win'
    elif player_move == "S":
        if computer_play == "R":
            current_state = "Lost"
            ai_score += 1
            result = 'win'
        elif computer_play == "P":
            current_state = "Won"
            player_score += 1
            result = 'loss'
        else:
            current_state = "Tie"
            result = 'tie'

    if last_strategy_used == 'cycle':
        if result == 'loss':
            cycle_just_failed = True

    # Prepare return data
    return {
        'computer_play': computer_play,
        'result': result,
        'current_state': current_state,
        'strategy_used': strategy_used,
        'strategy_info': strategy_info,
        'player_score': player_score,
        'ai_score': ai_score,
        'strategy_scores': {name: sum(scores) if len(scores) > 0 else 0
                            for name, scores in strategy_scores.items()}
    }