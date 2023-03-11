from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    founded = models.DateField()

    def __str__(self):
        string = self.name + " " + self.description
        return string

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dealer_id = models.IntegerField()
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    CONVERTIBLE = 'Convertible'
    HATCHBACK = 'Hatchback'
    PICKUP = 'Pickup'
    VAN = 'Van'
    OTHER = 'Other'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (CONVERTIBLE, 'Convertible'),
        (HATCHBACK, 'Hatchback'),
        (PICKUP, 'Pickup'),
        (VAN, 'Van'),
        (OTHER, 'Other')
    ]
    type = models.CharField(
        max_length=200, choices=CAR_TYPE_CHOICES, default=OTHER)
    year = models.DateField()

    def __str__(self):
        string = self.name + " " + self.type + " " + str(self.year)
        return string

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
""" class CarDealer(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    addressline1 = models.CharField(max_length=200)

    def __str__(self):
        string = self.firstname + " " + self.lastname + " " + self.email + " " + self.phone + " " + self.addressline1
        return string """


# <HINT> Create a plain Python class `DealerReview` to hold review data
""" class DealerReview(models.Model): """
