from claus_reader import read_file

FILE_PATH = 'small_states.txt'

if __name__ == '__main__':
    claus_ob = read_file(FILE_PATH)
    # print(claus_ob['OTHER'])
    print(claus_ob)
