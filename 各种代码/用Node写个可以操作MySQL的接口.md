以前也用 `Node`写过接口，但不涉及数据库操作。而我们发现，自己公司的后端写接口，基本都绕不开数据库操作。感觉不写一个能操作数据库的接口，就不算真正意义上学会了写接口。那我们今天就学习一下，如何写一个可以操作数据库的接口。下面我们进入正题。

### 创建Express项目

Express 是一个简洁而灵活的Node Web应用框架， 通过对底层接口进行封装，在简化代码的同时提供更强大的接口，大幅度提升开发效率和体验，将开发者从冗长、复杂、易错的代码中解放出来。与创建Vue和React应用一样，创建Express项目也有脚手架可供使用。express-generator是Express的应用生成器，用它可以快速创建一个Express的应用骨架。

[Express 教程2：创建站点框架- 学习Web 开发| MDN](https://developer.mozilla.org/zh-CN/docs/Learn/Server-side/Express_Nodejs/skeleton_website)

[Express 应用程序生成器](https://expressjs.com/zh-cn/starter/generator.html)



### 使用Docker安装MySQL

为什么不直接安装MySQL，而要使用Docker安装MySQL呢？因为Docker能保证运行环境的一致性，不会出现开发环境，测试环境，生产环境同样的配置表现不一致的问题。其次，我看公司的生产环境也是在Docker上运行MySQL。

作者：去伪存真
链接：https://juejin.cn/post/7374293974577823778
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



作者：去伪存真
链接：https://juejin.cn/post/7374293974577823778
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
