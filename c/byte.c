#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define BUFFER_SIZE 1024

/**
 * Convert byte string `bin' with length `len' to hex string.
 */
char *
bin2hex(const unsigned char *bin, unsigned int len)
{
    static char buf[BUFFER_SIZE + 1];  // static is convenient for debugging purpose
    unsigned int i;

    if(len > (BUFFER_SIZE / 2)) {
        len = BUFFER_SIZE / 2;
    }

    for(i = 0; i < len; i++) {
        sprintf(buf + 2 * i, "%02x", bin[i]);
    }
    buf[2 * i] = 0;

    return buf;
}

/**
 * Convert a hex string `hex' to byte string store at `*bin' with length `len'.
 *
 * @return 0: success, -1: failed
 */
int
hex2bin(const char *hex, unsigned char **bin, unsigned int *out_len)
{
    static unsigned char buf[BUFFER_SIZE + 1];
    unsigned int i, in_len;
    int ch1, ch2;
    unsigned char byte;

    in_len = strlen(hex);
    if(in_len % 2) {
        return -1;
    }

    if(in_len > (BUFFER_SIZE / 2)) {
        in_len = BUFFER_SIZE / 2;
    }
    *out_len = 0;
    for(i = 0; i < in_len;) {
        ch1 = hex[i];
        ch2 = hex[i + 1];
        if(!isxdigit(ch1) || !isxdigit(ch1)) {
            return -1;
        }
        ch1 = tolower(ch1);
        ch2 = tolower(ch2);

        if(ch1 >= 'a') {
            ch1 = ch1 - 'a' + 10;
        } else {
            ch1 = ch1 - '0';
        }
        if(ch2 >= 'a') {
            ch2 = ch2 - 'a' + 10;
        } else {
            ch2 = ch2 - '0';
        }
        byte = ch1 * 16 + ch2;

        buf[(*out_len)] = byte;
        (*out_len)++;
        i += 2;
    }
    buf[(*out_len)] = 0;
    *bin = buf;

    return 0;
}

#include <assert.h>

int
main(void)
{
    unsigned char *buf;
    int len;
    int rc;

    assert(!strcmp(bin2hex("0aA", 3), "306141"));

    rc = hex2bin(bin2hex("hello", 5), &buf, &len);
    assert(rc == 0);
    assert(!strcmp("hello", buf));

    return 0;
}
