import numpy as np


def make_car(desired_v:float=20.0, dt:float=0.1) -> dict:
    """ 
    Generates a dictionary that holds all the car's values. Keeps track of state varaibles.
    """
    car_state_dictionary : dict[str, float] = {
        "v" : 0, #velocity of your car 
        "a" : 0, #acceleration of your car
        "t" : 0, #time of your car
        "x" : 0, #position of your car
        "dt" : dt, #time step of your car, how much the time changes every time you update/step
        "desired_v" : desired_v, #desired velocity of your car, the velocity you want to maintain
        "step" : 0,
    
        #hint: use these variables in the integral and derivative portion of your PID control (steps 5 and 6 )
        "error_prev" : None,
        "net_integral" : 0.0
    }
    return car_state_dictionary

def update(car: dict, throttle_perc: float, mass: float = 1000, max_throttle_force: float = 5000, friction: float = 2.0) -> None:
        """
        Updates the car's state variables based on the throttle percentage.
        Use this function after finding throttle percentage to update the car's state variables.

        Inputs:
        car: dictionary containing the car's state variables
        throttle_perc: float, throttle percentage (-1 to 1)

        Outputs:
        None, but updates the car's state variables
        """
        force = throttle_perc * max_throttle_force
        car["a"] = (force / mass) - friction
        car["v"] += car["a"] * car["dt"]
        car["x"] += car["v"] * car["dt"]
        car["t"] += car["dt"]
        car["step"] += 1


def calculate_desired_acceleration(car: dict, K_P: float, K_I: float = 0.0, K_D: float = 0.0) -> tuple[float, float]:
        #input: car["v"], car["desired_v"] (floats)
        #output: desired acceleration and error tuple(float, float)

        # calculates the  acceleration based on the car's current velocity and desired velocity
        error = car["desired_v"] - car["v"]

        # current error multiplied by time step to get integral of error over time
        car["net_integral"] += error * car["dt"]

        # stop interval from getting too big or small
        car["net_integral"] = np.clip(car["net_integral"], -100, 100)

        # calculate the proportional, integral, and derivative terms
        proportional = K_P * error

        integral = K_I * car["net_integral"]

        if car["error_prev"] is None:
            derivative = 0.0
        else:
            derivative = (error - car["error_prev"]) / car["dt"]

        derivative_term = K_D * derivative

        # update the previous error for the next iteration
        car["error_prev"] = error
        
        desired_acceleration = proportional + integral + derivative_term

        # return the desired acceleration and error
        return desired_acceleration, error


def acceleration_to_throttle_percentage(acceleration_desired: float, mass: float = 1000, max_throttle_force: float = 5000) -> float:
        #input: desired_acceleration(float)
        #output: throttle percentage (float, -1 to 1)

        # Converts the max acceleration to throttle percentage
        max_acceleration = max_throttle_force / mass
        throttle_percentage = acceleration_desired / max_acceleration
        return np.clip(throttle_percentage, -1, 1)