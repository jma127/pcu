/**
 * $USER
 * $SRCFILE
 */

#include <assert.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long long int lli;

int gInt () {
    int i;
    scanf("%d", &i);
    return i;
}

lli gLong () {
    lli i;
    scanf("%lld", &i);
    return i;
}

double gDouble () {
    double i;
    scanf("%lf", &i);
    return i;
}

void quit () {
    fflush(stdout);
    exit(0);
}

int main (int argc, char ** argv) {
    quit();
}