class House:

    def __init__(self,house_number,seeds,seeds_number) -> None:
        self.house_number =  house_number
        self.seeds = seeds
        self.seeds_number = seeds_number


    def get_house(self):
        return {
            'house_number': self.house_number,
            'seeds':self.seeds,
            'seeds_number':self.seeds_number
        }