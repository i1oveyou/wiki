> 杂七杂八



# 面向对象

public不多说

private就是不对外访问

protect也是不对外访问,,,区别于private体现在在继承上

也就是子类可以访问父类的public和protect,,但是不能访问private

说一下关于继承吧,,,子类可以通过3种方式去继承父类的一些东西

比如提供public,private,protect的方式去继承父类的成员和函数

在子类对父类的访问上,,,一直都是子类可以访问父类的public,protect,,但是不可以访问private

在对外访问上,,,该怎么样就怎么样...

比如你是private,protect继承,那么父类的所有都不对外开放

如果你是public继承,,,只有父类的public对外开放



# C++和C函数相互调用

- C++调用C的函数

mm.h

```c
void showMsg2(char* lpData, int shellcode_size);
```

mm.c

```c
void showMsg2(char* lpData, int shellcode_size){
	//....
}
```

main.cpp

```c
extern "C"
{
	#include "mm.h"
}
//
int main{

//然后就是正常调用即可
}
```



# 关于malloc和new

这里我通过IDA跟踪`malloc`和`new`的调用过程，如下所示

```
malloc -> _nh_malloc_dbg -> _heap_alloc_dbg -> _heap_alloc_base -> HeapAlloc
new -> _nh_malloc -> _nh_malloc_dbg -> _heap_alloc_dbg -> _heap_alloc_base -> HeapAlloc
```

貌似,,在大多数情况下

`malloc`和`new` 不会实际上分配内存,,,,

而是从已经分配的内存中取出一块小的内存...

