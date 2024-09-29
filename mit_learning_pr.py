#%%
import datetime

class Person(object):
    def __init__(self, name):
        """Create a person with a name."""
        self.name = name
        try:
            # Find the last space in the name to separate last name
            lastBlank = name.rindex(' ')
            self.lastName = name[lastBlank + 1:]
        except:
            # If there's no space, the whole name is the last name
            self.lastName = name
        self.birthday = None  # Birthday is initially not set

    def getName(self):
        """Return the full name of the person."""
        return self.name

    def getLastName(self):
        """Return the last name of the person."""
        return self.lastName

    def setBirthday(self, birthdate):
        """Set the birthday of the person.
        
        Args:
            birthdate: A date object representing the person's birthday.
        """
        self.birthday = birthdate

    def getAge(self):
        """Return the person's age in days."""
        if self.birthday is None:
            raise ValueError("Birthday not set")
        return (datetime.date.today() - self.birthday).days

    def __lt__(self, other):
        """Compare two people to see which comes first alphabetically."""
        if self.lastName == other.lastName:
            return self.name < other.name  # Compare full names if last names are the same
        return self.lastName < other.lastName

    def __str__(self):
        """Return the person's name as a string."""
        return self.name


# Create Person instances and demonstrate functionality
me = Person('Michael Guttag')
him = Person('Barack Hussein Obama')
her = Person('Madonna')
print(him.getLastName())
him.setBirthday(datetime.date(1961, 8, 4))  # Set birthday for 'him'
her.setBirthday(datetime.date(1958, 8, 16))  # Set birthday for 'her'
print(him.getName(), 'is', him.getAge(), 'days old')  # Print age of 'him'
print(her.getName())  # Print name of 'her'


#%%
class IntSet(object):
    """An IntSet is a collection of unique integers."""
    
    def __init__(self):
        """Create an empty set of integers."""
        self.vals = []

    def insert(self, e):
        """Add an integer to the set.
        
        Args:
            e: An integer to insert.
        """
        if e not in self.vals:  # Only add if not already in set
            self.vals.append(e)

    def member(self, e):
        """Check if an integer is in the set.
        
        Args:
            e: An integer to check.
        
        Returns:
            True if e is in the set, False otherwise.
        """
        return e in self.vals

    def remove(self, e):
        """Remove an integer from the set.
        
        Args:
            e: An integer to remove.
        
        Raises:
            ValueError: If e is not found in the set.
        """
        try:
            self.vals.remove(e)
        except ValueError:
            raise ValueError(str(e) + ' not found')  # Handle case where e is not in the set

    def getMembers(self):
        """Return a list of all integers in the set."""
        return self.vals[:]  # Return a copy of the list of integers

    def __str__(self):
        """Return a string representation of the set."""
        self.vals.sort()  # Sort the values
        result = ''
        for e in self.vals:
            result = result + str(e) + ','
        return '{' + result[:-1] + '}'  # Remove trailing comma and format

# Create an IntSet instance and demonstrate functionality
N = int(input("N="))  # Input number of elements to add to the set
c = IntSet()
c.vals = [1, 2, 3, 4]  # Initial values in the set
for i in range(N):
    a = int(input("a="))  # Input an integer to insert into the set
    c.insert(a)
    print(c.member(a))  # Check if the inserted integer is a member of the set
print(c.vals)  # Print the values in the set
print(IntSet.getMembers(c))  # Print all members of the set


#%%
class PartyAnimal:
    """A class that represents a party animal."""
    
    x = 0  # Number of parties attended
    name = ""

    def __init__(self, nam):
        """Create a PartyAnimal with a name."""
        self.name = nam
        print(self.name, "constructed")  # Confirm construction of the PartyAnimal

    def party(self):
        """Increase party count and print the current count."""
        self.x += 1
        print(self.name, "party", self.x)


class FootballFan(PartyAnimal):
    """A class that represents a football fan who is also a party animal."""
    
    points = 0  # Points scored by the fan

    def touchdown(self):
        """Increase points when a touchdown is scored and call party method."""
        self.points += 7  # Increment points for a touchdown
        self.party()  # Call the party method
        print(self.name, "points", self.points)  # Print total points scored


# Create instances of PartyAnimal and FootballFan
s = PartyAnimal("Daler")  # Create a PartyAnimal named Daler
s.party()  # Call the party method

j = FootballFan("Diyor")  # Create a FootballFan named Diyor
j.party()  # Call the party method for the FootballFan
j.touchdown()  # Simulate scoring a touchdown


#%%
import sys
print(sys.version)  # Print the current Python version
