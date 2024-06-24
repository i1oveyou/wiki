---
title: wiki-Reverse-elfRe-秘籍-防守-反调试大法-ptrace-基本功
---
# attach

A attach B



A:  A发起**ptrace(PTRACE_ATTACH,)**, 然后进入**wait**状态

B: 进入暂停状态, 发一个信号给A

A: 收到信号后,wait结束, B继续保持暂停状态

A: **ptrace(PTRACE_CONT,** B继续运行



> summary

B进程不需要做什么. 等待被调试即可



如果我们对B进行 CTRL+C, 此刻A会受到信号

如果A的处理是PTRACE_CONT, 那么B会继续正常运行,不会退出

如果A进程退出, B进程貌似不受影响



### 案例1





```c
//#include <jni.h>
#include <stdio.h>
#include <string.h>
#include <sys/ptrace.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/wait.h>

static int child_pid;

void* monitor_pid(void *) {
    //only works when target-sDK below 28, now removed
//    int status;
//
//    waitpid(child_pid, &status, 0);
//
//    if (status != 11) {
//
//        // If this is a release build, the child will segfault (status 11). Otherwise, waitpid() should never return.
//
//        goodbye(); // Commit seppuku
//    }

    pthread_exit(NULL);

}

void   anti_debug() {

    child_pid = fork();

    if (child_pid == 0)
    {
        int ppid = getppid();

        int status;

        if (ptrace(PTRACE_ATTACH, ppid, NULL, NULL) == 0)
        {
            waitpid(ppid, &status, 0);

            ptrace(PTRACE_CONT, ppid, NULL, NULL);

            while (waitpid(ppid, &status, 0)) {

                if (WIFSTOPPED(status)) {
                    // If parent stops, tell it to resume.
                    ptrace(PTRACE_CONT, ppid, NULL, NULL);
                } else {
                    // Parent has exited for some reason.
                    _exit(0);
                }
            }
        }

    } else {
        pthread_t t;

        // Start the monitoring thread

        pthread_create(&t, NULL, monitor_pid, (void *)NULL);
    }
}


int main(){
	int i;
	printf("hi, i am %d \n", getppid());
	anti_debug();
	printf("now, i am %d \n", getppid());
	while(1){
		i=i;
		sleep(3);
	}
	return 0;
}

```



### 案例2

在 Android-UnCrackable-L3 有应用

在案例1的基础上,monitor_pid函数发生了改变



```c
 void *monitor_pid(void *) {

    int status;

    waitpid(child_pid, &status, 0);

    if (status != 11) {

        // If this is a release build, the child will segfault (status 11). Otherwise, waitpid() should never return.

        _exit(0); // Commit seppuku
    }

    pthread_exit(NULL);

}
```



