

# webpack中 loader 与 plugin 有什么区别

在 Webpack 中，`loader` 和 `plugin` 是两种不同的扩展机制，它们的作用和使用场景也有所不同。

### Loader

`Loader` 用于转换模块的源代码。它们在模块被引入时应用，可以对文件进行预处理，比如将 TypeScript 转换为 JavaScript，或者将 SCSS 转换为 CSS。Loader 是函数，接收源文件内容作为参数，返回转换后的内容。

```js
module: {
  rules: [
    {
      test: /\.tsx?$/,
      use: 'ts-loader',
      exclude: /node_modules/,
    },
  ],
},

```


### Plugin

`Plugin` 用于执行更广泛的任务，通常涉及到打包的各个阶段。它们可以用于优化打包结果、管理资源、注入环境变量等。Plugin 提供了更强大的 API，可以访问 Webpack 的编译过程。

```js
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
    }),
  ],
};

```


### 总结

* **Loader** ：用于转换文件内容，处理单个文件。
* **Plugin** ：用于执行更复杂的任务，处理整个打包过程。


# 我们写代码的时候是 es6，浏览器运行的时候是 es5，在做代码转化的时候，webpack 做了什么？

在代码转化过程中，Webpack 主要做了以下几件事情：

1. **模块打包** ：Webpack 会将你的代码和依赖打包成一个或多个文件（bundle），以便浏览器能够加载和执行。
2. **代码转换** ：通过使用 Babel 等工具，Webpack 可以将 ES6+ 代码转换成 ES5 代码，以确保在不支持 ES6 的浏览器中也能运行。具体步骤包括：

* **解析代码** ：Babel 解析你的 ES6+ 代码，生成抽象语法树（AST）。
* **转换代码** ：Babel 根据预设（presets）和插件（plugins）将 AST 转换成 ES5 代码。
* **生成代码** ：Babel 将转换后的 AST 重新生成代码。

1. **加载器（Loaders）** ：Webpack 使用加载器来处理不同类型的文件。例如，`babel-loader` 可以处理 JavaScript 文件并使用 Babel 转换代码。
2. **插件（Plugins）** ：Webpack 插件可以扩展 Webpack 的功能，例如压缩代码、优化性能等。常见的插件包括 `UglifyJSPlugin`、`HtmlWebpackPlugin` 等。
3. **代码拆分** ：Webpack 可以将代码拆分成多个 chunk，以实现按需加载和优化性能。

一个简单的 Webpack 配置示例如下：

```js
const path = require('path');

module.exports = {
  entry: './src/index.js', // 入口文件
  output: {
    filename: 'bundle.js', // 输出文件名
    path: path.resolve(__dirname, 'dist') // 输出路径
  },
  module: {
    rules: [
      {
        test: /\.js$/, // 匹配所有 .js 文件
        exclude: /node_modules/, // 排除 node_modules 目录
        use: {
          loader: 'babel-loader', // 使用 babel-loader
          options: {
            presets: ['@babel/preset-env'] // 使用 @babel/preset-env 预设
          }
        }
      }
    ]
  }
};

```

通过上述配置，Webpack 会将 `src/index.js` 及其依赖打包成 `dist/bundle.js`，并使用 Babel 将 ES6+ 代码转换成 ES5。
