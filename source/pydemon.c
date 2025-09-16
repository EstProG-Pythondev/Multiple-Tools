#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <sys/inotify.h>
#include <libgen.h>
#include <limits.h>

#define EVENT_SIZE (sizeof(struct inotify_event))
#define BUF_LEN (1024 * (EVENT_SIZE + 16))

typedef struct {
    char *filepath;    // absolute path
    char *filename;    // basename only
    char *dirpath;     // directory of file
    pid_t process_id;
} Handler;

void *watch_directory(void *arg) {
    Handler *handler = (Handler *)arg;
    int fd = inotify_init();
    if (fd < 0) {
        perror("inotify_init");
        return NULL;
    }

    int wd = inotify_add_watch(fd, handler->dirpath, IN_MODIFY);
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

            if ((event->mask & IN_MODIFY) && event->len > 0) {
                if (strcmp(event->name, handler->filename) == 0) {
                    printf("File %s modified. Restarting...\n", handler->filepath);
                    kill(handler->process_id, SIGTERM);
                    handler->process_id = fork();
                    if (handler->process_id == 0) {
                        execlp("python", "python", handler->filepath, NULL);
                        perror("execlp");
                        exit(1);
                    }
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
    char input[PATH_MAX];
    printf("Masukkan path file Python yang ingin dijalankan: ");
    scanf("%1023s", input);

    char abs_path[PATH_MAX];
    if (realpath(input, abs_path) == NULL) {
        perror("realpath");
        return 1;
    }

    Handler handler;
    handler.filepath = strdup(abs_path);
    handler.filename = strdup(basename(abs_path));
    handler.dirpath  = strdup(dirname(abs_path));

    if (!handler.filepath || !handler.filename || !handler.dirpath) {
        perror("strdup");
        return 1;
    }

    // Jalankan pertama kali
    handler.process_id = fork();
    if (handler.process_id == 0) {
        execlp("python", "python", handler.filepath, NULL);
        perror("execlp");
        exit(1);
    }

    // Thread watcher
    pthread_t thread_id;
    pthread_create(&thread_id, NULL, watch_directory, (void *)&handler);
    pthread_join(thread_id, NULL);

    free(handler.filepath);
    free(handler.filename);
    free(handler.dirpath);

    return 0;
}	
