import dis

def assemble_assignment(N):
    LHS1 = ','.join(f"name{num}" for num in range(N))
    LHS2 = ','.join(f"name{num}" for num in range(N, 2*N))
    return f"{LHS1}, *nameSTARRED, {LHS2} = range({2*N + 100})"

if __name__ == "__main__":
    dis.dis(assemble_assignment(2**8 - 1))
    dis.dis(assemble_assignment(2**8))
