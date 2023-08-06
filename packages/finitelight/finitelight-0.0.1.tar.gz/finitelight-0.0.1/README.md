# finitelight

Finitelight is a python package which adds functionality for calculating the time it takes light to travel a distance.

To calculate the time it takes for light to travel from an observer to an object given the following parameters:
* The distance to the object in kilometers 

example:
```angular2html
    import finitelight as fl

    distance_to_object = 300
    light_travel_time = fl.lightspeed_time(distance_to_object)
```

To calculate the time difference it takes for light to reach two observers from an object given:
* From observer 1's frame of reference, the viewing angle between the second observer and the object

* from observer 1's frame of reference, the distance to the object, and the distance to the second observer

```angular2html
    import finitelight as fl

    distance_to_object = 300
    distance_to_observer = 300
    viewing_angle = 90

    light_travel_difference = (distance_to_object, viewing_angle, distance_to_observer)
```