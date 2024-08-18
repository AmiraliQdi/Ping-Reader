def meters_per_sample(ping_message, v_sound=1500):
    """ Returns the target distance per sample, in meters.

    'ping_message' is the message being analysed.
    'v_sound' is the operating speed of sound [m/s]. Default 1500.

    """
    # sample_period is in 25ns increments
    # time of flight includes there and back, so divide by 2
    return v_sound * ping_message.sample_period * 12.5e-9


sample_average_distance = (sample_index + 0.5) * meters_per_sample(ping_message, v_sound)

