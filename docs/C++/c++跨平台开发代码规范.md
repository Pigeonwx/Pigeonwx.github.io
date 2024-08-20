
工程简介
 

该工程是会议项目的跨平台层，包括音视频引擎(xCast)、基础库(base)、会议封装层(wmp)等。

 

开发设计思想
 

以简洁、轻量、稳定为核心目标，开发过程中尽量避免使用"锁"，减少工程维护成本。

 

开发命名规范
 

本工程开发将严格遵守 Google 开源项目规范，下面简单描述部分规范。

 

1. 文件命名
 

文件名要全部小写, 单词之间通过下划线 (_) 来区分，如 tcp_sender.h、tcp_sender.cc等

 

2. 命名空间
 

命名空间以小写字母命名，最高级命名空间的名字取决于项目名称. 要注意避免嵌套命名空间的名字之间和常见的顶级命名空间的名字之间发生冲突，如


 wmp::base::net
 

3. 类型命名
 

类型名称的每个单词首字母均大写, 不包含下划线: MyExcitingClass, MyExcitingEnum

 

4. 变量命名
 

变量 (包括函数参数) 和数据成员名一律小写, 单词之间用下划线连接. 类的成员变量以下划线结尾, 但结构体的就不用, 如:
a_local_variable, a_struct_data_member, a_class_data_member_

 

注:管是静态的还是非静态的, 结构体数据成员都可以和普通变量一样, 不用像类那样接下划线
 

5. 常量命名及枚举类型
 

声明为 constexpr 或 const 的变量, 或在程序运行期间其值始终保持不变的, 命名时以 “k” 开头, 大小写混合. 例如: const int kDaysInAWeek = 7

 

6. 注释
 

所有注释统一使用 // 来进行注释，包括单行和多行场景

 

7. 代码换行
 

只使用空格, 每次缩进 2 个空格

 

8. 结构体 vs 类
 

仅当只有数据成员时使用 struct, 其它一概使用 class

 

9. 参数顺序
 

函数的参数顺序为: 输入参数在先, 后跟输出参数

 

10. 引用传参
 

所有按引用传递的参数必须加上 const

 

11. 对外参数封装
 

所有对外接口的参数一概使用基础类型及组合(如int、char等)，禁止使用其他标准库(包括std)，比如字符串使用 char*，不要使用 std::string，防止让业务方增加依赖

 

12. 对外函数回调
 

所有对外函数回调接口使用 Delegate 结尾，单一回调使用 Set，多回调使用 Add 和 Remove，如SetAuthDelegate、AddCreateMeetingDelegate 、RemoveCreateMeetingDelegate

 

13. 智能指针
 

智能指针使用 base 目录下的同名类型替换 std 中的 unique_ptr、shared_ptr，如使用 base::unique_ptr 替换 std::unique_ptr

 

注:C++11不支持make_unique，base 同时支持 base::make_unique和 base::make_shared.
 

14. XML 节点命名规范
 

节点命名遵守 XML 命名规范， 使用 "_" 来区分名字，如 <user_id> 等

 

15. 结构体规范
 

结构体使用 typedef 声明，格式为 typedef tagXXX { ... } XXX，在结构体内成员变量在前面，构造方法在后面，构造方法使用函数体内初始化方式。例如：


typedef struct tagUserInfo {

  int app_id;

  int app_uid;

  tagUserInfo() {

    app_id = 12345678;

app_uid = 87654321;

  }

} UserInfo;
 

16. 函数参数规范
 

函数方法中，*和&等操作符统一为紧靠参数类型，例如：


void foo(const char* data)
而非


void foo(const char *data) 
 

17. IF_ELSE条件语句规范
 

不管是否存在表达式，if和else里面都使用大括号来包含内容，例如


if (Condition()) {

return XXX1;

}

else {

return XXX2;

} 
或者


if (Condition()) {

return XXX1;

}

return XXX2;
而非


if (Condition()) return XXX;   
 

18. enum枚举声明规范
 


// C++11

enum class EnumType : int {

 kOne = 1,

 kTwo = 2

};


int type(1);

EnumType enum_type(static_cast<EnumType>(type));

// 有作用域

if (EnumType::kOne == enum_type) {

 // ..

}
19. include <> or include ""
 

规则：相同模块下使用""，跨模块调用使用<>，包括系统库

 

Example 1: 比如WMP层代码使用BASE层代码，则使用

 


#include <base/include/base_header.h>

#include <base/include/network_util.h>

#include "wmp/xmpp/xmpp_signal_client.h"
 

Example 2: 比如BASE层代码内部，则使用

 


#include "base_header.h"
