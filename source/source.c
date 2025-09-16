#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <sys/inotify.h>

#define EVENT_SIZE (sizeof(struct inotify_event))
#define BUF_LEN (1024 * (EVENT_SIZE + 16))

typedef struct {
    char *filename;
    pid_t process_id;
} Handler;

void *watch_directory(void *arg) {
    Handler *handler = (Handler *)arg;
    int fd = inotify_init();
    if (fd < 0) {
        perror("inotify_init");
        return NULL;
    }

    int wd = inotify_add_watch(fd, handler->filename, IN_MODIFY);
    if (wd < 0) {
        perror("inotify_add_watch");
        close(fd);
        return NULL;
    }

    char buffer[BUF_LEN];
    while (1) {
        int length = read(fd, buffer, BUF_LEN);
        if (length < 0) {
            perror("read");
            break;
        }

        for (int i = 0; i < length;) {
            struct inotify_event *event = (struct inotify_event *)&buffer[i];

            if (event->mask & IN_MODIFY) {
                printf("File %s modified. Restarting...\n", handler->filename);
                kill(handler->process_id, SIGTERM);
                handler->process_id = fork();
                if (handler->process_id == 0) {
                    execlp("python", "python", handler->filename, NULL);
                    perror("execlp");
                    exit(1);
                }
            }

            i += EVENT_SIZE + event->len;
        }
    }

    inotify_rm_watch(fd, wd);
    close(fd);
    return NULL;
}

int main() {
    char filename[256];
    printf("Masukkan nama file Python yang ingin dijalankan: ");
    scanf("%255s", filename);

    Handler handler;
    handler.filename = strdup(filename); // alokasi dinamis
    if (!handler.filename) {
        perror("strdup");
        return 1;
    }

    handler.process_id = fork();
    if (handler.process_id == 0) {
        execlp("python", "python", handler.filename, NULL);
        perror("execlp");
        exit(1);
    }

    pthread_t thread_id;
    pthread_create(&thread_id, NULL, watch_directory, (void *)&handler);
    pthread_join(thread_id, NULL);

    free(handler.filename);
    return 0;
}