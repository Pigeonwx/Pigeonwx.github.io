[TOC]

# JAVA 并发

> 参考资料如下：
>
> http://concurrent.redspider.group/
>
> https://mynamelancelot.github.io/java/concurrent.html#park--unpark

# 一、多线程基础



# 二、 多线程的实现

### 2.1 Thread 抽象类

> 通过继承Thread类来创建并启动线程的步骤如下：
>
> 1. 定义Thread类的子类，并重写该类的run()方法，该run()方法将作为线程执行体。
> 2. 创建Thread子类的实例，即创建了线程对象。
> 3. 调用线程对象的start()方法来启动该线程。

Thread类常用静态方法：

```java
currentThread()：返回当前正在执行的线程；
interrupted()：返回当前执行的线程是否已经被中断；
sleep(long millis)：使当前执行的线程睡眠多少毫秒数；
yield()：使当前执行的线程自愿暂时放弃对处理器的使用权并允许其他线程执行；
```

Thread类常用实例方法：

```java
getId()：返回该线程的id；
getName()：返回该线程的名字；
getPriority()：返回该线程的优先级；
interrupt()：使该线程中断；
isInterrupted()：返回该线程是否被中断；
isAlive()：返回该线程是否处于活动状态；
isDaemon()：返回该线程是否是守护线程；
setDaemon(boolean on)：将该线程标记为守护线程或用户线程，如果不标记默认是非守护线程；
setName(String name)：设置该线程的名字；
setPriority(int newPriority)：改变该线程的优先级；
join()：等待该线程终止；
join(long millis)：等待该线程终止,至多等待多少毫秒数。
```

### 2.2.2 Runnable 接口 

通过实现Runnable接口来创建并启动线程的步骤如下：

1. 定义Runnable接口的实现类，并实现该接口的run()方法，该run()方法将作为线程执行体。
2. 创建Runnable实现类的实例，并将其作为Thread的target来创建Thread对象，Thread对象为线程对象。
3. 调用线程对象的start()方法来启动该线程。

### 2.2.3 Callable 接口

通过实现Callable接口来创建并启动线程的步骤如下：

1. 创建Callable接口的实现类，并实现call()方法，该call()方法将作为线程执行体，且该call()方法有返回值。然后再创建Callable实现类的实例。
2. 使用FutureTask类来包装Callable对象，该FutureTask对象封装了该Callable对象的call()方法的返回值。
3. 使用FutureTask对象作为Thread对象的target创建并启动新线程。
4. 调用FutureTask对象的get()方法来获得子线程执行结束后的返回值。

```java
class MyTask implements Callable<Integer> {  
    private int upperBounds;  
      
    public MyTask(int upperBounds) {  
        this.upperBounds = upperBounds;  
    }  
      
    @Override  
    public Integer call() throws Exception {  
        int sum = 0;   
        for(int i = 1; i <= upperBounds; i++) {  
            sum += i;  
        }  
        return sum;  
    }  
      
}  
public class Test {  
    public static void main(String[] args) throws Exception {  
        List<Future<Integer>> list = new ArrayList<>();  
        ExecutorService service = Executors.newFixedThreadPool(10);  
        for(int i = 0; i < 10; i++) {  
            list.add(service.submit(new MyTask((int) (Math.random() * 100))));  
        }  
          
        int sum = 0;  
        for(Future<Integer> future : list) {  
            while(!future.isDone()) ;  
            sum += future.get();  
        }            
        System.out.println(sum);  
    }  
}  
```



### 2.2.4 Future 接口

当使用 `Future` 时，通常包括以下几个步骤：

1. **创建线程池**：首先，需要创建一个线程池，用于执行异步任务。可以使用 `Executors` 工厂类来创建不同类型的线程池，如 `newFixedThreadPool`、`newCachedThreadPool` 等。

2. **提交任务**：将需要执行的任务封装成 `Callable` 或 `Runnable` 对象，并通过线程池的 `submit` 方法提交任务。`submit` 方法会返回一个 `Future` 对象，用于获取任务执行结果。

3. **执行其他任务**：可以继续执行其他任务，而不必等待异步任务的执行结果。这是 `Future` 的一个重要特性，允许主线程在等待异步任务完成的同时执行其他操作。

4. **获取任务结果**：当需要获取异步任务的执行结果时，可以调用 `Future` 对象的 `get` 方法。这个方法会阻塞当前线程，直到任务执行完成并返回结果。可以选择传入超时参数，避免无限期地等待任务完成。

5. **关闭线程池**：当不再需要执行任务时，应该及时关闭线程池，释放资源。可以调用线程池的 `shutdown` 方法来关闭线程池。

---

**代码示例**：

```java
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        // 创建一个线程池
        ExecutorService executor = Executors.newCachedThreadPool();

        // 提交一个 Callable 任务给线程池，得到一个 Future 对象
        Future<Integer> future = executor.submit(new Callable<Integer>() {
            @Override
            public Integer call() throws Exception {
                // 模拟一个耗时的计算任务
                Thread.sleep(1000);
                return 42; // 返回计算结果
            }
        });

        // 可以继续执行其他任务，这里假设在等待计算结果的过程中可以做一些其他操作
        System.out.println("Do something else while waiting for the result...");

        // 阻塞等待任务执行结果
        int result = future.get(); // 这里会阻塞直到任务执行完成并返回结果
        System.out.println("Result: " + result);

        // 关闭线程池
        executor.shutdown();
    }
}
```

在这个示例中，我们首先创建了一个线程池，并且通过 `executor.submit(Callable)` 方法提交了一个 `Callable` 任务给线程池。这个方法会返回一个 `Future` 对象，通过这个对象可以获取任务执行的结果。然后我们可以继续执行其他任务，而不必等待计算结果。最后，我们调用 `future.get()` 方法来获取任务执行的结果，这个方法会阻塞直到任务执行完成并返回结果。

### 2.2.5 **FutureTask**类

使用 `FutureTask` 可以方便地执行异步任务并获取任务执行结果。以下是使用 `FutureTask` 的一般步骤：

1. **创建任务**：首先，创建一个 `Callable` 或 `Runnable` 对象，表示需要执行的异步任务。

2. **创建 FutureTask 对象**：使用任务对象创建一个 `FutureTask` 对象，将任务对象作为参数传入构造函数。

3. **提交任务**：将 `FutureTask` 对象提交给线程池执行，或者在单独的线程中执行。可以使用 `ExecutorService` 的 `submit()` 方法提交任务，也可以使用 `Thread` 类的 `start()` 方法启动任务线程。

4. **获取任务结果**：可以调用 `FutureTask` 的 `get()` 方法来获取任务执行结果。这个方法会阻塞当前线程，直到任务执行完成并返回结果。可以选择传入超时参数，避免无限期地等待任务完成。

5. **处理任务完成后的操作**：如果需要在任务完成后执行特定的操作，可以重写 `done()` 方法。这个方法会在任务执行完成后自动被调用，可以在其中进行一些清理操作或者通知其他线程。

下面是一个示例代码，演示了如何使用 `FutureTask`：

```java
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        // 创建一个 Callable 对象表示异步任务
        Callable<Integer> task = () -> {
            // 模拟一个耗时的计算任务
            Thread.sleep(1000);
            return 42; // 返回计算结果
        };

        // 创建 FutureTask 对象，并将任务对象作为参数传入构造函数
        FutureTask<Integer> futureTask = new FutureTask<>(task);

        // 提交 FutureTask 对象给线程池执行
        ExecutorService executor = Executors.newCachedThreadPool();
        executor.submit(futureTask);

        // 可以继续执行其他任务，这里假设在等待计算结果的过程中可以做一些其他操作
        System.out.println("Do something else while waiting for the result...");

        // 获取任务执行结果
        int result = futureTask.get(); // 这里会阻塞直到任务执行完成并返回结果
        System.out.println("Result: " + result);

        // 关闭线程池
        executor.shutdown();
    }
}
```

在这个示例中，我们创建了一个 `Callable` 对象表示异步任务，然后将它传入 `FutureTask` 的构造函数创建了一个 `FutureTask` 对象。接着，我们将 `FutureTask` 对象提交给线程池执行，然后可以继续执行其他任务。最后，我们调用 `futureTask.get()` 方法获取任务执行结果。

# 三、 线程

### 2.7.1 线程状态

Java 线程的状态有以下几种：

1. **新建（New）**：当线程对象被创建但还没有调用 `start()` 方法时，线程处于新建状态。
2. **可运行（Runnable）**：线程对象调用了 `start()` 方法之后，线程进入可运行状态。此时，线程可以被线程调度器选中执行，也可能处于等待执行的状态。
3. **运行（Running）**：线程被线程调度器选中执行，处于运行状态。此时，线程正在执行任务代码。
4. **阻塞（Blocked）**：线程因为某些原因放弃了 CPU 使用权，暂时停止执行，进入阻塞状态。常见的情况包括等待某个资源、等待 I/O 操作完成等。
5. **等待（Waiting）**：线程进入等待状态，等待其他线程发出通知或中断。
6. **超时等待（Timed Waiting）**：线程进入等待状态，并指定了等待的时间，在等待一定时间后自动返回。
7. **终止（Terminated）**：线程执行完任务代码后，或者因为异常而提前退出，线程处于终止状态。

Java 线程在不同状态之间的切换通常会通过线程调度器来实现。

Java 中常见的线程队列有：

1. **就绪队列（Ready Queue）**：存放处于可运行状态的线程，等待被线程调度器选中执行。
2. **阻塞队列（Blocked Queue）**：存放因为某些原因而暂时停止执行的线程，等待被唤醒或者条件满足后重新进入就绪队列。
3. **等待队列（Waiting Queue）**：存放因为调用了 `wait()`、`sleep()` 或者 `join()` 方法而进入等待状态的线程，等待其他线程的通知或者等待指定的时间后重新进入就绪队列。
4. **线程池队列（Thread Pool Queue）**：存放线程池中等待执行的任务，等待线程池中的工作线程取出执行。

这些队列在 Java 线程的管理和调度中起着重要的作用，有助于实现多线程的协作和资源共享。

### 2.7.2 守护线程和用户线程

> Java中有两类线程：User Thread(用户线程)、Daemon Thread(守护线程)
>
> - 用户线程即运行在前台的线程，而守护线程是运行在后台的线程。 守护线程作用是为其他前台线程的运行提供便利服务，而且仅在普通、非守护线程仍然运行时才需要，比如垃圾回收线程就是一个守护线程。当JVM检测仅剩一个守护线程，而用户线程都已经退出运行时，JVM就会退出，因为如果没有了用户线程，也就没有继续运行程序的必要了。如果有非守护线程仍然活着，JVM就不会退出
> - 守护线程并非只有虚拟机内部提供，用户在编写程序时也可以自己设置守护线程。用户可以用Thread的setDaemon(true)方法设置当前线程为守护线程。
> - 虽然守护线程可能非常有用，但必须小心确保其它所有非守护线程消亡时，不会由于它的终止而产生任何危害。因为你不可能知道在所有的用户线程退出运行前，守护线程是否已经完成了预期的服务任务。一旦所有的用户线程退出了，虚拟机也就退出运行了。因此，不要再守护线程中执行业务逻辑操作(比如对数据的读写等)。



**注意点**

- setDaemon(true)必须在调用线程的start()方法之前设置，否则会跑出IllegalThreadStateException异常。
- 在守护线程中产生的新线程也是守护线程
- 不要认为所有的应用都可以分配守护线程来进行服务，比如读写操作或者计算逻辑。





### 2.7.3 线程阻塞

**线程可以阻塞于四种状态**

1. 当线程执行Thread.sleep()时，它一直阻塞到指定的毫秒时间之后，或者阻塞被另一个线程打断
2. 当线程碰到一条wait()语句时，它会一直阻塞到接到通知(notify())、被中断或经过了指定毫秒 时间为止(若指定了超时值的话)
3. 线程阻塞与不同的I/O的方式有多种。常见的一种方式是InputStream的read()方法，该方法一直阻塞到从流中读取一个字节的数据为止，它可以无限阻塞，因此不能指定超时时间
4. 线程也可以阻塞等待获取某个对象锁的排它性访问权限(即等待获得synchronized语句必须的锁时阻塞)

并非所有的阻塞状态都是可中断的，以上阻塞状态的前两种可以被中断，后两种不会对中断做出反应。



### 2.7.4 **中断阻塞线程**

- 当一个线程处于阻塞状态（如等待、休眠、阻塞）时，如果它被中断，通常会抛出 `InterruptedException` 异常。线程的对象锁不会因为线程被中断而自动释放。

- 线程中断并不会自动释放对象锁，因为在大多数情况下，线程只是处于等待状态，希望能够继续执行。如果线程在等待状态被中断，它会收到 `InterruptedException` 异常，然后可以根据需要执行一些清理工作并决定是否继续等待或退出。如果线程拥有某个对象的锁，并且在同步代码块中等待，那么线程不会释放该对象的锁。
- 当一个阻塞线程被中断后，它会从阻塞状态返回到可运行状态（Runnable状态），但它的中断状态会被设置为true。这意味着线程被中断，但并不是立即终止或停止运行。线程将在适当的时机继续执行，但可以根据中断状态的设置来决定是否继续执行或执行其他操作。

### 2.7.6 中断线程

#### 使用interrupt()中断线程

当一个线程运行时，另一个线程可以调用对应的Thread对象的interrupt()方法来中断它，该方法只是在目标线程中设置一个标志，表示它已经被中断，并立即返回。这里需要注意的是，如果只是单纯的调用interrupt()方法，线程并没有实际被中断，会继续往下执行。

```java
public class SleepInterrupt extends Object implements Runnable{

	@Override
	public void run() {
		
		try {
			System.out.println("in run() - about to sleep for 20 seconds");
			Thread.sleep(20000);
			System.out.println("in run() - woke up");
		} catch (InterruptedException e) {
			System.out.println("in run() - interrupted while sleeping");
			//处理完中断异常后，返回到run()方法入口
			//如果没有return,线程不会实际被中断，它会继续打印下面的信息
			return;
		}
		System.out.println("in run() - leaving normally");
	}
	
	public static void main(String[] args) {
		SleepInterrupt si = new SleepInterrupt();
		Thread t = new Thread(si);
		t.start();
		//住线程休眠2秒，从而确保刚才启动的线程有机会执行一段时间
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println("in main() - interrupting other thread"); 
		//中断线程t
		t.interrupt();
		System.out.println("in main() - leaving");
	}

}

```

**运行结果如下**

```java
in run() - about to sleep for 20 seconds
in main() - interrupting other thread
in main() - leaving
in run() - interrupted while sleeping
```





#### 待决中断

> 在上面的例子中，sleep()方法的实现检查到休眠线程被中断，它会相当友好地终止线程，并抛出InterruptedException异常。另外一种情况，如果线程在调用sleep()方法前被中断，那么该中断称为待决中断，它会在刚调用sleep()方法时，立即抛出InterruptedException异常。

**代码示例**

```java
public class PendingInterrupt extends Object{

    public static void main(String[] args) {
        //如果输入了参数，则在main线程中中断当前线程（即main线程）
//        if(args.length > 0){
            Thread.currentThread().interrupt();
//        }
        //获取当前时间
        long startTime = System.currentTimeMillis();
        try {
            Thread.sleep(2000);
            System.out.println("was NOT interrupted");
        } catch (InterruptedException e) {
            System.out.println("was interrupted");
        }
        //计算中间代码执行的时间
        System.out.println("elapsedTime=" + (System.currentTimeMillis() - startTime));
    }
}

```

**输出**

```java
was interrupted
elapsedTime=0
```

这种模式下，main线程中断它自身。除了将中断标志（它是Thread的内部标志）设置为true外，没有其他任何影响。线程被中断了，但main线程仍然运行，main线程继续监视实时时钟，并进入try块，一旦调用sleep()方法，它就会注意到待决中断的存在，并抛出InterruptException。于是执行跳转到catch块，并打印出线程被中断的信息。最后，计算并打印出时间差。



####  isInterrupted()方法判断中断状态

> 可以在Thread对象上调用isInterrupted()方法来检查任何线程的中断状态。这里需要注意：线程一旦被中断，isInterrupted()方法便会返回true，而一旦sleep()方法抛出异常，它将清空中断标志，此时isInterrupted()方法将返回false。

**代码示例**

```java
public class InterruptCheck extends Object{
	
	public static void main(String[] args) {
		Thread t = Thread.currentThread();
		System.out.println("Point A: t.isInterrupted()=" + t.isInterrupted());  
        //待决中断，中断自身  
        t.interrupt();  
        System.out.println("Point B: t.isInterrupted()=" + t.isInterrupted());  
        System.out.println("Point C: t.isInterrupted()=" + t.isInterrupted());  
	
        try {
			Thread.sleep(2000);
			System.out.println("was NOT interrupted");  
		} catch (InterruptedException e) {
			System.out.println("was interrupted");  
		}
        //跑出异常后，会清除中断标志，这里会返回false
        System.out.println("Point D: t.isInterrupted()=" + t.isInterrupted());
	}

}
```

**运行结果**

```java
Point A: t.isInterrupted()=false
Point B: t.isInterrupted()=true
Point C: t.isInterrupted()=true
was interrupted
Point D: t.isInterrupted()=false
```



####  Thread.interrupted()方法判断中断状态

> 可以使用Thread.interrupted()方法来检查当前线程的中断状态（并隐式重置为false）。又由于它是静态方法，因此不能在特定的线程上使用，而只能报告调用它的线程的中断状态，如果线程被中断，而且中断状态尚不清楚，那么，这个方法返回true。与isInterrupted()不同，它将自动重置中断状态为false，第二次调用Thread.interrupted()方法，总是返回false，除非中断了线程。

**代码示例**

```java
public class InterruptReset extends Object{
	
	public static void main(String[] args) {
		System.out.println(  
	            "Point X: Thread.interrupted()=" + Thread.interrupted());  
	        Thread.currentThread().interrupt();  
	        System.out.println(  
	            "Point Y: Thread.interrupted()=" + Thread.interrupted());  
	        System.out.println(  
	            "Point Z: Thread.interrupted()=" + Thread.interrupted());  
	}

}
```

**运行结果**

```java
Point X: Thread.interrupted()=false
Point Y: Thread.interrupted()=true
Point Z: Thread.interrupted()=false
```

### 2.7.7 yield

> - `yield` 是一个静态方法，用于告诉当前线程让出 CPU 时间片，允许其他具有相同优先级的线程运行。
> - 如果没有其他线程处于就绪状态，那么 `yield` 方法没有任何效果。

**代码示例**

```java
public class YieldExample {
    public static void main(String[] args) {
        Thread thread1 = new Thread(new MyRunnable(), "Thread 1");
        Thread thread2 = new Thread(new MyRunnable(), "Thread 2");
        
        thread1.start();
        thread2.start();
    }
}

class MyRunnable implements Runnable {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(Thread.currentThread().getName() + " is running");
            Thread.yield(); // 让出CPU时间片
        }
    }
}
```

**运行结果**

```java
Thread 1 is running
Thread 2 is running
Thread 1 is running
Thread 2 is running
Thread 1 is running
Thread 2 is running
Thread 1 is running
Thread 2 is running
Thread 1 is running
Thread 2 is running
```

### 2.7.8 join

> - `join` 方法用于等待一个线程完成其执行，然后再继续当前线程的执行。
>
> - 调用 `join` 方法的线程会被阻塞，直到被等待的线程执行完成。
>
> - yield vs jion
>
>   - `yield` 不会使当前线程进入等待状态。它只是通知调度器可以选择其他线程执行，但当前线程仍然处于就绪状态，可能随时会再次执行。
>
>   - `join` 会导致主线程进入等待状态，直到指定的线程执行完成才会继续执行。

**代码示例**

```java
public class JoinExample {
    public static void main(String[] args) {
        Thread thread1 = new Thread(new Worker(), "Worker 1");
        Thread thread2 = new Thread(new Worker(), "Worker 2");
        
        thread1.start();
        thread2.start();
        
        try {
            thread1.join(); // 等待Worker 1执行完成
            thread2.join(); // 等待Worker 2执行完成
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("All workers have completed.");
    }
}

class Worker implements Runnable {
    @Override
    public void run() {
        System.out.println(Thread.currentThread().getName() + " is working.");
        try {
            Thread.sleep(1000); // 模拟工作
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

```

**运行结果**

```java
Worker 1 is working.
Worker 2 is working.
All workers have completed.

```

## 

# 四、线程池

**线程池的优势**

- 降低资源消耗。通过重复利用已创建的线程降低线程创建和销毁造成的消耗。
- 提高响应速度。当任务到达时，任务可以不需要的等到线程创建就能立即执行。
- 提高线程的可管理性。线程是稀缺资源，如果无限制的创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一的分配，调优和监控。

### 使用原始API创建线程池

```java
/**
 * corePoolSize:线程池的核心大小，当提交一个任务到线程池时，线程池会创建一个线程来执行任务
 *              即使其他空闲的基本线程能够执行新任务也会创建线程，如需要执行的任务数大于线
 *              程池基本大小时就不再创建。如果调用了线程池的prestartAllCoreThreads()方法
 *              线程池会提前创建并启动所有基本线程。
 * maximumPoolSize:线程池最大大小，线程池允许创建的最大线程数。如果队列满了，并且已创建的线程数
 *                 小于最大线程数大于等于核心线程数，则线程池会再创建新的线程执行任务。如果使用
 *                 了无界的任务队列这个参数就没什么效果。
 * keepAliveTime:救急线程活动保持时间，线程池的工作线程空闲后，保持存活的时间。所以如果任务很多
 *               并且每个任务执行的时间比较短，可以调大这个时间，提高线程的利用率。
 * TimeUnit:救急线程活动保持时间的单位，可选的单位有天(DAYS)，小时(HOURS)，分钟(MINUTES)，
 *          毫秒(MILLISECONDS)，微秒(MICROSECONDS, 千分之一毫秒)和毫微秒(NANOSECONDS, 
 *          千分之一微秒)
 * workQueue:任务对列，用于保存等待执行的任务的阻塞队列
 *           - ArrayBlockingQueue：基于数组结构的有界阻塞队列
 *           - LinkedBlockingQueue：基于链表的阻塞队列,如果没构造函数没传入队列大小则为无界队列
 *                                  Executors.newFixedThreadPool()使用了这个队列
 *           - SynchronousQueue：一个不存储元素的阻塞队列。每个插入操作必须等到另一个线程调用
 *                               移除操作，否则插入操作一直处于阻塞状态
 *                               Executors.newCachedThreadPool使用了这个队列
 *           - PriorityBlockingQueue：个具有优先级得无限阻塞队列
 * threadFactory:用于设置创建线程的工厂，可以通过线程工厂给每个创建出来的线程设置更有意义的名字，
 *               Debug和定位问题时非常有帮助。
 * handler:当队列和线程池都满了，必须采取一种策略处理提交的新任务。
 *         - AbortPolicy：默认策略，无法处理新任务时抛出异常
 *         - CallerRunsPolicy：使用调用者所在线程来运行任务
 *         - DiscardOldestPolicy：丢弃队列里最近的一个任务，并执行当前任务
 *         - DiscardPolicy：不处理，丢弃掉
 */
public ThreadPoolExecutor(int corePoolSize, 
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler);
```

- 线程池源代码概览

```java
public class ThreadPoolExecutor extends AbstractExecutorService {

  public void execute(Runnable command) {
    if (command == null)
      throw new NullPointerException();
    // 获取线程池控制状态
    int c = ctl.get();
    if (workerCountOf(c) < corePoolSize) { // worker数量小于corePoolSize
      if (addWorker(command, true)) // 添加worker
        return;
      // 不成功则再次获取线程池控制状态
      c = ctl.get();
    }
    // 线程池处于RUNNING状态，将用户自定义的Runnable对象添加进workQueue队列
    if (isRunning(c) && workQueue.offer(command)) { 
      // 再次检查，获取线程池控制状态
      int recheck = ctl.get();
      // 线程池不处于RUNNING状态，将自定义任务从workQueue队列中移除
      if (! isRunning(recheck) && remove(command)) 
        // 拒绝执行命令
        reject(command);
      else if (workerCountOf(recheck) == 0) // worker数量等于0
        // 添加worker
        addWorker(null, false);
    }
    else if (!addWorker(command, false)) // 添加worker失败
      // 拒绝执行命令
      reject(command);
  }
}
private boolean addWorker(Runnable firstTask, boolean core) {
  //...
  if (workerAdded) { // worker被添加
    // 开始执行worker的run方法，调用线程start启动线程
    t.start();  
    // 设置worker已开始标识
    workerStarted = true;
  }
  //...
  return workerStarted;
}

private final class Worker extends AbstractQueuedSynchronizer implements Runnable{
  public void run() {
    runWorker(this);
  } 
  final void runWorker(Worker w) {
    Thread wt = Thread.currentThread();
    Runnable task = w.firstTask;
    w.firstTask = null;
    w.unlock(); // allow interrupts
    boolean completedAbruptly = true;
    try {
      while (task != null || (task = getTask()) != null) {
        w.lock();
        if ((runStateAtLeast(ctl.get(), STOP) ||
             (Thread.interrupted() &&
              runStateAtLeast(ctl.get(), STOP))) &&
            !wt.isInterrupted())
          wt.interrupt();
        try {
          beforeExecute(wt, task);
          Throwable thrown = null;
          try {
            // 执行run方法
            task.run();
          } catch (RuntimeException x) {
            thrown = x; throw x;
          } catch (Error x) {
            thrown = x; throw x;
          } catch (Throwable x) {
            thrown = x; throw new Error(x);
          } finally {
            afterExecute(task, thrown);
          }
        } finally {
          task = null;
          w.completedTasks++;
          w.unlock();
        }
      }
      completedAbruptly = false;
    } finally {
      processWorkerExit(w, completedAbruptly);
    }
  }
}
```

### 2.3.1 Executor

> Executor 管理多个异步任务的执⾏，⽽⽆需程序员显式地管理线程的⽣命周期。这⾥的异步是指多个任务的执⾏互不⼲扰，不需要进⾏同步操作。

**主要有如下三种Executor**

- CachedThreadPool：⼀个任务创建⼀个线程；

- FixedThreadPool：所有任务只能使⽤固定⼤⼩的线程；

- SingleThreadExecutor：相当于⼤⼩为 1 的 FixedThreadPool。

**代码示例**

```java
public static void main(String[] args) {
  ExecutorService executorService = Executors.newCachedThreadPool();
  for (int i = 0; i < 5; i++) {
    executorService.execute(new MyRunnable());
  }
  executorService.shutdown();
}
```

### 2.3.2 CachedThreadPool

`CachedThreadPool` 是 Java 中 `ExecutorService` 接口的一个实现类，它提供了一个基于线程池的执行器，用于执行异步任务。

`CachedThreadPool` 的特点如下：

1. **动态线程池大小**：`CachedThreadPool` 允许线程数量根据需要动态增长或收缩。如果有新任务提交，而当前线程数少于核心线程数，则会创建新线程。如果当前线程池中的线程都处于空闲状态，并且等待新任务超过指定的时间（默认为 60 秒），则会停止这些空闲线程并且移除它们，从而避免资源浪费。

2. **无界队列**：`CachedThreadPool` 使用一个无界队列来保存待执行的任务。这意味着如果提交的任务数量远远超过线程池的最大线程数，那么线程池会持续地创建新线程来处理这些任务，直到达到系统资源限制。

由于其动态调整线程池大小的特性，`CachedThreadPool` 适合执行大量的短期异步任务，例如处理短暂且频繁的 I/O 操作，或者是需要大量并发处理的任务。

以下是一个简单的示例，演示了如何使用 `CachedThreadPool`：

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Main {
    public static void main(String[] args) {
        // 创建一个 CachedThreadPool
        ExecutorService executor = Executors.newCachedThreadPool();

        // 提交任务给 CachedThreadPool 执行
        for (int i = 0; i < 10; i++) {
            final int taskNumber = i;
            executor.execute(() -> {
                System.out.println("Task " + taskNumber + " executed by thread: " + Thread.currentThread().getName());
            });
        }

        // 关闭线程池
        executor.shutdown();
    }
}
```

在这个示例中，我们使用 `Executors.newCachedThreadPool()` 方法创建了一个 `CachedThreadPool` 实例。然后我们提交了 10 个任务给线程池执行，每个任务都会打印执行线程的名称。最后，我们调用 `shutdown()` 方法关闭线程池。

### 2.3.5 线程池参数

线程池在 Java 中通常由 `ThreadPoolExecutor` 类来实现，其构造函数提供了一些参数来配置线程池的行为。主要参数包括：

1. **corePoolSize（核心线程数）**：线程池中始终保持活动的线程数量，即使它们处于空闲状态也会保持存活。如果任务数量超过了核心线程数，线程池会根据需要创建新的线程。

2. **maximumPoolSize（最大线程数）**：线程池中允许存在的最大线程数量。当任务队列满了且线程池中的线程数达到最大线程数时，新提交的任务会被拒绝。

3. **keepAliveTime（线程空闲超时时间）**：线程池中的线程在空闲超过该时间后会被终止并从线程池中移除，直到线程池中的线程数量等于核心线程数。

4. **unit（时间单位）**：用于指定 keepAliveTime 的时间单位。

5. **workQueue（任务队列）**：用于保存等待执行的任务。可以是一个有界队列或者无界队列。

6. **threadFactory（线程工厂）**：用于创建新线程的工厂。

7. **handler（拒绝策略）**：用于处理任务队列满了且线程池中的线程数达到最大线程数时的情况。常见的拒绝策略包括抛出异常、丢弃任务、丢弃最旧的任务等。

这些参数可以根据实际需求来进行配置，以控制线程池的大小、行为和性能。

---

工作队列（workQueue）是线程池中用来存储等待被执行的任务的数据结构。当线程池中的线程数量达到上限并且工作队列已满时，新提交的任务将会被放入工作队列中等待执行。工作队列的作用是缓解任务提交与任务执行之间的压力，提高系统的吞吐量和性能。

阿里巴巴推荐的线程池拒绝策略有以下几种：

1. ThreadPoolExecutor.AbortPolicy：丢弃任务并抛出 RejectedExecutionException 异常（默认拒绝策略）。
2. ThreadPoolExecutor.DiscardPolicy：丢弃任务，但是不抛出异常。
3. ThreadPoolExecutor.DiscardOldestPolicy：丢弃队列中最前面的任务，然后重新提交被拒绝的任务。
4. ThreadPoolExecutor.CallerRunsPolicy：由调用线程（提交任务的线程）处理该任务。

根据具体的业务场景和需求，可以选择适合的拒绝策略来处理线程池无法执行的任务。

---

工作队列和核心线程数在线程池中起着不同的作用：

1. **工作队列**（Work Queue）：
   - 工作队列用于存储等待被执行的任务。
   - 当线程池中的线程数达到核心线程数（corePoolSize）上限且有新的任务提交时，新的任务会被放入工作队列中等待执行。
   - 工作队列可以帮助缓解任务提交与任务执行之间的压力，提高系统的吞吐量和性能。
   - 不同的工作队列类型（如有界队列、无界队列、同步移交队列等）会影响线程池的行为和性能。

2. **核心线程数**（Core Pool Size）：
   - 核心线程数是线程池中保持活动状态的线程数量，即使这些线程处于空闲状态也会保持存活。
   - 当有任务提交时，线程池会优先使用核心线程来处理任务。
   - 如果核心线程数未达到上限，新的任务会创建新的核心线程来处理。
   - 当任务量大于核心线程数并且工作队列已满时，线程池会根据最大线程数（maximumPoolSize）来动态扩展线程池的线程数量。

总结来说，工作队列用于存储等待执行的任务，而核心线程数是线程池中保持活动状态的线程数量，用于处理任务。在线程池中，这两个因素共同决定了任务的执行方式和线程的数量。

---

在线程池中，工作队列是用于存储等待被执行的任务的数据结构。不同类型的工作队列对任务的存储和执行方式有不同的影响。以下是常见的工作队列类型及其特点：

1. **有界队列（Bounded Queue）**：
   - 有界队列有固定的容量，当队列已满时，新的任务会被拒绝或触发拒绝策略。
   - 常见的有界队列包括 ArrayBlockingQueue 和 LinkedBlockingQueue（带有界限）。

2. **无界队列（Unbounded Queue）**：
   - 无界队列没有固定的容量限制，可以存储任意数量的任务。
   - 当任务提交速度大于任务执行速度时，可能会导致内存溢出。
   - 常见的无界队列包括 LinkedBlockingQueue（不带界限）。

3. **同步移交队列（Synchronous Queue）**：
   - 同步移交队列不存储任务，每个插入操作必须等待一个对应的移除操作，反之亦然。
   - 当任务提交时，必须有线程立即接收并处理，否则任务会被拒绝或触发拒绝策略。
   - 常见的同步移交队列为 SynchronousQueue。

4. **优先级队列（Priority Queue）**：
   - 优先级队列根据任务的优先级来决定执行顺序，优先级高的任务会被优先执行。
   - 常见的优先级队列为 PriorityBlockingQueue。

5. **延迟队列（Delayed Queue）**：
   - 延迟队列中的任务会在一定延迟时间之后才能被取出并执行。
   - 常见的延迟队列为 DelayQueue。

不同类型的工作队列适用于不同的场景，选择合适的工作队列类型可以提高线程池的性能和效率。在使用线程池时，根据任务的特性和需求选择适合的工作队列类型是很重要的。

### 2.3.6 关闭线程池

调⽤ Executor 的 shutdown() ⽅法会等待线程都执⾏完毕之后再关闭，但是如果调⽤的是shutdownNow() ⽅法，则相当于调⽤每个线程的 interrupt() ⽅法。

**中断代码示例**

```java
public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        executorService.execute(() -> {
            try {
                Thread.sleep(2000);
                System.out.println("Thread run");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        executorService.shutdownNow();
        System.out.println("Main run");
    }
```

如果只想中断 Executor 中的⼀个线程，可以通过使⽤ submit() ⽅法来提交⼀个线程，它会返回⼀个Future<?> 对象，通过调⽤该对象的 cancel(true) ⽅法就可以中断线程。

```java
Future<?> future = executorService.submit(() -> {
 // ..
});
future.cancel(true);
```



**关闭线程池源码**

```java
/*
  线程池状态变为 SHUTDOWN
   - 不会接收新任务
   - 但已提交任务会执行完
   - 此方法不会阻塞调用线程的执行
*/
public void shutdown() {
  final ReentrantLock mainLock = this.mainLock;
  mainLock.lock();
  try {
    checkShutdownAccess();
    // 修改线程池状态
    advanceRunState(SHUTDOWN);
    // 仅会打断空闲线程
    interruptIdleWorkers();
    onShutdown(); // 扩展点 ScheduledThreadPoolExecutor
  } finally {
    mainLock.unlock();
  }
  // 尝试终结(没有运行的线程可以立刻终结，如果还有运行的线程也不会等)
  tryTerminate();
}
/*
  线程池状态变为 STOP
   - 不会接收新任务
   - 会将队列中的任务返回
   - 并用 interrupt 的方式中断正在执行的任务
*/
public List<Runnable> shutdownNow() {
  List<Runnable> tasks;
  final ReentrantLock mainLock = this.mainLock;
  mainLock.lock();
  try {
    checkShutdownAccess();
    // 修改线程池状态
    advanceRunState(STOP);
    // 打断所有线程
    interruptWorkers();
    // 获取队列中剩余任务
    tasks = drainQueue();
  } finally {
    mainLock.unlock();
  }
  // 尝试终结
  tryTerminate();
  return tasks;
}
```

# 五、 线程同步

### 2.4.1 synchronized

> 采用synchronized修饰符实现的同步机制叫做互斥锁机制，它所获得的锁叫做互斥锁。每个对象都有一个monitor(锁标记)，当线程拥有这个锁标记时才能访问这个资源，没有锁标记便进入锁池。任何一个对象系统都会为其创建一个互斥锁，这个锁是为了分配给线程的，防止打断原子操作。每个对象的锁只能分配给一个线程，因此叫做互斥锁。
>
> 参考资料：
>
> https://www.cnblogs.com/aspirant/p/11470858.html



- 内存的可见性
  - 加锁（synchronized同步）的功能不仅仅局限于互斥行为，同时还存在另外一个重要的方面：内存可见性。我们不仅希望防止某个线程正在使用对象状态而另一个线程在同时修改该状态，而且还希望确保当一个线程修改了对象状态后，其他线程能够看到该变化。而线程的同步恰恰也能够实现这一点。
- **同步机制获取互斥锁的一些说明**：
  1. 如果同一个方法内同时有两个或更多线程，则每个线程有自己的局部变量拷贝。
  2. 类的每个实例都有自己的对象级别锁。当一个线程访问实例对象中的synchronized同步代码块或同步方法时，该线程便获取了该实例的对象级别锁，其他线程这时如果要访问synchronized同步代码块或同步方法，便需要阻塞等待，直到前面的线程从同步代码块或方法中退出，释放掉了该对象级别锁。
  3. 访问同一个类的不同实例对象中的同步代码块，不存在阻塞等待获取对象锁的问题，因为它们获取的是各自实例的对象级别锁，相互之间没有影响。
  4. 持有一个对象级别锁不会阻止该线程被交换出来，也不会阻塞其他线程访问同一示例对象中的非synchronized代码。当一个线程A持有一个对象级别锁（即进入了synchronized修饰的代码块或方法中）时，线程也有可能被交换出去，此时线程B有可能获取执行该对象中代码的时间，但它只能执行非同步代码（没有用synchronized修饰），当执行到同步代码时，便会被阻塞，此时可能线程规划器又让A线程运行，A线程继续持有对象级别锁，当A线程退出同步代码时（即释放了对象级别锁），如果B线程此时再运行，便会获得该对象级别锁，从而执行synchronized中的代码。
  5. 持有对象级别锁的线程会让其他线程阻塞在所有的synchronized代码外。例如，在一个类中有三个synchronized方法a，b，c，当线程A正在执行一个实例对象M中的方法a时，它便获得了该对象级别锁，那么其他的线程在执行同一实例对象（即对象M）中的代码时，便会在所有的synchronized方法处阻塞，即在方法a，b，c处都要被阻塞，等线程A释放掉对象级别锁时，其他的线程才可以去执行方法a，b或者c中的代码，从而获得该对象级别锁。
  6. 使用synchronized（obj）同步语句块，可以获取指定对象上的对象级别锁。obj为对象的引用，如果获取了obj对象上的对象级别锁，在并发访问obj对象时时，便会在其synchronized代码处阻塞等待，直到获取到该obj对象的对象级别锁。当obj为this时，便是获取当前对象的对象级别锁。
  7. 类级别锁被特定类的所有示例共享，它用于控制对static成员变量以及static方法的并发访问。具体用法与对象级别锁相似。
  8. 互斥是实现同步的一种手段，临界区、互斥量和信号量都是主要的互斥实现方式。synchronized关键字经过编译后，会在同步块的前后分别形成monitorenter和monitorexit这两个字节码指令。根据虚拟机规范的要求，在执行monitorenter指令时，首先要尝试获取对象的锁，如果获得了锁，把锁的计数器加1，相应地，在执行monitorexit指令时会将锁计数器减1，当计数器为0时，锁便被释放了。由于synchronized同步块对同一个线程是可重入的，因此一个线程可以多次获得同一个对象的互斥锁，同样，要释放相应次数的该互斥锁，才能最终释放掉该锁。
- 作用对象丰富
  - 同步实例
    - 同步成员变量
    - 同步代码块
    - 同步方法
  - 同步类
    - 同步类
    - 同步静态成员变量
    - 同步静态方法

### 2.4.2 ReentrantLock 锁

![2F192BDFAD9C22C62FE4D23692FDE892](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/Java/2F192BDFAD9C22C62FE4D23692FDE892.png)

**代码示例**

```java
public class LockExample {
    private Lock lock = new ReentrantLock();

    public void func() {
        lock.lock();
        try {
            for (int i = 0; i < 10; i++) {
                System.out.print(i + " ");
            }
        } finally {
            lock.unlock(); // 确保释放锁，从⽽避免发⽣死锁。
        }
    }

    public static void main(String[] args) {
        LockExample lockExample = new LockExample();
        ExecutorService executorService = Executors.newCachedThreadPool();
        executorService.execute(() -> lockExample.func());
        executorService.execute(() -> lockExample.func());
    }
}
```

**运行结果**

```java
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 
```



**ReentrantLock和synchronized的比较**

1. **锁的实现** 

synchronized 是 JVM 实现的，⽽ ReentrantLock 是 JDK 实现的。

2. **性能** 

新版本 Java 对 synchronized 进⾏了很多优化，例如⾃旋锁等，synchronized 与 ReentrantLock ⼤致相同。

3. **等待可中断** 

   - `ReentrantLock` 提供了 `lockInterruptibly()` 方法，允许线程在等待锁时被中断。

   - `synchronized` 不支持线程中断，一旦进入同步代码块，只有等待获取锁的线程自己主动退出或者获取锁才能继续执行。

4. **公平锁** 

   - 公平锁是指多个线程在等待同⼀个锁时，必须按照申请锁的时间顺序来依次获得锁。

   - synchronized 中的锁是⾮公平的，ReentrantLock 默认情况下也是⾮公平的，但是也可以是公平的。

5. **锁绑定多个条件** 

⼀个 ReentrantLock 可以同时绑定多个 Condition 对象。

6. **灵活性**：
   - `ReentrantLock` 提供了更多的扩展功能，例如可以获取锁的状态、条件变量、公平锁和非公平锁等。
   - `synchronized` 是 Java 语言内置的关键字，提供了更简单直接的方式来进行同步操作，但功能相对较少。

**使⽤选择**

- 除⾮需要使⽤ ReentrantLock 的⾼级功能，否则优先使⽤ synchronized。这是因为 synchronized 是JVM 实现的⼀种锁机制，JVM 原⽣地⽀持它，⽽ ReentrantLock 不是所有的 JDK 版本都⽀持。并且使⽤ synchronized 不⽤担⼼没有释放锁⽽导致死锁问题，因为 JVM 会确保锁的释放



### 2.4.3 BlockingQueue-生产者消费者模式

`BlockingQueue` 是 Java 并发包中提供的一个接口，用于实现生产者-消费者模式中的数据传输。它是一个支持线程安全的队列，提供了阻塞操作的方法，当队列满时，插入操作会被阻塞；当队列空时，移除操作会被阻塞。

`BlockingQueue` 接口继承自 `Queue` 接口，提供了以下常用方法：

- `put(E e)`：将指定元素添加到队列中，如果队列满了则阻塞等待。
- `take()`：移除并返回队列头部的元素，如果队列为空则阻塞等待。
- `offer(E e)`：将指定元素添加到队列中，如果队列满了则返回 false，不阻塞。
- `poll()`：移除并返回队列头部的元素，如果队列为空则返回 null，不阻塞。
- `peek()`：返回队列头部的元素但不移除，如果队列为空则返回 null。

常见的实现类有：

- `ArrayBlockingQueue`：基于数组实现的有界阻塞队列。
- `LinkedBlockingQueue`：基于链表实现的可选有界阻塞队列。
- `PriorityBlockingQueue`：支持优先级排序的无界阻塞队列。
- `DelayQueue`：延迟队列，用于存放具有延迟时间的元素。

`BlockingQueue` 可以很好地用于解决生产者-消费者问题，生产者线程向队列中添加元素，消费者线程从队列中取出元素，从而实现了线程之间的解耦和协作。

**代码示例**

```java
package Java_test;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

class Producer implements Runnable {
    private BlockingQueue<Integer> buffer;
    private int data = 0;

    public Producer(BlockingQueue<Integer> buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        try {
            while (true) {
                buffer.put(produce());
                Thread.sleep(1000); // 模拟生产过程
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private int produce() {
        System.out.println("Producing: " + data);
        return data++;
    }
}

class Consumer implements Runnable {
    private BlockingQueue<Integer> buffer;

    public Consumer(BlockingQueue<Integer> buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        try {
            while (true) {
                consume(buffer.take());
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void consume(int data) {
        System.out.println("Consuming: " + data);
    }
}

public class PorducerAndConsumer {
    public static void main(String[] args) {
        BlockingQueue<Integer> buffer = new ArrayBlockingQueue<>(10); // 缓冲区大小为10

        Thread producerThread = new Thread(new Producer(buffer));
        Thread consumerThread = new Thread(new Consumer(buffer));

        producerThread.start();
        consumerThread.start();

        try {
            Thread.sleep(5000); // 运行5秒后停止
            producerThread.interrupt();
            consumerThread.interrupt();
            producerThread.join();
            consumerThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

```

**运行结果**

```java
Producing: 0
Consuming: 0
Producing: 1
Consuming: 1
Producing: 2
Consuming: 2
Producing: 3
Consuming: 3
Producing: 4
Consuming: 4
```



### 2.4.4 ThreadLocal

`ThreadLocal` 是 Java 中的一个线程本地变量工具类，它提供了一种线程级别的数据隔离机制，使得每个线程都可以拥有自己独立的变量副本，避免了线程间共享变量带来的线程安全问题。具体来说，`ThreadLocal` 允许你创建的变量在每个线程中都有其自己的副本，每个线程都可以独立地修改自己的副本，而不会影响到其他线程。

`ThreadLocal` 主要用于解决线程范围内的数据共享问题，例如在多线程环境下实现用户身份认证、数据库连接管理、线程池任务分配等场景下，可以使用 `ThreadLocal` 来保存每个线程的相关数据，避免了使用全局变量或者在方法间传递参数的方式，使得代码更加简洁清晰。

`ThreadLocal` 的常用方法包括：

- `set(T value)`：设置当前线程的局部变量值。
- `get()`：获取当前线程的局部变量值。
- `remove()`：移除当前线程的局部变量值。

使用 `ThreadLocal` 时需要注意以下几点：

1. 内存泄漏：由于 `ThreadLocal` 中使用了 `ThreadLocalMap` 来保存每个线程的局部变量值，如果没有及时清理，会导致内存泄漏问题。因此，使用完毕后应该调用 `remove()` 方法进行清理。
2. 线程安全：虽然 `ThreadLocal` 可以解决多线程环境下的数据共享问题，但并不是线程安全的，需要开发者自行保证线程安全性。
3. 初始化：如果需要对 `ThreadLocal` 变量进行初始化，可以通过重写 `initialValue()` 方法或者使用 `withInitial()` 方法来实现。

总的来说，`ThreadLocal` 是一种非常实用的工具类，可以简化多线程编程中的数据共享问题，但在使用时需要注意内存泄漏和线程安全性等问题。

---

以下是一个使用 `ThreadLocal` 的简单示例，展示了如何在多线程环境下保存和获取线程局部变量：

```java
public class ThreadLocalExample {

    // 创建一个 ThreadLocal 变量，用于保存线程局部变量
    private static ThreadLocal<Integer> threadLocal = ThreadLocal.withInitial(() -> 0);

    public static void main(String[] args) {
        // 创建两个线程并启动
        Thread t1 = new Thread(() -> {
            // 设置线程局部变量的值
            threadLocal.set(1);
            // 打印线程局部变量的值
            System.out.println("Thread 1 - Local variable: " + threadLocal.get());
        });

        Thread t2 = new Thread(() -> {
            // 设置线程局部变量的值
            threadLocal.set(2);
            // 打印线程局部变量的值
            System.out.println("Thread 2 - Local variable: " + threadLocal.get());
        });

        t1.start();
        t2.start();
    }
}
```

在这个示例中，我们创建了一个 `ThreadLocal` 变量 `threadLocal`，并使用 `withInitial()` 方法设置了初始值为 0。然后创建了两个线程 `t1` 和 `t2`，每个线程都设置了 `threadLocal` 的值，并打印了它的值。由于 `threadLocal` 是线程局部变量，因此每个线程都可以独立地修改和访问它，不会相互影响。

## 2.4.5 volatile 关键词

> **说明：**
>
> 在JDK1.2之前，Java的类型模型实现总是从主存(即共享内存)读取变量，是不需要进行特别的注意的。而随着JVM的成熟和优化，现在在多线程环境下volatile关键字的使用变的非常重要。在当前的Java内存模型下，线程可以把变量保存在本地内存(比如机器的寄存器)中，而不是直接在主存中进行读写。这就可能造成一个线程在主存中修改了一个变量的值，而另一个线程还在继续使用它在寄存器中的变量值的拷贝，造成数据的不一致。
>
> 要解决这个问题，就需要把变量声明为volatile，这就指示JVM，这个变量是不稳定的，每次使用它都到主存中进行读取。一般来说，多任务环境下，各任务间共享的变量都应该加volatile修饰符。volatile修饰的成员变量在每次被线程访问时，都强迫从共享内存中重读该成员变量的值。而且，当成员变量发生变化时，强迫线程将变化值回写到共享内存。这样在任何时刻，两个不同的线程总是看到某个成员变量的同一个值。
>
> volatile是一种稍弱的同步机制，在访问volatile变量时不会执行加锁操作，也就不会执行线程阻塞，因此volatilei变量是一种比synchronized关键字更轻量级的同步机制。使用建议：在两个或者更多的线程需要访问的成员变量上使用volatile。当要访问的变量已在synchronized代码块中，或者为常量时，或者为常量时，没必要使用volatile。

### 指令重排序

 Java编译器为了优化程序的性能，会重新对字节码指令排序，虽然会重排序，但是指令重排序运行的结果一定是正常的。在程序运行过程中（多核CPU环境下）也可能处理器会对执行的指令进行重排序。

 在单线程中对我们程序的帮助一定是正向的，它能够很好的优化我们程序的性能。但是在多线程环境下，如果由于出现指令重排序情况导致线程安全性问题，这种情况下比较少见（出现概率小，难复现）很隐蔽。例如：双检查锁单例模式

**指令重排序需要满足一定条件才能进行的，能够进行指令重排序的地方，需要看这个段代码是否具有数据依赖性**

| 名称   | 代码示例     | 说明                         |
| :----- | :----------- | :--------------------------- |
| 写后读 | a = 1;b = a; | 写一个变量之后，再读这个位置 |
| 写后写 | a = 1;a = 2; | 写一个变量之后，再写这个变量 |
| 读后写 | a = b;b = 1; | 读一个变量之后，再写这个变量 |

> 在单线程环境下编译器、runtime和处理器都遵循`as-if-serial`语义【不管怎么重排序，执行结果不变】

**final变量的指令重排序**

```
/**
 * 步骤1：为new出来的对象开辟内存空间
 * 步骤2：初始化，执行构造器方法的逻辑代码片段
 * 步骤3：完成obj引用的赋值操作，将其指向刚刚开辟的内存地址
 * 这三个步骤可能进行指令重排序变为：步骤1、步骤3、步骤2
 * 如果发生重排序可能obj不为null但是未初始化完成
 */
ObjectVarilabe obj = new ObjectVarilabe()
```

- 在构造函数内对一个final变量的写入，与随后把这个被构造对象的引用赋值给一个引用变量，这个两个操作不能被重排序，即需要先初始化final变量才可以给构造的对象地址赋给引用【普通域可能在地址赋给引用之后才初始化】

  ```
    public class FinalExample {
      int i = 0;
      final int f;
      static FinalExample obj;
      
      public FinalExample() { // 构造函数
        i = 1;              // 写普通域
        f = 2;              // 写final域
      }
      
      
      public static void writer() { 
        /**
          	 * 此代码执行之时，另一线程读取obj不为null那么obj.f一定初始化完成
          	 * 另一线程读取obj不为null，但是i不一定初始化完成
          	 */
        obj = new FinalExample();	
      }
    }
  ```

- 初次读一个包含final的对象的引用，与随后初次读这个final域，这两个操作之间不能重排序

  ```
    // ①一定发生在③之前，但是①不一定发生在②之前
    public static void reader() { 
      FinalExample example = obj;    // ①读对象引用
      System.out.println(example.i); // ②读普通域
      System.out.println(example.f); // ③读final域
  ```



### volatile原子可见性

**Java内存模型规定在多线程情况下，线程操作主内存（类比内存条）变量，需要通过线程独有的工作内存（类比CPU高速缓存）拷贝主内存变量副本来进行。此处的所谓内存模型要区别于通常所说的虚拟机堆模型**

![work-memory](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/Java/work-memory.png)

如果是一个大对象，并不会从主内存完全拷贝一份，而是这个被访问对象引用的对象、对象中的字段可能存在拷贝

**线程独有的工作内存和进程内存（主内存）之间通过8中原子操作来实现，如下所示**

![main-work-swap](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/Java/main-work-swap.png)

`read load` 从主存复制变量到当前工作内存

`use assign` 执行代码，改变共享变量值，可以多次出现

`store write` 用工作内存数据刷新主存相关内容

这些操作并不是原子性，也就是在`read load`之后，如果主内存变量发生修改之后，线程工作内存中的值由于已经加载，不会产生对应的变化，所以计算出来的结果会和预期不一样，对于volatile修饰的变量，jvm虚拟机只是保证从主内存加载到线程工作内存的值是最新的。

### 内存屏障

- Load Barrier（加载屏障）

Load Barrier 确保在屏障之前的所有读取操作在屏障之后的所有读取操作之前完成，这意味着在加载屏障之前进行的所有读取操作对当前线程都可见。

- Store Barrier（存储屏障）

Store Barrier 确保在屏障之前的所有写入操作在屏障之后的所有写入操作之前完成，这意味着在存储屏障之前进行的所有写入操作对其他线程可见。

- Full Barrier（全屏障）

Full Barrier 结合了加载屏障和存储屏障的效果。它确保在屏障之前的所有读取和写入操作在屏障之后的所有读取和写入操作之前完成。这种屏障确保了内存操作的严格顺序。

### happen-before

 JMM(java memory model)可以通过happens-before关系向提供跨线程的内存可见性保证（如果A线程的写操作a与B线程的读操作b之间存在happens-before关系，尽管a操作和b操作在不同的线程中执行，但JMM向程序员保证a操作将对b操作可见）**happen-before是可见性保证，不是发生性保证**

- **定义**

  1）如果一个操作happens-before另一个操作，那么第一个操作的执行结果将对第二个操作可见，而且第一个操作的执行顺序排在第二个操作之前。

  2）两个操作之间存在happens-before关系，**并不意味着Java平台的具体实现必须要按照happens-before关系指定的顺序来执行**。如果重排序之后的执行结果，与按happens-before关系来执行的结果一致，那么这种重排序合法。

- **具体规则**

  - 程序顺序规则：一个线程中的每个操作，happens-before于该线程中的任意后续操作
  - 监视器锁规则：对一个锁的解锁，happens-before于随后对这个锁的加锁
  - volatile变量规则：对一个volatile变量，happens-before于任意后续对这个volatile域的读
  - 传递性：如果A happens-before B，且B happens-before C，那么A happens-before C
  - start()规则：如果线程A执行操作ThreadB.start()，那么A线程的ThreadB.start()操作happens-before于线程B中的任意操作。
  - Join()规则：如果线程A执行操作ThreadB.join()并成功返回，那么线程B中的任意操作happens-before于线程A从ThreadB.join()操作成功返回。
  - 程序中断规则：对线程interrupted()方法的调用先行于被中断线程的代码检测到中断时间的发生。
  - 对象finalize规则：一个对象的初始化完成（构造函数执行结束）先行于发生它的finalize()方法的开始

### 伪共享

- **缓存行**：缓存行是缓存中数据存储的基本单位，通常为32字节、64字节或128字节。

- **伪共享**

 伪共享的非标准定义为：缓存系统中是以缓存行（cache line）为单位存储的，当多线程修改互相独立的变量时，如果这些变量位于同一个缓存行，只要这个缓存行里有一个变量失效则此缓存行所有数据全部失效。

 在JDK8以前，我们一般是在属性间填充长整型变量来分隔每一组属性。JDK8之后加入`@Contended`注解方式【JVM需要添加参数-XX:-RestrictContended才能开启此功能 】

伪共享（False Sharing）是多处理器系统中一种性能问题，它发生在多个线程频繁访问并修改彼此独立但共享缓存行（cache line）的变量时。伪共享不会改变程序的正确性，但会显著影响性能，导致缓存一致性协议频繁无效、缓存失效（cache invalidation）和处理器间通信开销增加

- **缓存一致性协议**：现代多核处理器使用缓存一致性协议（如MESI协议）来保证缓存一致性的。当一个处理器修改了一个缓存行，其他包含这个缓存行的处理器必须将其标记为无效。



**什么是伪共享？**

伪共享发生在多个线程访问不同变量，这些变量共享同一个缓存行时：

- 即使这些变量是独立的，位于不同的内存位置，但由于它们共享同一个缓存行。
- 当一个线程修改了其中的一个变量，整个缓存行会被标记为无效，迫使其他线程重新加载这个缓存行，即使它们并没有访问被修改的变量。
- 这种频繁的缓存行失效和重新加载导致性能显著下降。

**举例说明**

假设有两个线程分别操作两个变量 `a` 和 `b`，但 `a` 和 `b` 位于同一缓存行。

```java
public class FalseSharing implements Runnable {
    public static volatile long a;
    public static volatile long b;

    private final int threadId;

    public FalseSharing(int threadId) {
        this.threadId = threadId;
    }

    @Override
    public void run() {
        for (int i = 0; i < 1000_000_000; i++) {
            if (threadId == 0) {
                a++;
            } else {
                b++;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(new FalseSharing(0));
        Thread t2 = new Thread(new FalseSharing(1));

        long start = System.nanoTime();

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        long end = System.nanoTime();
        System.out.println("Duration: " + (end - start) / 1_000_000 + " ms");
    }
}
```

在上述代码中，两个线程分别操作 `a` 和 `b`。由于 `a` 和 `b` 可能在内存上是相邻的，因此共享同一个缓存行。伪共享导致每次任何一个变量的修改都会使缓存行无效，迫使另一个线程重新加载该缓存行，极大降低性能。

**解决伪共享的方法**

解决伪共享问题的核心思路是避免两个频繁访问的变量共享同一个缓存行。这可以通过填充无关数据来将它们分离到不同的缓存行。

- Java 的 `@sun.misc.Contended` 注解

从 Java 8 开始，JVM 提供了 `@sun.misc.Contended` 注解，可以用于避免伪共享。需要注意的是，该注解是非标准的，并且需要通过 JVM 参数开启。

```java
import sun.misc.Contended;

public class FalseSharingFixed implements Runnable {
    @Contended
    public static volatile long a;
    @Contended
    public static volatile long b;

    private final int threadId;

    public FalseSharingFixed(int threadId) {
        this.threadId = threadId;
    }

    @Override
    public void run() {
        for (int i = 0; i < 1000_000_000; i++) {
            if (threadId == 0) {
                a++;
            } else {
                b++;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // 启动参数中添加：-XX:-RestrictContended
        Thread t1 = new Thread(new FalseSharingFixed(0));
        Thread t2 = new Thread(new FalseSharingFixed(1));

        long start = System.nanoTime();

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        long end = System.nanoTime();
        System.out.println("Duration: " + (end - start) / 1_000_000 + " ms");
    }
}
```

- 填充 `padding`

另一种通用的方式是在变量之间填充一些无关的数据，以确保这些变量分布在不同的缓存行中。

```java
public class FalseSharingPadding implements Runnable {
    public static volatile long a;
    private static long padding1, padding2, padding3, padding4, padding5, padding6, padding7;
    public static volatile long b;

    private final int threadId;

    public FalseSharingPadding(int threadId) {
        this.threadId = threadId;
    }

    @Override
    public void run() {
        for (int i = 0; i < 1000_000_000; i++) {
            if (threadId == 0) {
                a++;
            } else {
                b++;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(new FalseSharingPadding(0));
        Thread t2 = new Thread(new FalseSharingPadding(1));

        long start = System.nanoTime();

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        long end = System.nanoTime();
        System.out.println("Duration: " + (end - start) / 1_000_000 + " ms");
    }
}
```



伪共享问题通常比较隐蔽，可能需要通过性能测试和CPU分析工具来检测。例如，可以使用硬件性能计数器（如 Intel VTune、Perf）来监测缓存一致性流量和缓存失效情况。

- **伪共享**：是在多个线程频繁访问和修改共享缓存行中的独立变量时，导致的性能下降问题。
- **影响**：主要导致缓存一致性协议频繁触发，增加处理器之间的通信开销。
- **解决方法**：可以通过使用 `@Contended` 注解或填充 `padding` 来解决，避免不同线程频繁访问的变量共享同一个缓存行。

理解并解决伪共享问题对于提升多线程程序的性能和效率是非常重要的。通过适当的优化，可以显著减少缓存失效和处理器间的通信开销，从而提高程序的并发性能。

### volatile的禁止指令重排序

**volatile止指令重排序的实现原理**

`volatile`变量的禁止指令重排序是基于内存屏障（Memory Barrier）实现**【synchronized不具有此功能】**。内存屏障又称内存栅栏，是一个CPU指令，内存屏障会导致JVM无法优化屏障内的指令集。

- 对`volatile`变量的写指令后会加入写屏障，对共享变量的改动，都同步到主存当中
- 对`volatile`变量的读指令前会加入读屏障，对共享变量的读取，加载的是主存中最新数据

> 如果单例模式中的懒汉式变量没有使用volatile仅仅使用synchronized双重检测加锁依旧会因为重排序问题产生线程安全性问题[参见](https://mynamelancelot.github.io/java/concurrent.html#lazy-questions)。

**注意点**

1. volatile变量是一种稍弱的同步机制在访问volatile变量时不会执行加锁操作，因此也就不会使执行线程阻塞，因此volatile变量是一种比synchronized关键字更轻量级的同步机制。
2. 从内存可见性的角度看，写入volatile变量相当于退出同步代码块，而读取volatile变量相当于进入同步代码块。
3. 在代码中如果过度依赖volatile变量来控制状态的可见性，通常会比使用锁的代码更脆弱，也更难以理解。仅当volatile变量能简化代码的实现以及对同步策略的验证时，才应该使用它。一般来说，用同步机制会更安全些。
4. 加锁机制（即同步机制）既可以确保可见性又可以确保原子性，而volatile变量只能确保可见性，原因是声明为volatile的简单变量如果当前值与该变量以前的值相关，那么volatile关键字不起作用，也就是说如下的表达式都不是原子操作：“count++”、“count = count+1”。

**当且仅当满足以下所有条件时，才应该使用volatile变量：**

1. 对变量的写入操作不依赖变量的当前值，或者你能确保只有单个线程更新变量的值。
2. 该变量没有包含在具有其他变量的不变式中。

**总结**

在需要同步的时候，第一选择应该是synchronized关键字，这是最安全的方式，尝试其他任何方式都是有风险的。尤其在、jdK1.5之后，对synchronized同步机制做了很多优化，如：自适应的自旋锁、锁粗化、锁消除、轻量级锁等，使得它的性能明显有了很大的提升。

---

下面分别给出符合和不符合`volatile`变量应用条件的例子：

**符合条件的例子**：

1. **对变量的写入操作不依赖变量的当前值**：

```java
public class VolatileExample {
    private volatile boolean flag = false;

    public void setFlag() {
        flag = true;
    }

    public boolean isFlag() {
        return flag;
    }
}
```

在这个例子中，`flag`变量的写入操作不依赖于当前值，只是简单地将其设置为`true`。这种情况下适合使用`volatile`修饰。

**不符合条件的例子**：

1. **变量的写入操作依赖变量的当前值**：

```java
public class NonVolatileExample {
    private volatile int count = 0;

    public void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}
```

在这个例子中，`count`变量的写入操作依赖于当前值的增加。多个线程同时调用`increment`方法可能会导致竞态条件，因此不适合使用`volatile`修饰。

2. **变量包含在具有其他变量的不变式中**：

```java
public class InvariantExample {
    private volatile int x = 0;
    private int y = 0;

    public void updateX() {
        x = y + 1;
    }

    public int getX() {
        return x;
    }

    public void updateY() {
        y = 10;
    }

    public int getY() {
        return y;
    }
}
```

在这个例子中，`x`变量的更新依赖于`y`变量的值，两者存在关联。如果使用`volatile`修饰`x`，可能会导致多线程环境下`x`和`y`之间的关系出现问题，不适合使用`volatile`修饰`x`。

### 2.4.6 可重入锁

> 当某个线程请求一个由其他线程持有的锁时，发出请求的线程就会阻塞。然而，由于内置锁是可重入的，因此如果摸个线程试图获得一个已经由它自己持有的锁，那么这个请求就会成功。“重入”意味着获取锁的操作的粒度是“线程”，而不是调用。重入的一种实现方法是，为每个锁关联一个获取计数值和一个所有者线程。当计数值为0时，这个锁就被认为是没有被任何线程所持有，当线程请求一个未被持有的锁时，JVM将记下锁的持有者，并且将获取计数值置为1，如果同一个线程再次获取这个锁，计数值将递增，而当线程退出同步代码块时，计数器会相应地递减。当计数值为0时，这个锁将被释放。

**代码示例如下：**

```java
public class Father  
{  
    public synchronized void doSomething(){  
        ......  
    }  
}  
  
public class Child extends Father  
{  
    public synchronized void doSomething(){  
        ......  
        super.doSomething();  
    }  
}  
```

**解释：**

- 子类覆写了父类的同步方法，然后调用父类中的方法，此时如果没有可重入的锁，那么这段代码件产生死锁。
- 由于Father和Child中的doSomething方法都是synchronized方法，因此每个doSomething方法在执行前都会获取Child对象实例上的锁。如果内置锁不是可重入的，那么在调用super.doSomething时将无法获得该Child对象上的互斥锁，因为这个锁已经被持有，从而线程会永远阻塞下去，一直在等待一个永远也无法获取的锁。重入则避免了这种死锁情况的发生。



###   2.4.7 wait/notify/notifyAll

- wait
  - 该方法用来将当前线程置入休眠状态，直到接到通知或被中断为止。在调用wait()之前，线程必须要获得该对象的对象级别锁，即只能在同步方法或同步块中调用wait()方法。进入wait()方法后，当前线程释放锁。在从wait()返回前，线程与其他线程竞争重新获得锁。如果调用wait()时，没有持有适当的锁，则抛出IllegalMonitorStateException，它是RuntimeException的一个子类，因此，不需要try-catch结构。
- notify
  - 该方法也要在同步方法或同步块中调用，即在调用前，线程也必须要获得该对象的对象级别锁，如果调用notify()时没有持有适当的锁，也会抛出IllegalMonitorStateException。
  - 该方法用来通知那些可能等待该对象的对象锁的其他线程。如果有多个线程等待，则线程规划器任意挑选出其中一个wait()状态的线程来发出通知，并使它等待获取该对象的对象锁（notify后，当前线程不会马上释放该对象锁，wait所在的线程并不能马上获取该对象锁，要等到程序退出synchronized代码块后，当前线程才会释放锁，wait所在的线程也才可以获取该对象锁），但不惊动其他同样在等待被该对象notify的线程们。当第一个获得了该对象锁的wait线程运行完毕以后，它会释放掉该对象锁，此时如果该对象没有再次使用notify语句，则即便该对象已经空闲，其他wait状态等待的线程由于没有得到该对象的通知，会继续阻塞在wait状态，直到这个对象发出一个notify或notifyAll。这里需要注意：它们等待的是被notify或notifyAll，而不是锁。这与下面的notifyAll()方法执行后的情况不同。
- notifyAll()
  - notifyAll使所有原来在该对象上wait的线程统统退出wait的状态（即全部被唤醒，不再等待notify或notifyAll，但由于此时还没有获取到该对象锁，因此还不能继续往下执行），变成等待获取该对象上的锁，一旦该对象锁被释放（notifyAll线程退出调用了notifyAll的synchronized代码块的时候），他们就会去竞争。如果其中一个线程获得了该对象锁，它就会继续往下执行，在它退出synchronized代码块，释放锁后，其他的已经被唤醒的线程将会继续竞争获取该锁，一直进行下去，直到所有被唤醒的线程都执行完毕。

---

`wait()`、`notify()` 和 `notifyAll()` 是 Java 中用于线程间通信的方法，它们通常用于协调多个线程之间的操作。这些方法都是定义在 `Object` 类中，因此所有对象都可以调用这些方法。

- `wait()`: 当线程调用 `wait()` 方法时，它会进入等待状态，并释放持有的对象锁，直到其他线程调用相同对象上的 `notify()` 或 `notifyAll()` 方法唤醒它。如果调用 `wait()` 方法时没有持有对象锁，则会抛出 `IllegalMonitorStateException` 异常。
- `notify()`: 当线程调用 `notify()` 方法时，它会唤醒在相同对象上调用 `wait()` 方法进入等待状态的一个线程。如果有多个线程在等待，它们中的一个将被随机选择唤醒。如果没有线程在等待，`notify()` 方法不会产生任何影响。
- `notifyAll()`: 当线程调用 `notifyAll()` 方法时，它会唤醒在相同对象上调用 `wait()` 方法进入等待状态的所有线程。如果没有线程在等待，`notifyAll()` 方法不会产生任何影响。

下面是一个简单的示例，演示了如何使用 `wait()`、`notify()` 和 `notifyAll()` 方法进行线程间的通信：

```java
public class WaitNotifyExample {

    public static void main(String[] args) {
        final Object lock = new Object(); // 创建一个对象作为锁

        // 等待线程
        Thread waiter = new Thread(() -> {
            synchronized (lock) {
                System.out.println("等待线程开始等待...");
                try {
                    lock.wait(); // 等待
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("等待线程被唤醒...");
            }
        });

        // 唤醒线程
        Thread notifier = new Thread(() -> {
            try {
                Thread.sleep(1000); // 等待一段时间
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            synchronized (lock) {
                System.out.println("唤醒线程开始唤醒等待线程...");
                // lock.notify(); // 唤醒等待线程
                lock.notifyAll(); // 唤醒所有等待线程
                System.out.println("唤醒线程完成唤醒操作...");
            }
        });

        // 启动线程
        waiter.start();
        notifier.start();
    }
}
```

在这个例子中，等待线程先获得了锁，然后调用 `wait()` 方法进入等待状态。在等待一段时间后，唤醒线程获取了相同的锁，并调用 `notify()` 或 `notifyAll()` 方法唤醒等待线程。当被唤醒的线程再次获得锁时，它将继续执行。

###  2.4.8 await/signal/signalAll

`await()`、`signal()` 和 `signalAll()` 是 `java.util.concurrent.locks.Condition` 接口中定义的方法，用于实现线程间的等待和通知机制。它们通常与 `ReentrantLock` 结合使用，以替代传统的 `wait()`、`notify()` 和 `notifyAll()` 方法。与 `wait()`、`notify()` 和 `notifyAll()` 相比，它们提供了更灵活、更安全的线程间通信方式。

1. **await()**：
   - `await()` 方法用于使当前线程等待，直到其他线程调用相同条件对象的 `signal()` 或 `signalAll()` 方法唤醒它，或者等待超时。
   - 当前线程在调用 `await()` 方法后会释放当前持有的锁，并进入等待状态。

2. **signal()**：
   - `signal()` 方法用于唤醒等待在相同条件对象上的一个线程（随机选择），使其从 `await()` 方法返回。
   - 调用 `signal()` 方法会通知等待在条件对象上的一个线程，使其继续执行。

3. **signalAll()**：
   - `signalAll()` 方法用于唤醒等待在相同条件对象上的所有线程，使它们从 `await()` 方法返回。
   - 调用 `signalAll()` 方法会通知所有等待在条件对象上的线程，使它们继续执行。

---

**代码示例**

```java
public class AwaitSignalExample {
    private Lock lock = new ReentrantLock();
    private Condition condition = lock.newCondition();
    public void before() {
        lock.lock();
        try {
            System.out.println("before");
            condition.signalAll();
        } finally {
            lock.unlock();
        }
    }
    public void after() {
        lock.lock();
        try {
            condition.await();
            System.out.println("after");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
    public static void main(String[] args) {
   		ExecutorService executorService = Executors.newCachedThreadPool();
 			AwaitSignalExample example = new AwaitSignalExample();
 			executorService.execute(() -> example.after());
 			executorService.execute(() -> example.before());
		}
}
```

**运行结果**

```java
before
after
```



# 六、java.util.concurrent（J.U.C）

### 2.5.1 **AQS**

AQS（AbstractQueuedSynchronizer）是Java中用于实现同步器的抽象基类。它提供了一种实现各种同步原语（如锁、信号量、倒计数器等）的框架，包括了一套FIFO队列来管理等待线程。AQS是Java并发包中许多同步工具的基础，包括ReentrantLock、Semaphore、CountDownLatch等。

AQS的核心思想是基于“共享”和“排他”两种不同的模式来管理资源。它提供了两种队列来分别处理这两种模式：

1. **独占模式**：适用于只有一个线程能够获得资源的情况，如ReentrantLock。在独占模式下，AQS维护了一个等待队列，当一个线程获取到锁时，其他线程会被阻塞并排队等待。

2. **共享模式**：适用于多个线程可以同时获得资源的情况，如Semaphore。在共享模式下，AQS也维护了一个等待队列，但多个线程可以同时获得资源，不一定要排队等待。

AQS的核心方法包括：

- `acquire`：尝试获取资源，如果获取不到，将当前线程排队等待。
- `release`：释放资源，唤醒等待队列中的线程。

AQS的内部实现主要基于一个双向链表，用于管理等待线程。当一个线程请求资源时，如果资源不可用，它会被封装为一个节点并加入到等待队列的队尾。当资源可用时，它会被唤醒。

AQS支持自定义同步器，即通过继承AQS并实现`tryAcquire`和`tryRelease`等方法来定义新的同步原语。这使得AQS非常灵活，可以满足各种同步需求。

总的来说，AQS是实现同步器的一个强大工具，它提供了一种通用的框架，简化了同步机制的实现，提高了并发性能，同时也是Java并发包中各种同步工具的基础。

### 2.5.2 ReentrantLock 锁

- [ReentrantLock](###2.4.2 ReentrantLock 锁)

### **2.5.3 CountDownLatch**

> ⽤来控制⼀个或者多个线程等待多个线程。维护了⼀个计数器 cnt，每次调⽤ countDown() ⽅法会让计数器的值减 1，减到 0 的时候，那些因为调⽤ await() ⽅法⽽在等待的线程就会被唤醒

**代码示例**

```java
public class CountdownLatchExample {
    public static void main(String[] args) throws InterruptedException {
        final int totalThread = 10;
        CountDownLatch countDownLatch = new CountDownLatch(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("run..");
                countDownLatch.countDown();
            });
        }
        countDownLatch.await();
        System.out.println("end");
        executorService.shutdown();
    }
}
```

**运行结果**

```java
run..run..run..run..run..run..run..run..run..run..end
```





### 2.5.4 CyclicBarrier

>  ⽤来控制多个线程互相等待，只有当多个线程都到达时，这些线程才会继续执⾏。和 CountdownLatch 相似，都是通过维护计数器来实现的。线程执⾏ await() ⽅法之后计数器会减 1，并进⾏等待，直到计数器为 0，所有调⽤ await() ⽅法⽽在等待的线程才能继续执⾏。CyclicBarrier 和 CountdownLatch 的⼀个区别是，CyclicBarrier 的计数器通过调⽤ reset() ⽅法可以循环使⽤，所以它才叫做循环屏障。
>
>  CyclicBarrier 有两个构造函数，其中 parties 指示计数器的初始值，barrierAction 在所有线程都到达屏障的时候会执⾏⼀次。

**代码示例**

```java
public class CyclicBarrierExample {
    public static void main(String[] args) {
        final int totalThread = 10;
        CyclicBarrier cyclicBarrier = new CyclicBarrier(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("before..");
                try {
                    cyclicBarrier.await();
                } catch (InterruptedException | BrokenBarrierException e) {
                    e.printStackTrace();
                }
                System.out.print("after..");
            });
        }
        executorService.shutdown();
    }
}
```

**运行结果**

```java
before..before..before..before..before..before..before..before..before..before..after..after..after..after..after..after..after..after..after..after..
```



### 2.5.5 Semaphore

> Semaphore 类似于操作系统中的信号量，可以控制对互斥资源的访问线程数。以下代码模拟了对某个服务的并发请求，每次只能有 3 个客户端同时访问，请求总数为 10。

**代码示例**

```java
public class SemaphoreExample {
    public static void main(String[] args) {
        final int clientCount = 3;
        final int totalRequestCount = 10;
        Semaphore semaphore = new Semaphore(clientCount);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalRequestCount; i++) {
            executorService.execute(() -> {
                try {
                    semaphore.acquire();
                    System.out.print(semaphore.availablePermits() + " ");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    semaphore.release();
                }
            });
        }
        executorService.shutdown();
    }
}
```

**运行结果**

```java
2 1 2 2 2 2 2 1 2 2
```



### 2.5.6 ForkJoin

> 主要⽤于并⾏计算中，和 MapReduce 原理类似，都是把⼤的计算任务拆分成多个⼩任务并⾏计算。

**原理**

ForkJoinPool 实现了⼯作窃取算法来提⾼ CPU 的利⽤率。每个线程都维护了⼀个双端队列，⽤来存储需要执⾏的任务。⼯作窃取算法允许空闲的线程从其它线程的双端队列中窃取⼀个任务来执⾏。窃取的任务必须是最晚的任务，避免和队列所属线程发⽣竞争。例如Thread2 从 Thread1 的队列中拿出最晚的 Task1 任务，Thread1 会拿出 Task2 来执⾏，这样就避免发⽣竞争。但是如果队列中只有⼀个任务时还是会发⽣竞争。

`ForkJoin` 是 Java 并发包中用于实现分治任务并行处理的框架，主要用于解决计算密集型任务的并行化处理。它的核心思想是将大任务拆分成小任务，分配给不同的线程进行处理，然后将处理结果合并得到最终结果。`ForkJoin` 框架主要包含以下几个重要的组件：

1. **ForkJoinPool**：`ForkJoinPool` 是 `ForkJoin` 框架的线程池，用于管理并发执行的任务。它采用工作窃取（work-stealing）算法来提高任务的执行效率。

2. **RecursiveTask**：`RecursiveTask` 是用于返回结果的分治任务抽象类，它的 `compute()` 方法会返回一个泛型类型的结果。

3. **RecursiveAction**：`RecursiveAction` 是不返回结果的分治任务抽象类，通常用于执行一些没有返回值的操作。

`ForkJoin` 框架的基本使用步骤如下：

1. **定义任务类**：继承 `RecursiveTask` 或 `RecursiveAction`，实现 `compute()` 方法来定义任务的执行逻辑。

2. **创建任务对象**：根据实际业务需要创建 `RecursiveTask` 或 `RecursiveAction` 对象，并设置任务的起始和结束位置。

3. **创建线程池**：创建 `ForkJoinPool` 对象，并通过 `invoke()` 方法提交任务。

4. **等待任务执行完成**：使用 `join()` 方法等待任务执行完成，并获取最终的结果。



**代码示例**

```java
public class ForkJoinExample extends RecursiveTask<Integer> {
    private final int threshold = 5;
    private int first;
    private int last;

    public ForkJoinExample(int first, int last) {
        this.first = first;
        this.last = last;
    }

    @Override
    protected Integer compute() {
        int result = 0;
        if (last - first <= threshold) {
            // 任务⾜够⼩则直接计算
            for (int i = first; i <= last; i++) {
                result += i;
            }
        } else {
            // 拆分成⼩任务
            int middle = first + (last - first) / 2;
            ForkJoinExample leftTask = new ForkJoinExample(first, middle);
            ForkJoinExample rightTask = new ForkJoinExample(middle + 1,
                    last);
            leftTask.fork();
            rightTask.fork();
            result = leftTask.join() + rightTask.join();
        }
        return result;
    }


    public static void main(String[] args) throws ExecutionException,
            InterruptedException {
        ForkJoinExample example = new ForkJoinExample(1, 10000);
        ForkJoinPool forkJoinPool = new ForkJoinPool(); // 使用默认的构造函数
        Future result = forkJoinPool.submit(example);
        System.out.println(result.get());
    }
}
```

### 2.5.7 ConcurrentHashMap

`ConcurrentHashMap` 使用了 **CAS（Compare-And-Swap）** 操作来实现并发控制。CAS是一种无锁的原子操作，用于确保多个线程可以同时访问和修改`ConcurrentHashMap`的不同部分而不会导致数据不一致。

以下是`ConcurrentHashMap`中使用CAS的几个关键方面：

1. **桶（Buckets）**：`ConcurrentHashMap`内部采用了分段（Segment）的机制，每个分段包含一个桶数组，用于存储键值对。在每个桶中，CAS操作用于添加、删除和更新键值对，以确保并发线程可以安全地访问同一分段内的桶。

2. **分段锁（Segment Locks）**：`ConcurrentHashMap`使用了分段锁，每个分段上都有一个独立的锁。这意味着在修改同一个分段内的不同桶时，只有该分段上的锁会被占用，其他分段仍然可以并发地操作。这减少了锁的粒度，提高了并发性。

3. **CAS操作**：每次插入、删除或更新操作时，`ConcurrentHashMap`使用CAS操作来保证数据的一致性。CAS操作允许多个线程同时尝试修改同一个桶内的键值对，但只有一个线程会成功，其他线程需要重试或尝试其他桶。

4. **扩容**：当`ConcurrentHashMap`需要扩容时，CAS操作也用于安全地将桶数组的大小增加。这确保了在进行扩容时不会导致数据不一致。

总之，`ConcurrentHashMap`使用CAS操作以及分段锁等技术，以实现高效的并发控制。这使得它能够在多线程环境中提供高性能的并发访问，而不需要显式地使用锁。CAS操作允许多线程同时进行并发读写操作，只有在必要时才会阻塞或重试，从而提高了并发性。



## 原子操作类

在高并发编程中，确保线程安全和高效是非常重要的。JDK 提供了一系列原子类型操作类，用于无锁（锁自由，Lock-Free）的方式保证操作的原子性。这些类使用了 CAS（Compare-And-Swap）算法，以避免线程阻塞，从而提高系统的并发性能。

### 1. 使用原子方式更新基本类型

JDK 提供了以下原子类，用于对基本类型的原子操作：

- **`AtomicBoolean`**：用于原子地更新布尔值。
- **`AtomicInteger`**：用于原子地更新整数。
- **`AtomicLong`**：用于原子地更新长整数。

**示例代码**

```java
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class AtomicExample {
    public static void main(String[] args) {
        AtomicBoolean atomicBoolean = new AtomicBoolean(false);
        AtomicInteger atomicInteger = new AtomicInteger(0);
        AtomicLong atomicLong = new AtomicLong(0L);

        // 原子操作示例
        atomicBoolean.set(true);
        atomicInteger.incrementAndGet(); // +1
        atomicLong.addAndGet(10L); // +10

        System.out.println("AtomicBoolean: " + atomicBoolean.get());
        System.out.println("AtomicInteger: " + atomicInteger.get());
        System.out.println("AtomicLong: " + atomicLong.get());
    }
}
```

### 2. 使用原子的方式更新数组类型

JDK 还提供了原子更新数组类型的类，可以对数组元素进行原子操作：

- **`AtomicIntegerArray`**：用于原子地更新整数数组。
- **`AtomicLongArray`**：用于原子地更新长整数数组。
- **`AtomicReferenceArray`**：用于原子地更新引用数组。

**示例代码**

```java
import java.util.concurrent.atomic.AtomicIntegerArray;
import java.util.concurrent.atomic.AtomicLongArray;
import java.util.concurrent.atomic.AtomicReferenceArray;

public class AtomicArrayExample {
    public static void main(String[] args) {
        int[] intArray = new int[10];
        long[] longArray = new long[10];
        String[] strArray = new String[10];

        AtomicIntegerArray atomicIntegerArray = new AtomicIntegerArray(intArray);
        AtomicLongArray atomicLongArray = new AtomicLongArray(longArray);
        AtomicReferenceArray<String> atomicReferenceArray = new AtomicReferenceArray<>(strArray);

        // 原子操作示例
        atomicIntegerArray.set(0, 42);
        atomicLongArray.addAndGet(0, 100L);
        atomicReferenceArray.set(0, "Atomic Reference");

        System.out.println("AtomicIntegerArray[0]: " + atomicIntegerArray.get(0));
        System.out.println("AtomicLongArray[0]: " + atomicLongArray.get(0));
        System.out.println("AtomicReferenceArray[0]: " + atomicReferenceArray.get(0));
    }
}
```

### 3. 使用原子方式更新引用类型

针对引用类型的原子操作，JDK 提供了以下类：

- **`AtomicReference`**：用于原子地更新引用对象。
- **`AtomicStampedReference`**：使用时间戳记录引用版本，解决 ABA 问题，但时间戳相同也会产生 ABA 问题。
- **`AtomicMarkableReference`**：使用 `Boolean` 类型记录引用版本，适用于只需要知道对象是否有被修改的场景。

**示例代码**

```java
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicStampedReference;
import java.util.concurrent.atomic.AtomicMarkableReference;

public class AtomicReferenceExample {
    public static void main(String[] args) {
        AtomicReference<String> atomicReference = new AtomicReference<>("Initial");
        AtomicStampedReference<String> atomicStampedReference = new AtomicStampedReference<>("Initial", 1);
        AtomicMarkableReference<String> atomicMarkableReference = new AtomicMarkableReference<>("Initial", false);

        // 原子操作示例
        atomicReference.set("Updated");
        atomicStampedReference.compareAndSet("Initial", "Updated", 1, 2);
        atomicMarkableReference.compareAndSet("Initial", "Updated", false, true);

        System.out.println("AtomicReference: " + atomicReference.get());
        System.out.println("AtomicStampedReference: " + atomicStampedReference.getReference() + " (stamp: " + atomicStampedReference.getStamp() + ")");
        System.out.println("AtomicMarkableReference: " + atomicMarkableReference.getReference() + " (marked: " + atomicMarkableReference.isMarked() + ")");
    }
}
```

### 4. 使用原子方式更新字段

JDK 提供了以下类，用于对对象的字段进行原子更新：

- **`AtomicIntegerFieldUpdater`**：用于原子地更新整数字段。
- **`AtomicLongFieldUpdater`**：用于原子地更新长整数字段。
- **`AtomicReferenceFieldUpdater`**：用于原子地更新引用字段。

**示例代码**

```java
import java.util.concurrent.atomic.AtomicIntegerFieldUpdater;
import java.util.concurrent.atomic.AtomicLongFieldUpdater;
import java.util.concurrent.atomic.AtomicReferenceFieldUpdater;

public class AtomicFieldUpdaterExample {
    static class Person {
        volatile int age;
        volatile long salary;
        volatile String status;
    }

    public static void main(String[] args) {
        Person person = new Person();
        AtomicIntegerFieldUpdater<Person> ageUpdater = AtomicIntegerFieldUpdater.newUpdater(Person.class, "age");
        AtomicLongFieldUpdater<Person> salaryUpdater = AtomicLongFieldUpdater.newUpdater(Person.class, "salary");
        AtomicReferenceFieldUpdater<Person, String> statusUpdater = AtomicReferenceFieldUpdater.newUpdater(Person.class, String.class, "status");

        // 原子操作示例
        ageUpdater.set(person, 30);
        salaryUpdater.set(person, 100000L);
        statusUpdater.set(person, "Single");

        System.out.println("Age: " + ageUpdater.get(person));
        System.out.println("Salary: " + salaryUpdater.get(person));
        System.out.println("Status: " + statusUpdater.get(person));
    }
}
```

### 5. 高并发环境下更好性能的更新基本类型

为了在高并发环境下提供更高效的更新操作，JDK 还提供了以下类：

- **`DoubleAdder`**：用于高效地更新 double 类型变量。
- **`LongAdder`**：用于高效地更新 long 类型变量。
- **`DoubleAccumulator`**：用于高效地执行带自定义函数的 double 类型积累操作。
- **`LongAccumulator`**：用于高效地执行带自定义函数的 long 类型积累操作。
- `LongAdder` `DoubleAdder` 通过将对值的更新操作分散到多个单独的变量（称为“cells”），从而减少线程竞争。当每个线程更新计数时，事实上是更新其中一个分散的变量而不是单个变量。读取总值时，则是将所有分散的变量的值求和，得到最终的计数值。

**示例代码**

```java
import java.util.concurrent.atomic.DoubleAdder;
import java.util.concurrent.atomic.LongAdder;
import java.util.concurrent.atomic.DoubleAccumulator;
import java.util.concurrent.atomic.LongAccumulator;
import java.util.function.DoubleBinaryOperator;
import java.util.function.LongBinaryOperator;

public class HighConcurrencyExample {
    public static void main(String[] args) {
        DoubleAdder doubleAdder = new DoubleAdder();
        LongAdder longAdder = new LongAdder();
        DoubleBinaryOperator doubleOperator = (x, y) -> x + y;
        LongBinaryOperator longOperator = (x, y) -> x * y;
        DoubleAccumulator doubleAccumulator = new DoubleAccumulator(doubleOperator, 0.0);
        LongAccumulator longAccumulator = new LongAccumulator(longOperator, 1L);

        // 原子操作示例
        doubleAdder.add(3.5);
        longAdder.increment();
        doubleAccumulator.accumulate(2.0); // 2.0 + 0.0
        longAccumulator.accumulate(3L); // 1 * 3

        System.out.println("DoubleAdder: " + doubleAdder.sum());
        System.out.println("LongAdder: " + longAdder.sum());
        System.out.println("DoubleAccumulator: " + doubleAccumulator.get());
        System.out.println("LongAccumulator: " + longAccumulator.get());
    }
}
```

### 总结

- **`AtomicBoolean`、`AtomicInteger`、`AtomicLong`**：用于原子地更新布尔值和基本类型。
- **`AtomicIntegerArray`、`AtomicLongArray`、`AtomicReferenceArray`**：用于原子地更新数组类型。
- **`AtomicReference`、`AtomicStampedReference`、`AtomicMarkableReference`**：用于原子地更新引用类型，具有解决 ABA 问题的能力。
- **`AtomicIntegerFieldUpdater`、`AtomicLongFieldUpdater`、`AtomicReferenceFieldUpdater`**：用于原子地更新对象的字段。
- **`DoubleAdder`、`LongAdder`、`DoubleAccumulator`、`LongAccumulator`**：在高并发环境下提供性能更高的更新操作。

通过这些原子类，Java 提供了在并发环境中安全且高效地进行各种类型更新的机制，极大简化了多线程编程中的复杂性。这些工具类在构建高性能、高可靠性的并发应用程序时非常有用。

## 并发容器

### CopyOnWrite容器

`CopyOnWrite` 容器是 Java 并发编程中的一种用于实现线程安全的容器。这种容器在写操作（如增加、删除、修改）时，会创建原始容器的副本，并在副本上进行操作，写完后再将修改后的副本设置为新的容器。这种机制在读操作较多而写操作较少的场景中非常高效，因为读操作不会加锁，可以并发进行，不会阻塞。Java 中的 `CopyOnWriteArrayList` 和 `CopyOnWriteArraySet` 是典型的 `CopyOnWrite` 容器。`CopyOnWrite` 容器的核心思想是写时复制（Copy-On-Write）。当需要修改容器时，而不是直接修改容器本身，首先会复制一份副本，对副本进行修改，最后再将副本替换掉原容器。这样可以保证读操作在进行时不受写操作的影响，从而避免锁竞争。

#### CopyOnWriteArrayList
`CopyOnWriteArrayList` 是 `CopyOnWrite` 的一个实现，常用于并发的场景下替代 `ArrayList`。

```java
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class CopyOnWriteExample {
    public static void main(String[] args) {
        List<String> list = new CopyOnWriteArrayList<>();

        // 添加元素
        list.add("A");
        list.add("B");
        list.add("C");

        // 启动一个线程进行迭代操作
        new Thread(() -> {
            for (String item : list) {
                System.out.println(Thread.currentThread().getName() + " - " + item);
                try {
                    Thread.sleep(100); // 模拟延迟
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();

        // 主线程添加新元素
        new Thread(() -> {
            list.add("D");
            System.out.println(Thread.currentThread().getName() + " - Added D");
        }).start();
    }
}
```

```java
public boolean add(E e) {
  final ReentrantLock lock = this.lock;
  lock.lock();
  try {
    Object[] elements = getArray();
    int len = elements.length;
    Object[] newElements = Arrays.copyOf(elements, len + 1);
    newElements[len] = e;
    setArray(newElements);
    return true;
  } finally {
    lock.unlock();
  }
}
```

#### CopyOnWriteArraySet

`CopyOnWriteArraySet` 是 `CopyOnWriteArrayList` 的一个封装，用于创建线程安全的集（Set）。内部通过 `CopyOnWriteArrayList` 实现。



```java
import java.util.Set;
import java.util.concurrent.CopyOnWriteArraySet;

public class CopyOnWriteSetExample {
    public static void main(String[] args) {
        Set<String> set = new CopyOnWriteArraySet<>();

        // 添加元素
        set.add("X");
        set.add("Y");
        set.add("Z");

        // 启动一个线程进行迭代操作
        new Thread(() -> {
            for (String item : set) {
                System.out.println(Thread.currentThread().getName() + " - " + item);
                try {
                    Thread.sleep(100); // 模拟延迟
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();

        // 主线程添加新元素
        new Thread(() -> {
            set.add("W");
            System.out.println(Thread.currentThread().getName() + " - Added W");
        }).start();
    }
}
```

**特性**

- **线程安全**：多线程环境下，可以安全进行读写操作，读操作不会阻塞。
- **读写分离**：读操作非常高效，不需要加锁，但写操作如增加、删除和修改会创建新的副本，开销较大。
- **内存消耗**：每次写操作会创建新的副本，可能增加内存消耗。

**适用场景**

- **读多写少**：适用于读操作比写操作多的场景，例如缓存、黑白名单等。
- **不需要高实时性写操作的场景**：由于写操作需要复制数据，存在延迟，不适用于高实时性要求的写场景。

**注意事项**

- **不可用于大量写操作**：频繁的写操作会导致频繁的内存复制，严重影响性能。
- **一致性问题**：在大量读写并发的情况下，读操作可能会读取到旧数据，因为新的数据仅在写操作完成后才能替换掉旧的数据。

**总结**

`CopyOnWrite` 容器是一种在多线程环境中实现线程安全的有力工具，适用于读操作频繁、写操作较少的场景。它通过在写操作时复制数据来确保读操作的并发性，从而在一定程度上提高了系统的吞吐量。然而，`CopyOnWrite` 容器在写操作较多的情况下性能较差，因此在选择使用时需要谨慎评估实际需求。



在 Java 并发编程中，为了满足多线程环境下的数据一致性和高效性，Java 提供了多种并发集合类，其中包括 `ConcurrentHashMap` 和 `ConcurrentSkipListMap`。这些类提供线程安全的 `Map` 实现，并且针对不同的使用场景进行了优化。

### 并发Map

#### ConcurrentHashMap

`ConcurrentHashMap` 是一种基于哈希表的并发集合，它允许多个线程并发地进行读写操作。在 Java 8 之前，`ConcurrentHashMap` 使用了一种分段锁机制（Segment-based locking），将整个哈希表分成多个段（Segment），每个段都可以独立地进行加锁操作。在 Java 8 之后，分段锁机制被细粒度锁机制替代，使用 CAS（Compare-And-Swap）操作和内置锁进一步提高并发性能。

`ConcurrentHashMap`内部使用段（Segment）来表示这些不同的部分，每个段其实就是一个小的HashTable，它们有自己的锁。只要多个修改操作发生在不同的段上，它们就可以并发进行。把一个整体分成了16个段。也就是说最高支持16个线程的并发修改操作。而且大量使用volatile关键字，第一时间获取修改的内容。

**主要特性**

- **线程安全**：通过细粒度锁和无锁（CAS）机制，允许高并发操作。
- **高并发性**：在高并发环境下，读操作几乎不需要加锁，写操作锁定的是哈希桶（bucket），而不是整个数据结构。
- **无序**：无法保证遍历的顺序，每次遍历的顺序可能会不同。

**示例代码**

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class ConcurrentHashMapExample {
    public static void main(String[] args) {
        Map<String, String> map = new ConcurrentHashMap<>();

        // 添加元素
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        // 并发读取元素
        Runnable readTask = () -> {
            for (Map.Entry<String, String> entry : map.entrySet()) {
                System.out.println(Thread.currentThread().getName() + " - " + entry.getKey() + ":" + entry.getValue());
            }
        };

        // 并发写入元素
        Runnable writeTask = () -> {
            map.put("key4", "value4");
            System.out.println(Thread.currentThread().getName() + " - Added key4:value4");
        };

        // 启动多个线程并发读取
        for (int i = 0; i < 5; i++) {
            new Thread(readTask).start();
        }

        // 启动多个线程并发写入
        for (int i = 0; i < 5; i++) {
            new Thread(writeTask).start();
        }
    }
}
```

#### ConcurrentSkipListMap

`ConcurrentSkipListMap` 是一种基于跳表（Skip List）的并发集合，它实现了 `NavigableMap` 接口，并且默认情况下是按照键的自然顺序（或自定义的比较器）排序的。跳表是一种基于多层链表的数据结构，它能够在 O(log n) 时间复杂度下完成插入、删除和查找操作。

**主要特性**

- **线程安全**：使用无锁（lock-free）的算法来实现高效的并发操作。
- **有序**：支持排序操作，遍历时保证顺序，可以按照键的自然顺序或自定义顺序。
- **高并发性**：读操作不需要加锁，写操作使用无锁算法，支持高并发操作。

**示例代码**

```java
import java.util.concurrent.ConcurrentSkipListMap;
import java.util.Map;

public class ConcurrentSkipListMapExample {
    public static void main(String[] args) {
        Map<String, String> map = new ConcurrentSkipListMap<>();

        // 添加元素
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");

        // 并发读取元素
        Runnable readTask = () -> {
            for (Map.Entry<String, String> entry : map.entrySet()) {
                System.out.println(Thread.currentThread().getName() + " - " + entry.getKey() + ":" + entry.getValue());
            }
        };

        // 并发写入元素
        Runnable writeTask = () -> {
            map.put("key4", "value4");
            System.out.println(Thread.currentThread().getName() + " - Added key4:value4");
        };

        // 启动多个线程并发读取
        for (int i = 0; i < 5; i++) {
            new Thread(readTask).start();
        }

        // 启动多个线程并发写入
        for (int i = 0; i < 5; i++) {
            new Thread(writeTask).start();
        }
    }
}
```

- **ConcurrentHashMap 内部机制 (Java 8 及之后)**

  - **CAS 操作**：使用 CAS 操作来确保并发情况下的数据安全。

  - **细粒度锁**：锁住特定的哈希桶，而不是整个表，减少锁竞争。

  - **红黑树**：在桶中元素数量较少时使用链表结构，当桶中元素数量超过一定阈值（默认为 8）时，使用红黑树来优化查找性能。


- **ConcurrentSkipListMap 内部机制**

  - **跳表**：使用跳表（Skip List）数据结构，能够在 O(log n) 时间复杂度下完成插入、删除和查找操作。

  - **无锁操作**：通过无锁算法来实现高效的并发操作。


- **适用场景**

  - **ConcurrentHashMap**

    - 适用于需要高并发读、写、不关心元素顺序的场景。

    - 典型应用场景包括缓存存储、计数器等。


  - **ConcurrentSkipListMap**

    - 适用于需要高并发且需要保持元素顺序的场景。

    - 典型应用场景包括排行榜、需要快速查找范围查询的场景等。


- **总结**

  - **ConcurrentHashMap**：一个线程安全的哈希表实现，主要通过细粒度锁和 CAS 操作实现高并发读写性能，适用于对顺序不敏感但要求线程安全的场景。

  - **ConcurrentSkipListMap**：一个基于跳表的数据结构，支持排序操作，通过无锁算法实现高并发性能，适用于需要有序访问且要求线程安全的场景。


### 并发Queue

#### 非阻塞Queue

【`ConcurrentLinkedQueue`、`ConcurrentLinkedDeque`】

 是一个适用于高并发场景下的队列，通过CAS无锁的方式，实现了高并发状态下的高性能。它是一个基于链接节点的无界线程安全队列。该队列不允许null元素。

- add()和offer()都是加入元素，无区别
- poll()和peek()都是取头元素节点，前者会删除元素，后者不会

`ConcurrentLinkedQueue` 和 `ConcurrentLinkedDeque` 是 Java 提供的用于并发场景的高效无锁（lock-free）数据结构，适用于线程安全的队列和双端队列操作。下面将介绍它们的用法、原理和特点。

##### ConcurrentLinkedQueue

- `ConcurrentLinkedQueue` 是基于无锁算法的线程安全队列，实现了 `Queue` 接口，并遵循 FIFO（先进先出）原则。
- 通过使用 CAS（Compare-And-Swap）操作，在多线程环境中实现高效的并发操作。
- **无锁算法**：采用 CAS（Compare-And-Swap）算法来实现无锁操作，极大提高了并发性能。
- **无阻塞**：由于无锁机制，不会出现阻塞等待，通过自旋等待（spin-wait）方式处理并发访问。

**主要特点**

- **高并发**：使用无锁算法，极大提高了并发性能。
- **线程安全**：所有操作都是线程安全的，多个线程可以并发地进行插入和删除操作。
- **非阻塞**：队列操作不会被锁住，因此可以减少线程切换开销。

**示例代码**

```java
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class ConcurrentLinkedQueueExample {
    public static void main(String[] args) {
        Queue<String> queue = new ConcurrentLinkedQueue<>();

        // 添加元素
        queue.add("Element1");
        queue.add("Element2");
        queue.add("Element3");

        // 启动一个线程进行元素消费
        Runnable consumer = () -> {
            while (!queue.isEmpty()) {
                String element = queue.poll();
                System.out.println("Consumed: " + element);
            }
        };

        // 启动多个线程并发消费
        for (int i = 0; i < 3; i++) {
            new Thread(consumer).start();
        }
    }
}
```

`ConcurrentLinkedQueue` 通过 CAS 操作实现无锁的入队和出队操作。内部使用链表结构，头节点和尾节点分别指向链表的头和尾。入队操作更新尾节点的 `next` 指针；出队操作更新头节点的 `next` 指针。

##### ConcurrentLinkedDeque

- `ConcurrentLinkedDeque` 是一个基于无锁算法的线程安全双端队列，实现了 `Deque` 接口。
- 支持在双端进行插入和删除操作，提供较 `ConcurrentLinkedQueue` 更灵活的操作。
- **无锁算法**：同样采用 CAS 算法来实现无锁的双端队列操作。
- **无阻塞**：通过自旋等待（spin-wait）方式处理并发访问，不出现阻塞等待。

**主要特点**

- **高并发**：使用无锁算法，部分操作通过 CAS 实现高效并发。
- **线程安全**：所有操作都是线程安全的，支持在队列的两端进行并发的插入和删除操作。
- **非阻塞**：双端操作不会被锁住，提高了并发性能。

**示例代码**

```java
import java.util.concurrent.ConcurrentLinkedDeque;
import java.util.Deque;

public class ConcurrentLinkedDequeExample {
    public static void main(String[] args) {
        Deque<String> deque = new ConcurrentLinkedDeque<>();

        // 添加元素到队列末尾
        deque.addLast("Element1");
        deque.addLast("Element2");

        // 添加元素到队列头部
        deque.addFirst("Element3");
        deque.addFirst("Element4");

        // 启动一个线程消费队列从头部
        Runnable consumeHead = () -> {
            while (!deque.isEmpty()) {
                String element = deque.pollFirst();
                System.out.println("Consumed from head: " + element);
            }
        };

        // 启动一个线程消费队列从尾部
        Runnable consumeTail = () -> {
            while (!deque.isEmpty()) {
                String element = deque.pollLast();
                System.out.println("Consumed from tail: " + element);
            }
        };

        // 启动多个线程并发消费
        new Thread(consumeHead).start();
        new Thread(consumeTail).start();
    }
}
```

`ConcurrentLinkedDeque` 通过双向链表结构实现无锁的双端队列操作。内部使用两个指针分别指向头节点和尾节点，双端操作都通过 CAS 来实现指针的更新，从而达到无锁的效果。

##### 特点对比
- **ConcurrentLinkedQueue**：
  - 通过 CAS 实现无锁的并发队列。
  - 适用于高并发环境下的单向 FIFO 队列操作。
  - 各操作都需要遍历到链表末尾，可能涉及到多次 CAS 操作。

- **ConcurrentLinkedDeque**：
  - 通过双向链表和 CAS 实现无锁的并发双端队列。
  - 适用于需要在队列两端同时进行操作的场景。
  - 操作灵活，支持在头部和尾部进行插入和删除操作。

**适用场景**

- **ConcurrentLinkedQueue**：适用于生产者-消费者模型中的并发队列，或其他需要高并发访问的队列场景。
- **ConcurrentLinkedDeque**：适用于需要双端操作的高并发场景，比如任务调度、双端队列缓存等。

通过理解 `ConcurrentLinkedQueue` 和 `ConcurrentLinkedDeque` 的特点和用法，可以在多线程开发中选择合适的并发数据结构，提升程序的并发性能和安全性。

#### 阻塞Queue

【`ArrayBlockingQueue`、`LinkedBlockingQueue`、`LinkedBlockingDeque`、`PriorityBlockingQueue`】

- `ArrayBlockingQueue`：基于数组的有界阻塞队列实现，在ArrayBlockingQueue内部，维护了一个定长数组，以便从缓存队列中的数据对象，其实内部没实现读写分离，也就意味着生产者和消费者不能完全并行，长度需要定义，可以指定先进先出或者先进后出，在很多场合非常适合使用。
- `LinkedBlockingQueue`：基于链表的阻塞队列，同ArrayBlockingQueue类似，其内部也维持着一个数据缓存队列。LinkedBlockingQueue内部采用分离锁（读写分离两个锁），从而实现生产者和消费者操作的完全并行运行。他是一个无界队列（如果初始化指定长度则为有界队列）。
- `PriorityBlockingQueue`：基于优先级的阻塞队列（队列中的对象必须实现Comparable接口），内部控制线程同步的锁采用公平锁，也是无界队列。

在 Java 并发编程中，JDK 提供了一系列线程安全的阻塞队列，它们可以在多线程环境中方便地进行线程通信和同步。以下是 `ArrayBlockingQueue`、`LinkedBlockingQueue`、`LinkedBlockingDeque` 和 `PriorityBlockingQueue` 这些常用的阻塞队列的关键使用方法和内部实现原理简要介绍。

##### ArrayBlockingQueue

`ArrayBlockingQueue` 是一个由数组实现的有界阻塞队列，支持 FIFO（先进先出）顺序。容量是固定的，必须在构造时指定。

- **锁分离**：采用单一锁（`ReentrantLock`）机制来控制并发访问。
- **条件变量**：使用两个条件变量（`notEmpty` 和 `notFull`）来处理队列满和队列空的情况，通过 `Condition` 接口实现阻塞和唤醒机制。

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class ArrayBlockingQueueExample {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);

        // 添加元素
        queue.put("Element1"); // 阻塞直到有空间为止
        queue.offer("Element2"); // 如果队列已满，返回false

        // 移除元素
        String element1 = queue.take(); // 阻塞直到队列有元素为止
        String element2 = queue.poll(); // 如果队列为空，返回null

        System.out.println(element1); // 输出: Element1
        System.out.println(element2); // 输出: Element2
    }
}
```

**原理**

- **数组结构**：内部使用数组进行存储，容量固定。
- **两个锁**：使用两个不同的锁对象分别控制入队和出队操作（`ReentrantLock`）。
- **条件变量**：两个条件变量（`notEmpty` 和 `notFull`）来管理填充和消费时的阻塞，通过 `Condition` 接口实现。

##### LinkedBlockingQueue

`LinkedBlockingQueue` 是一个由链表实现的可选有界的阻塞队列。默认情况下，容量为 `Integer.MAX_VALUE`，但可以在构造时指定。

- **双锁机制**：使用两个锁对象，一个用于控制入队操作，另一个用于控制出队操作（每个操作分别一个锁），以提高并发性。
- **条件变量**：使用两个条件变量（`notEmpty` 和 `notFull`）来控制队列的状态变化。

```java
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class LinkedBlockingQueueExample {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> queue = new LinkedBlockingQueue<>(10); // 有界队列

        // 添加元素
        queue.put("Element1");
        queue.offer("Element2");

        // 移除元素
        String element1 = queue.take();
        String element2 = queue.poll();

        System.out.println(element1); // 输出: Element1
        System.out.println(element2); // 输出: Element2
    }
}
```

**原理**

- **链表结构**：内部使用链表存储元素。
- **双锁机制**：同样使用两个锁（一个控制入队，一个控制出队）和两个条件变量（`notEmpty` 和 `notFull`）来实现阻塞和唤醒机制。
- **可选有界**：可以在构造时指定容量。

##### LinkedBlockingDeque

`LinkedBlockingDeque` 是一个由链表实现的可选有界的阻塞双端队列。它既支持 FIFO，也支持 LIFO（后进先出）操作。

- **双锁机制**：同样使用两个锁对象，一个用于控制头部操作，另一个用于控制尾部操作。
- **条件变量**：使用两个条件变量（`notEmpty` 和 `notFull`）来处理队列满和队列空的情况。

```java
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.BlockingDeque;

public class LinkedBlockingDequeExample {
    public static void main(String[] args) throws InterruptedException {
        BlockingDeque<String> deque = new LinkedBlockingDeque<>(10); // 有界deque

        // 添加元素到队列尾部
        deque.putLast("Element1");
        deque.offerLast("Element2");

        // 添加元素到队列头部
        deque.putFirst("Element3");
        deque.offerFirst("Element4");

        // 移除元素从队列头部
        String element1 = deque.takeFirst();
        String element2 = deque.pollFirst();

        // 移除元素从队列尾部
        String element3 = deque.takeLast();
        String element4 = deque.pollLast();

        System.out.println(element1); // 输出: Element4
        System.out.println(element2); // 输出: Element3
        System.out.println(element3); // 输出: Element2
        System.out.println(element4); // 输出: Element1
    }
}
```

**原理**

- **双向链表结构**：内部基于双向链表存储元素。
- **双锁机制**：两个锁分别控制头部和尾部的操作。
- **可选有界**：可以在构造时指定容量。

##### PriorityBlockingQueue

`PriorityBlockingQueue` 是一个支持优先级排序的无界阻塞队列。默认情况下，元素会按照自然顺序进行排序，也可以在构造时提供一个 `Comparator` 来定制排序规则。

- **单锁机制**：使用一个全局锁（`ReentrantLock`）控制并发访问。
- **条件变量**：使用一个条件变量（`notEmpty`）来处理队列空的情况，通过 `Condition` 接口实现阻塞和唤醒机制。

```java
import java.util.concurrent.PriorityBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.Comparator;

public class PriorityBlockingQueueExample {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> queue = new PriorityBlockingQueue<>(10, Comparator.reverseOrder());

        // 添加元素
        queue.put("Element1");
        queue.put("Element3");
        queue.put("Element2");

        // 移除元素按照优先级处理
        String element1 = queue.take();
        String element2 = queue.take();
        String element3 = queue.take();

        System.out.println(element1); // 输出: Element3
        System.out.println(element2); // 输出: Element2
        System.out.println(element3); // 输出: Element1
    }
}
```

**原理**

- **堆结构**：内部基于二叉堆实现优先级队列。
- **无界队列**：没有容量限制，因此添加元素永远不会阻塞，但取元素会阻塞直到有元素为止。
- **单锁**：所有操作都基于一个锁来控制，主要是 `ReentrantLock`，并结合条件变量 `notEmpty` 来实现阻塞和唤醒机制。

##### 主要特点对比
- **ArrayBlockingQueue**：
  - 基于数组的有界阻塞队列。
  - 两个锁对象控制入队和出队操作，提供较好的并发性能。

- **LinkedBlockingQueue**：
  - 基于链表的可选有界阻塞队列。
  - 双锁机制，也适用于高并发场景。

- **LinkedBlockingDeque**：
  - 基于链表的可选有界阻塞双端队列。
  - 支持双端操作，灵活性更高，适合需要头尾两端操作的场景。

- **PriorityBlockingQueue**：
  - 基于堆的优先级阻塞队列。
  - 无界队列，支持优先级调度，适用于需要优先级处理的场景。

**适用场景**

- **ArrayBlockingQueue**：适合生产者-消费者模型中的固定容量场景，特别需要明确确定队列容量上限。
- **LinkedBlockingQueue**：适合需要高并发且处理大规模任务的场景，内部链表结构比较灵活。
- **LinkedBlockingDeque**：适合需要双端操作的高并发场景，如任务调度系统。
- **PriorityBlockingQueue**：适用于需要元素优先级排序的并发处理，如任务优先级调度等。

通过理解这些阻塞队列的使用方法和内部机制，可以在多线程编程中选择合适的数据结构来提高并发性能和代码的健壮性。

#### 特殊Queue

`DelayQueue`：带有延迟时间的Queue，其中的元素只有当其指定的延迟时间到了，才能够从队列中获取到该元素。DelayQueue中的元素必须实现Delayed接口，DelayQueue是一个没有大小限制的队列。DelayQueue支持阻塞和非阻塞两种模式。

`SynchronousQueue`：一种没有缓冲的队列，生存者生产的数据直接会被消费者获取并消费。每个put操作必须等待一个take，反之亦然。同步队列没有任何内部容量，甚至连一个队列的容量都没有。

##### DelayQueue

`DelayQueue` 是一个带有延迟时间的无界阻塞队列，队列中的元素只有在其指定的延迟时间到期之后才能被获取。`DelayQueue` 的元素必须实现 `Delayed` 接口，这个接口要求实现 `getDelay` 方法，该方法返回剩余的延迟时间。

**关键特点**

1. **延迟元素**：队列中的元素有一个特定的延迟时间，只有当延迟时间到期时该元素才能被取出。
2. **无界队列**：`DelayQueue` 是一个无界队列，不限制其容量。
3. **阻塞/非阻塞模式**：支持阻塞和非阻塞两种模式。
4. **优先级队列**：内部基于 `PriorityQueue` 实现，元素按照到期时间的顺序排序

**并发安全机制**

1. **锁控制**：使用 `ReentrantLock` 来保证并发访问的线程安全性。
2. **条件变量**：使用条件变量 `available` 来管理元素到期的阻塞和唤醒操作。

**插入与删除操作示意**

- **插入操作**：直接将元素加入优先级队列，并通过上滤操作恢复堆的性质。
- **删除操作**：取元素时，如果队列为空或所有元素的延迟时间未到期，则线程将被阻塞，直到有元素到期。

```java
import java.util.concurrent.DelayQueue;
import java.util.concurrent.Delayed;
import java.util.concurrent.TimeUnit;

class DelayElement implements Delayed {
    private long delayTime;
    private long expire;

    public DelayElement(long delay, TimeUnit unit) {
        this.delayTime = TimeUnit.MILLISECONDS.convert(delay, unit);
        this.expire = System.currentTimeMillis() + this.delayTime;
    }

    @Override
    public long getDelay(TimeUnit unit) {
        long remaining = expire - System.currentTimeMillis();
        return unit.convert(remaining, TimeUnit.MILLISECONDS);
    }

    @Override
    public int compareTo(Delayed o) {
        if (this.expire < ((DelayElement) o).expire) {
            return -1;
        }
        if (this.expire > ((DelayElement) o).expire) {
            return 1;
        }
        return 0;
    }
}

public class DelayQueueExample {
    public static void main(String[] args) throws InterruptedException {
        DelayQueue<DelayElement> delayQueue = new DelayQueue<>();

        delayQueue.put(new DelayElement(5, TimeUnit.SECONDS));
        delayQueue.put(new DelayElement(10, TimeUnit.SECONDS));

        while (true) {
            DelayElement element = delayQueue.take();
            System.out.println("Element expired at: " + System.currentTimeMillis() + " - " + element);
        }
    }
}
```

##### SynchronousQueue

`SynchronousQueue` 是一种没有内部缓冲的队列，生产者生产的数据必须直接被消费者获取并消费。每一个 `put` 操作必须等待一个 `take` 操作，也反之亦然。

**关键特点**

1. **无内部容量**：队列没有任何内部容量。
2. **同步交换**：只有在有消费者时，生产者的数据才能被插入队列。
3. **阻塞模式**：`put` 和 `take` 操作都是阻塞的。

**并发安全机制**

1. **独占锁**：通过 `ReentrantLock` 保证单个操作的原子性。
2. **公平性**：支持公平和非公平模式，通过内部的公平策略确保线程按照等待顺序公平地获取插入/移除的机会。

**插入与删除操作示意**

- **插入操作**：生产者先尝试插入数据，如果没有消费者等待，则阻塞直到有消费者调用 `take`。
- **删除操作**：消费者尝试获取数据，如果没有生产者插入数据，则阻塞直到有生产者调用 `put`。

```java
import java.util.concurrent.SynchronousQueue;

public class SynchronousQueueExample {
    public static void main(String[] args) {
        SynchronousQueue<String> queue = new SynchronousQueue<>();

        Thread producer = new Thread(() -> {
            try {
                queue.put("Element");
                System.out.println("Produced Element");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Thread consumer = new Thread(() -> {
            try {
                String element = queue.take();
                System.out.println("Consumed " + element);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        producer.start();
        consumer.start();
    }
}
```

通过了解 `DelayQueue` 和 `SynchronousQueue` 的特点和并发安全机制，可以更好地在合适的场景中应用这些数据结构，以提高程序的并发性能和数据处理能力。这些队列在不同的需求场景下，各自发挥着重要的作用，为多线程编程提供了便捷的工具。



### Collection相关



> - public static Collection synchronizedCollention(Collection c)
>
> - public static List synchronizedList(list l)
>
> - public static Map synchronizedMap(Map m)
>
> - public static Set synchronizedSet(Set s)
>
> - public static SortedMap synchronizedSortedMap(SortedMap sm)
>
> - public static SortedSet synchronizedSortedSet(SortedSet ss)
>
> 
>
> 注意，ArrayList实例马上封装起来，不存在对未同步化ArrayList的直接引用（即直接封装匿名实例）。这是一种最安全的途径。如果另一个线程要直接引用ArrayList实例，它可以执行非同步修改。

下面给出一段多线程中安全遍历集合元素的示例。我们使用Iterator逐个扫描List中的元素，在多线程环境中，当遍历当前集合中的元素时，一般希望阻止其他线程添加或删除元素。安全遍历的实现方法如下：

```java
import java.util.*;  
  
public class SafeCollectionIteration extends Object {  
    public static void main(String[] args) {  
        //为了安全起见，仅使用同步列表的一个引用，这样可以确保控制了所有访问  
        //集合必须同步化，这里是一个List  
        List wordList = Collections.synchronizedList(new ArrayList());  
  
        //wordList中的add方法是同步方法，会获取wordList实例的对象锁  
        wordList.add("Iterators");  
        wordList.add("require");  
        wordList.add("special");  
        wordList.add("handling");  
  
        //获取wordList实例的对象锁，  
        //迭代时，阻塞其他线程调用add或remove等方法修改元素  
        synchronized ( wordList ) {  
            Iterator iter = wordList.iterator();  
            while ( iter.hasNext() ) {  
                String s = (String) iter.next();  
                System.out.println("found string: " + s + ", length=" + s.length());  
            }  
        }  
    }  
}  
```



## Java CompletableFuture

`CompletableFuture` 是 Java 中强大的异步编程工具。它不仅扩展了 `Future` 接口，还提供了丰富的 API 用于异步操作、任务组合和结果处理。以下是 `CompletableFuture` 的各种用法整理，帮助开发者全面掌握其功能。

- **基本用法**：
  - 创建已完成的 `CompletableFuture`。
  - 使用 `runAsync` 和 `supplyAsync` 创建异步任务。

- **链式操作**：
  - 使用 `thenApply`、`thenAccept` 和 `thenRun` 进行任务后的操作。

- **异常处理**：
  - 使用 `exceptionally` 和 `handle` 捕获和处理异常。

- **任务组合**：
  - 使用 `thenCombine`、`thenCompose`、`allOf` 和 `anyOf` 组合多个任务。

- **自定义 Executor**：
  - 指定自定义的 Executor 来执行异步任务。

### 创建 CompletableFuture

已完成的 CompletableFuture

```java
CompletableFuture<String> completedFuture = CompletableFuture.completedFuture("Hello, World!");
```

使用 `runAsync` 和 `supplyAsync`

- **`runAsync`**：用于执行无需结果的异步任务。

```java
CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
    System.out.println("Running asynchronously");
});
```

- **`supplyAsync`**：用于执行并返回结果的异步任务。

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "Result from async task";
});
```

### 链式操作

任务完成后的处理

- **thenApply**：接收任务结果并返回新结果。

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "Hello")
    .thenApply(result -> result + ", World!");
```

- **thenAccept**：接收任务结果但不返回新结果。

```java
CompletableFuture<Void> future = CompletableFuture.supplyAsync(() -> "Hello")
    .thenAccept(result -> System.out.println(result));
```

- **thenRun**：不接收结果，完成后执行一个 Runnable 任务。

```java
CompletableFuture<Void> future = CompletableFuture.supplyAsync(() -> "Hello")
    .thenRun(() -> System.out.println("Task completed"));
```

### 异常处理

- **exceptionally**

用于在任务异常时提供默认值。

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    if (true) throw new RuntimeException("Error");
    return "Result";
}).exceptionally(ex -> {
    return "Recovered from error";
});
```

- **handle**

用于在任务完成或出现异常时处理结果和异常。

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    if (true) throw new RuntimeException("Error");
    return "Result";
}).handle((result, ex) -> {
    if (ex != null) {
        return "Recovered from error";
    } else {
        return result;
    }
});
```

### 组合多个任务

##### thenCombine

用于组合两个任务的结果。

```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

CompletableFuture<String> combinedFuture = future1.thenCombine(future2, (result1, result2) -> result1 + " " + result2);
```

##### thenCompose

用于将一个异步任务的结果传递给另一个异步任务。

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "Hello")
    .thenCompose(result -> CompletableFuture.supplyAsync(() -> result + " World!"));
```

##### allOf

用于等待多个任务全部完成。

```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

CompletableFuture<Void> allOfFuture = CompletableFuture.allOf(future1, future2);
allOfFuture.thenRun(() -> {
    try {
        String result1 = future1.get();
        String result2 = future2.get();
        System.out.println(result1 + " " + result2);
    } catch (Exception e) {
        e.printStackTrace();
    }
});
```

##### anyOf

用于等待任意一个任务完成。

```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

CompletableFuture<Object> anyOfFuture = CompletableFuture.anyOf(future1, future2);
anyOfFuture.thenAccept(result -> System.out.println(result));
```

### 自定义 Executor

可以指定自定义的线程池来执行异步任务。

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

ExecutorService executor = Executors.newFixedThreadPool(3);

CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "Hello from custom executor";
}, executor);

future.thenAccept(result -> {
    System.out.println(result);
});

// 记得关闭自定义线程池
executor.shutdown();
```

### 延伸功能

#### 组合式异步编程

组合异步操作，通过多种组合方法构建复杂的异步工作流。

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "Hello")
    .thenApply(result -> result + " World")
    .thenApply(result -> result + "!")
    .thenApply(result -> result.toUpperCase());

future.thenAccept(System.out::println); // 输出: HELLO WORLD!
```





# 七、 锁机制优化

> https://juejin.cn/post/6844903759047294983#heading-22

Java 中的并发锁大致分为隐式锁和显式锁两种。隐式锁就是我们最常使用的 synchronized 关键字，显式锁主要包含两个接口：Lock 和 ReadWriteLock，主要实现类分别为 ReentrantLock 和 ReentrantReadWriteLock，这两个类都是基于 AQS(AbstractQueuedSynchronizer) 实现的。还有的地方将 CAS 也称为一种锁，在包括 AQS 在内的很多并发相关类中，CAS 都扮演了很重要的角色。

- 悲观锁和乐观锁

悲观锁和独占锁是一个意思，它假设一定会发生冲突，因此获取到锁之后会阻塞其他等待线程。这么做的好处是简单安全，但是挂起线程和恢复线程都需要转入内核态进行，这样做会带来很大的性能开销。悲观锁的代表是 synchronized。然而在真实环境中，大部分时候都不会产生冲突。悲观锁会造成很大的浪费。而乐观锁不一样，它假设不会产生冲突，先去尝试执行某项操作，失败了再进行其他处理（一般都是不断循环重试）。这种锁不会阻塞其他的线程，也不涉及上下文切换，性能开销小。代表实现是 CAS。

- 公平锁和非公平锁

公平锁是指各个线程在加锁前先检查有无排队的线程，按排队顺序去获得锁。 非公平锁是指线程加锁前不考虑排队问题，直接尝试获取锁，获取不到再去队尾排队。值得注意的是，在 AQS 的实现中，一旦线程进入排队队列，即使是非公平锁，线程也得乖乖排队。

- 可重入锁和不可重入锁

如果一个线程已经获取到了一个锁，那么它可以访问被这个锁锁住的所有代码块。不可重入锁与之相反。

### 2.6.1 Synchronized 关键字

Synchronized 是一种独占锁。在修饰静态方法时，锁的是类对象，如 Object.class。修饰非静态方法时，锁的是对象，即 this。修饰方法块时，锁的是括号里的对象。 每个对象有一个锁和一个等待队列，锁只能被一个线程持有，其他需要锁的线程需要阻塞等待。锁被释放后，对象会从队列中取出一个并唤醒，唤醒哪个线程是不确定的，不保证公平性。

#### 类锁与对象锁

synchronized 修饰静态方法时，锁的是类对象,如 Object.class。修饰非静态方法时，锁的是对象，即 this。 多个线程是可以同时执行同一个synchronized实例方法的，只要它们访问的对象是不同的。

synchronized 锁住的是对象而非代码，只要访问的是同一个对象的 synchronized 方法，即使是不同的代码，也会被同步顺序访问。

此外，需要说明的，synchronized方法不能防止非synchronized方法被同时执行，所以，一般在保护变量时，需要在所有访问该变量的方法上加上synchronized。

#### 实现原理

synchronized 是基于 Java 对象头和 Monitor 机制来实现的。

- Java 对象头：一个对象在内存中包含三部分：对象头，实例数据和对齐填充。其中 Java 对象头包含两部分：

  - Class Metadata Address （类型指针）。存储类的元数据的指针。虚拟机通过这个指针找到它是哪个类的实例。

  - Mark Word（标记字段）。存出一些对象自身运行时的数据。包括哈希码，GC 分代年龄，锁状态标志等。

- Monitor：Mark Word 有一个字段指向 monitor 对象。monitor 中记录了锁的持有线程，等待的线程队列等信息。前面说的每个对象都有一个锁和一个等待队列，就是在这里实现的。 monitor 对象由 C++ 实现。其中有三个关键字段：

  - _owner 记录当前持有锁的线程

  - _EntryList 是一个队列，记录所有阻塞等待锁的线程

  - _WaitSet 也是一个队列，记录调用 wait() 方法并还未被通知的线程。

- Monitor的操作机制如下：

  - 多个线程竞争锁时，会先进入 EntryList 队列。竞争成功的线程被标记为 Owner。其他线程继续在此队列中阻塞等待。

  - 如果 Owner 线程调用 wait() 方法，则其释放对象锁并进入 WaitSet 中等待被唤醒。Owner 被置空，EntryList 中的线程再次竞争锁。

  - 如果 Owner 线程执行完了，便会释放锁，Owner 被置空，EntryList 中的线程再次竞争锁。

#### JVM 对 synchronized 的处理

上面了解了 monitor 的机制，那虚拟机是如何将 synchronized 和 monitor 关联起来的呢？分两种情况：

- 如果同步的是代码块，编译时会直接在同步代码块前加上 monitorenter 指令，代码块后加上 monitorexit 指令。这称为显示同步。
- 如果同步的是方法，虚拟机会为方法设置 ACC_SYNCHRONIZED 标志。调用的时候 JVM 根据这个标志判断是否是同步方法。

#### JVM 对 synchronized 的优化

synchronized 是重量级锁，由于消耗太大，虚拟机对其做了一些优化。

- 自旋锁与自适应自旋
  - 在许多应用中，锁定状态只会持续很短的时间，为了这么一点时间去挂起恢复线程，不值得。我们可以让等待线程执行一定次数的循环，在循环中去获取锁。这项技术称为自旋锁，它可以节省系统切换线程的消耗，但仍然要占用处理器。在 JDK1.4.2 中，自选的次数可以通过参数来控制。 JDK 1.6又引入了自适应的自旋锁，不再通过次数来限制，而是由前一次在同一个锁上的自旋时间及锁的拥有者的状态来决定。

- 锁消除
  - 虚拟机在运行时，如果发现一段被锁住的代码中不可能存在共享数据，就会将这个锁清除。

- 锁粗化
  - 当虚拟机检测到有一串零碎的操作都对同一个对象加锁时，会把锁扩展到整个操作序列外部。如 StringBuffer 的 append 操作。

- 轻量级锁
  - 对绝大部分的锁来说，在整个同步周期内都不存在竞争。如果没有竞争，轻量级锁可以使用 CAS 操作避免使用互斥量的开销。

- 偏向锁
  - 偏向锁的核心思想是，如果一个线程获得了锁，那么锁就进入偏向模式，当这个线程再次请求锁时，无需再做任何同步操作，即可获取锁。

### 2.6.2 CAS

#### 操作模型

CAS 是 compare and swap 的简写，即比较并交换。它是指一种操作机制，而不是某个具体的类或方法。在 Java 平台上对这种操作进行了包装。在 Unsafe 类中，调用代码如下：

```java
unsafe.compareAndSwapInt(this, valueOffset, expect, update);
```

它需要三个参数，分别是内存位置 V，旧的预期值 A 和新的值 B。操作时，先从内存位置读取到值，然后和预期值A比较。如果相等，则将此内存位置的值改为新值 B，返回 true。如果不相等，说明和其他线程冲突了，则不做任何改变，返回 false。

这种机制在不阻塞其他线程的情况下避免了并发冲突，比独占锁的性能高很多。 CAS 在 Java 的原子类和并发包中有大量使用。

#### 重试机制（循环 CAS）

**有很多文章说，CAS 操作失败后会一直重试直到成功，这种说法很不严谨。**

第一，CAS 本身并未实现失败后的处理机制，它只负责返回成功或失败的布尔值，后续由调用者自行处理。只不过我们最常用的处理方式是重试而已。

第二，这句话很容易理解错，被理解成重新比较并交换。实际上失败的时候，原值已经被修改，如果不更改期望值，再怎么比较都会失败。而新值同样需要修改。

所以正确的方法是，使用一个死循环进行 CAS 操作，成功了就结束循环返回，失败了就重新从内存读取值和计算新值，再调用 CAS。看下 AtomicInteger 的源码就什么都懂了：

```java
public final int incrementAndGet () {
    for (;;) {
        int current = get();
        int next = current + 1;
        if (compareAndSet(current, next))
            return next;
    }
}
```

#### 底层实现

CAS 主要分三步，读取-比较-修改。其中比较是在检测是否有冲突，如果检测到没有冲突后，其他线程还能修改这个值，那么 CAS 还是无法保证正确性。所以最关键的是要保证比较-修改这两步操作的原子性。

CAS 底层是靠调用 CPU 指令集的 cmpxchg 完成的，它是 x86 和 Intel 架构中的 compare and exchange 指令。在多核的情况下，这个指令也不能保证原子性，需要在前面加上  lock 指令。lock 指令可以保证一个 CPU 核心在操作期间独占一片内存区域。那么 这又是如何实现的呢？

在处理器中，一般有两种方式来实现上述效果：总线锁和缓存锁。在多核处理器的结构中，CPU 核心并不能直接访问内存，而是统一通过一条总线访问。总线锁就是锁住这条总线，使其他核心无法访问内存。这种方式代价太大了，会导致其他核心停止工作。而缓存锁并不锁定总线，只是锁定某部分内存区域。当一个 CPU 核心将内存区域的数据读取到自己的缓存区后，它会锁定缓存对应的内存区域。锁住期间，其他核心无法操作这块内存区域。

CAS 就是通过这种方式实现比较和交换操作的原子性的。**值得注意的是， CAS 只是保证了操作的原子性，并不保证变量的可见性，因此变量需要加上 volatile 关键字。**

#### ABA 问题

上面提到，CAS 保证了比较和交换的原子性。但是从读取到开始比较这段期间，其他核心仍然是可以修改这个值的。如果核心将 A 修改为 B，CAS 可以判断出来。但是如果核心将 A 修改为 B 再修改回 A。那么 CAS 会认为这个值并没有被改变，从而继续操作。这是和实际情况不符的。解决方案是加一个版本号。

### 2.6.3 可重入锁 ReentrantLock

ReentrantLock 使用代码实现了和 synchronized 一样的语义，包括可重入，保证内存可见性和解决竞态条件问题等。相比 synchronized，它还有如下好处：

- 支持以非阻塞方式获取锁
- 可以响应中断
- 可以限时
- 支持了公平锁和非公平锁

基本用法如下：

```java
public class Counter {
    private final Lock lock = new ReentrantLock();
    private volatile int count;

    public void incr() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }

    public int getCount() {
        return count;
    }
}
```

ReentrantLock 内部有两个内部类，分别是 FairSync 和 NoFairSync，对应公平锁和非公平锁。他们都继承自 Sync。Sync 又继承自AQS。

### 2.6.4 AQS

AQS 全称 AbstractQueuedSynchronizer。AQS 中有两个重要的成员：

- 成员变量 state。用于表示锁现在的状态，用 volatile 修饰，保证内存一致性。同时所用对 state 的操作都是使用 CAS 进行的。state 为0表示没有任何线程持有这个锁，线程持有该锁后将 state 加1，释放时减1。多次持有释放则多次加减。
- 还有一个双向链表，链表除了头结点外，每一个节点都记录了线程的信息，代表一个等待线程。这是一个 FIFO 的链表。

下面以 ReentrantLock 非公平锁的代码看看 AQS 的原理。

#### 请求锁

请求锁时有三种可能：

1. 如果没有线程持有锁，则请求成功，当前线程直接获取到锁。
2. 如果当前线程已经持有锁，则使用 CAS 将 state 值加1，表示自己再次申请了锁，释放锁时减1。这就是可重入性的实现。
3. 如果由其他线程持有锁，那么将自己添加进等待队列。

```java
final void lock() {
    if (compareAndSetState(0, 1))   
        setExclusiveOwnerThread(Thread.currentThread()); //没有线程持有锁时，直接获取锁，对应情况1
    else
        acquire(1);
}

public final void acquire(int arg) {
    if (!tryAcquire(arg) && //在此方法中会判断当前持有线程是否等于自己，对应情况2
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg)) //将自己加入队列中，对应情况3
        selfInterrupt();
}
```

#### 创建 Node 节点并加入链表

如果没竞争到锁，这时候就要进入等待队列。队列是默认有一个 head 节点的，并且不包含线程信息。上面情况3中，addWaiter 会创建一个 Node，并添加到链表的末尾，Node 中持有当前线程的引用。同时还有一个成员变量 waitStatus，表示线程的等待状态，初始值为0。我们还需要关注两个值：

- CANCELLED，值为1，表示取消状态，就是说我不要这个锁了，请你把我移出去。
- SINGAL，值为-1，表示下一个节点正在挂起等待，注意是下一个节点，不是当前节点。

同时，加到链表末尾的操作使用了 CAS+死循环的模式，很有代表性，拿出来看一看：

```java
Node node = new Node(mode);
for (;;) {
    Node oldTail = tail;
    if (oldTail != null) {
        U.putObject(node, Node.PREV, oldTail);
        if (compareAndSetTail(oldTail, node)) {
            oldTail.next = node;
            return node;
        }
    } else {
        initializeSyncQueue();
    }
}
```

可以看到，在死循环里调用了 CAS 的方法。如果多个线程同时调用该方法，那么每次循环都只有一个线程执行成功，其他线程进入下一次循环，重新调用。N个线程就会循环N次。这样就在无锁的模式下实现了并发模型。

#### 挂起等待

- 如果此节点的上一个节点是头部节点，则再次尝试获取锁，获取到了就移除并返回。获取不到就进入下一步；
- 判断前一个节点的 waitStatus，如果是 SINGAL，则返回 true，并调用 LockSupport.park() 将线程挂起；
- 如果是 CANCELLED，则将前一个节点移除；
- 如果是其他值，则将前一个节点的 waitStatus 标记为 SINGAL，进入下一次循环。

可以看到，一个线程最多有两次机会，还竞争不到就去挂起等待。

```java
final boolean acquireQueued(final Node node, int arg) {
    try {
        boolean interrupted = false;
        for (;;) {
            final Node p = node.predecessor();
            if (p == head && tryAcquire(arg)) {
                setHead(node);
                p.next = null; // help GC
                return interrupted;
            }
            if (shouldParkAfterFailedAcquire(p, node) &&
                parkAndCheckInterrupt())
                interrupted = true;
        }
    } catch (Throwable t) {
        cancelAcquire(node);
        throw t;
    }
}
```

#### 释放锁

- 调用 tryRelease，此方法由子类实现。实现非常简单，如果当前线程是持有锁的线程，就将 state 减1。减完后如果 state 大于0，表示当前线程仍然持有锁，返回 false。如果等于0，表示已经没有线程持有锁，返回 true，进入下一步；
- 如果头部节点的 waitStatus 不等于0，则调用LockSupport.unpark()唤醒其下一个节点。头部节点的下一个节点就是等待队列中的第一个线程，这反映了 AQS 先进先出的特点。另外，即使是非公平锁，进入队列之后，还是得按顺序来。

```java
public final boolean release(int arg) {
    if (tryRelease(arg)) { //将 state 减1
        Node h = head;
        if (h != null && h.waitStatus != 0)
            unparkSuccessor(h);
        return true;
    }
    return false;
}

private void unparkSuccessor(Node node) {
    int ws = node.waitStatus;
    if (ws < 0)
        node.compareAndSetWaitStatus(ws, 0);
        
    Node s = node.next;
    if (s == null || s.waitStatus > 0) { 
        s = null;
        for (Node p = tail; p != node && p != null; p = p.prev)
            if (p.waitStatus <= 0)
                s = p;
    }
    if (s != null) //唤醒第一个等待的线程
        LockSupport.unpark(s.thread);
}
```

#### 公平锁如何实现

上面分析的是非公平锁，那公平锁呢？很简单，在竞争锁之前判断一下等待队列中有没有线程在等待就行了。

```java
protected final boolean tryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    int c = getState();
    if (c == 0) {
        if (!hasQueuedPredecessors() && //判断等待队列是否有节点
            compareAndSetState(0, acquires)) {
            setExclusiveOwnerThread(current);
            return true;
        }
    }
    ......
    return false;
}
```

### 2.6.4 可重入读写锁 ReentrantReadWriteLock

#### 读写锁机制

理解 ReentrantLock 和 AQS 之后，再来理解读写锁就很简单了。读写锁有一个读锁和一个写锁，分别对应读操作和锁操作。锁的特性如下：

- 只有一个线程可以获取到写锁。在获取写锁时，只有没有任何线程持有任何锁才能获取成功；
- 如果有线程正持有写锁，其他任何线程都获取不到任何锁；
- 没有线程持有写锁时，可以有多个线程获取到读锁。

上面锁的特点保证了可以并发读取，这大大提高了效率，在实际开发中非常有用。那么在具体是如何实现的呢？

#### 实现原理

读写锁虽然有两个锁，但实际上只有一个等待队列。

- 获取写锁时，要保证没有任何线程持有锁；
- 写锁释放后，会唤醒队列第一个线程，可能是读锁和写锁；
- 获取读锁时，先判断写锁有没有被持有，没有就可以获取成功；
- 获取读锁成功后，会将队列中等待读锁的线程挨个唤醒，知道遇到等待写锁的线程位置；
- 释放读锁时，要检查读锁数，如果为0，则唤醒队列中的下一个线程，否则不进行操作。



### 2.6.5 锁池和等待池

> 虽然java底层使用队列实现的,但是用池来描述会更容易理解,后面会看到
>
> 链接：https://juejin.cn/post/6844903876647190536

在Java中，每个对象都有两个池，锁(monitor)池和等待池

- 锁池:假设线程A已经拥有了某个对象的锁，而其它的线程想要调用这个对象的某个synchronized方法(或者synchronized块)，由于这些线程在进入对象的synchronized方法之前必须先获得该对象的锁的拥有权，但是该对象的锁目前正被线程A拥有，所以这些线程就进入了该对象的锁池中。
- 等待池:假设一个线程A调用了某个对象的wait()方法，线程A就会释放该对象的锁(因为wait()方法必须出现在synchronized中，这样自然在执行wait()方法之前线程A就已经拥有了该对象的锁)，同时线程A就进入到了该对象的等待池中。
  如果另外的一个线程调用了相同对象的notifyAll()方法，那么处于该对象的等待池中的线程就会全部进入该对象的锁池中，准备争夺锁的拥有权。如果另外的一个线程调用了相同对象的notify()方法，那么仅仅有一个处于该对象的等待池中的线程(随机)会进入该对象的锁池.

![16ba3e85f12c33b2~tplv-t2oaga2asx-jj-mark_3024_0_0_0_q75](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/Java/16ba3e85f12c33b2~tplv-t2oaga2asx-jj-mark_3024_0_0_0_q75.png)



这些都是与锁有关的优化技术，用于提高多线程程序的性能和并发能力。以下是它们的简要介绍：

1. **自适应的自旋锁（Adaptive Spin Lock）**：
   自适应的自旋锁是一种在多核处理器上进行性能优化的技术。在使用自旋锁时，线程会尝试获取锁，如果锁已经被其他线程持有，它会以自旋的方式等待锁释放。自适应的自旋锁能够根据当前线程竞争锁的情况动态调整自旋等待的时间，以提高性能。

2. **锁粗化（Lock Coarsening）**：
   锁粗化是一种将多个连续的加锁、解锁操作合并为一个锁操作的优化技术。当 JVM 发现一段代码中存在连续的加锁、解锁操作时，会将它们合并为一个更大的临界区，以减少加锁、解锁的次数，提高性能。

3. **锁消除（Lock Elimination）**：
   锁消除是一种在即时编译器中进行的优化技术，用于消除对不必要同步的操作。当编译器分析代码时发现某些对象只在单线程中访问，或者在同步块中对象的引用不会被逃逸到其他线程，就会将这些同步操作消除掉，以提高程序的执行效率。

4. **轻量级锁（Lightweight Lock）**：
   轻量级锁是一种针对多线程并发访问同步块的优化技术。当线程尝试获取锁时，首先会尝试通过CAS（Compare and Swap）操作来获取锁，如果成功则直接进入临界区执行；如果失败，则说明有其他线程持有了锁，此时会尝试自旋等待一段时间。如果自旋等待超时或者自旋次数达到一定阈值，那么锁升级为重量级锁（即使用操作系统提供的互斥量来实现），从而确保多个线程之间的同步安全。



# 八



# 八、RQs

1. RQ1: wait() vs sleep()

   - sleep()方法是线程类（Thread）的静态方法，导致此线程暂停执行指定时间，将执行机会给其他线程，但是监控状态依然保持，到时后会自动恢复（线程回到就绪（ready）状态），因为调用sleep 不会释放对象锁。

   - wait()是Object 类的方法，对此对象调用wait()方法导致本线程放弃对象锁(线程暂停执行)，进入等待此对象的等待锁定池，只有针对此对象发出notify 方法（或notifyAll）后本线程才进入对象锁定池准备获得对象锁进入就绪状态。
   - **对象锁定池（Object Monitor Pool）**：
     - **等待锁定池（Wait Set）**：这是一个主要的部分，用于管理等待获取对象锁的线程，这些线程会在调用对象的 `wait()` 方法后进入等待状态。
     - **拥有对象锁的线程（Owner）**：这是当前拥有对象锁的线程，即执行对象的 `synchronized` 方法或块的线程。只有一个线程可以拥有对象的锁。
     - **阻塞队列（Entry Set）**：这是一个线程队列，存储了请求获取对象锁但还未获取锁的线程。这些线程在等待队列中等待机会来争夺对象锁。



2. RQ2: run() vs start()
   - run()方法被称为线程执行体，它的方法体代表了线程需要完成的任务，而start()方法用来启动线程。调用start()方法启动线程时，系统会把该run()方法当成线程执行体来处理。但如果直接调用线程对象的run()方法，则run()方法立即就会被执行，而且在run()方法返回之前其他线程无法并发执行。也就是说，如果直接调用线程对象的run()方法，系统把线程对象当成一个普通对象，而run()方法也是一个普通方法，而不是线程执行体。

3. Thread vs Runnable 实现Runnable接口相比继承Thread类有如下优势
   - 可以避免由于Java的单继承特性而带来的局限
   - 增强程序的健壮性，代码能够被多个线程共享，代码与数据是独立的
   - 适合多个相同程序的线程区处理同一资源的情况
