def right_justify(s):
    needed_whitespace = 70 - len(s)
    print(' ' * needed_whitespace + s)

def do_twice(f):
    f()
    f()

def print_grid(rows, columns):
    for i in range(0, rows):
        print('+ - - - - ' * columns + '+')
        for j in range(1, 4):
            print('|         ' * columns + '|')
    print('+ - - - - ' * columns + '+')

def print_spam():
    print('spam')
