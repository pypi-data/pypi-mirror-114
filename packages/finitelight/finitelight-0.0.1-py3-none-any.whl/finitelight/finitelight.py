import math
def lightspeed_time(distance_to_object, full_angle=0, distance_to_second_observer=-1):
    '''
    Given:
    :param distance_to_object: distance in km
    Calculates the time it takes for light to travel `distance_to_object` in seconds.
    :returns: float: Time in seconds

    Given
    :param distance_to_object: Distance from `observer-1` to object
    :param full_angle: from `observer-1` frame of reference: viewing angle between `object` and `observer-2`
    :param distance_to_second_observer: Distance from `observer-1` to `observer-2`
    Calculates the difference in time it takes light emissions from `object` to reach `observer-1` and `observer-2`
    :return: float: time difference in seconds.exi
    '''
    if distance_to_second_observer < 0:
        distance_to_second_observer = distance_to_object
        full_angle=0
    hyp_squared = (distance_to_second_observer ** 2 + distance_to_object ** 2) - (2 * distance_to_second_observer * distance_to_object * math.cos(full_angle))
    hyp_left = math.sqrt((hyp_squared))

    c = 299792.458

    right_time = distance_to_object / c
    left_time = hyp_left/c

    time_diff = right_time-left_time

    time_diff = math.fabs(time_diff)
    return time_diff
