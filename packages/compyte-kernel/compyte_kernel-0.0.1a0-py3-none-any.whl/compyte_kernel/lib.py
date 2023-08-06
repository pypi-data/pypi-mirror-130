def binary_machines(n):
    return (4*n+2)**(2*n)


def init_table(colors, states):
    table = []
    for i in range(0, states):
        table.append([])
        for j in range(0, colors):
            table[i].append([None, None, None])
    return table


def fill_table(table, colors, states, number):
    base = colors * ((2 * states) + 1)

    for i in range(states-1, -1, -1):
        for j in range(0, colors):
            number, remainder = divmod(number, base)
            if (remainder < colors):
                table[i][j][0] = -1
                table[i][j][1] = remainder
                table[i][j][2] = 1
            else:
                remainder = remainder - colors
                table[i][j][1] = remainder % colors
                remainder = remainder // colors

                table[i][j][2] = 2 if remainder % 2 == 0 else 0
                remainder = remainder // 2
                table[i][j][0] = remainder % states


def a_step(tape, table, control, head, blank, halt, runtime):

    result = table[control][tape[head]]

    tape[head] = result[1]
    control = result[0]

    if result[0] == halt:
        return tape, runtime

    if result[2] > 1:
        if head == len(tape) - 1:
            tape.append(blank)
        head = head+1

    else:
        if head == 0:
            tape.insert(0, blank)

    return tape, runtime


def all_step(tape, table, control, head, blank, halt, runtime):
    while runtime > 0:
        tape, runtime = a_step(tape, table, control,
                               head, blank, halt, runtime)
        runtime = runtime-1


def execute(states, number, runtime):

    if number > binary_machines(states):
        raise Exception("it's out of range")
        
    blank = 0
    control = 0
    halt = -1
    colors = 2

    tape = [blank]
    head = 0

    table = init_table(colors, states)
    fill_table(table, colors, states, number)

    all_step(tape, table, control, head, blank, halt, runtime)

    return ''.join(str(x) for x in tape)


if __name__ == "__main__":
    print(execute(2, 5135, 107))
