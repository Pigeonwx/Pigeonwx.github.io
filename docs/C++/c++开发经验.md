# 易错经验
## 1. 不要把 if 条件语句的初始化部分当做条件判断
> 容易误解的地方: 容易将 init 语句当做初始化+条件判断来使用
- C++17 新特性：if 语句初始化 -- if (init; condition)
- C++17 前 if 语句需要这样写代码
```
int a = GetValue();
if (a < 101) {
    cout << a;
}
```

C++17之后可以这样写：
```
// if (init; condition)

if (int a = GetValue()); a < 101) {
    cout << a;
}
```

使用这种方式可以尽可能约束作用域，让代码更简洁

- DON'T DO：
```
// 此写法中，auto self = weak_self.lock() 仅为初始化语句，不具备条件判断能力
// 之后若直接使用 self，可能出现空指针问题
if (auto self = weak_self.lock(); self->IsValid()) {
  ...
}
 ```

- DO：
```
if (auto self = weak_self.lock(); self && self->IsValid()) {
  ...
}
 ```

## 2.不要在 if 条件语句中初始化变量的同时使用 &&

- DON'T DO：
```
// 此写法中，&& 的优先级要高于 =，params 最终是一个 bool 变量
// 传递给 DoSomething 函数的是一个 bool 的 Variant，导致异常
if (auto params = Variant(variant) && is_valid) {
  DoSomething(params);
  ...
}
```

- DO：
```
if (auto params = weak_params.lock(); params && is_valid) {
  DoSomething(params);
  ...
}
```