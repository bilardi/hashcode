import sys

class V(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ride = None
        self.last_step = -1
        self.ride_step = 0
        self.a_step = 0
        self.w_step = 0
        self.rides = []

    def is_busy(self, step):
        if step <= self.last_step:
#        if step < self.last_step:
            return 1
        return 0

    def add_ride(self, step, ride):
        self.ride_step = abs(ride.x - ride.a) + abs(ride.y - ride.b)
        self.a_step = abs(self.x - ride.a) + abs(self.y - ride.b)
        self.w_step = step + self.a_step
        if step + self.a_step <= ride.e:
            self.w_step = ride.e
        self.last_step = self.w_step + self.ride_step
        self.x = ride.x
        self.y = ride.y
        self.rides.append(ride.i)

class R(object):
    def __init__(self, a, b, x, y, e, l):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.e = e
        self.l = l
        self.i = 0

class Info(object):
    """The matrix."""

    def __init__(self, rows, cols, v, r, b, s):
        self.rows = rows
        self.cols = cols
        self.v = v
        self.r = r
        self.b = b
        self.s = s
        self.rides = []
        self.vehicles = []
        
    def __str__(self):
        """Display the matrix."""
        return '\n'.join(['<%s>' % ''.join(row) for row in self.rides])

    # def get_score(self):
    #     return 

    def get_ride_index(self, step, v, rides):
        max_score = 0
        index = -1
        c = len(rides)
        for i in range(0, c):
            r = rides[i]
            ride_score = abs(r.x - r.a) + abs(r.y - r.b)
            a_step = abs(v.x - r.a) + abs(v.y - r.b)
            w_step = step + a_step
            bonus_score = 0
            if w_step <= r.e:
                bonus_score = self.b
                w_step = r.e
            if r.l < w_step + ride_score:
                ride_score = 0
            total_score = bonus_score + ride_score
            if total_score > max_score:
                max_score = total_score
                index = i

        return index
    
    def loop(self):
        rides_todo = []

        for v in range(0, self.v):
            self.vehicles.append(V())

        for r in range(0, self.r):
            rides_todo.append(R(*[int(num) for num in self.rides[r].split()]))
            rides_todo[r].i = r
            
        for t in range(0, self.s):
            for v in range(0, self.v):
                if len(rides_todo) > 0:
                    if self.vehicles[v].is_busy(t) == 0:
                        ride_index = self.get_ride_index(t, self.vehicles[v], rides_todo)
                        self.vehicles[v].add_ride(t, rides_todo.pop(ride_index))

def read_matrix(filename):
    """Read the input file."""
    with open(filename, 'r') as fin:
        _info = Info(*[int(num) for num in fin.readline().split()])
        # read matrix
        for i in range(_info.r):
            str_line = fin.readline().strip()
            _info.rides.append(str_line)

    return _info

def write_matrix(info, filename):
    """Write output file."""
    with open(filename, 'w') as out:
        for v in range(0, info.v):
            out.write('%d %s\n' % (len(info.vehicles[v].rides), ' '.join([str(x) for x in info.vehicles[v].rides])))

def main():
    """Main function."""

    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])

    # read data and initialize the matrix
    info = read_matrix(sys.argv[1])

    info.loop()

#    print('score: %d' % info.get_score())

    # write output file
    write_matrix(info, sys.argv[2])

if __name__ == '__main__':
    main()