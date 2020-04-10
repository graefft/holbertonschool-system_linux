#ifndef __SIGNALS_H__
#define __SIGNALS_H__

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

int handle_signal(void);
void my_handler(int sig);
void (*current_handler_signal(void))(int);
int handle_sigaction(void);
void (*current_handler_sigaction(void))(int);
int trace_signal_sender(void);
void trace_handler(int sig, siginfo_t *siginfo, void *context);
int pid_exist(pid_t pid);

#endif /* __SIGNALS_H__ */