class Action:
    def __init__(self, index, cost, benefit):
        self.index = index + 1
        self.cost = cost
        self.benefit = benefit


class Wallet:
    def __init__(self, actions, max_price):
        self.actions = actions if actions else []
        self.max_price = max_price

    @property
    def total_cost(self):
        return sum([action.cost for action in self.actions])

    @property
    def gain(self):
        return sum([action.cost * action.benefit for action in self.actions])

    @property
    def actions_index(self):
        return [action.index for action in self.actions]

    def has_place_for(self, action):
        return False if self.total_cost + action.cost > self.max_price else True


def find_valid_wallets(actions, max_price):
    valid_wallets = [Wallet([], max_price)]
    for action in actions:
        new_wallets = []
        for wallet in valid_wallets:
            if wallet.has_place_for(action):
                new_actions = wallet.actions.copy()
                new_actions.append(action)
                new_wallets.append(Wallet(new_actions, max_price))
        valid_wallets += new_wallets
    return valid_wallets


def find_best_wallet(wallets):
    best_wallets = sorted(wallets, key=lambda wallet: wallet.gain, reverse=True)
    return best_wallets[0]


def main():
    available_actions = [
        {"cost": 20, "benefit": 0.05},
        {"cost": 30, "benefit": 0.1},
        {"cost": 50, "benefit": 0.15},
        {"cost": 70, "benefit": 0.2},
        {"cost": 60, "benefit": 0.17},
        {"cost": 80, "benefit": 0.25},
        {"cost": 22, "benefit": 0.07},
        {"cost": 26, "benefit": 0.11},
        {"cost": 48, "benefit": 0.13},
        {"cost": 34, "benefit": 0.27},
        {"cost": 42, "benefit": 0.17},
        {"cost": 110, "benefit": 0.09},
        {"cost": 38, "benefit": 0.23},
        {"cost": 14, "benefit": 0.01},
        {"cost": 18, "benefit": 0.03},
        {"cost": 8, "benefit": 0.08},
        {"cost": 4, "benefit": 0.12},
        {"cost": 10, "benefit": 0.14},
        {"cost": 24, "benefit": 0.21},
        {"cost": 114, "benefit": 0.18}
    ]
    actions = [Action(i, action["cost"], action["benefit"]) for (i, action) in enumerate(available_actions)]
    best_wallet = find_best_wallet(find_valid_wallets(actions, 500))
    print(best_wallet.actions_index, best_wallet.total_cost, round(best_wallet.gain, 2))


if __name__ == "__main__":
    main()
