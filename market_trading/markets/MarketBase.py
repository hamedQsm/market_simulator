class MarketBase:
    def __init__(self, start_timestamp=None):
        self.start_timestamp = start_timestamp

    def get_current_price(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def run(self, n_steps=None):
        steps_done = 0
        def is_end(steps_done):
            return True if n_steps is None else steps_done < n_steps

        while is_end(steps_done):
            yield self.get_current_price()
            steps_done += 1