def sector_s(radius,degree):
    pi = 3.1415926
    S = radius * radius * pi * (degree/360)
    print(str(S))

def sector_v(radius,arc_lenth):
    V = radius * 2 + arc_lenth
    print(str(V))
