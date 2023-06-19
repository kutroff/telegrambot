def encode(filename):
    s = []
    with open(filename, "rb") as f:
        while byte:=f.read(1):
            s.append(int.from_bytes(byte, byteorder="big", signed=False))
            st = str(bin(s[-1]))[2:]
            st = "0"*(8-len(st))+st
            for i in range(len(st)):
                if st[i] == '1':
                    st = st[:i] + '0' + st[i+1:]
                else:
                    st = st[:i] + '1' + st[i+1:]
            s[-1] = int("0b"+st, 2)

    with open(filename+".bin", "wb") as f:
        for i in s:
            f.write(i.to_bytes(1, "big"))
    return s

def decode(filename):
    s = []
    with open(filename, 'rb') as f:
        while byte:=f.read(1):
            s.append(int.from_bytes(byte, byteorder="big", signed=False))
            st = str(bin(s[-1]))[2:]
            st = "0"*(8-len(st))+st
            for i in range(len(st)):
                if st[i] == '1':
                    st = st[:i] + '0' + st[i+1:]
                else:
                    st = st[:i] + '1' + st[i+1:]
            s[-1] = int("0b"+st, 2)
    with open(filename+".txt", 'wb') as f:
        for i in s:
            f.write(i.to_bytes(1, 'big'))

encode("test.txt")