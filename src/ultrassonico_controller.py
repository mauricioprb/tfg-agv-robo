import RPi.GPIO as GPIO
import time

class UltrassonicoController:
    def __init__(self, trigger_pin, echo_pin, distance_threshold=10):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.distance_threshold = distance_threshold
        self.is_obstacle_detected = False
        
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trigger_pin, False)
        
    def measure_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001) 
        GPIO.output(self.trigger_pin, False)
        
        pulse_start = time.time()
        timeout = pulse_start + 0.1
        
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None
            
        pulse_end = time.time()
        timeout = pulse_end + 0.1 
        
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None
            
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150 
    
    def check_obstacle(self):
        distance = self.measure_distance()
        
        if distance is None:
            return True
            
        if distance <= self.distance_threshold and not self.is_obstacle_detected:
            self.is_obstacle_detected = True
            return True
        elif distance > self.distance_threshold and self.is_obstacle_detected:
            self.is_obstacle_detected = False
            return False
            
        return self.is_obstacle_detected
    
    def cleanup(self):
        """Clean up GPIO pins."""
        GPIO.cleanup([self.trigger_pin, self.echo_pin])