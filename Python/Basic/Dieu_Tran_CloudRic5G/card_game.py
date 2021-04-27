from card import Card, CardCreate
from sys import exit
from random import shuffle
from util.my_logs import get_logger
#------------------------DEBUG MODE---------------------
show_console = False
if show_console:
    console_level = 20
else:
    console_level = None
log = get_logger('card_game_log',console_level,10)
# log.disabled =False
#-------------------------------------------------------
card_create = CardCreate()
class Fac:
    def __init__(self) -> None:
        self._card = None
        self._kind = None
    
    @property
    def card(self) -> Card:
        return self._card
    
    @card.setter
    def card(self, card:Card):
        self._card = card

    def __str__(self):
        return f'{self._kind} card created {self.card}'
        
class TheHouse(Fac):
    def __init__(self) -> None:
        self._kind = 'The House'
    
class Player(Fac):
    def __init__(self, point = 60) -> None:
        self.point = point
        self._kind = 'Player'
    
    def __str__(self):
        stri = super().__str__() [:-1]
        stri += f'player point: {self.point} >'
        return stri
    
    def guess_card(self)->str:
        return input('your guess?')
    
class CardGame:
    def __init__(self, player: Player, the_house: TheHouse, reward = 20, pay =25) -> None:
        if self._check_property(player, the_house, reward, pay):    
            self.player = player
            self.the_house = the_house
            self.reward = reward
            self.pay = pay
            self.card = [suite[0] +'-'+ group for suite in CardCreate.suites for group in CardCreate.groups]
            for greatest in CardCreate.greatest:
                self.card.append(greatest[0])
    
    def shuffling(self):
        shuffle(self.card)
    
    def valid_guess(self, guess:str):
        guess = guess.lower()
        if guess in ('higher', 'h', 'y'):
            return True
        elif guess in ('lower', 'l', 'n'):
            return False
        else:
            raise ValueError(f'the anwser is invalid, anwser should be "higher" or "lower"')
    
    def continue_game(self, stri:str):
        stri = stri.lower()
        if stri in ('yes', 'y'):
            return True
        elif stri in ('no', 'n'):
            return False
        else:
            raise ValueError(f'the anwser is invalid, anwser should be "yes" or "no"')
    
    def quit_game(self):
        self.player.point += self.reward
    
    def game_over(self):
        print('game over!')
        print(f'your point: {self.player.point}')
        
    @property
    def iswin(self):
        if self.reward >= 1000:
            return True
        return False
    
    @property
    def islose(self, lose_condition = 30):
        if self.player.point < lose_condition:
            return True
        return False
    
    def _check_property(self, player, the_house, reward, pay) -> bool:
        if not isinstance(player, Player):
            raise ValueError(f'the "player" variable must be "Player type", current player:{type(player)} ')
        if not isinstance(the_house, TheHouse):
            raise ValueError(f'the "the_house" variable must be "TheHouse type", current the_house:{type(the_house)} ')
        if not isinstance(reward, int):
            raise ValueError(f'the "reward" variable must be "int type", current reward:{type(reward)} ')
        if not isinstance(pay, int):
            raise ValueError(f'the "pay" variable must be "int type", current pay:{type(pay)} ')
        return True
    
    def play_card(self):
        self.player.point -= self.pay
        while(1):
            self.shuffling()
            try:
                self.player.card = card_create(self.card[53])
                self.the_house.card = card_create(self.card[52])
                log.debug(f'{self.the_house}')
                log.debug(f'{self.player}')
            except ValueError as e:
                log.error(e)
                exit()
            print(f'The House card: {self.the_house.card.name}')
            while True:
                try:
                    guess = self.player.guess_card()
                    if self.valid_guess(guess):
                        print(f'player card: {self.player.card.name}')
                        if self.player.card < self.the_house.card:
                            print('you guess wrong')
                            log.debug('player guess wrong')
                            return
                    else:
                        print(f'player card: {self.player.card.name}')
                        if self.player.card > self.the_house.card:
                            print('you guess wrong')
                            log.debug('player guess wrong')
                            return
                    break
                except ValueError as e:
                    print(e)
                    log.warning(f'{e} -- player guess: {guess}')
            if self.iswin:
                print('you won the game')
                log.debug('player won the game')
                self.player.point += self.reward
                return 
            while 1:
                try:
                    answer = input('Continue? (y/n)')
                    if not self.continue_game(answer):
                        self.quit_game()
                        return
                    break
                except ValueError as e:
                    print(e)
                    log.warning(f'{e} --- anwser: {answer}')
            self.reward *=2
            print('===============================')
    
    def reset(self):
        self.reward = 20
if __name__ == '__main__':
    card_game = CardGame(Player(), TheHouse())
    while(1):
        try:
            if not card_game.islose:
                card_game.play_card()
                while 1:
                    try:
                        answer = input('start another match? (y/n)')
                        if not card_game.continue_game(answer):
                            log.info('end game')
                            card_game.game_over()
                            exit()
                        else:
                            card_game.reset()
                            break
                    except ValueError as e:
                        print(e)
                        log.warning(f'{e} --- anwser: {answer}')
            else:
                log.info('player have not engouh point to play')
                print('you do not have enough point to play')
                break
        except KeyboardInterrupt:
            log.info('player press ctrl+c, end game')
            card_game.game_over()
            break