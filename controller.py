from pygame import *

class Controller:
    """
    Handles input mapping and execution of associated callbacks for key events.
    Supports discrete presses (down), releases (up), and continuous holding (step).
    """
    def __init__(self):
        self.binds = {} 
        self.activePresses = {}

    def addBind(self, key: int, down=None, up=None, whileDown=None):
        """
        Registers a set of callbacks to a specific key.
        
        Args:
            key (int): The Pygame key constant (e.g., K_SPACE).
            down (function): Function triggered for down operation
            up (function): Triggered once when the key is released. 
                            Receives 't' (total press duration).
            whileDown (function): Triggered every frame while held. 
                            Receives 'dt' (delta time).
        """
        self.binds[key] = {
            "down": down, 
            "up": up, 
            "whileDown": whileDown 
        }

    def process(self, press: int, time: float, action="down"):
        """
        Updates the internal state of a key based on Pygame events.
        
        Args:
            press (int): The key code being processed.
            time (float): The current timestamp from pygame.time.get_ticks().
            action (str): The event type, either "down" or "up".
            
        Returns:
            bool: False if the key has no associated bindings.
        """
        bind = self.binds.get(press)
        if bind:
            if action == 'down':
                # Execute the 'down' callback and track the start time
                if bind.get("down"):
                    bind["down"](0)
                self.activePresses[press] = [
                    time,  
                    bind.get("whileDown")
                ]
            elif action == 'up'  and press in  self.activePresses:
                # Execute the 'up' callback with the calculated duration 't'
                if bind.get("up"):
                    bind["up"](time - self.activePresses[press][0])
                del self.activePresses[press]
        else:
            return False 

    def step(self, dt: float):
        """
        Processes active 'whileDown' callbacks for all currently held keys.
        This should be called once per frame within the main loop.
        
        Args:
            dt (float): The time elapsed since the last frame.
        """
        for key, value in self.activePresses.items():
            # Check if a whileDown callback exists (index 1 of the stored list)
            if len(value) > 1 and value[1]:
                value[1](dt)