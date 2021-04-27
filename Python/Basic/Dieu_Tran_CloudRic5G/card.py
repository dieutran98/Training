from util.singleton import Singleton


class Card:
    def __init__(self, name:str=None, point = 0) -> None:
        self.name = name.upper()
        self.point = point

    def __lt__(self, another_card):
        return self.point < another_card.point
    
    def __gt__(self, anothercard):
        return self.point > anothercard.point
    
    def __eq__(self, anohtercard):
        return self.point == anohtercard.point
    
    def __str__(self):
        return f'< name: {self.name} point: {self.point} >'

class CardCreate(metaclass = Singleton):
    suites = (('spade', 's'),
             ('club', 'c'), 
             ('diamond', 'd'), 
             ('heart', 'h'))
    groups = ('a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k')
    greatest = (('black joker', 'bj'), 
                ('red joker', 'rj'))
    
    
    def _checknset(self, name:str) -> bool:
        if not isinstance(name,str):
            raise ValueError(f'your card name is wrong, card_name: {name}. It should have format "Suites-Groups" or "Black Joker"')
        name = name.lower()
        #check if name is greatest
        for gr in self.greatest:
            if name in gr:
                self.point = 100
                self.name = name
                return True
        #check if name is combined of suites and group
        try:
            suite, group = name.split('-')
        except ValueError:
            raise ValueError(f'your card name is wrong, card_name: {name}. It should have format "Suites-Groups" or "Black Joker"')
            
        #check suit
        for i, s in enumerate(self.suites):
            if suite in s:
                self.point = 13*(i+1)
                break
        else:
            raise ValueError(f'error the card name is not in suites, suite = "{suite}"')
        #check group
        for i, gs in enumerate(self.groups):
            if group in gs:
                self.point += i+1
                self.name = name
                return True
        else:
            raise ValueError(f'error the card name is not in group, group = "{group}"')
    
    def __call__(self, name: str) -> Card:
        if self._checknset(name):
            return Card(self.name,self.point)

if __name__ == '__main__'  :
    name = input('enter your card name: ')
    testobj = CardCreate().__call__(name)
    # name = input('enter your card name: ')
    # testobj1 = CardBuilder().card_gen(name)
