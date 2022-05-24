#include <stdlib.h>
#include <time.h>
#include <stdio.h>

// Folie 2-23

int foo2(int a, int b)
{
    return a * b;
}
int foo1(void)
{
    int a = 0;
    int b = 0;
    a = 2;
    b = 3;
    a = foo2(a, b);
    return a;
}

// Folie 2-34

int main(void)
{
    printf("Beispiel aus Folie 2-23: %d \n", foo1());
    printf("Beispiel aus Folie 2-34: \n");
    int random_nr = 0;
    srand((unsigned)time(NULL));
    random_nr = rand();
    if (random_nr < RAND_MAX / 2)
        printf("The random number is in the lower half!! \n");
    else
        printf("The random number is in the upper half! \n");
    return 0;
}