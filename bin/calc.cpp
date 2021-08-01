#include <stdio.h>

typedef enum {
  DEG, RAD, GRAD
}tmode;

class GB {
    public:
    double stack[15];
    char i;
    tmode mode;
    GB();
};

GB::GB() {
    i = 0;
    mode = DEG;
}

char line[100];
GB G;

class words {
    private:
    char* s;
    char word[20];

    public:
    words(char*);
    char* get();
};

words::words(char *i) {
    s = i;
}
char* words::get(void) {
    char i = 0;
    char j = 0;
    while(s[i] == ' ') {
        i++;
    }
    while(s[i] != 0 and s[i] != ' ') {
        word[j++] = s[i++];
    }
    word[j] = 0;
    s += i;
    if (word[0] == 0) {
        return NULL;
    }
    return word;
}

void calc(void) {
    words w(line);
    char* arg;
    while ((arg = w.get()) != NULL) {
        printf("%s\n", arg);
    }
}
/*
def calc(line):
    args = re.split(r'\s+', line)
    for arg in args:
        if re_match(r'^([+-]?)([\d\.]+)([kmgKMG]?)(e([+-]?)(\d+))?$', arg):
            n = float(G.m.group(2))
            power = G.m.group(3)
            expo = G.m.group(4)
            exposign = G.m.group(5)
            exponum = G.m.group(6)
            if G.m.group(1) == '-':
                n = 0 - n
            if power == 'k' or power == 'K':
                n = n * 1000
            elif power == 'm' or power == 'M':
                n = n * 1000000
            elif power == 'g' or power == 'G':
                n = n * 1000000000
            if expo is not None:
                exponum = float(exponum)
                if exposign == '-':
                    exponum = 0-exponum
                n = n * math.pow(10, exponum)
            G.stack.append(n)
        elif arg == 'pi':
            n = math.pi
            G.stack.append(n)
        elif arg == 'e':
            n = math.e
            G.stack.append(n)
        elif arg == 'G':             # Gravitational constant 6.67408 x 10-11 m3 kg-1 s-2
            n = 6.67408e-11
            G.stack.append(n)
        else:
            op(arg)

def op(arg):
    if  arg == '+':
        b = G.stack.pop()
        a = G.stack.pop()
        G.stack.append(a+b)
    elif  arg == '-':
        b = G.stack.pop()
        a = G.stack.pop()
        G.stack.append(a-b)
    elif  arg == '*':
        b = G.stack.pop()
        a = G.stack.pop()
        G.stack.append(a*b)
    elif  arg == '/':
        b = G.stack.pop()
        a = G.stack.pop()
        G.stack.append(a/b)
    elif  arg == '%':
        b = G.stack.pop()
        a = G.stack.pop()
        a = int(a)
        b = int(b)
        G.stack.append(a % b)
    elif  arg == '1/' or  arg == 'inv':
        a = G.stack.pop()
        G.stack.append(1/a)
    elif  arg == 'neg' or  arg == '0-':
        a = G.stack.pop()
        G.stack.append(0 - a)
    elif  arg == 'sq':
        a = G.stack.pop()
        G.stack.append(a*a)
    elif  arg == 'sqrt':
        a = G.stack.pop()
        G.stack.append(math.sqrt(a))
    elif  arg == '^':
        b = G.stack.pop()
        a = G.stack.pop()
        G.stack.append(math.pow(a, b))
    elif  arg == 'log':
        a = G.stack.pop()
        G.stack.append(math.log10(a))
    elif  arg == 'ln':
        a = G.stack.pop()
        G.stack.append(math.log(a))
    elif  arg == 'log2' or arg == 'logb':
        b = G.stack.pop()
        a = G.stack.pop()
        G.stack.append(math.log(b, a))
    elif  arg == 'rad':
        G.mode = 'RAD'
    elif  arg == 'deg':
        G.mode = 'DEG'
    elif  arg == 'grad':
        G.mode = 'GRAD'
    elif  arg == 'sin':
        a = G.stack.pop()
        if G.mode == 'DEG':
            a = math.pi * a / 180
        elif G.mode == 'GRAD':
            a = math.pi * a / 200 
        G.stack.append(math.sin(a))
    elif  arg == 'cos':
        a = G.stack.pop()
        if G.mode == 'DEG':
            a = math.pi * a / 180
        elif G.mode == 'GRAD':
            a = math.pi * a / 200 
        G.stack.append(math.cos(a))
    elif  arg == 'tan':
        a = G.stack.pop()
        if G.mode == 'DEG':
            a = math.pi * a / 180
        elif G.mode == 'GRAD':
            a = math.pi * a / 200 
        G.stack.append(math.tan(a))
    elif  arg == 'asin':
        a = G.stack.pop()
        a = math.asin(a)
        if G.mode == 'DEG':
            a = a * 180 / math.pi
        elif G.mode == 'GRAD':
            a = a * 200 / math.pi
        G.stack.append(a)
    elif  arg == 'acos':
        a = G.stack.pop()
        a = math.acos(a)
        if G.mode == 'DEG':
            a = a * 180 / math.pi
        elif G.mode == 'GRAD':
            a = a * 200 / math.pi
        G.stack.append(a)
    elif  arg == 'atan':
        a = G.stack.pop()
        a = math.atan(a)
        if G.mode == 'DEG':
            a = a * 180 / math.pi
        elif G.mode == 'GRAD':
            a = a * 200 / math.pi
        G.stack.append(a)
    elif  arg == 'pop':
        G.stack.pop()
    elif  arg == 'c':
        G.stack = []
    elif  arg == 'x':
        b = G.stack.pop()
        a = G.stack.pop()
        G.stack.append(b)
        G.stack.append(a)
    else:
        if arg == '':
            pass
        else:
            print('IGNORED: {arg}'.format(arg=arg))

def print_stack():
    print('    ---{mode}---'.format(mode=G.mode))
    n = 0
    for i in G.stack:
        print('    {n}: {i}'.format(n=n, i=i))
        n += 1

def re_match(rex, line):
    G.m = re.search(rex, line)
    if G.m:
        return True
    return False
        
*/

void raw_input(const char* s) {
    printf("%s", s);
    line[0] = 0;
    char i = 0;
    char c;
    while(1) {
        c = getc(stdin);
        if (c == 0x0a) {
            break;
        }
        else if (c == 0x0d) {
            break;
        }
        else {
            line[i++] = c;
        }
    }
    line[i] = 0;
}

int main() {

    while (1) {
        raw_input(">>> ");   // Fills line
        calc();
        // print_stack()
    }
}
