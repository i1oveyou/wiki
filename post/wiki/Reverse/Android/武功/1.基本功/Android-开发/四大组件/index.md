

四大组件分别是Activity、Service、BroadcastReceiver和ContentProvider

1，Activity是所有Android应用程序的门面，凡是在应用中你看得到的东西，都是放在Activity中的

2，Service就比较低调了，你无法看到它，但它会在后台默默地运行，即使用户退出了应用，Service仍然是可以继续运行的

3，BroadcastReceiver允许你的应用接收来自各处的广播消息，比如电话、短信等，当然，你的应用也可以向外发出广播消息

4，ContentProvider则为应用程序之间共享数据提供了可能，比如你想要读取系统通讯录中的联系人，就需要通过ContentProvider来实现