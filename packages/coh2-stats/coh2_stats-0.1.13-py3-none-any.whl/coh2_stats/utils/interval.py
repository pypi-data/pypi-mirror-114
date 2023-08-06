class Interval:
    def generate(self, min, max, interval):
        count = min
        while count <= max:
            smaller_than_interval = [count, count + interval]
            bigger_than_interval = [count, max]
            current_interval = [bigger_than_interval, smaller_than_interval][count + interval <= max]
            yield current_interval[0], current_interval[1]
            count += interval