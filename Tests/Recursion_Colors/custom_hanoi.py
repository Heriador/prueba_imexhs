


# def solve_hanoi(n, disks, source, target, auxiliary):
#     if n == 0:
#         return print(f'{disks[n]} from {source} to {target}');

def hanoi_with_colors(n, disks, source, target, auxiliary, moves):
    if n == 0:
        return True

    # Mover n-1 discos de source a auxiliary
    if not hanoi_with_colors(n-1, disks[:-1], source, auxiliary, target, moves):
        return False

    # Mover el disco n de source a target
    if target and disks[-1][1] == target[-1][1]:
        return False  # No se puede mover porque el color es el mismo
    if source:
        disk = source.pop()
        target.append(disk)
        moves.append((disk[0], "A", "C"))

    # Mover n-1 discos de auxiliary a target
    if not hanoi_with_colors(n-1, disks[:-1], auxiliary, target, source, moves):
        return False

    return True

def solve_hanoi(n, disks):
    source = disks[:]
    target = []
    auxiliary = []
    moves = []
    print(source)
    if hanoi_with_colors(n, disks, source, target, auxiliary, moves):
        return moves
    else:
        return -1



        

if __name__ == '__main__':
    n = 3;
    disks = [(3, 'red'), (2, 'green'), (1, 'blue')];
    result = solve_hanoi(n, disks)
    print(result)