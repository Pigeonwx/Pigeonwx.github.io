# C++

> https://leetcode.cn/leetbook/read/da-han-hou-duan-gang-ti-mu-he-ji-shang/nlfox5/

# 基本语法
智能指针是 C++ 中的一种特殊指针类型，用于自动管理动态分配的内存。它们通过封装原始指针，提供了更安全和方便的内存管理方式，帮助防止内存泄漏和悬空指针等问题。

## 智能指针

- 智能指针的优点
  - **自动内存管理**：智能指针会在超出作用域时自动释放内存，减少了手动管理内存的负担。
  - **防止内存泄漏**：由于智能指针会自动释放内存，减少了内存泄漏的风险。
  - **安全性**：智能指针提供了更安全的内存管理，避免了悬空指针和双重释放等问题。

C++ 标准库提供了几种智能指针，主要包括：

1. **`std::unique_ptr`**：
   - 表示对动态分配对象的独占所有权。
   - 不能被复制，只能移动（move），确保同一时间只有一个 `unique_ptr` 拥有该对象。
   - 当 `unique_ptr` 被销毁时，它所管理的对象也会被自动释放。

   ```cpp
   std::unique_ptr<MyClass> ptr(new MyClass());
   ```

2. **`std::shared_ptr`**：
   - 表示对动态分配对象的共享所有权。
   - 可以被多个 `shared_ptr` 实例共享，内部使用引用计数来管理对象的生命周期。
   - 当最后一个 `shared_ptr` 被销毁时，所管理的对象才会被释放。

   ```cpp
   std::shared_ptr<MyClass> ptr1(new MyClass());
   std::shared_ptr<MyClass> ptr2 = ptr1; // 共享所有权
   ```

3. **`std::weak_ptr`**：
   - 用于解决 `shared_ptr` 可能导致的循环引用问题。
   - 不增加引用计数，因此不会阻止所管理对象的销毁。
   - 可以通过 `shared_ptr` 来访问对象，但需要先检查对象是否仍然存在。

   ```cpp
   std::weak_ptr<MyClass> weakPtr = ptr1; // 不增加引用计数
   ```
---

**使用示例**

```cpp
#include <iostream>
#include <memory>

class MyClass {
public:
    MyClass() { std::cout << "MyClass created\n"; }
    ~MyClass() { std::cout << "MyClass destroyed\n"; }
};

int main() {
    {
        std::unique_ptr<MyClass> ptr1(new MyClass()); // 创建 unique_ptr
        // std::unique_ptr<MyClass> ptr2 = ptr1; // 错误：不能复制
        std::unique_ptr<MyClass> ptr2 = std::move(ptr1); // 移动所有权
    } // ptr2 超出作用域，MyClass 被销毁

    {
        std::shared_ptr<MyClass> ptr1(new MyClass()); // 创建 shared_ptr
        std::shared_ptr<MyClass> ptr2 = ptr1; // 共享所有权
    } // ptr1 和 ptr2 超出作用域，MyClass 被销毁

    return 0;
}
```

## Lambda
C++11 引入了 lambda 表达式，这是一种可以在代码中定义匿名函数的方式。Lambda 表达式使得在需要函数对象的地方（如 STL 算法、线程等）能够更方便地使用函数。下面将详细介绍 C++ lambda 表达式的语法、特性和使用示例。

### 1. Lambda 表达式的基本语法

C++ 中的 lambda 表达式的基本语法如下：

```cpp
[capture](parameters) -> return_type {
    // function body
}
```

- **capture**：捕获列表，用于指定 lambda 表达式可以访问的外部变量。
- **parameters**：参数列表，类似于普通函数的参数。
- **return_type**：返回类型，可以省略，编译器会根据函数体推导。
- **function body**：函数体，包含要执行的代码。

### 2. 捕获列表

捕获列表用于指定 lambda 表达式可以访问的外部变量。捕获方式有以下几种：

- **按值捕获**：使用 `=`，表示按值捕获外部变量的副本。
- **按引用捕获**：使用 `&`，表示按引用捕获外部变量。
- **混合捕获**：可以同时使用按值和按引用捕获。
- **捕获所有变量**：使用 `=` 捕获所有变量的副本，使用 `&` 捕获所有变量的引用。

**示例**

```cpp
int x = 10;
int y = 20;

// 按值捕获
auto lambda1 = [x]() {
    return x + 5; // 这里 x 是按值捕获的
};

// 按引用捕获
auto lambda2 = [&y]() {
    return y + 5; // 这里 y 是按引用捕获的
};

// 混合捕获
auto lambda3 = [x, &y]() {
    return x + y; // x 按值捕获，y 按引用捕获
};
```

### 3. 参数和返回类型

参数和返回类型的定义与普通函数相似。可以省略返回类型，编译器会根据函数体推导。

**示例**

```cpp
auto lambda = [](int a, int b) -> int {
    return a + b;
};

// 使用 lambda
int result = lambda(5, 3); // result = 8
```

### 4. 使用示例

#### 4.1 在 STL 算法中使用

Lambda 表达式常用于 STL 算法，如 `std::sort`、`std::for_each` 等。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};

    // 使用 lambda 表达式打印每个元素
    std::for_each(vec.begin(), vec.end(), [](int n) {
        std::cout << n << " ";
    });
    std::cout << std::endl;

    // 使用 lambda 表达式进行排序
    std::sort(vec.begin(), vec.end(), [](int a, int b) {
        return a > b; // 降序排序
    });

    // 打印排序后的结果
    std::for_each(vec.begin(), vec.end(), [](int n) {
        std::cout << n << " ";
    });
    std::cout << std::endl;

    return 0;
}
```

### 5. Lambda 表达式的特性

- **类型**：Lambda 表达式的类型是一个唯一的、不可命名的类型。可以通过 `auto` 关键字来声明 lambda。
- **可调用性**：Lambda 表达式可以像普通函数一样被调用。
- **状态**：Lambda 表达式可以捕获外部变量的状态，这使得它们在某些情况下非常灵活。
- **内联**：Lambda 表达式可以在需要函数的地方直接定义，避免了额外的函数定义。

### 6. 递归 Lambda

C++14 引入了支持递归的 lambda 表达式。可以通过使用 `std::function` 来实现递归。

```cpp
#include <iostream>
#include <functional>

int main() {
    std::function<int(int)> factorial = [&](int n) {
        return (n <= 1) ? 1 : n * factorial(n - 1);
    };

    std::cout << "Factorial of 5: " << factorial(5) << std::endl; // 输出 120

    return 0;
}
```

### 7. 总结

C++ 的 lambda 表达式提供了一种简洁的方式来定义匿名函数，支持捕获外部变量，适用于 STL 算法和多线程编程等场景。通过灵活的捕获方式和可调用性，lambda 表达式使得代码更加简洁和易于维护。

# C++特性
C++ 语言自其首次发布以来经历了多个版本的演进。以下是 C++ 的主要版本及其关键特性：

| 版本   | 发布年份 | 关键特性                                                                                     |
|--------|----------|----------------------------------------------------------------------------------------------|
| C++98  | 1998     | - 引入标准模板库（STL）<br>- 支持命名空间（namespace）<br>- 异常处理（try, catch, throw）<br>- 模板（template） |
| C++03  | 2003     | - 对 C++98 的小幅修订，主要是修复缺陷和不一致性                                             |
| C++11  | 2011     | - 自动类型推导（auto）<br>- 范围基于的 for 循环<br>- Lambda 表达式<br>- 智能指针（如 `std::shared_ptr`）<br>- 线程库支持<br>- 右值引用和移动语义<br>- `nullptr` |
| C++14  | 2014     | - 泛型 lambda<br>- `std::make_unique`<br>- 二进制字面量（如 `0b1010`）<br>- 增强的 constexpr |
| C++17  | 2017     | - 结构化绑定<br>- `std::optional`<br>- `std::variant`<br>- 增强的并行算法<br>- 文件系统库（`<filesystem>`） |
| C++20  | 2020     | - 概念（concepts）<br>- 范围（ranges）<br>- 协程（coroutines）<br>- 增强的 constexpr<br>- `std::format` |
| C++23  | 2023（预计） | - 计划引入更多语言特性和库功能，如 `std::expected` 和 `std::flat_map`（尚未完全确定） |

## 1. C++98
- **发布年份**：1998
- **关键特性**：
  - 引入了标准模板库（STL），提供了常用的数据结构和算法。
  - 支持命名空间（namespace），解决了名称冲突的问题。
  - 引入了异常处理机制（try, catch, throw）。
  - 支持模板（template），允许编写泛型代码。

## 2. C++03
- **发布年份**：2003
- **关键特性**：
  - C++03 是对 C++98 的小幅修订，主要是修复了一些缺陷和不一致性，没有引入新的特性。

## 3. C++11
- **发布年份**：2011
- **关键特性**：
  - 引入了自动类型推导（auto）。
  - 支持范围基于的 for 循环（range-based for loop）。
  - 引入了 lambda 表达式，支持更简洁的函数对象。
  - 引入了智能指针（如 `std::shared_ptr` 和 `std::unique_ptr`）。
  - 支持线程库（`<thread>`），引入了多线程编程的支持。
  - 引入了右值引用（rvalue references）和移动语义（move semantics），提高了性能。
  - 引入了 `nullptr`，替代了 `NULL`。

### std::move
`std::move` 是 C++11 引入的一个标准库函数，位于 `<utility>` 头文件中。它的主要作用是将一个对象的值转换为一个右值引用，从而支持移动语义（move semantics）。移动语义允许资源（如动态分配的内存、文件句柄等）在对象之间高效地转移，而不是进行昂贵的复制操作。

#### 1. **基本概念**

- **右值和左值**：
  - **左值**（lvalue）：表示一个持久的对象，可以取地址的表达式。
  - **右值**（rvalue）：表示一个临时的对象，通常是一个表达式的结果，不能取地址。

- **移动语义**：通过移动语义，可以将资源的所有权从一个对象转移到另一个对象，而不需要复制资源。这在处理大型对象时可以显著提高性能。

#### 2. **`std::move` 的作用**

`std::move` 的作用是将一个左值转换为右值引用。它本身并不执行任何移动操作，而是提供了一种将对象标记为可以被移动的方式。

```cpp
#include <iostream>
#include <utility> // for std::move
#include <vector>

class MyClass {
public:
    MyClass() { std::cout << "Constructor\n"; }
    MyClass(const MyClass&) { std::cout << "Copy Constructor\n"; }
    MyClass(MyClass&&) noexcept { std::cout << "Move Constructor\n"; }
    ~MyClass() { std::cout << "Destructor\n"; }
};

int main() {
    MyClass obj1; // Constructor
    MyClass obj2 = std::move(obj1); // Move Constructor
    return 0;
}
```

在上面的例子中，`std::move(obj1)` 将 `obj1` 转换为右值引用，从而调用了移动构造函数，而不是复制构造函数。

#### 3. **使用场景**

- **容器类**：在 STL 容器（如 `std::vector`、`std::string` 等）中，使用 `std::move` 可以在插入或返回对象时避免不必要的复制。
  
- **自定义类**：在自定义类中实现移动构造函数和移动赋值运算符，以便在对象之间高效地转移资源。

#### 4. **注意事项**

- **使用后状态**：使用 `std::move` 后，原对象的状态是未定义的。虽然它仍然可以被使用，但不应依赖于其值。
  
- **避免误用**：不要对临时对象使用 `std::move`，因为临时对象本身就是右值，使用 `std::move` 只会增加不必要的复杂性。

#### 5. **示例**

以下是一个更复杂的示例，展示了如何在自定义类中使用 `std::move`：

```cpp
#include <iostream>
#include <utility>
#include <vector>

class Resource {
public:
    Resource(size_t size) : data(new int[size]), size(size) {
        std::cout << "Resource acquired\n";
    }
    
    // 移动构造函数
    Resource(Resource&& other) noexcept : data(other.data), size(other.size) {
        other.data = nullptr; // 使原对象失去对资源的控制
        other.size = 0;
        std::cout << "Resource moved\n";
    }
    
    ~Resource() {
        delete[] data;
        std::cout << "Resource released\n";
    }

private:
    int* data;
    size_t size;
};

int main() {
    Resource res1(10); // Resource acquired
    Resource res2 = std::move(res1); // Resource moved
    return 0; // Resource released
}
```

在这个示例中，`Resource` 类实现了移动构造函数，使用 `std::move` 将资源从 `res1` 移动到 `res2`，避免了不必要的复制。

#### 总结

`std::move` 是 C++11 中一个非常重要的工具，它使得移动语义成为可能，从而提高了程序的性能。通过合理使用 `std::move`，可以在对象之间高效地转移资源，减少不必要的复制开销。
## 4. C++14
- **发布年份**：2014
- **关键特性**：
  - 增强了 lambda 表达式，支持泛型 lambda。
  - 引入了 `std::make_unique`，简化了智能指针的创建。
  - 支持二进制字面量（如 `0b1010`）。
  - 增强了 constexpr，允许在编译时进行更多的计算。

## 5. C++17
- **发布年份**：2017
- **关键特性**：
  - 引入了结构化绑定（structured bindings），简化了元组和数组的解构。
  - 支持 `std::optional`，表示可能缺失的值。
  - 引入了 `std::variant`，支持类型安全的联合体。
  - 增强了并行算法，提供了并行执行的 STL 算法。
  - 引入了文件系统库（`<filesystem>`），提供了对文件系统的操作支持。

## 6. C++20
- **发布年份**：2020
- **关键特性**：
  - 引入了概念（concepts），提供了对模板参数的约束。
  - 支持范围（ranges），提供了更强大的序列操作。
  - 引入了协程（coroutines），支持异步编程。
  - 增强了 constexpr，允许在编译时执行更多的代码。
  - 引入了 `std::format`，提供了格式化字符串的功能。

## 7. C++23（正在进行中）
- **预计发布年份**：2023（或稍后）
- **关键特性**（尚未完全确定）：
  - 计划引入更多的语言特性和库功能，例如更好的支持范围、改进的元编程功能等。
  - 可能会引入新的标准库组件，如 `std::expected` 和 `std::flat_map`。



# 二、常见面试题
