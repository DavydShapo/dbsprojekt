#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>

#define NUM_THREADS 100 // Anzahl der Autos
#define MAX_BRIDGE 100000
#define DURATION_BRIDGE 1000 //überfahren der Brücke dauert 1 Mikrosekunde

struct bridge
{
    int brCounter; // wie oft ist Brücke bereits befahren worden
    bool brUsed;   // wird Brücke von Auto derzeit befahren
};

// Initialisieren der "Brücke"
struct bridge Bridge = {0, false}; // Brücke wurde 0 mal überfahren, Kein Auto auf Brücke

int iAccCounter = 0;

pthread_mutex_t lock;

void *car(void *threadid)
{
    srand(time(NULL));

    long tid = (long)threadid;

    while (Bridge.brCounter < MAX_BRIDGE)
    {
        long lRandomWait = (rand() % 100) * 10000;
        nanosleep((const struct timespec[]){{0, lRandomWait}}, NULL);

        // lock
        pthread_mutex_lock(&lock);

        //Überprüfen, ob Brücke besetzt -> Unfall passiert
        if (Bridge.brUsed)
        {
            iAccCounter++;
        }

        Bridge.brUsed = true;
        nanosleep((const struct timespec[]){{0, DURATION_BRIDGE}}, NULL);
        Bridge.brUsed = false;

        (Bridge.brCounter)++;
        //unlock
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void)
{
    pthread_t threads[NUM_THREADS];
    long t;
    int rc;

    pthread_mutex_init(&lock, NULL);

    for (t = 0; t < NUM_THREADS; t++)
    {
        rc = pthread_create(&threads[t], NULL, car, (void *)t);
        if (rc)
        {
            printf("ERROR; return code from pthread_create () is %d\n", rc);
            exit(-1);
        }
    }
    for (t = 0; t < NUM_THREADS; t++)
    {
        pthread_join(threads[t], NULL);
    }
    printf("Es sind bei %d Brückenüberfahrungen, %d Unfälle passiert \n", MAX_BRIDGE, iAccCounter);
    pthread_mutex_destroy(&lock);
    pthread_exit(NULL);
}
