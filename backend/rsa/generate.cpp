#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <random>
#include <cmath>


int gcd(int a, int b) {
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


int* bezout_recursive (int a, int b) {
    int *yxg = new int[3];
    if (b == 0) {
        yxg[0] = 1;
        yxg[1] = 0;
        yxg[2] = a;
        return yxg;
    }
    yxg = bezout_recursive(b, a % b);
    yxg[1] = yxg[1] - int(a / b) * yxg[1];
    return yxg;
}

bool pascal(int n, int limit=128) {
    std::vector<int> eratos{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,  113, 127};
    std::vector<std::string> numbers;
    return false;
}

int test(int a, int b, int mod) {
    int c = 1;
    for (int i=1; i < b; i++)
        c = (c * b) % mod;
    return c;
}

bool miller(int p) {
    int d = p - 1;
    int s = 0;
    int x = rand() % d + 2;
    while (d % 2 == 0) {
        d = int(d / 2);
        std::cout << d << std::endl;
        s++;
    }
    if (gcd(x, p) != 1)
        return false;

    int r = test(x, d, p);
//    int r = int(pow(x, d)) % p;
    std::cout << "asd";
    if (r != 1) {
        for (int i = 1; i < s; i++) {
            if (r == 1)
                return false;
            else
                r = (r ^ 2) % p;
        if (r != -1)
            return false;
        }
    }
    return true;
}


long int generate_random(int start, int stop=1000000000) {
    std::random_device rd;
    std::default_random_engine generator(rd());
    std::uniform_int_distribution<long long unsigned> distribution(start, stop);

    long int result = distribution(generator);
    return result;
}

int easy_number(int length) {
    int test;
    while (true) {
        test = generate_random(100, 2^16);
        std::cout << test << " << test \n";
        if (miller(test))
            break;
    }
    std::cout << "returned";
    return test;
}


int generated(int length) {
    int p = easy_number(32);
    int q = easy_number(32);
    int n = p * q;
    int oiler = (p - 1) * (q - 1);
    int e, d, counter = 1;
    while (true) {
        e = std::rand() % oiler + 2;
        if (gcd(e, oiler) == 1)
            break;

    d = bezout_recursive(e, oiler)[0];
    if (d < 0)
        d += oiler;
    }
    return e;
}

//int main() {
//    std::srand((int)time(0));
//    bool c = generated(128);
//    std::cout << "c = " << int(c);
//    std::cout << std::endl;
//    return 0;
//}
