import math, time

#######################################################################

# IMPLEMENTED VARIABLES TYPES

# - Numerical types are int, float, complex.

# - Physical types are lists or dictionaries with 2 elements in order,
#   a string contained in SI_phy_dims constant and a numerical.

#######################################################################

##############
# CONSTANTS
##############

SI_phy_dims = ('s', 'm', 'kg', 'A', 'K', 'Mol', 'cd')
letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
digits = (0,1,2,3,4,5,6,7,8,9)

##############
# IDENTIFIERS
##############
# Identifiers returns True if the argument is the same type of the function
# name, false otherwise. Identifiers can identify eventual substructures
# with ascending positive integers.

# Returns True if the argument is a decimal digit, False otherwise
def is_digit(arg):
    if type(arg) is int:
        if arg in digits:
            return True
    return False

# Returns True if the argument is numerical, False otherwise.
def is_number(arg):
    if type(arg) in [int, float, complex]:
        return True
    return False

# Returns True if the argument is a latin alphabet letter, False otherwise.
def is_letter(arg):
    if type(arg) is str:
        if arg in letters:
            return True
    return False

# Returns True if the argument is a physical dimension, False otherwise.
def is_phy_dim(arg):
    if type(arg) is str and arg in SI_phy_dims:
        return True
    return False

# Returns True if the argument is a physical variable, False otherwise,
# if the argument is a list returns 0,
# if the argument is a dictionary returns 1.
def is_phy(arg):
    if type(arg) is list:
        if is_number(arg[0]) and len(arg) == 2 and type(arg[1]) is str:
            return 0
    elif type(arg) is dict:
        if len(arg) == 1 and (
        type(list(arg.keys())[0]) is str and is_number(list(arg.values())[0])):
            return 1
    return False

##############
# CONVERTERS
##############
# Converters return an item which is of the same type of 
# the calling function name.

# Returns the argument converted to numerical
def number(arg):
    conv_arg = None
    ret_neg = False
    if arg[0] == '-':
        arg = arg.lstrip('-')
        ret_neg = True
    try:
        conv_arg = int(arg)
    except:
        try:
            conv_arg = float(arg)
        except:
            try:
                conv_arg = complex(arg)
            except:
                try:
                    if arg == 'math.pi':
                        conv_arg = math.pi
                    elif arg == 'math.e':
                        conv_arg = math.e
                    elif arg == 'math.tau':
                        conv_arg = math.tau
                    elif arg == 'math.inf':
                        conv_arg = math.inf
                except:
                    pass
    if ret_neg == True:
        conv_arg = -conv_arg
    if conv_arg == None:
        print('Error on number conversion.')
        exit(0)
    return conv_arg

##############
# OPERATORS
##############
# Operators acts on two equal type arguments to return a variable 
# of the same type.

# Multiply SI physical dimensions.
def dim_mult(a,b):
    # divide numerators and denominators
    nums = ['','']
    dens = ['','']
    if a.count('\\') == 1 and a.count('/') == 0:
        nums[0] = a.split('\\')[0]
        dens[0] = a.split('\\')[1]
    elif a.count('\\') == 0 and a.count('/') == 1:
        nums[0] = a.split('/')[0]
        dens[0] = a.split('/')[1]
    elif a.count('\\') == 0 and a.count('6/') == 0:
        nums[0] = a
        dens[0] = None
    if b.count('\\') == 1 and b.count('/') == 0:
        nums[1] = b.split('\\')[0]
        dens[1] = b.split('\\')[1]
    elif b.count('\\') == 0 and b.count('/') == 1:
        nums[1] = b.split('/')[0]
        dens[1] = b.split('/')[1]
    elif b.count('\\') == 0 and b.count('/') == 0:
        nums[1] = b
        dens[1] = None
    # split powers and dimensions in numerators and denominators
    num_dims = [[],[]]
    num_pows = [[],[]]
    den_dims = [[],[]]
    den_pows = [[],[]]
    for i in range(2):
        for physdim in SI_phy_dims:
            if nums[i].count(physdim) == 1:
                num_dims[i].append(physdim)
                pow_mark = nums[i].find(physdim)+len(physdim)
                if pow_mark != len(nums[i]):
                    if nums[i][pow_mark] == '^':
                        pow_mark += 1
                        num_pow_temp = ''
                        while pow_mark < len(nums[i]):
                            if is_digit(number(nums[i][pow_mark])):
                                num_pow_temp = num_pow_temp+nums[i][pow_mark]
                            else:
                                break
                            pow_mark += 1
                        if num_pow_temp == '':
                            num_pow_temp = 1
                        num_pows[i].append(number(num_pow_temp))
                    else:
                        num_pows[i].append(1)
                else:
                    num_pows[i].append(1)
            if dens[i] != '' or dens[i] != '1':
                if dens[i].count(physdim) == 1:
                    den_dims[i].append(physdim)
                    pow_mark = dens[i].find(physdim)+len(physdim)
                    if pow_mark != len(dens[i]):
                        if dens[i][pow_mark] == '^':
                            pow_mark += 1
                            den_pow_temp = ''
                            while pow_mark < len(dens[i]):
                                if is_digit(number(dens[i][pow_mark])):
                                    den_pow_temp = den_pow_temp + (
                                    dens[i][pow_mark])
                                else:
                                    break
                                pow_mark += 1
                            if den_pow_temp == '':
                                den_pow_temp = 1
                            den_pows[i].append(number(den_pow_temp))
                        else:
                            den_pows[i].append(1)
                    else:
                        den_pows[i].append(1)
    # perform division by subtracting exponents
    for i in range(2):
        j = 0
        while j < len(num_dims[0]):
            if num_dims[0][j] in den_dims[i]:
                k = den_dims[i].index(num_dims[0][j])
                if num_pows[0][j] - den_pows[i][k] >= 0:
                    new_num_pow = num_pows[0][j] - den_pows[i][k]
                else:
                    new_num_pow = 0
                if den_pows[i][k] - num_pows[0][j] >= 0:
                    new_den_pow = den_pows[i][k] - num_pows[0][j]
                else:
                    new_den_pow = 0
                num_pows[0][j] = new_num_pow
                den_pows[i][k] = new_den_pow
            j += 1
        j = 0
        while j < len(num_dims[1]):
            if num_dims[1][j] in den_dims[i]:
                k = den_dims[i].index(num_dims[1][j])
                if num_pows[1][j] - den_pows[i][k] >= 0:
                    new_num_pow = num_pows[1][j] - den_pows[i][k]
                else:
                    new_num_pow = 0
                if den_pows[i][k] - num_pows[1][j] >= 0:
                    new_den_pow = den_pows[i][k] - num_pows[1][j]
                else:
                    new_den_pow = 0
                num_pows[1][j] = new_num_pow
                den_pows[i][k] = new_den_pow
            j += 1
    # remove 0 powers dimensions
    for j in range(2):
        i = 0
        while i < len(num_pows[j]):
            if num_pows[j][i] == 0:
                num_pows[j].pop(i)
                num_dims[j].pop(i)
                i -= 1
            i += 1
    for j in range(2):
        i = 0
        while i < len(den_pows[j]):
            if den_pows[j][i] == 0:
                den_pows[j].pop(i)
                den_dims[j].pop(i)
                i -= 1
            i += 1
    # multiply numerators and denominators powers
    i = 0
    while i < len(num_dims[0]):
        j = 0
        while j < len(num_dims[1]):
            if num_dims[0][i] == num_dims[1][j]:
                num_dims[1].pop(j)
                num_pows[0][i] += num_pows[1][j]
                num_pows[1].pop(j)
            j += 1
        i += 1
    i = 0
    while i < len(den_dims[0]):
        j = 0
        while j < len(den_dims[1]):
            if den_dims[0][i] == den_dims[1][j]:
                den_dims[1].pop(j)
                den_pows[0][i] += den_pows[1][j]
                den_pows[1].pop(j)
            j += 1
        i += 1
    # build final dimension multiplying dimensions with corresponding powers
    ret_str = ''
    j = 0
    while j < 2:
        i = 0
        while i < len(num_dims[j]):
            ret_str = ret_str + num_dims[j][i]
            try:
                if num_pows[j][i] != 1:
                    ret_str = ret_str + '^' + str(num_pows[j][i])
            except: pass
            i += 1
        j += 1
    ret_str = ret_str + '/'
    for j in range(2):
        i = 0
        while i < len(den_dims[j]):
            ret_str = ret_str + den_dims[j][i]
            try:
                if den_pows[j][i] != 1:
                    ret_str = ret_str + '^' + str(den_pows[j][i])
            except: pass
            i += 1
    if ret_str == '/':
        ret_str = ''
    return ret_str

# Sum physical variables.
def phy_sum(a,b):
    res = []
    if is_phy(a) == 0:
        if is_phy(b) == 0:
            if a[1] == b[1]:
                return [a[0] + b[0], a[1]]
        elif is_phy(b) == 1:
            if a[1] == list(b.keys())[0]:
                return [a[0] + list(b.values())[0], a[1]]
    elif is_phy(a) == 1:
        if is_phy(b) == 0:
            if list(a.keys())[0] == b[1]:
                 return [list(a.values())[0] + b[0], b[1]]
        elif is_phy(b) == 1:
            if list(a.keys())[0] == list(b.keys())[0]:
                return [list(a.values())[0] + list(b.values())[0], 
                        list(a.keys())[0]]
    print('Unable to sum different physical dimensions')
    exit(0)

# Multiply physical variables.
def phy_mult(a,b):
    res = []
    if is_phy(a) == 0:
        if is_phy(b) == 0:
            return [a[0] * b[0],  dim_mult(a[1], b[1])]
        elif is_phy(b) == 1:
            return [a[0] * list(b.values())[0], dim_mult(a[1], 
                    list(b.keys())[0])]
    elif is_phy(a) == 1:
        if is_phy(b) == 0:
            return [list(a.values())[0] * b[0], 
                    dim_mult(list(a.keys())[0], b[1])]
        elif is_phy(b) == 1:
            return [list(a.values())[0] * list(b.values())[0], 
                    dim_mult(list(a.keys())[0], list(b.keys())[0])]

##############
# DISCRETIZERS
##############
# Discretizers returns a finite countable version of an uncountable item.

# Returns a list which is finite version of an uncountable real range
# (split 'end-start' interval 'bins' times)
def discrete_range(start: float, end: float, bins: int):
    if end < start or bins <= 0:
        print('Discrete range boundaries error')
        exit(0)
    bin_len = (end-start)/bins
    return [bin_len*x for x in range(bins+1)]

##############
# ITERATORS
##############
# Iterators repeat a certain task multiple times.

# Repeat a function f with arguments args a defined number of times
def repeat(times, f, *args):
    for calls in range(times):
        f(*args)

# Clock that runs a function f with arguments args at fixed fps
class clock():
    def __init__(self, fps = 120):
        self.fps = fps
    def __call__(self, f = lambda:None, *args):
        prev_tick_time = time.time()
        while True:
            if time.time()-prev_tick_time >= 1/self.fps:
                print(time.time()-prev_tick_time)
                f(*args)
                prev_tick_time = time.time()

# Run a multivariable function at fixed fps on discrete ranges
def run(fps = 120, f = lambda:None, *discrete_ranges):
    x = list()
    i = 0
    while i < len(discrete_ranges):
        if type(discrete_ranges[i]) is not list or (
            len(discrete_ranges[i]) != len(discrete_ranges[0])):
            print('Run arguments can only be discrete ranges '
                '(lists of same length)')
            exit(0)
        i += 1

    i = 0
    while i < len(discrete_ranges[0]):
        j = 0
        while j < len(discrete_ranges):
            x.append(discrete_ranges[j][i])
            j += 1
        f(*tuple(x))
        x.clear()
        i += 1
        time.sleep(1/fps)