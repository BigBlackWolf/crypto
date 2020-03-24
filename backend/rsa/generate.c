#include <stdlib.h>

unsigned gcd(unsigned a, unsigned b) {
    if (a < 0)
        a = abs(a);
    while (a != 0 && b != 0) {
        if (a > b)
            a -= b;
        else
            b -= a;
    }
    return (a != 0 ? a : b);
}