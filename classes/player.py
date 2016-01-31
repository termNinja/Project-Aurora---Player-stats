class Player:
    def __init__ (self, name, surname, stats, overall):
        self.stats = stats
        self.name = name
        self.surname = surname
        self.overall = overall
    def get_tuple_stats(self):
        return tuple(self.stats.keys())

    def __str__ (self):
        return self.name.ljust(20) + self.surname.ljust(20) + str(self.overall).ljust(4) 
