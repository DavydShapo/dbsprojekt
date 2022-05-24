#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

#define NUM_THREADS 10

long array[NUM_THREADS];

int counter;

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

pthread_mutex_t lock;

void *crossingBridgeCar(void *arg) // funktion, auto fährt 1 sekunde über Brücke
{

    long tc = array[0];
    pthread_mutex_lock(&lock);

    for (long i = 0; i < sizeof(array) / sizeof(array[0]) - 1; i++)
    {
        if (sizeof(array) / sizeof(array[0]) <= 1)
        {
        }
        else
        {
            array[i] = array[i + 1];
        }
    }

    struct timespec tim, tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 10000L;

    struct Car *cars = arg;

    cars[tc].isCrossing = true;

    for (int z = 0; z < NUM_THREADS; z++)
    {
        if (tc == z)
        {
        }
        else
        {
            if ((cars[tc].isCrossing == 1) && (cars[z].isCrossing == 1))
            {
                counter++;
            }
        }
    }
    nanosleep(&tim, &tim2);
    cars[tc].isCrossing = false;
    pthread_mutex_unlock(&lock);
    nanosleep(&tim, &tim2);
    pthread_exit(NULL);
    return NULL;
}

// hier fixxen damit mehrere Argumente gegeben werden!

int main()
{
    counter = 0;
    pthread_mutex_init(&lock, NULL);

    // Ausgangssituation, Car1 u. Car2 stehen am Anfang der Brücke

    struct Car *car[NUM_THREADS];
    struct Car cars[NUM_THREADS] = {};

    for (int i = 0; i < NUM_THREADS; i++)
    {
        car[i] = (struct Car *)malloc(sizeof(struct Car));
        char a[50];
        char b[50];
        sprintf(a, "Car%d", i);
        strcpy(b, a);
        strcpy(car[i]->name, b);
        car[i]->isCrossing = false;
        cars[i] = *car[i];
    }

    // Makefiles machen wenn aufgabe 3 richtig, dann nur das abgeben, wenn nicht können alle 3 einzelne Dateien
    // seien              make test damit es alles runt
    //  ./a.out 4
    //  ./a.out 2
    // ./a.out -1

    pthread_t thread[NUM_THREADS];

    int rc;
    long t;

    for (int b = 0; b < 1000; b++)
    {
        for (long i = 0; i < NUM_THREADS; i++)
        {
            array[i] = i;
        };

        for (t = 0; t < NUM_THREADS; t++)
        {
            rc = pthread_create(&thread[t], NULL, crossingBridgeCar, cars);
            if (rc)
            {
                printf("Error %d", rc);
                exit(-1);
            }
        }

        for (int l = 0; l < NUM_THREADS; l++)
        {
            pthread_join(thread[l], NULL);
        }
    }

    printf("Crashed: %d times", counter);

    pthread_exit(NULL);

    return 0;
}
