import math
# {
#     "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
#     "x": float,                            # agent's x-coordinate in meters
#     "y": float,                            # agent's y-coordinate in meters
#     "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
#     "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
#     "distance_from_center": float,         # distance in meters from the track center
#     "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
#     "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not.
#     "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
#     "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
#     "heading": float,                      # agent's yaw in degrees
#     "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
#     "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
#     "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
#     "objects_location": [(float, float),], # list of object locations [(x,y), ...].
#     "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
#     "progress": float,                     # percentage of track completed
#     "speed": float,                        # agent's speed in meters per second (m/s)
#     "steering_angle": float,               # agent's steering angle in degrees
#     "steps": int,                          # number steps completed
#     "track_length": float,                 # track length in meters.
#     "track_width": float,                  # width of the track
#     "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
# }


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

    reward = 0

    reward = (math.exp(-5*(distance_from_center/(track_width*0.5))))*100
    reward = reward-(abs(steering_angle)*speed*0.5)
    forward_waypoints = math.ceil(speed*2)

    waypoint_index = closest_waypoints[1]+max(0, forward_waypoints-1)
    if waypoint_index > len(waypoints)-1:
        waypoint_index = waypoint_index-len(waypoints)-1
    waypoint = waypoints[waypoint_index]
    waypoint_direction = math.atan2(
        waypoint[1] - y_cordinate, waypoint[0] - x_cordinate)
    # Convert to degree
    waypoint_direction = math.degrees(waypoint_direction)

    direction_diff = abs(waypoint_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    # reward=reward+(1-(direction_diff/180))*20
    reward = reward+(math.exp(-5*(direction_diff/180)))*20*speed

    reward = reward+(progress*50)

    if not all_wheels_on_track:
        reward = reward*0.2*(4/speed)
    if is_offtrack or is_reversed:
        reward = -100*speed
    return float(reward)
