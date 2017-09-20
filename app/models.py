"""
Models for Paranuara government data
------------------------------------

We include models for given collections, companies and people. As it is customary,
the single noun naming convention is used.
"""

from mongoengine import *
import os

HOST=os.environ['MONGODB_HOST']
connect(db='paranuara', host=HOST, connect=False)

class Company(Document):
    """Mongo model for companies collection."""
    meta = {'collection': 'companies'}

    index = IntField(required=True)
    company = StringField(required=True)

    def employees(self):
        """Find all registered persons linked to this company."""
        return Person.objects(company_id=self.index)

    def __str__(self):
        """Helper for pretty console output if needed"""
        return str(dict(index=self.index, company=self.company))

class FriendRef(EmbeddedDocument):
    """Holds a friend reference."""
    index = IntField(required=True)

    def __str__(self):
        """Helper for pretty console output if needed"""
        return str(dict(index=self.index))

class Person(Document):
    """Mongo model for people collection."""
    meta = {'collection': 'people'}

    index = IntField(required=True)
    has_died = BooleanField(required=True)
    eyeColor = StringField(required=True)
    name = StringField(required=True)
    age = IntField(required=True)
    address = StringField(required=True)
    phone = StringField(required=True)
    friends = EmbeddedDocumentListField(FriendRef)
    favouriteFood = ListField(StringField())
    tags = ListField(StringField())
    company_id = IntField(required=True)
    registered = StringField()
    greeting = StringField()
    email = EmailField()
    about = StringField()
    guid = StringField()
    balance = DecimalField()
    picture = URLField()
    gender = StringField(required=True, choices=['male', 'female'])

    def friend_indexes(self):
        """Return indexes for friend from associated FriendRefs"""
        # note: in `people` collection there are circular references, i.e. a person
        # is a friend with him/herself
        return [friend_ref.index for friend_ref in self.friends]

    def special_common_friends_with(self, other_person):
        common_friends = list(filter(lambda p: p in other_person.friend_indexes(),
                                     self.friend_indexes()))
        special_friends = Person.objects(index__in=common_friends)(eyeColor='brown')(has_died=False)
        special_friends = list(map(lambda p: p.as_dict(), special_friends))
        return dict(person=self.as_dict(),
                    other_person=other_person.as_dict(),
                    special_friends=special_friends)

    def diet_preferences(self):
        fruits = FoodClass.objects(food__in=self.favouriteFood)(kind='fruit')
        vegetables = FoodClass.objects(food__in=self.favouriteFood)(kind='vegetable')
        return dict(username=self.name,
                    age=self.age,
                    fruits=[i.food for i in fruits],
                    vegetables=[i.food for i in vegetables])

    def __str__(self):
        """Helper to nice console output if needed"""
        return str(dict(index=self.index, name=self.name))

    def as_dict(self):
        """Helper to render a person as dict with basic attributes"""
        return dict(name=self.name, age=self.age, address=self.address, phone=self.phone)

class FoodClass(Document):
    """Mongo model for food_classes collection."""
    meta = {'collection': 'food_classes'}

    food = StringField(required=True)
    kind = StringField(required=True, choices=['fruit', 'vegetable'])

    def __str__(self):
        """Helper to nice console output if needed"""
        return str(dict(food=self.food, kind=self.kind))
