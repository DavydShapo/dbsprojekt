#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

int counter;

char _lock[2];

int lock(long tid)
{
    struct timespec tim, tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 100000L;

    _lock[tid] = 1;
    while (_lock[2 - 1 - tid])
    {
        _lock[tid] = 0;
        nanosleep(&tim, &tim2);
        _lock[tid] = 1;
    }

    return 0;
}

int unlock(long tid)
{
    _lock[tid] = 0;
    return 0;
}

typedef enum
{
    false,
    true
} bool;

struct Car
{
    char name[50];
    bool isCrossing;
};

void *crossingBridgeCar1(void *arg) // funktion, auto fährt 1 sekunde über Brücke
{
    struct timespec tim, tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 10000L;

    struct Car *cars = arg;
    lock(0);
    cars[0].isCrossing = true;
    if ((cars[0].isCrossing == 1) && (cars[1].isCrossing == 1))
    {
        counter++;
    }
    nanosleep(&tim, &tim2);
    cars[0].isCrossing = false;
    unlock(0);
    nanosleep(&tim, &tim2);
    pthread_exit(NULL);
    return NULL;
}

void *crossingBridgeCar2(void *arg) // funktion, auto fährt 1 sekunde über Brücke
{
    struct timespec tim, tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 15000L; // 2 auto etwas langsamer

    struct Car *cars = arg;
    lock(1);
    cars[1].isCrossing = true;
    if ((cars[0].isCrossing == 1) && (cars[1].isCrossing == 1))
    {
        counter++;
    }
    nanosleep(&tim, &tim2);
    cars[1].isCrossing = false;
    unlock(1);
    nanosleep(&tim, &tim2);
    pthread_exit(NULL);
    return NULL;
}
// hier fixxen damit mehrere Argumente gegeben werden!

int main()
{
    counter = 0;

    // Ausgangssituation, Car1 u. Car2 stehen am Anfang der Brücke
    struct Car *car1;
    struct Car *car2;

    car1 = (struct Car *)malloc(sizeof(struct Car));
    car2 = (struct Car *)malloc(sizeof(struct Car));

    strcpy(car1->name, "Car1");
    strcpy(car2->name, "Car2");

    car1->isCrossing = false;
    car2->isCrossing = false;

    struct Car cars[] = {*car1, *car2};
    //  threads Car1, Car2 wenn Brücke crossed

    pthread_t threadCar1;
    pthread_t threadCar2;

    for (int j = 0; j < 1000; j++)
    {
        pthread_create(&threadCar1, NULL, crossingBridgeCar1, cars);
        pthread_create(&threadCar2, NULL, crossingBridgeCar2, cars);

        pthread_join(threadCar1, NULL);
        pthread_join(threadCar2, NULL);
    }

    printf("Crashed: %d times \n", counter);

    return 0;
}
