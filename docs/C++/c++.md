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
