

[TOC]

# JVM

参考资料

- https://pdai.tech/md/java/jvm/java-jvm-gc.html
- GPT-4o
- 狂神说-JVM

# 一、 JVM 体系结构

![截屏2024-02-26 16.03.19](./Java/截屏2024-02-2616.03.19.png)

# 二、存储结构

## 方法区

1. 放了些什么：每个类的结构信息（字段、方法数据、普通方法、构造方法），运行时常量池，静态变量内容。（这是规范，不同虚拟机的实现是不同的 最典型的就是永久代PermGen space和元空间Metaspace）实例变量在堆内存中，和方法区无关。

2. 绝对不是用来放方法的

3. 这块区域所有线程共享，存在垃圾回收。



## 栈

每个线程都有自己的栈，栈中的数据都是以栈帧的格式存在；在这个线程上正在执行的每一个方法都各自对应一个栈帧；栈帧是一个内存区块，是一个数据集维系着方法执行过程中的各种数据信息

- 栈：8大基本类型+对象引用+实例的方法

栈是运行时的单位，Java 虚拟机栈，线程私有，生命周期和线程一致。描述的是 Java 方法执行的内存模型：每个方法在执行时都会创建一个栈帧(Stack Frame)用于存储局部变量表、操作数栈、动态链接、方法出口等信息。每一个方法从调用直至执行结束，就对应着一个栈帧从虚拟机栈中入栈到出栈的过程。（方法头开始入栈，结束出栈，方法里面调用别的方法 新的方法就会把旧的压在底下，最上面永远是正在执行的方法，也对应先入后出。）

- 局部变量表：存放了编译期可知的各种基本类型(boolean、byte、char、short、int、float、long、double)、对象引用(reference 类型)和 returnAddress 类型(指向了一条字节码指令的地址)



## 堆

Heap，一个jvm只有一个堆内存，堆内存的大小是可以调节的。类加载器读取了类文件后，一般会把类、方法、常量、变量，保存我们所有引用类型的真实对象。

（下图为jdk8之前的，jdk8以后永久存储区的名字改为“元空间”）



![截屏2024-02-26 16.13.16](./Java/截屏2024-02-2616.13.16.png)



## 永久区

这个区域常驻内存的。用来存放JDK自身携带的class对象，interface元数据，储存的是java运行时的一些环境或类信息，这个区域不存在垃圾回收，关闭VM虚拟机就会释放这个区域的内存



Jdk1.6之前：永久代，常量池在方法区

Jdk1.7：永久代，慢慢退化，去永久代，常量池在堆中

Jdk1.8之后：无永久代，常量池在元空间

# 垃圾回收机制GC

## 判断一个对象是否可被回收

### 1. 引用计数算法

给对象添加一个引用计数器，当对象增加一个引用时计数器加 1，引用失效时计数器减 1。引用计数为 0 的对象可被回收。

两个对象出现循环引用的情况下，此时引用计数器永远不为 0，导致无法对它们进行回收。

正因为循环引用的存在，因此 Java 虚拟机不使用引用计数算法。

```java
public class ReferenceCountingGC {

    public Object instance = null;

    public static void main(String[] args) {
        ReferenceCountingGC objectA = new ReferenceCountingGC();
        ReferenceCountingGC objectB = new ReferenceCountingGC();
        objectA.instance = objectB;
        objectB.instance = objectA;
    }
}
```

### 2. 可达性分析算法

通过 GC Roots 作为起始点进行搜索，能够到达到的对象都是存活的，不可达的对象可被回收。

![0635cbe8](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/0635cbe8.png)

Java 虚拟机使用该算法来判断对象是否可被回收，在 Java 中 GC Roots 一般包含以下内容:

- 虚拟机栈中引用的对象
- 本地方法栈中引用的对象
- 方法区中类静态属性引用的对象
- 方法区中的常量引用的对象

### 3. 方法区的回收

因为方法区主要存放永久代对象，而永久代对象的回收率比新生代低很多，因此在方法区上进行回收性价比不高。主要是对常量池的回收和对类的卸载。

在大量使用反射、动态代理、CGLib 等 ByteCode 框架、动态生成 JSP 以及 OSGi 这类频繁自定义 ClassLoader 的场景都需要虚拟机具备类卸载功能，以保证不会出现内存溢出。

类的卸载条件很多，需要满足以下三个条件，并且满足了也不一定会被卸载:

- 该类所有的实例都已经被回收，也就是堆中不存在该类的任何实例。
- 加载该类的 ClassLoader 已经被回收。
- 该类对应的 Class 对象没有在任何地方被引用，也就无法在任何地方通过反射访问该类方法。

可以通过 -Xnoclassgc 参数来控制是否对类进行卸载。

### 4. finalize()

finalize() 类似 C++ 的析构函数，用来做关闭外部资源等工作。但是 try-finally 等方式可以做的更好，并且该方法运行代价高昂，不确定性大，无法保证各个对象的调用顺序，因此最好不要使用。

当一个对象可被回收时，如果需要执行该对象的 finalize() 方法，那么就有可能通过在该方法中让对象重新被引用，从而实现自救。自救只能进行一次，如果回收的对象之前调用了 finalize() 方法自救，后面回收时不会调用 finalize() 方法。



- `inalize()` 的功能

`finalize()` 方法是定义在 `java.lang.Object` 类中的一个方法。在对象即将被垃圾回收（Garbage Collection，GC）之前，垃圾回收器会调用这个方法。这个方法允许对象在被销毁之前进行清理工作，比如释放资源（文件句柄、数据库连接等）。

- `finalize()` 的声明

```
protected void finalize() throws Throwable {
    // 清理代码
}
```

- 缺点

  - **不可预测性**：
    - `finalize()` 的调用时间是不确定的，因为垃圾回收器何时运行是不确定的。在一些情况下，可能永远不会调用。

  - **性能开销**：
    - `finalize()` 的存在会增加对象的生命周期，因为垃圾回收器需要保持这些对象直到进入`finalize()` 阶段，导致内存无法及时释放。

  - **异常处理**：
    - 若 `finalize()` 方法抛出异常，且未被捕获，异常会被垃圾回收器忽略，不会向上抛出。

  - **替代方案更优**：
    - `finalize()` 已经被更好的清理机制取代，如`try-with-resources` 和 `java.lang.AutoCloseable` 接口。



## 引用类型

无论是通过引用计算算法判断对象的引用数量，还是通过可达性分析算法判断对象是否可达，判定对象是否可被回收都与引用有关。

Java 具有四种强度不同的引用类型。

### 1. 强引用

被强引用关联的对象不会被回收。

使用 new 一个新对象的方式来创建强引用。

```java
Object obj = new Object();
```

### 2. 软引用

被软引用关联的对象只有在内存不够的情况下才会被回收。

使用 SoftReference 类来创建软引用。

```java
Object obj = new Object();
SoftReference<Object> sf = new SoftReference<Object>(obj);
obj = null;  // 使对象只被软引用关联
```

### 3. 弱引用

被弱引用关联的对象一定会被回收，也就是说它只能存活到下一次垃圾回收发生之前。

使用 WeakReference 类来实现弱引用。

```java
Object obj = new Object();
WeakReference<Object> wf = new WeakReference<Object>(obj);
obj = null;
```

### 4. 虚引用

又称为幽灵引用或者幻影引用。一个对象是否有虚引用的存在，完全不会对其生存时间构成影响，也无法通过虚引用取得一个对象。

为一个对象设置虚引用关联的唯一目的就是能在这个对象被回收时收到一个系统通知。使用 PhantomReference 来实现虚引用。

```java
Object obj = new Object();
PhantomReference<Object> pf = new PhantomReference<Object>(obj);
obj = null;
```

1. 创建 PhantomReference 和 ReferenceQueue

`PhantomReference` 必须与 `ReferenceQueue` 一起使用。一个对象是否有虚引用的存在，完全不会对其生存时间构成影响，也无法通过虚引用直接取得一个对象。然而，当对象被垃圾回收时，如果该对象的虚引用被加入到与之关联的 `ReferenceQueue` 中，那么就可以通过 `ReferenceQueue` 来检测到这个事件。

2. 收到通知的机制

- 当垃圾回收器发现一个对象仅被虚引用引用时，会在该对象被回收后，将这个虚引用加入到与之关联的 `ReferenceQueue` 中。这种机制保证了在回收对象之后，但在对象内存被实际释放之前，我们可以通过 `ReferenceQueue` 接收到此对象已被回收的通知，并可以执行一些额外的清理操作。

---

代码示例

以下是一个使用 `PhantomReference` 和 `ReferenceQueue` 的示例，展示如何捕捉对象被垃圾回收的通知：

```java
import java.lang.ref.PhantomReference;
import java.lang.ref.ReferenceQueue;

class MyObject {
    @Override
    protected void finalize() throws Throwable {
        super.finalize();
        System.out.println("MyObject's finalize() method called");
    }
}

public class PhantomReferenceDemo {
    public static void main(String[] args) throws InterruptedException {
        // 创建一个ReferenceQueue
        ReferenceQueue<MyObject> referenceQueue = new ReferenceQueue<>();

        // 创建一个对象
        MyObject obj = new MyObject();

        // 创建一个PhantomReference，将obj和referenceQueue关联起来
        PhantomReference<MyObject> phantomReference = new PhantomReference<>(obj, referenceQueue);

        // 使obj不再强引用指向MyObject对象
        obj = null;

        // 强制进行垃圾回收（注意：在真实环境中不一定立刻进行回收）
        System.gc();
        System.runFinalization();

        // 检查是否有PhantomReference对象入队
        while (true) {
            PhantomReference<? extends MyObject> refFromQueue = (PhantomReference<? extends MyObject>) referenceQueue.poll();
            if (refFromQueue != null) {
                // 收到了对象被回收的通知
                System.out.println("PhantomReference is enqueued, MyObject is collected.");
                break;
            }
            // 休眠一段时间以防止CPU占用过高
            Thread.sleep(100);
        }
    }
}
```

**解释**

1. **创建ReferenceQueue**：
   - `ReferenceQueue<MyObject> referenceQueue = new ReferenceQueue<>();`
   - 创建一个`ReferenceQueue`对象。
2. **创建对象与PhantomReference**：
   - `MyObject obj = new MyObject();`
   - `PhantomReference<MyObject> phantomReference = new PhantomReference<>(obj, referenceQueue);`
   - 创建一个`MyObject`对象，并将其与一个`PhantomReference`以及`ReferenceQueue`关联。
3. **清除强引用**：
   - `obj = null;`
   - 将`obj`置为`null`，以便这个`MyObject`对象只有虚引用指向它。
4. **触发垃圾回收**：
   - `System.gc();` 和 `System.runFinalization();`
   - 触发垃圾回收器。这在真实的环境中不一定会立即尝试回收，但是为了演示的目的，我们强制执行垃圾回收和终结操作。
5. **收到通知**：
   - 通过`referenceQueue.poll();`方法检查是否有`PhantomReference`入队列。
   - 如果有则表示`MyObject`对象已被垃圾回收器回收，然后打印通知。

**注意事项**

- **不可直接访问对象**：通过虚引用无法直接访问所指向的对象。
- **垃圾回收时机不可控**：`System.gc()` 只是建议JVM进行垃圾回收，并不保证立即执行。而且对象的回收时机依赖于垃圾回收算法和JVM的实现，可能不会立即触发。
- **finalize方法**：由于`PhantomReference` 应该是在 `finalize` 方法执行之后才会通知我们，因此在实际编程中尽量避免依赖 `finalize` 方法进行关键业务逻辑。



## 垃圾回收算法

### 1. 标记 - 清除

![a4248c4b-6c1d-4fb8-a557-86da92d3a294](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/a4248c4b-6c1d-4fb8-a557-86da92d3a294.jpg)

**将存活的对象进行标记，然后清理掉未被标记的对象。**

- 不足:

  - 标记和清除过程效率都不高；

  - 会产生大量不连续的内存碎片，导致无法给大对象分配内存。

### 2. 标记 - 整理

![902b83ab-8054-4bd2-898f-9a4a0fe52830](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/902b83ab-8054-4bd2-898f-9a4a0fe52830.jpg)

让所有存活的对象都向一端移动，然后直接清理掉端边界以外的内存。

### 3. 复制

![e6b733ad-606d-4028-b3e8-83c3a73a3797](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/e6b733ad-606d-4028-b3e8-83c3a73a3797.jpg)

- 将内存划分为大小相等的两块，每次只使用其中一块，当这一块内存用完了就将还存活的对象复制到另一块上面，然后再把使用过的内存空间进行一次清理。主要不足是只使用了内存的一半。

- 现在的商业虚拟机都采用这种收集算法来回收新生代，但是并不是将新生代划分为大小相等的两块，而是分为一块较大的 Eden 空间和两块较小的 Survivor 空间，每次使用 Eden 空间和其中一块 Survivor。在回收时，将 Eden 和 Survivor 中还存活着的对象一次性复制到另一块 Survivor 空间上，最后清理 Eden 和使用过的那一块 Survivor。

- HotSpot 虚拟机的 Eden 和 Survivor 的大小比例默认为 8:1，保证了内存的利用率达到 90%。如果每次回收有多于 10% 的对象存活，那么一块 Survivor 空间就不够用了，此时需要依赖于老年代进行分配担保，也就是借用老年代的空间存储放不下的对象。

### 4. 分代收集

现在的商业虚拟机采用分代收集算法，它根据对象存活周期将内存划分为几块，不同块采用适当的收集算法。

一般将堆分为新生代和老年代。

- 新生代使用: 复制算法
- 老年代使用: 标记 - 清除 或者 标记 - 整理 算法

## 垃圾收集器

![c625baa0-dde6-449e-93df-c3a67f2f430f](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/c625baa0-dde6-449e-93df-c3a67f2f430f.jpg)

以上是 HotSpot 虚拟机中的 7 个垃圾收集器，连线表示垃圾收集器可以配合使用。

- 单线程与多线程: 单线程指的是垃圾收集器只使用一个线程进行收集，而多线程使用多个线程；
- 串行与并行: 串行指的是垃圾收集器与用户程序交替执行，这意味着在执行垃圾收集的时候需要停顿用户程序；并形指的是垃圾收集器和用户程序同时执行。除了 CMS 和 G1 之外，其它垃圾收集器都是以串行的方式执行。



### 1. Serial 收集器

![22fda4ae-4dd5-489d-ab10-9ebfdad22ae0](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/22fda4ae-4dd5-489d-ab10-9ebfdad22ae0.jpg)

Serial 翻译为串行，也就是说它以串行的方式执行。

它是单线程的收集器，只会使用一个线程进行垃圾收集工作。

它的优点是简单高效，对于单个 CPU 环境来说，由于没有线程交互的开销，因此拥有最高的单线程收集效率。

它是 Client 模式下的默认新生代收集器，因为在用户的桌面应用场景下，分配给虚拟机管理的内存一般来说不会很大。Serial 收集器收集几十兆甚至一两百兆的新生代停顿时间可以控制在一百多毫秒以内，只要不是太频繁，这点停顿是可以接受的。

### 2. ParNew 收集器

![81538cd5-1bcf-4e31-86e5-e198df1e013b](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/81538cd5-1bcf-4e31-86e5-e198df1e013b.jpg)

它是 Serial 收集器的多线程版本。

是 Server 模式下的虚拟机首选新生代收集器，除了性能原因外，主要是因为除了 Serial 收集器，只有它能与 CMS 收集器配合工作。

默认开启的线程数量与 CPU 数量相同，可以使用 -XX:ParallelGCThreads 参数来设置线程数。

### 3. Parallel Scavenge 收集器

与 ParNew 一样是多线程收集器。

其它收集器关注点是尽可能缩短垃圾收集时用户线程的停顿时间，而它的目标是达到一个可控制的吞吐量，它被称为“吞吐量优先”收集器。这里的吞吐量指 CPU 用于运行用户代码的时间占总时间的比值。

停顿时间越短就越适合需要与用户交互的程序，良好的响应速度能提升用户体验。而高吞吐量则可以高效率地利用 CPU 时间，尽快完成程序的运算任务，主要适合在后台运算而不需要太多交互的任务。

缩短停顿时间是以牺牲吞吐量和新生代空间来换取的: 新生代空间变小，垃圾回收变得频繁，导致吞吐量下降。

可以通过一个开关参数打开 GC 自适应的调节策略(GC Ergonomics)，就不需要手动指定新生代的大小(-Xmn)、Eden 和 Survivor 区的比例、晋升老年代对象年龄等细节参数了。虚拟机会根据当前系统的运行情况收集性能监控信息，动态调整这些参数以提供最合适的停顿时间或者最大的吞吐量。

### 4. Serial Old 收集器

------

![08f32fd3-f736-4a67-81ca-295b2a7972f2](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/08f32fd3-f736-4a67-81ca-295b2a7972f2.jpg)

是 Serial 收集器的老年代版本，也是给 Client 模式下的虚拟机使用。如果用在 Server 模式下，它有两大用途:

- 在 JDK 1.5 以及之前版本(Parallel Old 诞生以前)中与 Parallel Scavenge 收集器搭配使用。
- 作为 CMS 收集器的后备预案，在并发收集发生 Concurrent Mode Failure 时使用。

### 5. Parallel Old 收集器



![278fe431-af88-4a95-a895-9c3b80117de3](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/278fe431-af88-4a95-a895-9c3b80117de3.jpg)

是 Parallel Scavenge 收集器的老年代版本。

在注重吞吐量以及 CPU 资源敏感的场合，都可以优先考虑 Parallel Scavenge 加 Parallel Old 收集器。

### 6. CMS 收集器

![62e77997-6957-4b68-8d12-bfd609bb2c68](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/62e77997-6957-4b68-8d12-bfd609bb2c68.jpg)

CMS(Concurrent Mark Sweep)，Mark Sweep 指的是标记 - 清除算法。

分为以下四个流程:

- 初始标记: 仅仅只是标记一下 GC Roots 能直接关联到的对象，速度很快，需要停顿。
- 并发标记: 进行 GC Roots Tracing 的过程，它在整个回收过程中耗时最长，不需要停顿。
- 重新标记: 为了修正并发标记期间因用户程序继续运作而导致标记产生变动的那一部分对象的标记记录，需要停顿。
- 并发清除: 不需要停顿。

在整个过程中耗时最长的并发标记和并发清除过程中，收集器线程都可以与用户线程一起工作，不需要进行停顿。

具有以下缺点:

- 吞吐量低: 低停顿时间是以牺牲吞吐量为代价的，导致 CPU 利用率不够高。
- 无法处理浮动垃圾，可能出现 Concurrent Mode Failure。浮动垃圾是指并发清除阶段由于用户线程继续运行而产生的垃圾，这部分垃圾只能到下一次 GC 时才能进行回收。由于浮动垃圾的存在，因此需要预留出一部分内存，意味着 CMS 收集不能像其它收集器那样等待老年代快满的时候再回收。如果预留的内存不够存放浮动垃圾，就会出现 Concurrent Mode Failure，这时虚拟机将临时启用 Serial Old 来替代 CMS。
- 标记 - 清除算法导致的空间碎片，往往出现老年代空间剩余，但无法找到足够大连续空间来分配当前对象，不得不提前触发一次 Full GC。

### 7. G1 收集器

G1(Garbage-First)，它是一款面向服务端应用的垃圾收集器，在多 CPU 和大内存的场景下有很好的性能。HotSpot 开发团队赋予它的使命是未来可以替换掉 CMS 收集器。

堆被分为新生代和老年代，其它收集器进行收集的范围都是整个新生代或者老年代，而 G1 可以直接对新生代和老年代一起回收。

![4cf711a8-7ab2-4152-b85c-d5c226733807](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/4cf711a8-7ab2-4152-b85c-d5c226733807.png)

G1 把堆划分成多个大小相等的独立区域(Region)，新生代和老年代不再物理隔离。

![9bbddeeb-e939-41f0-8e8e-2b1a0aa7e0a7](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/9bbddeeb-e939-41f0-8e8e-2b1a0aa7e0a7.png)

通过引入 Region 的概念，从而将原来的一整块内存空间划分成多个的小空间，使得每个小空间可以单独进行垃圾回收。这种划分方法带来了很大的灵活性，使得可预测的停顿时间模型成为可能。通过记录每个 Region 垃圾回收时间以及回收所获得的空间(这两个值是通过过去回收的经验获得)，并维护一个优先列表，每次根据允许的收集时间，优先回收价值最大的 Region。

每个 Region 都有一个 Remembered Set，用来记录该 Region 对象的引用对象所在的 Region。通过使用 Remembered Set，在做可达性分析的时候就可以避免全堆扫描。

![f99ee771-c56f-47fb-9148-c0036695b5fe](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/f99ee771-c56f-47fb-9148-c0036695b5fe.jpg)

如果不计算维护 Remembered Set 的操作，G1 收集器的运作大致可划分为以下几个步骤:

- 初始标记
- 并发标记
- 最终标记: 为了修正在并发标记期间因用户程序继续运作而导致标记产生变动的那一部分标记记录，虚拟机将这段时间对象变化记录在线程的 Remembered Set Logs 里面，最终标记阶段需要把 Remembered Set Logs 的数据合并到 Remembered Set 中。这阶段需要停顿线程，但是可并行执行。
- 筛选回收: 首先对各个 Region 中的回收价值和成本进行排序，根据用户所期望的 GC 停顿时间来制定回收计划。此阶段其实也可以做到与用户程序一起并发执行，但是因为只回收一部分 Region，时间是用户可控制的，而且停顿用户线程将大幅度提高收集效率。

具备如下特点:

- 空间整合: 整体来看是基于“标记 - 整理”算法实现的收集器，从局部(两个 Region 之间)上来看是基于“复制”算法实现的，这意味着运行期间不会产生内存空间碎片。
- 可预测的停顿: 能让使用者明确指定在一个长度为 M 毫秒的时间片段内，消耗在 GC 上的时间不得超过 N 毫秒。



## 内存分配与回收策略

### Minor GC、Major GC、Full GC

JVM 在进行 GC 时，并非每次都对堆内存（新生代、老年代；方法区）区域一起回收的，大部分时候回收的都是指新生代。

针对 HotSpot VM 的实现，它里面的 GC 按照回收区域又分为两大类：部分收集（Partial GC），整堆收集（Full GC）

- 部分收集：不是完整收集整个 Java 堆的垃圾收集。其中又分为： 
  - 新生代收集（Minor GC/Young GC）：只是新生代的垃圾收集
  - 老年代收集（Major GC/Old GC）：只是老年代的垃圾收集 
    - 目前，只有 CMS GC 会有单独收集老年代的行为
    - 很多时候 Major GC 会和 Full GC 混合使用，需要具体分辨是老年代回收还是整堆回收
  - 混合收集（Mixed GC）：收集整个新生代以及部分老年代的垃圾收集 
    - 目前只有 G1 GC 会有这种行为
- 整堆收集（Full GC）：收集整个 Java 堆和方法区的垃圾

### 内存分配策略

#### 1. 对象优先在 Eden 分配

大多数情况下，对象在新生代 Eden 区分配，当 Eden 区空间不够时，发起 Minor GC。

#### 2. 大对象直接进入老年代

大对象是指需要连续内存空间的对象，最典型的大对象是那种很长的字符串以及数组。

经常出现大对象会提前触发垃圾收集以获取足够的连续空间分配给大对象。

-XX:PretenureSizeThreshold，大于此值的对象直接在老年代分配，避免在 Eden 区和 Survivor 区之间的大量内存复制。

#### 3. 长期存活的对象进入老年代

为对象定义年龄计数器，对象在 Eden 出生并经过 Minor GC 依然存活，将移动到 Survivor 中，年龄就增加 1 岁，增加到一定年龄则移动到老年代中。

-XX:MaxTenuringThreshold 用来定义年龄的阈值。

#### 4. 动态对象年龄判定

虚拟机并不是永远地要求对象的年龄必须达到 MaxTenuringThreshold 才能晋升老年代，如果在 Survivor 中相同年龄所有对象大小的总和大于 Survivor 空间的一半，则年龄大于或等于该年龄的对象可以直接进入老年代，无需等到 MaxTenuringThreshold 中要求的年龄。

#### 5. 空间分配担保

在发生 Minor GC 之前，虚拟机先检查老年代最大可用的连续空间是否大于新生代所有对象总空间，如果条件成立的话，那么 Minor GC 可以确认是安全的。

如果不成立的话虚拟机会查看 HandlePromotionFailure 设置值是否允许担保失败，如果允许那么就会继续检查老年代最大可用的连续空间是否大于历次晋升到老年代对象的平均大小，如果大于，将尝试着进行一次 Minor GC；如果小于，或者 HandlePromotionFailure 设置不允许冒险，那么就要进行一次 Full GC。

### Full GC 的触发条件

对于 Minor GC，其触发条件非常简单，当 Eden 空间满时，就将触发一次 Minor GC。而 Full GC 则相对复杂，有以下条件:

#### 1. 调用 System.gc()

只是建议虚拟机执行 Full GC，但是虚拟机不一定真正去执行。不建议使用这种方式，而是让虚拟机管理内存。

#### 2. 老年代空间不足

老年代空间不足的常见场景为前文所讲的大对象直接进入老年代、长期存活的对象进入老年代等。

为了避免以上原因引起的 Full GC，应当尽量不要创建过大的对象以及数组。除此之外，可以通过 -Xmn 虚拟机参数调大新生代的大小，让对象尽量在新生代被回收掉，不进入老年代。还可以通过 -XX:MaxTenuringThreshold 调大对象进入老年代的年龄，让对象在新生代多存活一段时间。

#### 3. 空间分配担保失败

使用复制算法的 Minor GC 需要老年代的内存空间作担保，如果担保失败会执行一次 Full GC。具体内容请参考上面的第五小节。

#### 4. JDK 1.7 及以前的永久代空间不足

在 JDK 1.7 及以前，HotSpot 虚拟机中的方法区是用永久代实现的，永久代中存放的为一些 Class 的信息、常量、静态变量等数据。

当系统中要加载的类、反射的类和调用的方法较多时，永久代可能会被占满，在未配置为采用 CMS GC 的情况下也会执行 Full GC。如果经过 Full GC 仍然回收不了，那么虚拟机会抛出 java.lang.OutOfMemoryError。

为避免以上原因引起的 Full GC，可采用的方法为增大永久代空间或转为使用 CMS GC。

#### 5. Concurrent Mode Failure

执行 CMS GC 的过程中同时有对象要放入老年代，而此时老年代空间不足(可能是 GC 过程中浮动垃圾过多导致暂时性的空间不足)，便会报 Concurrent Mode Failure 错误，并触发 Full GC。

## GC - Java 垃圾回收器之G1详解

> G1垃圾回收器是在Java7 update 4之后引入的一个新的垃圾回收器。同优秀的CMS垃圾回收器一样，G1也是关注最小时延的垃圾回收器，也同样适合大尺寸堆内存的垃圾收集，官方在ZGC还没有出现时也推荐使用G1来代替选择CMS。G1最大的特点是引入分区的思路，弱化了分代的概念，合理利用垃圾收集各个周期的资源，解决了其他收集器甚至CMS的众多缺陷。



### 1. 概述

G1垃圾回收器是在Java7 update 4之后引入的一个新的垃圾回收器。G1是一个分代的，增量的，并行与并发的标记-复制垃圾回收器。它的设计目标是为了适应现在不断扩大的内存和不断增加的处理器数量，进一步降低暂停时间（pause time），同时兼顾良好的吞吐量。G1回收器和CMS比起来，有以下不同：

- G1垃圾回收器是**compacting**的，因此其回收得到的空间是连续的。这避免了CMS回收器因为不连续空间所造成的问题。如需要更大的堆空间，更多的floating garbage。连续空间意味着G1垃圾回收器可以不必采用空闲链表的内存分配方式，而可以直接采用bump-the-pointer的方式；
- G1回收器的内存与CMS回收器要求的内存模型有极大的不同。G1将内存划分一个个固定大小的region，每个region可以是年轻代、老年代的一个。**内存的回收是以region作为基本单位的**；
- G1还有一个及其重要的特性：**软实时**（soft real-time）。所谓的实时垃圾回收，是指在要求的时间内完成垃圾回收。“软实时”则是指，用户可以指定垃圾回收时间的限时，G1会努力在这个时限内完成垃圾回收，但是G1并不担保每次都能在这个时限内完成垃圾回收。通过设定一个合理的目标，可以让达到90%以上的垃圾回收时间都在这个时限内。

### 2. G1的内存模型

#### 2.1 分区概念

- G1分区示意图

![java-jvm-gc-g1-1](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/java-jvm-gc-g1-1.jpeg)



##### 2.1.1 分区Region

G1采用了分区(Region)的思路，将整个堆空间分成若干个大小相等的内存区域，每次分配对象空间将逐段地使用内存。因此，在堆的使用上，G1并不要求对象的存储一定是物理上连续的，只要逻辑上连续即可；每个分区也不会确定地为某个代服务，可以按需在年轻代和老年代之间切换。启动时可以通过参数-XX:G1HeapRegionSize=n可指定分区大小(1MB~32MB，且必须是2的幂)，默认将整堆划分为2048个分区。

##### 2.1.2 卡片Card

在每个分区内部又被分成了若干个大小为512 Byte卡片(Card)，标识堆内存最小可用粒度所有分区的卡片将会记录在全局卡片表(Global Card Table)中，分配的对象会占用物理上连续的若干个卡片，当查找对分区内对象的引用时便可通过记录卡片来查找该引用对象(见RSet)。每次对内存的回收，都是对指定分区的卡片进行处理。

##### 2.1.3 堆Heap

G1同样可以通过-Xms/-Xmx来指定堆空间大小。当发生年轻代收集或混合收集时，通过计算GC与应用的耗费时间比，自动调整堆空间大小。如果GC频率太高，则通过增加堆尺寸，来减少GC频率，相应地GC占用的时间也随之降低；目标参数-XX:GCTimeRatio即为GC与应用的耗费时间比，G1默认为9，而CMS默认为99，因为CMS的设计原则是耗费在GC上的时间尽可能的少。另外，当空间不足，如对象空间分配或转移失败时，G1会首先尝试增加堆空间，如果扩容失败，则发起担保的Full GC。Full GC后，堆尺寸计算结果也会调整堆空间。

#### 2.2 分代模型

![java-jvm-gc-g1-2](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/java-jvm-gc-g1-2.jpeg)

##### 2.2.1 分代垃圾收集

分代垃圾收集可以将关注点集中在最近被分配的对象上，而无需整堆扫描，避免长命对象的拷贝，同时独立收集有助于降低响应时间。虽然分区使得内存分配不再要求紧凑的内存空间，但G1依然使用了分代的思想。与其他垃圾收集器类似，G1将内存在逻辑上划分为年轻代和老年代，其中年轻代又划分为Eden空间和Survivor空间。但年轻代空间并不是固定不变的，当现有年轻代分区占满时，JVM会分配新的空闲分区加入到年轻代空间。

整个年轻代内存会在初始空间`-XX:G1NewSizePercent`(默认整堆5%)与最大空间(默认60%)之间动态变化，且由参数目标暂停时间`-XX:MaxGCPauseMillis`(默认200ms)、需要扩缩容的大小以`-XX:G1MaxNewSizePercent`及分区的已记忆集合(RSet)计算得到。当然，G1依然可以设置固定的年轻代大小(参数-XX:NewRatio、-Xmn)，但同时暂停目标将失去意义。

##### 2.2.2 本地分配缓冲 Local allocation buffer (Lab)

值得注意的是，由于分区的思想，每个线程均可以"认领"某个分区用于线程本地的内存分配，而不需要顾及分区是否连续。因此，每个应用线程和GC线程都会独立的使用分区，进而减少同步时间，提升GC效率，这个分区称为本地分配缓冲区(Lab)。

其中，应用线程可以独占一个本地缓冲区(TLAB)来创建的对象，而大部分都会落入Eden区域(巨型对象或分配失败除外)，因此TLAB的分区属于Eden空间；而每次垃圾收集时，每个GC线程同样可以独占一个本地缓冲区(GCLAB)用来转移对象，每次回收会将对象复制到Suvivor空间或老年代空间；对于从Eden/Survivor空间晋升(Promotion)到Survivor/老年代空间的对象，同样有GC独占的本地缓冲区进行操作，该部分称为晋升本地缓冲区(PLAB)。

#### 2.3 分区模型

![java-jvm-gc-g1-3](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/java-jvm-gc-g1-3.jpeg)

G1对内存的使用以分区(Region)为单位，而对对象的分配则以卡片(Card)为单位。

##### 2.3.1 巨形对象Humongous Region

一个大小达到甚至超过分区大小一半的对象称为巨型对象(Humongous Object)。当线程为巨型分配空间时，不能简单在TLAB进行分配，因为巨型对象的移动成本很高，而且有可能一个分区不能容纳巨型对象。因此，巨型对象会直接在老年代分配，所占用的连续空间称为巨型分区(Humongous Region)。G1内部做了一个优化，一旦发现没有引用指向巨型对象，则可直接在年轻代收集周期中被回收。

巨型对象会独占一个、或多个连续分区，其中第一个分区被标记为开始巨型(StartsHumongous)，相邻连续分区被标记为连续巨型(ContinuesHumongous)。由于无法享受Lab带来的优化，并且确定一片连续的内存空间需要扫描整堆，因此确定巨型对象开始位置的成本非常高，如果可以，应用程序应避免生成巨型对象。

##### 2.3.2 已记忆集合Remember Set (RSet)

在串行和并行收集器中，GC通过整堆扫描，来确定对象是否处于可达路径中。然而G1为了避免STW式的整堆扫描，在每个分区记录了一个已记忆集合(RSet)，内部类似一个反向指针，记录引用分区内对象的卡片索引。当要回收该分区时，通过扫描分区的RSet，来确定引用本分区内的对象是否存活，进而确定本分区内的对象存活情况。

事实上，并非所有的引用都需要记录在RSet中，如果一个分区确定需要扫描，那么无需RSet也可以无遗漏的得到引用关系。那么引用源自本分区的对象，当然不用落入RSet中；同时，G1 GC每次都会对年轻代进行整体收集，因此引用源自年轻代的对象，也不需要在RSet中记录。最后只有老年代的分区可能会有RSet记录，这些分区称为拥有RSet分区(an RSet’s owning region)。

##### 2.3.3 Per Region Table (PRT)

RSet在内部使用Per Region Table(PRT)记录分区的引用情况。由于RSet的记录要占用分区的空间，如果一个分区非常"受欢迎"，那么RSet占用的空间会上升，从而降低分区的可用空间。G1应对这个问题采用了改变RSet的密度的方式，在PRT中将会以三种模式记录引用：

- 稀少：直接记录引用对象的卡片索引
- 细粒度：记录引用对象的分区索引
- 粗粒度：只记录引用情况，每个分区对应一个比特位

由上可知，粗粒度的PRT只是记录了引用数量，需要通过整堆扫描才能找出所有引用，因此扫描速度也是最慢的。

#### 2.4 收集集合 (CSet)

CSet收集示意图

![java-jvm-gc-g1-4](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/Java/JVM/java-jvm-gc-g1-4.jpeg)













# 三、 类加载机制

- 说明：当某个类加载器需要加载某个.class文件时，它首先把这个任务委托给他的上级类加载器，递归这个操作，如果上级的类加载器没有加载，自己才会去加载这个类。

- 作用：

  1. 防止重复加载同一个.class。通过委托去向上面问一问，加载过了，就不用再加载一遍。保证数据安全。

  2. 保证核心.class不能被篡改。通过委托方式，不会去篡改核心.class，即使篡改也不会去加载，即使加载也不会是同一个.class对象了。不同的加载器加载同一个.class也不是同一个Class对象。这样保证了Class执行安全。

- 类加载器类别：（由上至下）

  - BootstrapClassLoader（启动类加载器）-> ExtClassLoader （标准扩展类加载器）-> AppClassLoader（系统类加载器）->CustomClassLoader（用户自定义类加载器）

- 流程图（理解，向上委托，向下加载）

  ![截屏2024-02-26 16.05.51](./Java/截屏2024-02-2616.05.51.png)





##  native关键字

1、一个native方法就是一个Java调用非Java代码的接口。一个native方法是指该方法的实现由非Java语言实现，比如用C或C++实现。

2、在定义一个native方法时，并不提供实现体（比较像定义一个Java Interface），因为其实现体是由非Java语言在外面实现的。主要是因为JAVA无法对操作系统底层进行操作，但是可以通过JNI(java native interface java本地方法接口)调用其他语言来实现底层的访问。

举例：Thread类中的start() 方法中调用一个start0()的native方法。





### OOM

发生**OOM**内存溢出，解决方法

A、 尝试扩大堆内存看结果

B、 分析内存，看一下哪个地方出现问题（专业工具）

**1**、内存溢出：（**Out Of Memory—-OOM**）

系统已经不能再分配出你所需要的空间，比如系统现在只有1G的空间，但是你偏偏要2个G空间，这就叫内存溢出

例子：一个盘子用尽各种方法只能装4个果子，你装了5个，结果掉倒地上不能吃了。这就是溢出。比方说栈，栈满时再做进栈必定产生空间

溢出，叫上溢，栈空时再做退栈也产生空间溢出，称为下溢。就是分配的内存不足以放下数据项序列,称为内存溢出。说白了就是我承受不了

那么多，那就报错。

**2**、内存泄漏： **(Memory Leak)**

强引用所指向的对象不会被回收，可能导致内存泄漏，虚拟机宁愿抛出OOM也不会去回收他指向的对象，意思就是你用资源的时候为他开辟了一段空间，当你用完时忘记释放资源了，这时内存还被占用着，一次没关系，但是内存泄漏次数多了就会导致内存溢出

**3**、**JProfiler**工具分析**OOM**原因：

分析Dump内存文件，快速定位内存泄漏

获得堆中的数据

获得大的对象



#  JVM 调优

对JVM内存的系统级的调优主要的目的是减少GC的频率和Full GC的次数。

JVM性能调优方法和步骤：

1.监控GC的状态；

2.生成堆的dump文件；

3.分析dump文件；

4.分析结果，判断是否需要优化；

5.调整GC类型和内存分配；

6.不断的分析和调整





# 常见面试问题

## 5.3 JVM

### 5.3.1 GC root有哪些

在Java中，GC（Garbage Collection）Roots是指一组对象，它们被认为是存活的对象，不会被垃圾回收器回收。GC Roots主要包括以下几种类型：

1. **虚拟机栈中引用的对象**：虚拟机栈中保存着每个线程的栈帧，栈帧中包含了局部变量表。如果局部变量表中引用了对象，这些对象被认为是GC Roots。

2. **方法区中静态变量引用的对象**：方法区存储了类的信息、常量、静态变量等。如果静态变量引用了对象，这些对象被认为是GC Roots。

3. **方法区中常量引用的对象**：方法区中的常量池保存了字符串常量、类名、方法名等信息。如果常量池中引用了对象，这些对象被认为是GC Roots。

4. **本地方法栈中JNI（Java Native Interface）引用的对象**：JNI是Java调用本地方法的接口，本地方法中引用的对象被认为是GC Roots。

5. **活动线程**：正在执行的线程被认为是GC Roots，因为它们持有虚拟机栈中的引用。

6. **JNI引用的全局变量**：JNI中使用的全局变量引用的对象被认为是GC Roots。

这些GC Roots对象被认为是存活的对象，它们可以直接或间接引用其他对象，形成对象之间的引用链。垃圾回收器通过扫描GC Roots对象，找到所有可达的对象，将不可达的对象标记为垃圾并进行回收。GC Roots的存在保证了内存中的对象之间的引用关系，防止出现内存泄漏和不可达对象无法被回收的情况。



### 5.3.2 栈会溢出吗？什么时候溢出？方法区会溢出吗？

- 栈是线程私有的，它的生命周期与线程相同，每个方法在执行的时候都会创建一个栈帧，用来存储局部变量表，操作数栈，动态链接，方法出口等信息。局部变量表又包含基本数据类型，对象引用类型。
- 如果线程请求的栈深度大于虚拟机所允许的最大深度，将抛出 StackOverflowError 异常，方法递归调用产生这种结果。如果Java虚拟机栈可以动态扩展，并且扩展的动作已经尝试过，但是无法申请到足够的内存去完成扩展，或者在新建立线程的时候没有足够的内存去创建对应的虚拟机栈，那么Java虚拟机将抛出一个OutOfMemory异常。(线程启动过多)。
- 方法区会发生溢出。方法区用于存放 Class 的相关信息，如类名、访问修饰符、常量池、字段描述、方法描述等，如果动态生成大量的 Class 文件，也会产生内存溢出。常见的场景还有：大量 JSP 或动态产生 JSP 文件的应用（JSP 第一次运行时需要编译为 java 类）、基于 OSGi 的应用（即使是同一个类文件，被不同的类加载器加载也会视为不同的类）



### 5.3.3 哪些情况下的对象会被垃圾回收机制处理掉？

利用可达性分析算法，虚拟机会将一些对象定义为 GCRoots，从 GCRoots 出发沿着引用链向下寻找，如果某个对象不能通过 GCRoots 寻找到，虚拟机就认为该对象可以被回收掉。

- 哪些对象可以被看做是 GCRoots 呢？
  1）虚拟机栈（栈帧中的本地变量表）中引用的对象；
  2）方法区中的类静态属性引用的对象，常量引用的对象；
  3）本地方法栈中 JNI(Native 方法）引用的对象；

- 对象不可达，一定会被垃圾收集器回收么？
  即使不可达，对象也不一定会被垃圾收集器回收

  1）先判断对象是否有必要执行 finalize() 方法，对象必须重写 finalize() 方法且没有被运行过。

  2）若有必要执行，会把对象放到一个队列中，JVM 会开一个线程去回收它们，这是对象最后一次可以逃逸清理的机会。

---

垃圾回收机制主要处理以下情况下的对象：
1. **不再被引用的对象**：当一个对象没有任何引用指向它时，即没有任何变量指向该对象，这个对象就成为垃圾对象，会被垃圾回收机制处理掉。
2. **循环引用的对象**：如果一组对象之间相互引用形成了循环，即使这组对象互相引用，但与程序的根对象之间没有引用链，这些对象也会被当作垃圾对象处理。
3. **弱引用、软引用、虚引用对象**：当对象只有弱引用、软引用或虚引用指向时，垃圾回收机制可能会回收这些对象，根据引用的强度来决定对象的生命周期。
4. **过期的对象**：某些对象可能会根据一定的规则被标记为过期对象，例如缓存中的对象超过一定时间没有被访问就可以被回收。
5. **堆内存不足时**：当堆内存不足时，垃圾回收机制会根据不同的算法来回收一些不再被使用的对象，以释放内存空间。

总的来说，垃圾回收机制主要处理那些不再被程序使用的对象，以释放内存空间并提高程序的性能和效率。通过自动回收这些不再需要的对象，垃圾回收机制可以减少内存泄漏和提高内存利用率。

---

`finalize()` 方法是Java中的一个方法，定义在`Object`类中，用于在对象被垃圾收集器回收之前执行一些清理操作。当一个对象即将被回收时，垃圾收集器会首先调用该对象的`finalize()`方法，然后再将其回收。

在对象的生命周期中，`finalize()` 方法可以被重写，以实现一些清理操作，比如关闭文件、释放资源、断开网络连接等。开发人员可以在`finalize()`方法中编写需要在对象被回收前执行的清理代码。

需要注意的是，虽然`finalize()`方法提供了一种机制来执行清理操作，但它并不保证一定会被及时执行，也不建议过度依赖它。因为垃圾收集器的回收行为是不确定的，`finalize()`方法的执行时机也是不确定的，可能会导致一些不可预测的问题。

从Java 9 开始，`finalize()`方法被标记为`@Deprecated`，意味着不建议继续使用它。推荐使用更可靠的资源管理方式，比如使用`try-with-resources`语句来确保资源的及时释放。

---

`try-with-resources` 是 Java 7 引入的一个特性，用于简化资源管理的代码编写，并确保在代码块结束时自动关闭资源。这个特性可以自动关闭实现了 `AutoCloseable` 接口的资源，比如文件流、网络连接等，无需手动编写 `finally` 块来释放资源。

**原理**：

`try-with-resources` 使用了 Java 中的自动关闭资源的机制，通过在 `try` 关键字后面的括号中声明资源，这些资源会在代码块执行结束后自动关闭。在 `try` 块结束时，会调用资源的 `close()` 方法来释放资源。

**代码实现**：

下面是一个简单的示例，演示如何使用 `try-with-resources` 来自动关闭文件流：

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TryWithResourcesExample {
    public static void main(String[] args) {
        String filePath = "example.txt";

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

在上面的代码中，我们使用 `try-with-resources` 语句来创建一个 `BufferedReader` 对象，并读取文件内容。在 `try` 块结束时，会自动调用 `BufferedReader` 对象的 `close()` 方法来关闭文件流。

使用 `try-with-resources` 可以减少代码量，提高代码的可读性，同时确保资源的及时释放，避免资源泄漏的问题。



### 5.3.4  G1 收集器有哪些特点？

- G1 的全称是 Garbage-First，意为垃圾优先，哪一块的垃圾最多就优先清理它。
- G1 GC 最主要的设计目标是：将 STW 停顿的时间和分布，变成可预期且可配置的。被视为 JDK1.7 中 HotSpot 虚拟机的一个重要进化特征。它具备一下特点：
- 并行与并发：G1 能充分利用 CPU、多核环境下的硬件优势，使用多个 CPU（CPU 或者 CPU 核心）来缩短 Stop-The-World 停顿时间。部分其他收集器原本需要停顿 Java 线程执行的 GC 动作，G1 收集器仍然可以通过并发的方式让 java 程序继续执行。
- 分代收集：虽然 G1 可以不需要其他收集器配合就能独立管理整个 GC 堆，但是还是保留了分代的概念。
- 空间整合：与 CMS 的“标记-清理”算法不同，G1 从整体来看是基于“标记-整理”算法实现的收集器；从局部上来看是基于“标记-复制”算法实现的。
- 可预测的停顿：这是 G1 相对于 CMS 的另一个大优势，降低停顿时间是 G1 和 CMS 共同的关注点，但 G1 除了追求低停顿外，还能建立可预测的停顿时间模型，能让使用者明确指定在一个长度为 M 毫秒的时间片段内。G1 收集器在后台维护了一个优先列表，每次根据允许的收集时间，优先选择回收价值最大的 Region（这也就是它的名字 Garbage-First 的由来）

### 5.3.5 有哪些手段来排查 OOM 的问题？

- 增加两个参数
  -  -XX:+HeapDumpOnOutOfMemoryError
  - -XX:HeapDumpPath=/tmp/heapdump.hprof，当 OOM 发生时自动 dump 堆内存信息到指定目录。

- 同时 jstat 查看监控 JVM 的内存和 GC 情况，先观察问题大概出在什么区域。
- 使用 MAT 工具载入到 dump 文件，分析大对象的占用情况，比如 HashMap 做缓存未清理，时间长了就会内存溢出，可以把改为弱引用

---

排查 OutOfMemoryError（OOM）问题是一个常见的任务，以下是一些常用的手段来排查 OOM 问题：

1. **查看堆内存使用情况**：通过监控工具（如VisualVM、JConsole、JMC等）来查看应用程序的堆内存使用情况，包括堆内存大小、已使用内存、垃圾回收情况等。

2. **查看堆内存快照**：通过工具（如MAT、YourKit等）获取堆内存快照，分析哪些对象占用了大量内存，是否存在内存泄漏。

3. **分析代码逻辑**：检查代码中是否存在内存泄漏的情况，比如未关闭资源、静态集合持有大量对象、缓存对象过多等。

4. **查看日志**：查看应用程序的日志文件，寻找是否有内存相关的异常信息或警告。

5. **调整 JVM 参数**：根据应用程序的需求和性能表现，调整 JVM 参数，如堆内存大小、GC 算法、GC 垃圾回收器等。

6. **分析 GC 日志**：通过启用 GC 日志并分析日志内容，了解垃圾回收的情况和频率，是否存在频繁的 Full GC 情况。

7. **使用内存分析工具**：结合内存分析工具（如Eclipse Memory Analyzer、VisualVM、MAT等）来分析内存使用情况，找出内存占用较高的对象和代码路径。

8. **代码 Review**：进行代码审查，检查是否存在不当的内存使用方式或者设计问题。

通过以上手段的结合使用，可以帮助定位并解决应用程序中的 OutOfMemoryError 问题。

