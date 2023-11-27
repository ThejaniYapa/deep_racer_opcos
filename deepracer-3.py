import math

def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    x_cordinate = params['x']
    y_cordinate = params['y']
    closest_waypoints = params['closest_waypoints']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
    heading = params['heading']
    progress = params['progress']
    speed = params['speed']
    steering_angle = params['steering_angle']
    steps = params['steps']
    track_length = params['track_length']
    track_width = params['track_width']
    waypoints = params['waypoints']
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    reward = 1e-3

    if all_wheels_on_track and ((0.5*track_width - distance_from_center) >= 0.05):
        reward = 1.0

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    ABS_STEERING_THRESHOLD = 15 

    steering = abs(params['steering_angle'])

    # Penalize reward if the car is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    direction_diff = abs(track_direction - heading)

    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    reward += (progress*5)

    return float(reward)