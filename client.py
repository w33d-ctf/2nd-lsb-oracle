import pwn
proc = pwn.remote('127.0.0.1', 7000)
while True:
    print(proc.recv().decode())
    inp = input().encode()
    proc.send(inp)
    if inp.strip() == b"2":
        proc.send(input().encode())
    