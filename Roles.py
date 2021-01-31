
class Role():

    def __init__(self, instanceOwner: int):

        self.instanceOwner = instanceOwner
        self.status = "Alive"

    def NightAction(self, target):

        return target

class Mafia(Role):

    pass

class Innocent(Role):

    pass

class NightImmune():

    pass

class Unique():

    pass

class DayActor():

    def DayAction(self, target: Role) -> Role:

        return target

#Innocent Roles

class Investigator(Innocent):

    def __init__(self, instanceOwner):

        super().__init__(instanceOwner)
        self.roleName = "Investigator"
        self.roleSub = "Investigative"
        self.investDesc = "This person works detailed, they must be an Investigator"

class Sheriff(Innocent):

    def __init__(self, instanceOwner):

       super().__init__(instanceOwner)
       self.roleName = "Sheriff"
       self.roleSub = "Investigative"
       self.investDesc = "This person has a strong sense of justice, they must be a Sheriff or a Jailor"

class Doctor(Innocent):

    def __init__(self, instanceOwner):
    
        super().__init__(instanceOwner)
        self.roleName = "Doctor"
        self.roleSub = "Support"
        self.investDesc = "This person owns a lot of sharp object, they must be a Doctor or Serial Killer"

class Bodyguard(Innocent):

    def __init__(self, instanceOwner):

        super().__init__(instanceOwner)
        self.roleName = "Bodyguard"
        self.roleSub = "Support"
        self.investDesc = "This person is extremely loyal, they must be a Bodyguard"

class Vigilante(Innocent):

    def __init__(self, instanceOwner):
    
        super().__init__(instanceOwner)
        self.roleName = "Vigilante"
        self.roleSub = "Killing"
        self.investDesc = "This person owns a lot of firearms, they must be a Vigilante or a Mafioso"

class Jailor(Innocent, Unique, DayActor):

    def __init__(self, instanceOwner):
        
        super().__init__(instanceOwner)
        self.roleName = "Jailor"
        self.roleSub = "Killing"
        self.investDesc = "This person has a strong sense of justice, they must be a Sheriff or a Jailor"

#Mafia Roles

class Godfather(Mafia, NightImmune, Unique):

    def __init__(self, instanceOwner):
    
        super().__init__(instanceOwner)
        self.roleName = "Godfather"
        self.roleSub = "Killing"
        self.investDesc = "This person is very good at managing people, they must be a Mayor or Godfather"

class Mafioso(Mafia):

    def __init__(self, instanceOwner):
    
        super().__init__(instanceOwner)
        self.roleName = "Mafioso"
        self.roleSub = "Killing"
        self.investDesc = "This person owns a lot of firearms, they must be a Vigilante or a Mafioso"

class Consort(Mafia):

    def __init__(self, instanceOwner):
    
        super().__init__(instanceOwner)
        self.roleName = "Consort"
        self.roleSub = "Support"
        self.investDesc = "This person likes to interrupt people, they must be an Escort or a Consort"

#Neutral Roles

class SerialKiller(Role, NightImmune):

    def __init__(self, instanceOwner):
        
        super().__init__(instanceOwner)
        self.roleName = "Serial Killer"
        self.roleSub = "Killing"
        self.investDesc = "This person owns a lot of sharp tools, they must be a Doctor or Serial Killer"
