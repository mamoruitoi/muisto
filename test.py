def main():
    k = int(input())
    a, b = map(int,input().split())
    c = False
    for i in range(a, b+1):
        if k % i == 0:
            print("OK")
            c = True
            break
    if c == False:
        print("NG")