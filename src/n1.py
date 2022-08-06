

def main():
    with open('html/index.html') as f:
        index_contents = f.read()

    print(index_contents)

    with open('html/lines.txt') as f:
        while True:
            x = f.readline().strip()
            if x is None or len(x) == 0:
                break
            print(x)

    print('{:,}'.format(1000))

if __name__ == '__main__':
    main()
