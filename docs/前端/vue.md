# 常用命令

## yarn-常用命令

**命令官方文档：**[https://yarn.bootcss.com/docs/cli/index.html](https://yarn.bootcss.com/docs/cli/index.html)

**Yarn是一个现代的包管理器，与npm类似，用于管理JavaScript项目中的依赖项。**

**初始化新项目：**

```shell
yarn init
```

**这个命令会初始化一个新的项目，并创建一个新的**`<span class="ne-text">package.json</span>`文件。

**添加依赖包：**

```shell
yarn add [package]
yarn add [package]@[version]
yarn add [package]@[tag]
```

**使用**`<span class="ne-text">add</span>`命令将依赖项添加到项目中。你可以指定包的版本号或标签。如果不指定版本号，则默认添加最新版本。

**升级依赖包：**

```shell
yarn upgrade [package]
yarn upgrade [package]@[version]
yarn upgrade [package]@[tag]
```

**这个命令用来升级项目中的依赖项。**

**移除依赖包：**

```shell
yarn remove [package]
```

**使用**`<span class="ne-text">remove</span>`命令可以从项目中删除依赖项。

**安装项目所有依赖项：**

```shell
yarn install
```

**这条命令会根据**`<span class="ne-text">package.json</span>`文件安装所有必需的包。

**锁定依赖版本：**

```shell
yarn install --frozen-lockfile
```

**如果存在**`<span class="ne-text">yarn.lock</span>`文件，这个命令将根据该文件中的版本信息来安装依赖项，而不是根据`<span class="ne-text">package.json</span>`文件。

**添加开发依赖包：**

```shell
yarn add [package] --dev
```

**此命令将包作为开发依赖项添加到项目中。**

**安装全局包：**

```shell
yarn global add [package]
```

**使用**`<span class="ne-text">global</span>`命令来全局安装包。

**更新全局包：**

```shell
yarn global upgrade [package]
```

**用于更新全局安装的包。**

**删除全局包：**

```shell
yarn global remove [package]
```

**用于删除全局安装的包。**

**创建yarn.lock文件：**

```shell
yarn lockfile
```

**这条命令用于生成一个新的**`<span class="ne-text">yarn.lock</span>`文件。

**清除缓存：**

```shell
yarn cache clean [package]
```

**清除指定包的缓存。如果不指定包，则清除所有缓存。**

**列出已安装的依赖包：**

```shell
yarn list
```

**列出已安装在当前项目中的所有依赖包。**

**运行定义的脚本：**

```shell
yarn run [script]
```

**执行在**`<span class="ne-text">package.json</span>`内的`<span class="ne-text">scripts</span>`部分定义的脚本。

**检查依赖项版本匹配：**

```shell
yarn check
```

**检查**`<span class="ne-text">node_modules</span>`中的安装是否匹配`<span class="ne-text">package.json</span>`中的依赖项描述。

**每一次使用Yarn时，它都会生成或更新**`<span class="ne-text">yarn.lock</span>`文件，这个文件确保在不同环境下依赖项的版本一致性。这是Yarn的一个重要特性，使得团队之间的协作变得更加可靠。

**查看特定包的版本：**

**要查看某个具体包的版本，例如 **`<span class="ne-text">vue</span>`，你可以使用以下方法：

**方法 1: 查看 **`<span class="ne-text">package.json</span>`

**在你的项目的根目录下，打开** `<strong><span class="ne-text">package.json</span></strong>` **文件，并查找** `<strong><span class="ne-text">dependencies</span></strong>` **或** `<strong><span class="ne-text">devDependencies</span></strong>`** 对象。这里会列出你安装的所有包及其版本。例如：**

```json
"dependencies": {
    "vue": "^2.6.11"
}
```

**这里的 "^2.6.11" 表示安装了** `<strong><span class="ne-text">vue</span></strong>`** 的 2.6.x 版本，其中 x 不小于 11。符号 "^" 允许安装最新的次要版本更新。**

**方法 2: 使用 **`<span class="ne-text">yarn list</span>`

**在终端，进入你的项目的根目录，运行：**

```shell
yarn list vue
```

**这会显示已安装的** `<strong><span class="ne-text">vue</span></strong>` **包的版本，以及任何其他依赖于** `<strong><span class="ne-text">vue</span></strong>`** 的包。**

**方法 3: 查看 **`<span class="ne-text">node_modules</span>` 目录

**进入** `<strong><span class="ne-text">node_modules/vue</span></strong>` **目录，然后查看该目录中的** `<strong><span class="ne-text">package.json</span></strong>`** 文件。这个文件包含了该具体包的元数据，包括版本号。**

```shell
cat node_modules/vue/package.json
```

**在显示的 JSON 数据中，查找** `<strong><span class="ne-text">version</span></strong>`** 字段以获取版本号。**

**方法 4: 使用 **`<span class="ne-text">yarn info</span>`

**如果你想查看远程仓库中** `<strong><span class="ne-text">vue</span></strong>` **的最新版本或特定版本信息，你可以使用** `<strong><span class="ne-text">yarn info</span></strong>`** 命令：**

```shell
yarn info vue
```

**这将会打印** `<strong><span class="ne-text">vue</span></strong>`** 包在 npm 注册表中的信息，包括当前所有可用的版本。**

```shell
yarn info vue version
```

**这条命令直接给出** `<strong><span class="ne-text">vue</span></strong>`** 的当前最新版本。**

**方法 5: 使用 **`<span class="ne-text">npm</span>` 命令

**虽然你问的是关于** `<strong><span class="ne-text">yarn</span></strong>` **的命令，但如果你的项目同时使用** `<strong><span class="ne-text">npm</span></strong>`**，你也可以通过它来检查具体包的版本：**

```shell
npm list vue
```

**这将会显示你项目中安装的** `<strong><span class="ne-text">vue</span></strong>`** 包的版本。**

**方法 6: 使用 **`<span class="ne-text">yarn why</span>`

**这个命令可以帮助你了解为什么某个包被安装，它也显示了版本信息。**

```shell
yarn why vue
```

**选择适合你需求的方法来查找** `<strong><span class="ne-text">vue</span></strong>` **或其他任何 npm 包的版本。如果你只关心本地安装的版本，通常使用** `<strong><span class="ne-text">yarn list</span></strong>` **命令或查看** `<strong><span class="ne-text">package.json</span></strong>` **会非常便捷。如果需要更详细的信息或想知道可用的版本，则使用** `<strong><span class="ne-text">yarn info</span></strong>`**。**

## nvm-常用命令

[https://juejin.cn/post/7132680379898527757](https://juejin.cn/post/7132680379898527757)

[https://juejin.cn/post/7083026831263137800](https://juejin.cn/post/7083026831263137800)

```shell
# 安装指定node版本
nvm install v14.15.0
# 运行指定node版本
nvm use v14.15.0
# 指定默认版本
nvm alias default v16.16.0
nvm current
# 切换到最新的node版本
nvm use node
# 远程服务器上所有的可用版本
nvm ls-remote
# 给不同的版本号设置别名
nvm alias node_cms 14.15.0
# 使用该别名
nvm use node_cms
# 查看已安装node列表
nvm ls
```

# HTML/JS/CSS通用知识

**快速回顾**

## HTML

### HTML DOM

[https://www.runoob.com/htmldom/htmldom-intro.html](https://www.runoob.com/htmldom/htmldom-intro.html)

#### 简介

**HTML DOM 是：**

* **HTML 的标准对象模型**
* **HTML 的标准编程接口**
* **W3C 标准**

**HTML DOM 定义了所有 HTML 元素的***对象*和*属性***，以及访问它们的***方法***。**

*换言之，HTML DOM 是关于如何获取、修改、添加或删除 HTML 元素的标准。*

#### HTML DOM NODE

**根据 W3C 的 HTML DOM 标准，HTML 文档中的所有内容都是节点：**

* **整个文档是一个文档节点**
* **每个 HTML 元素是元素节点**
* **HTML 元素内的文本是文本节点**
* **每个 HTML 属性是属性节点**
* **注释是注释节点**

![](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1714014828222-d8cfec4b-f9b4-41c0-94f8-c9222d2020ec.png)

#### HTML DOM METHOD

**可通过 JavaScript （以及其他编程语言）对 HTML DOM 进行访问。**

**所有 HTML 元素被定义为对象，而编程接口则是对象方法和对象属性。**

**方法是您能够执行的动作（比如添加或修改元素）。**

**属性是您能够获取或设置的值（比如节点的名称或内容）。**

**常用的方法：**


| **方法**                     | **描述**                                                            |
| ---------------------------- | ------------------------------------------------------------------- |
| **getElementById()**         | **返回带有指定 ID 的元素。**                                        |
| **getElementsByTagName()**   | **返回包含带有指定标签名称的所有元素的节点列表（集合/节点数组）。** |
| **getElementsByClassName()** | **返回包含带有指定类名的所有元素的节点列表。**                      |
| **appendChild()**            | **把新的子节点添加到指定节点。**                                    |
| **removeChild()**            | **删除子节点。**                                                    |
| **replaceChild()**           | **替换子节点。**                                                    |
| **insertBefore()**           | **在指定的子节点前面插入新的子节点。**                              |
| **createAttribute()**        | **创建属性节点。**                                                  |
| **createElement()**          | **创建元素节点。**                                                  |
| **createTextNode()**         | **创建文本节点。**                                                  |
| **getAttribute()**           | **返回指定的属性值。**                                              |
| **setAttribute()**           | **把指定属性设置或修改为指定的值。**                                |

#### HTML DOM ATTRIBUTE

**获取元素内容的最简单方法是使用 innerHTML 属性。**

**innerHTML 属性对于获取或替换 HTML 元素的内容很有用。**

**nodeName 属性规定节点的名称。**

* **nodeName 是只读的**
* **元素节点的 nodeName 与标签名相同**
* **属性节点的 nodeName 与属性名相同**
* **文本节点的 nodeName 始终是 #text**
* **文档节点的 nodeName 始终是 #document**

**注意：** **nodeName 始终包含 HTML 元素的大写字母标签名。**

---

**nodeValue 属性规定节点的值。**

* **元素节点的 nodeValue 是 undefined 或 null**
* **文本节点的 nodeValue 是文本本身**
* **属性节点的 nodeValue 是属性值**

#### HTML DOM CRUD

* **访问：**[https://www.runoob.com/htmldom/htmldom-access.html](https://www.runoob.com/htmldom/htmldom-access.html)
* **修改：**

  * [https://www.runoob.com/htmldom/htmldom-modify.html](https://www.runoob.com/htmldom/htmldom-modify.html)
  * [https://www.runoob.com/htmldom/htmldom-content.html](https://www.runoob.com/htmldom/htmldom-content.html)
* **元素操作：**[https://www.runoob.com/htmldom/htmldom-elements.html](https://www.runoob.com/htmldom/htmldom-elements.html)
* **事件：**[https://www.runoob.com/htmldom/htmldom-events.html](https://www.runoob.com/htmldom/htmldom-events.html)

## CSS

### CSS选择器

**CSS选择器是CSS中的一种模式，用于选择需要向其应用样式的HTML元素。**

**1. 元素选择器（Type Selector）**

**元素选择器，又称为标签选择器或类型选择器，通过HTML元素的名称来选择特定类型的元素。例如，要为所有的段落应用样式，可以使用**`<span class="ne-text">p</span>`选择器。

```css
p {
    color: red;
}
```

**2. 类选择器（Class Selector）**

**类选择器使用点（**`<span class="ne-text">.</span>`）后跟HTML元素的类属性值来选择具有特定类的元素。一个元素可以有多个类，类选择器可以选择所有具有该类的元素。例如，`<span class="ne-text">.warning</span>`选择器会选择所有具有`<span class="ne-text">class="warning"</span>`的元素。

```css
.warning {
    font-weight: bold;
    color: orange;
}
```

**3. ID选择器（ID Selector）**

**ID选择器使用井号（**`<span class="ne-text">#</span>`）后跟HTML元素的ID属性值来选择具有特定ID的单个元素。每个ID在文档中应该是唯一的。例如，`<span class="ne-text">#unique-element</span>`选择器会选择具有`<span class="ne-text">id="unique-element"</span>`的单个元素。

```css
#unique-element {
    background-color: lightblue;
}
```

**4. 通配符选择器（Universal Selector）**

**通配符选择器使用星号（**`<span class="ne-text">*</span>`）来选择HTML中的所有元素。它可以用于设置全局的基础样式。

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

**5. 属性选择器（Attribute Selector）**

**属性选择器基于HTML元素的属性及其值来选择元素。它有几种形式，可以选择具有特定属性的元素，或者选择属性值等于、包含或以某个给定值开始的元素。**

```css
/* 选择所有具有特定属性的元素 */
[type] {
    border: 1px solid black;
}

/* 选择属性值等于特定值的元素 */
[type="button"] {
    background-color: green;
}
```

**6. 后代选择器（Descendant Combinator）**

**后代选择器使用空格来选择某元素的后代元素。例如，**`<span class="ne-text">div p</span>`选择器会选择所有`<span class="ne-text">div</span>`元素内的`<span class="ne-text">p</span>`元素。

```css
div p {
    color: blue;
}
```

**7. 子选择器（Child Combinator）**

**子选择器使用**`<span class="ne-text">></span>`来选择某元素的直接子元素。例如，`<span class="ne-text">ul > li</span>`选择器会选择所有`<span class="ne-text">ul</span>`元素的直接子`<span class="ne-text">li</span>`元素。

```css
ul > li {
    list-style-type: square;
}
```

**8. 相邻兄弟选择器（Adjacent Sibling Combinator）**

**相邻兄弟选择器使用**`<span class="ne-text">+</span>`来选择紧随其后的一个兄弟元素。例如，`<span class="ne-text">h2 + p</span>`选择器会选择所有紧接在`<span class="ne-text">h2</span>`元素后的`<span class="ne-text">p</span>`元素。

```css
h2 + p {
    font-weight: bold;
}
```

**9. 通用兄弟选择器（General Sibling Combinator）**

**通用兄弟选择器使用**`<span class="ne-text">~</span>`来选择相同父元素下的所有兄弟元素。例如，`<span class="ne-text">h2 ~ p</span>`选择器会选择所有与`<span class="ne-text">h2</span>`元素同级的`<span class="ne-text">p</span>`元素。

```css
h2 ~ p {
    border: 1px solid gray;
}
```

**10. 伪类选择器（Pseudo-class Selector）**

**伪类选择器使用冒号（**`<span class="ne-text">:</span>`）来选择处于特定状态的元素，如悬停状态（`<span class="ne-text">:hover</span>`），焦点状态（`<span class="ne-text">:focus</span>`），第一个子元素（`<span class="ne-text">:first-child</span>`）等。

```css
a:hover {
    color: green;
}

input:focus {
    border-color: red;
}
```

**11. 伪元素选择器（Pseudo-element Selector）**

**伪元素选择器（Pseudo-element Selector）允许你样式化元素的特定部分或在元素周围添加特定的内容，其本身不会创建任何HTML元素，但可以影响元素内容的显示方式。以下是一些常用的伪元素选择器：**

**::first-line**该选择器用于选择块级元素的第一行。

```css
解释1p::first-line {
  2    color: red;
  3    font-weight: bold;
  4}
```

**这会将每个 **<p>** 标签的第一行文本设置为红色并加粗。**

### 预处理指令

**在 CSS 中，元素选择器通常不会与 **`<span class="ne-text">@</span>` 符号一起使用。相反，`<span class="ne-text">@</span>` 符号在 CSS 中被用于预处理指令，这些指令被称为 `<span class="ne-text">at-rules</span>`。`<span class="ne-text">at-rules</span>` 用来传达元信息、条件信息或描述文档的样式和行为。以下是一些常见的 `<span class="ne-text">at-rules</span>`：

[@import ](/import )

**用于导入外部样式表到当前样式表中。**

```css
@import url('another-stylesheet.css');
```

[@media ](/media )

**用于定义根据媒体类型和查询应用不同样式规则的条件规则。**

```css
@media screen and (min-width: 768px) {
  /* 在屏幕尺寸大于或等于768像素时应用样式 */
}
```

[@keyframes ](/keyframes )

**用于定义动画关键帧。**

```css
@keyframes slidein {
  from {
    transform: translateX(0%);
  }
  to {
    transform: translateX(100%);
  }
}
```

[@font-face ](/font-face )

**用于定义自定义字体。**

```css
@font-face {
  font-family: "MyCustomFont";
  src: url('mycustomfont.woff2') format('woff2');
}
```

[@supports ](/supports )

**用于检查浏览器是否支持特定的 CSS 特性，并根据支持情况应用样式。**

```css
@supports (display: grid) {
  .container {
    display: grid;
  }
}
```

[@namespace ](/namespace )

**用于指定 XML 命名空间。**

```css
@namespace url(http://www.w3.org/1999/xhtml);
```

[@page ](/page )

**用于定义在打印文档时页面的样式。**

```css
@page {
  margin: 1cm;
}
```

[@charset ](/charset )

**用于指定样式表中使用的字符编码。**

```css
@charset "UTF-8";
```

**@document（非标准化并受限支持）**

**应用到指定容器或特定 URL 上的样式。**

```css
@document url(http://www.example.com/) {
  /* 在特定 URL 下应用的样式 */
}
```

**@counter-style（在较新的浏览器中支持）**

**用于定义列表项的标记样式。**

```css
@counter-style custom {
  system: cyclic;
  symbols: ★;
  suffix: " ";
}
```

**CSS 中 **`<span class="ne-text">@</span>` 符号的使用与元信息和特定行为的描述有关，而不是直接用于选择文档中的元素。这些规则可以改变整个文档的行为或是为特定情况提供样式规则。所以如果你在 CSS 中见到 `<span class="ne-text">@</span>` 符号，它几乎肯定是与上述的 `<span class="ne-text">at-rules</span>` 相关的。

# Vue

## Vue简介

**编写风格：选项式+单文件组件**

**参考资料：**[https://cn.vuejs.org/guide/introduction.html#api-styles](https://cn.vuejs.org/guide/introduction.html#api-styles)

### SFC-概念

**Vue 单文件组件 (Single-File Component，缩写为 SFC)。SFC 是一种可复用的代码组织形式，它将从属于同一个组件的 HTML、CSS 和 JavaScript 封装在使用 **.vue** 后缀的文件中。**

### 核心特点

**Vue 的两个核心功能：**

* **声明式渲染****：Vue 基于标准 HTML 拓展了一套模板语法，使得我们可以声明式地描述最终输出的 HTML 和 JavaScript 状态之间的关系。**
* **响应性****：Vue 会自动跟踪 JavaScript 状态并在其发生变化时响应式地更新 DOM。**

### 书写风格

**Vue 的组件可以按两种不同的风格书写：****选项式 API** 和**组合式 API****。**

#### 选项式 API (Options API)

**使用选项式 API，我们可以用包含多个选项的对象来描述组件的逻辑，例如 **data**、**methods** 和 **mounted**。选项所定义的属性都会暴露在函数内部的 **this** 上，它会指向当前的组件实例。**

```vue
<script>
export default {
  // data() 返回的属性将会成为响应式的状态
  // 并且暴露在 `this` 上
  data() {
    return {
      count: 0
    }
  },

  // methods 是一些用来更改状态与触发更新的函数
  // 它们可以在模板中作为事件处理器绑定
  methods: {
    increment() {
      this.count++
    }
  },

  // 生命周期钩子会在组件生命周期的各个不同阶段被调用
  // 例如这个函数就会在组件挂载完成后被调用
  mounted() {
    console.log(`The initial count is ${this.count}.`)
  }
}
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
```

#### 组合式 API (Composition API)

**通过组合式 API，我们可以使用导入的 API 函数来描述组件逻辑。在单文件组件中，组合式 API 通常会与 **[<script setup>](https://cn.vuejs.org/api/sfc-script-setup.html) 搭配使用。这个 **setup** attribute 是一个标识，告诉 Vue 需要在编译时进行一些处理，让我们可以更简洁地使用组合式 API。比如，**<script setup>** 中的导入和顶层变量/函数都能够在模板中直接使用。下面是使用了组合式 API 与 **<script setup>** 改造后和上面的模板完全一样的组件：

## 快速入门

### 声明式渲染

[https://cn.vuejs.org/tutorial/#step-2](https://cn.vuejs.org/tutorial/#step-2)

**Vue 的核心功能是****声明式渲染****：通过扩展于标准 HTML 的模板语法，我们可以根据 JavaScript 的状态来描述 HTML 应该是什么样子的。当状态改变时，HTML 会自动更新。能在改变时触发更新的状态被认为是****响应式**的。在 Vue 中，响应式状态被保存在组件中。

```vue
<script>
  export default {
    data() {
      return {
        message: 'Hello World!',
        counter: {
          count: 0
        }
      }
    }
  }
</script>

<template>
  <h1>{{ message }}</h1>
  <p>Count is: {{ counter.count }}</p>
</template>
```

### Attribute 绑定

[https://cn.vuejs.org/tutorial/#step-3](https://cn.vuejs.org/tutorial/#step-3)

**在 Vue 中，mustache 语法 (即双大括号) 只能用于文本插值。为了给 attribute 绑定一个动态值，需要使用 **v-bind** 指令：**

```vue
<div v-bind:id="dynamicId"></div>
```

**指令**是由** **v-** **开头的一种特殊 attribute。它们是 Vue 模板语法的一部分。和文本插值类似，指令的值是可以访问组件状态的 JavaScript 表达式。关于** **v-bind** **和指令语法的完整细节请详阅[指南 - 模板语法](https://cn.vuejs.org/guide/essentials/template-syntax.html)。

**冒号后面的部分 (**:id**) 是指令的“参数”。此处，元素的 **id** attribute 将与组件状态里的 **dynamicId** 属性保持同步。由于 **v-bind** 使用地非常频繁，它有一个专门的简写语法：**

```plain
<div :id="dynamicId"></div>
```

### 事件监听

[https://cn.vuejs.org/tutorial/#step-4](https://cn.vuejs.org/tutorial/#step-4)

**我们可以使用 **v-on** 指令监听 DOM 事件：**

```vue
<button v-on:click="increment">{{ count }}</button>
```

**因为其经常使用，**v-on** 也有一个简写语法：**

```vue
<button @click="increment">{{ count }}</button>
```

**此处，**increment** 引用了一个使用 **methods** 选项声明的函数**

```vue
export default {
  data() {
    return {
      count: 0
    }
  },
  methods: {
    increment() {
      // 更新组件状态
      this.count++
    }
  }
}
```

**在方法中，我们可以使用 **this** 来访问组件实例。组件实例会暴露 **data** 中声明的数据属性。我们可以通过改变这些属性的值来更新组件状态。事件处理函数也可以使用内置表达式，并且可以使用修饰符简化常见任务。这些细节包含在**[指南 - 事件处理](https://cn.vuejs.org/guide/essentials/event-handling.html)。

### 表单绑定

[https://cn.vuejs.org/tutorial/#step-5](https://cn.vuejs.org/tutorial/#step-5)

**我们可以同时使用 **v-bind** 和 **v-on** 来在表单的输入元素上创建双向绑定：**

```vue
<input :value="text" @input="onInput">
```

```vue
methods: {
  onInput(e) {
    // v-on 处理函数会接收原生 DOM 事件
    // 作为其参数。
    this.text = e.target.value
  }
}
```

**试着在文本框里输入——你会看到** **<p>** **里的文本也随着你的输入更新了。**

**为了简化双向绑定，Vue 提供了一个 **v-model** 指令，它实际上是上述操作的语法糖：**

```vue
<input v-model="text">
```

**v-model** **会将被绑定的值与** **<input>** **的值自动同步，这样我们就不必再使用事件处理函数了。**

**v-model** 不仅支持文本输入框，也支持诸如多选框、单选框、下拉框之类的输入类型。我们在[指南 - 表单绑定](https://cn.vuejs.org/guide/essentials/forms.html)中讨论了更多的细节。

### 条件渲染

[https://cn.vuejs.org/tutorial/#step-6](https://cn.vuejs.org/tutorial/#step-6)

**我们可以使用 **v-if** 指令来有条件地渲染元素：**

```vue
<h1 v-if="awesome">Vue is awesome!</h1>
```

**这个 **<h1>** 标签只会在 **awesome** 的值为**[真值 (Truthy)](https://developer.mozilla.org/zh-CN/docs/Glossary/Truthy) 时渲染。若 **awesome** 更改为[假值 (Falsy)](https://developer.mozilla.org/zh-CN/docs/Glossary/Falsy)，它将被从 DOM 中移除。我们也可以使用 **v-else** 和 **v-else-if** 来表示其他的条件分支：

```vue
<h1 v-if="awesome">Vue is awesome!</h1>
  <h1 v-else>Oh no 😢</h1>
```

**现在，示例程序同时展示了两个 **<h1>** 标签，并且按钮不执行任何操作。尝试给它们添加 **v-if** 和 **v-else** 指令，并实现 **toggle()** 方法，让我们可以使用按钮在它们之间切换。更多细节请查阅 **v-if**：**[指南 - 条件渲染](https://cn.vuejs.org/guide/essentials/conditional.html)

### 列表渲染

[https://cn.vuejs.org/tutorial/#step-7](https://cn.vuejs.org/tutorial/#step-7)

**我们可以使用 **v-for** 指令来渲染一个基于源数组的列表：**

```vue
<ul>
  <li v-for="todo in todos" :key="todo.id">
                                             {{ todo.text }}
  </li>
    </ul>
```

**这里的** **todo** **是一个局部变量，表示当前正在迭代的数组元素。它只能在** **v-for** **所绑定的元素上或是其内部访问，就像函数的作用域一样。**

**注意，我们还给每个 todo 对象设置了唯一的** **id**，并且将它作为[特殊的keyattribute](https://cn.vuejs.org/api/built-in-special-attributes.html#key) **绑定到每个** **<li>**。**key** **使得 Vue 能够精确的移动每个** **<li>**，以匹配对应的对象在数组中的位置。

**更新列表有两种方式：**

1. **在源数组上调用**[变更方法](https://stackoverflow.com/questions/9009879/which-javascript-array-functions-are-mutating)：

```vue
this.todos.push(newTodo)
```

2. **使用新的数组替代原数组：**

```vue
this.todos = this.todos.filter(/* ... */)
```

**这里有一个简单的 todo 列表——试着实现一下 **addTodo()** 和 **removeTodo()** 这两个方法的逻辑，使列表能够正常工作！关于 **v-for** 的更多细节：**[指南 - 列表渲染](https://cn.vuejs.org/guide/essentials/list.html)

### 计算属性

[https://cn.vuejs.org/tutorial/#step-8](https://cn.vuejs.org/tutorial/#step-8)

**让我们在上一步的 todo 列表基础上继续。现在，我们已经给每一个 todo 添加了切换功能。这是通过给每一个 todo 对象添加 **done** 属性来实现的，并且使用了 **v-model** 将其绑定到复选框上：**

```vue
<li v-for="todo in todos">
  <input type="checkbox" v-model="todo.done">
  ...
</li>
```

**下一个可以添加的改进是隐藏已经完成的 todo。我们已经有了一个能够切换** **hideCompleted** **状态的按钮。但是应该如何基于状态渲染不同的列表项呢？**

**介绍一个新概念：**[计算属性](https://cn.vuejs.org/guide/essentials/computed.html)。我们可以使用 **computed** 选项声明一个响应式的属性，它的值由其他属性计算而来：

```vue
export default {
  // ...
  computed: {
    filteredTodos() {
      // 根据 `this.hideCompleted` 返回过滤后的 todo 项目
    }
  }
}
```

```vue
- <li v-for="todo in todos">
+ <li v-for="todo in filteredTodos">
```

**计算属性会自动跟踪其计算中所使用的到的其他响应式状态，并将它们收集为自己的依赖。计算结果会被缓存，并只有在其依赖发生改变时才会被自动更新。现在，试着添加 **filteredTodos** 计算属性并实现计算逻辑！如果实现正确，在隐藏已完成项目的状态下勾选一个 todo，它也应当被立即隐藏。**

### 生命周期和模板引用

[https://cn.vuejs.org/tutorial/#step-9](https://cn.vuejs.org/tutorial/#step-9)

**目前为止，Vue 为我们处理了所有的 DOM 更新，这要归功于响应性和声明式渲染。然而，有时我们也会不可避免地需要手动操作 DOM。**

**这时我们需要使用****模板引用****——也就是指向模板中一个 DOM 元素的 ref。我们需要通过**[这个特殊的refattribute](https://cn.vuejs.org/api/built-in-special-attributes.html#ref) 来实现模板引用：

```vue
<p ref="pElementRef">hello</p>
```

**此元素将作为** **this.\$refs.pElementRef** **暴露在** **this.\$refs** **上。然而，你只能在组件****挂载**之后访问它。

**要在挂载之后执行代码，我们可以使用 **mounted** 选项：**

**这被称为****生命周期钩子****——它允许我们注册一个在组件的特定生命周期调用的回调函数。还有一些其他的钩子如** **created** **和** **updated**。更多细节请查阅[生命周期图示](https://cn.vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram)。

**现在，尝试添加一个** **mounted** **钩子，然后通过** **this.\$refs.pElementRef** **访问** **<p>**，并直接对其执行一些 DOM 操作。(例如修改它的** **textContent**)。**

```vue
export default {
  mounted() {
    // 此时组件已经挂载。
  }
}
```

### 侦听器

[https://cn.vuejs.org/tutorial/#step-10](https://cn.vuejs.org/tutorial/#step-10)

**有时我们需要响应性地执行一些“副作用”——例如，当一个数字改变时将其输出到控制台。我们可以通过侦听器来实现它：**

```vue
export default {
  data() {
    return {
      count: 0
    }
  },
  watch: {
    count(newCount) {
      // 没错，console.log() 是一个副作用
      console.log(`new count is: ${newCount}`)
    }
  }
}
```

**这里，我们使用 **watch** 选项来侦听 **count** 属性的变化。当 **count** 改变时，侦听回调将被调用，并且接收新值作为参数。更多详情请参阅**[指南 - 侦听器](https://cn.vuejs.org/guide/essentials/watchers.html)。

**一个比在控制台输出更加实际的例子是当 ID 改变时抓取新的数据。在右边的例子中就是这样一个组件。该组件被挂载时，会从模拟 API 中抓取 todo 数据，同时还有一个按钮可以改变要抓取的 todo 的 ID。现在，尝试实现一个侦听器，使得组件能够在按钮被点击时抓取新的 todo 项目。**

### 组件

[https://cn.vuejs.org/tutorial/#step-11](https://cn.vuejs.org/tutorial/#step-11)

**目前为止，我们只使用了单个组件。真正的 Vue 应用往往是由嵌套组件创建的。**

**父组件可以在模板中渲染另一个组件作为子组件。要使用子组件，我们需要先导入它：**

```vue
解释import ChildComp from './ChildComp.vue'

  export default {
  components: {
  ChildComp
  }
  }
```

**我们还需要使用** **components** **选项注册组件。这里我们使用对象属性的简写形式在** **ChildComp** **键下注册** **ChildComp** **组件。**

**然后我们就可以在模板中使用组件，就像这样：**

```vue
<ChildComp />
```

**现在自己尝试一下——导入子组件并在模板中渲染它。**

### Props

[https://cn.vuejs.org/tutorial/#step-12](https://cn.vuejs.org/tutorial/#step-12)

**子组件可以通过 ****props** 从父组件接受动态数据。首先，需要声明它所接受的 props：

```vue
解释// 在子组件中
  export default {
    props: {
      msg: String
    }
  }
```

**一旦声明，**msg** **prop 就会暴露在** **this** **上，并可以在子组件的模板中使用。

**父组件可以像声明 HTML attributes 一样传递 props。若要传递动态值，也可以使用 **v-bind** 语法：**

```vue
<ChildComp :msg="greeting" />
```

**现在在编辑器中自己尝试一下吧。**

### Emits

[https://cn.vuejs.org/tutorial/#step-13](https://cn.vuejs.org/tutorial/#step-13)

**除了接收 props，子组件还可以向父组件触发事件：**

```vue
解释export default {
  // 声明触发的事件
  emits: ['response'],
    created() {
    // 带参数触发
    this.$emit('response', 'hello from child')
  }
}
```

**this.\$emit()** **的第一个参数是事件的名称。其他所有参数都将传递给事件监听器。**

**父组件可以使用 **v-on** 监听子组件触发的事件——这里的处理函数接收了子组件触发事件时的额外参数并将它赋值给了本地状态：**

```vue
<ChildComp @response="(msg) => childMsg = msg" />
```

**现在在编辑器中自己尝试一下吧。**

### 插槽

[https://cn.vuejs.org/tutorial/#step-14](https://cn.vuejs.org/tutorial/#step-14)

**除了通过 props 传递数据外，父组件还可以通过****插槽** (slots) 将模板片段传递给子组件：

```vue
<ChildComp>
     This is some slot content!
</ChildComp>
```

**在子组件中，可以使用 **<slot>** 元素作为插槽出口 (slot outlet) 渲染父组件中的插槽内容 (slot content)：**

```vue
<!-- 在子组件的模板中 -->
<slot/>
```

**<slot>** 插口中的内容将被当作“默认”内容：它会在父组件没有传递任何插槽内容时显示：

```vue
<slot>Fallback content</slot>
```

**现在我们没有给 **<ChildComp>** 传递任何插槽内容，所以你将看到默认内容。让我们利用父组件的 **msg** 状态为子组件提供一些插槽内容吧。**

## 进阶

### 生命周期

[https://cn.vuejs.org/guide/essentials/lifecycle.html](https://cn.vuejs.org/guide/essentials/lifecycle.html)

![](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1714014094503-93113e98-4c67-4a40-bc1c-217473d5f8d9.png)

### 路由

[https://cn.vuejs.org/guide/scaling-up/routing.html](https://cn.vuejs.org/guide/scaling-up/routing.html)

* **从头开始实现一个简单的路由**
  * **如果你只需要一个简单的页面路由，而不想为此引入一整个路由库，你可以通过**[动态组件](https://cn.vuejs.org/guide/essentials/component-basics.html#dynamic-components)的方式，监听浏览器 [hashchange事件](https://developer.mozilla.org/en-US/docs/Web/API/Window/hashchange_event)或使用 [History API](https://developer.mozilla.org/en-US/docs/Web/API/History) 来更新当前组件。下面是一个简单的例子：

```vue
<script>
  import Home from './Home.vue'
  import About from './About.vue'
  import NotFound from './NotFound.vue'
  const routes = {
    '/': Home,
    '/about': About
  }
  export default {
    data() {
      return {
        currentPath: window.location.hash
      }
    },
    computed: {
      currentView() {
        return routes[this.currentPath.slice(1) || '/'] || NotFound
      }
    },
    mounted() {
      window.addEventListener('hashchange', () => {
        this.currentPath = window.location.hash
      })
    }
  }
</script>
<template>
  <a href="#/">Home</a> |
  <a href="#/about">About</a> |
  <a href="#/non-existent-path">Broken Link</a>
  <component :is="currentView" />
</template>
```

---

### VUEX
