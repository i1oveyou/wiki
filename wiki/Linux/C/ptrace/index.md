

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ptrace.h>
#include <errno.h>

int main() {
    pid_t father_pid, child_pid;

    // 获取父进程 PID
    father_pid = getpid();
    printf("[father]: My PID is %d\n", father_pid);

    // 创建子进程
    child_pid = fork();
    if (child_pid == 0) { // 子进程
        printf("[child]: My PID is %d, attaching to father process %d\n", getpid(), father_pid);

        // 尝试附加到父进程
        if (ptrace(PTRACE_ATTACH, father_pid, 0, 0) == -1) {
            printf("[child]: Failed to attach to father process, error: %d (%s)\n", errno, strerror(errno));
            return 1;
        }

        printf("[child]: Successfully attached to father process %d\n", father_pid);

        // 等待父进程停止
        int status;
        waitpid(father_pid, &status, 0);
        printf("[child]: Father process %d has stopped\n", father_pid);

        // 在这里你可以对父进程进行调试或者其他操作

        // 最后,分离父进程
        if (ptrace(PTRACE_DETACH, father_pid, 0, 0) == -1) {
            printf("[child]: Failed to detach from father process, error: %d (%s)\n", errno, strerror(errno));
            return 1;
        }

        printf("[child]: Successfully detached from father process %d\n", father_pid);
    } else if (child_pid > 0) { // 父进程
        printf("[father]: Waiting for child process %d to attach\n", child_pid);
        int status;
        waitpid(child_pid, &status, 0);
        printf("[father]: Child process %d has attached\n", child_pid);

        // 在这里你可以继续执行父进程的代码
    } else { // 创建子进程失败
        printf("[father]: Failed to create child process\n");
        return 1;
    }

    return 0;
}
```



调试发现如下：

IDA 调试父进程，子进程无法attach。