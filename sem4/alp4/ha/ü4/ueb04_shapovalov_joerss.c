#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_Philosophers 5

int forks[NUM_Philosophers];
int philosophers[NUM_Philosophers];

int counterVerklemmung = 0;

int allPhilosophersAte()
{
    int sum = 0;
    for (int i = 0; i < NUM_Philosophers; i++)
    {
        sum += philosophers[i];
    }
    return sum;
}

void *eatAndThink(void *threadid)
{
    int sum = allPhilosophersAte();

    if (sum != NUM_Philosophers)
    {
        for (int i = 0; i < NUM_Philosophers; i++)
        {
            if ((philosophers[i] == 0) && ((i + 1) != NUM_Philosophers))
            {
                philosophers[i] = 1;
                printf("thinking... \n");
                sleep(1);
                if ((forks[i] == 0) && (forks[i + 1] == 0))
                {
                    forks[i] = 1;
                    forks[i + 1] = 1;
                    printf("eating... \n");
                    sleep(1);
                    forks[i] = 0;
                    forks[i + 1] = 0;
                    printf("finished \n");
                    break;
                }
                else
                {
                    forks[i] = 1;
                    forks[i + 1] = 1;
                    printf("eating... But with a Fork from someone else => Verklemmung \n");
                    counterVerklemmung += 1;
                    sleep(1);
                    forks[i] = 0;
                    forks[i + 1] = 0;
                    printf("finished \n");
                    break;
                }
            }
            else if ((philosophers[i] == 0) && ((i + 1) == NUM_Philosophers))
            {
                philosophers[i] = 1;
                printf("thinking... \n");
                sleep(1);
                if ((forks[i] == 0) && (forks[0] == 0))
                {
                    forks[i] = 1;
                    forks[0] = 1;
                    printf("eating... \n");
                    sleep(1);
                    forks[i] = 0;
                    forks[0] = 0;
                    printf("finished \n");
                    break;
                }
                else
                {
                    forks[i] = 1;
                    forks[0] = 1;
                    printf("eating... But with a Fork from someone else => Verklemmung \n");
                    counterVerklemmung += 1;
                    sleep(1);
                    forks[i] = 0;
                    forks[0] = 0;
                    printf("finished \n");
                    break;
                }
            }
        }
    }

    return NULL;
}

int main()
{
    printf("Philosopher: %d \n", NUM_Philosophers);

    for (int i = 0; i < NUM_Philosophers; i++)
    {
        forks[i] = 0;
        printf("F: %d ", forks[i]);
    }

    for (int i = 0; i < NUM_Philosophers; i++)
    {
        philosophers[i] = 0;
        printf("P: %d ", philosophers[i]);
    }

    pthread_t threads[NUM_Philosophers];
    long t;
    int rc;

    for (t = 0; t < NUM_Philosophers; t++)
    {
        rc = pthread_create(&threads[t], NULL, eatAndThink, (void *)t);
        if (rc)
        {
            printf("ERROR; return code from pthread_create () is %d\n", rc);
            exit(-1);
        }
    }
    for (t = 0; t < NUM_Philosophers; t++)
    {
        pthread_join(threads[t], NULL);
    }

    printf("Verklemmungen: %d \n", counterVerklemmung);

    for (int i = 0; i < NUM_Philosophers; i++)
    {
        printf("F: %d ", forks[i]);
    }

    for (int i = 0; i < NUM_Philosophers; i++)
    {
        printf("P: %d ", philosophers[i]);
    }
    pthread_exit(NULL);
    return 0;
}