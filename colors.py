NORMAL = "\033[0m"

BLA = "\033[30;0m"
RED = "\033[31;0m"
GRE = "\033[32;0m"
YEL = "\033[33;0m"
BLU = "\033[34;0m"
MAG = "\033[35;0m"
CYA = "\033[36;0m"
WHI = "\033[37;0m"
B_BLA = "\033[30;1m"
B_RED = "\033[31;1m"
B_GRE = "\033[32;1m"
B_YEL = "\033[33;1m"
B_BLU = "\033[34;1m"
B_MAG = "\033[35;1m"
B_CYA = "\033[36;1m"
B_WHI = "\033[37;1m"
D_BLA = "\033[30;2m"
D_RED = "\033[31;2m"
D_GRE = "\033[32;2m"
D_YEL = "\033[33;2m"
D_BLU = "\033[34;2m"
D_MAG = "\033[35;2m"
D_CYA = "\033[36;2m"
D_WHI = "\033[37;2m"
I_BLA = "\033[30;3m"
I_RED = "\033[31;3m"
I_GRE = "\033[32;3m"
I_YEL = "\033[33;3m"
I_BLU = "\033[34;3m"
I_MAG = "\033[35;3m"
I_CYA = "\033[36;3m"
I_WHI = "\033[37;3m"
U_BLA = "\033[30;4m"
U_RED = "\033[31;4m"
U_GRE = "\033[32;4m"
U_YEL = "\033[33;4m"
U_BLU = "\033[34;4m"
U_MAG = "\033[35;4m"
U_CYA = "\033[36;4m"
U_WHI = "\033[37;4m"

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def add(text, color):
	return color + str(text) + NORMAL

def bold(color):
	return color.replace('0m', '1m')