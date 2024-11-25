write=0
def binary_to_hex(binary_str):
    # Убедимся, что длина кратна 4, добавляя нули слева
    binary_str = binary_str.zfill((len(binary_str) + 3) // 4 * 4)
    # Перевод в шестнадцатеричное
    hex_str = hex(int(binary_str, 2))[2:].upper()
    return hex_str

while True:
    a=0
    b=-1
    c=-1
    d=-1
    e=-1
    res = ''
    while a==0 or a>2**7:
        a=int(input(f"Input A less than 2^7 ({2**7}) (<0==exit): "))
        if a<0:

            exit()
    res=format(a,"06b")+res

    while b==-1 or b>2**18:
        b = int(input(f"Input B less than 2^18({2**18}): "))
    res = format(b, "017b") + res

    if a==35:
        while c==-1 or c>2**15:
            c = int(input(f"Input C less than 2^15({2**15}): "))

        res = format(c, "014b") + res
    else:
        while c==-1 or c>2**18:
            c = int(input(f"Input C less than 2^18({2**18}): "))
        res = format(c, "017b") + res

    if a==54:
        while d ==-1 or d > 2 ** 18:
            d = int(input(f"Input D less than 2^18({2**18}): "))
        res = format(d, "017b") + res

        while e ==-1 or e > 2 ** 7:
            e = int(input(f"Input E less than 2^7({2**18}): "))
        res = format(e, "06b") + res

    print(res)
    res=binary_to_hex(res)

    while len(res)<16:
        res="0"+res
    print(res)
    co=[]
    for i in range(0,len(res)):
        if i%2!=0:
            co.append((res[i-1]+res[i]).upper())
    co=co[::-1]
    while len(co)<8:
        co.append("00")
    res=''
    for i in co:
        res+=f"0x{i}, "
    print(res[:-2])






