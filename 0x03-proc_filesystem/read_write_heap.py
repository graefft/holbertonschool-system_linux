#!/usr/bin/python3
'''
Locates and replaces first occurrence of a string in the heap of a process

Usage: ./read_write_heap.py PID search_string replace_by_string

PID is the PID of the running process
strings are ASCII
'''

import sys


def print_usage():
    print('Usage: {} pid search write'.format(sys.argv[0]))
    sys.exit(1)


def main():
    if len(sys.argv) != 4:
        print_usage()

    pid = int(sys.argv[1])
    if pid <= 0:
        print_usage()
    search_string = str(sys.argv[2])
    write_string = str(sys.argv[3])
    if len(write_string) > len(search_string):
        raise IndexError

    map_file_name = '/proc/{}/maps'.format(pid)
    mem_file_name = '/proc/{}/mem'.format(pid)

    try:
        map_file = open('/proc/{}/maps'.format(pid), 'r')
    except IOError as e:
        print('[ERROR] Cannot open file {}'.format(map_file_name))
        sys.exit(1)

    for line in map_file:
        split_line = line.split(' ')
        if split_line[-1][:-1] != "[heap]":
            continue
        mem_addr = split_line[0]
        perms = split_line[1]
        offset = split_line[2]
        device = split_line[3]
        inode = split_line[4]
        pathname = split_line[-1][:-1]

        #   CHECK FOR READ AND WRITE PERMISSION
        if perms[0] != 'r' or perms[1] != 'w':
            print('{} does not have read/write permission'.format(pathname))
            raise PermissionError

        #   GET START AND END OF HEAP IN VIRUTAL MEMORY
        address = mem_addr.split('-')
        if len(address) != 2:
            print('Wrong address format')
            map_file.close()
            exit(1)

        addr_start = int(address[0], 16)
        addr_end = int(address[1], 16)

        #   OPEN AND READ MEMORY
        try:
            mem_file = open(mem_file_name, 'rb+')
        except IOError as e:
            print('[ERROR] Cannot open file {}'.format(mem_file_name))
            map_file.close()
            exit(1)

        #   READ HEAP
        mem_file.seek(addr_start)
        heap = mem_file.read(addr_end - addr_start)

        #   FIND STRING
        try:
            i = heap.index(bytes(search_string, 'ASCII'))
        except Exception:
            print("Can't find '{}'".format(search_string))
            map_file.close()
            mem_file.close()
            exit(1)

        #   WRITE NEW STRING
        print("changing '{}' to '{}' in {}:"
              .format(search_string, write_string, pid))
        mem_file.seek(addr_start + i)
        mem_file.write(bytes(write_string + '\0', 'ASCII'))
        if len(write_string) > 0:
            print("String changed!")
        map_file.close()
        mem_file.close()
        break

if __name__ == '__main__':
    main()
