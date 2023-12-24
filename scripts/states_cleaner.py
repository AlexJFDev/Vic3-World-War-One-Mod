from claus_reader import read_file

FILE_PATH = 'simple.txt'

if __name__ == '__main__':
    with open(FILE_PATH, 'rt') as file:
        claus_ob = read_file(file)
    print(claus_ob)
