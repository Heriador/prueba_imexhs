def hanoi_with_colors(n, disks, source, target, auxiliary):
    moves = []

    def move_disks(num_disks, src, tgt, aux, src_stack, tgt_stack, aux_stack):
        if num_disks == 0:
            return

        # Move n-1 disks from source to auxiliary, using target as auxiliary
        move_disks(num_disks - 1, src, aux, tgt, src_stack, aux_stack, tgt_stack)

        # Get the current disk to move
        disk = src_stack.pop()

        # Ensure that the target rod rules are satisfied
        if tgt_stack and (tgt_stack[-1][0] < disk[0] or tgt_stack[-1][1] == disk[1]):
            raise ValueError(f"Disk {disk} cannot be placed on {tgt_stack[-1]}")

        tgt_stack.append(disk)
        moves.append((disk, src, tgt))

        # Move n-1 disks from auxiliary to target, using source as auxiliary
        move_disks(num_disks - 1, aux, tgt, src, aux_stack, tgt_stack, src_stack)

        return True

    # Create stacks for each rod
    source_stack = disks.copy()
    target_stack = []
    auxiliary_stack = []

    move_disks(n, source, target, auxiliary, source_stack, target_stack, auxiliary_stack)

    return moves

if __name__ == "__main__":

    disks = [(4,'blue'),(3, "red"), (2, "green"), (1, "red")]
  
    # Solve the problem and display the moves
    try:
        result = hanoi_with_colors(len(disks), disks, "A", "C", "B")
        for move in result:
            print(f"Move disk {move[0]} from {move[1]} to {move[2]}")
    except ValueError as e:
        print(e)
