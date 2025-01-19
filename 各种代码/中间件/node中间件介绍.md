[Express.js中的中间件详解](https://juejin.cn/post/7387353297693671434)

## Express.js 中的中间件（Middleware）

> @[如何使用中间件](https://expressjs.com/en/guide/using-middleware.html#using-middleware) Express is a routing and middleware web framework that has minimal functionality of its own: An Express application is essentially a series of middleware function calls.
>
> Middleware functions are functions that have access to the request object (req), the response object (res), and the next middleware function in the application’s request-response cycle. The next middleware function is commonly denoted by a variable named next.

Express 是一个用于路由和中间件的 Web 框架，它本身的功能非常简洁：一个 Express 应用程序基本上就是一系列中间件函数的调用。

中间件函数是那些在应用程序的请求-响应周期中可以访问请求对象（req）、响应对象（res）以及下一个中间件函数的函数。下一个中间件函数通常由一个名为 next 的变量表示。中间件可以执行以下任务：

1. 执行任何代码。
2. 修改请求和响应对象。
3. 结束请求-响应周期。
4. 调用堆栈中的下一个中间件函数。

如果当前中间件没有结束请求-响应周期，则必须调用** **`next()` 方法，将控制传递给下一个中间件函数。否则，请求将挂起。

## 中间件的类型

1. **应用级中间件** ：绑定在** **`app` 对象上的中间件。
2. **路由级中间件** ：绑定在** **`express.Router()` 实例上的中间件。
3. **错误处理中间件** ：带有四个参数（`err`、`req`、`res`、`next`）的中间件函数。
4. **内置中间件** ：Express 自带的一些功能中间件，如** **`express.static`。
5. **第三方中间件** ：通过** **`npm` 安装的第三方中间件。

## 使用中间件

#### 应用级中间件

应用级中间件绑定在** **`app` 对象上，使用** **`app.use()` 和** **`app.METHOD()`方法（其中 METHOD 是 HTTP 请求方法）。

```javascript
const express = require('express');
const app = express();

// 应用级中间件
app.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

#### 路由级中间件

路由级中间件与应用级中间件类似，但它绑定在** **`express.Router()`实例上。

```javascript
const express = require('express');
const app = express();
const router = express.Router();

// 路由级中间件
router.use((req, res, next) => {
  console.log('Request URL:', req.originalUrl);
  next();
});

router.get('/', (req, res) => {
  res.send('Hello from Router!');
});

app.use('/router', router);

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

#### 错误处理中间件

错误处理中间件必须有四个参数，并且在其他中间件之后定义。

```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  throw new Error('Something went wrong!');
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

#### 内置中间件

从版本 4.x 开始，Express 不再依赖于** **[Connect](https://github.com/senchalabs/connect)。中间件 以前包含在 Express 中的函数现在位于单独的模块中;[请参阅中间件函数列表](https://github.com/senchalabs/connect#middleware)。

Express 内置了以下中间件功能：

* [express.static](https://expressjs.com/en/4x/api.html#express.static) 提供静态资产，例如 HTML 文件、图像等。
* [express.json](https://expressjs.com/en/4x/api.html#express.json) 使用 JSON 有效负载分析传入请求。**注意：适用于 Express 4.16.0+**
* [express.urlencoded](https://expressjs.com/en/4x/api.html#express.urlencoded) 使用 URL 编码的有效负载解析传入请求。**注意：适用于 Express 4.16.0+**

> 这段原文直接搬过来的

```javascript
const express = require('express');
const app = express();

// 内置中间件
app.use(express.static('public'));

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

#### 第三方中间件

通过** **`npm` 安装的中间件，如** **`body-parser`。

```javascript
const express = require('express');
const app = express();
const bodyParser = require('body-parser');

// 第三方中间件
app.use(bodyParser.json());

app.post('/', (req, res) => {
  res.send(req.body);
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

## 中间件的执行顺序

中间件的执行顺序很重要，按照它们在代码中声明的顺序依次执行。如果某个中间件没有调用** **`next()`，则请求-响应周期在此中断。

```javascript
const express = require('express');
const app = express();

app.use((req, res, next) => {
  console.log('First middleware');
  next();
});

app.use((req, res, next) => {
  console.log('Second middleware');
  res.send('Hello World!');
});

app.use((req, res, next) => {
  console.log('This will not be logged');
  next();
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

在上述示例中，第三个中间件不会被执行，因为第二个中间件已经结束了请求-响应周期。

### 1. body-parser

 **用途** ：解析请求体，特别是 JSON 和 URL 编码的数据。

 **安装** ：

```bash
npm install body-parser
```

 **使用** ：

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// 使用 body-parser 中间件
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/', (req, res) => {
  res.send(req.body);
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

1. **全局使用** ：在应用的顶层中间件中添加解析器会解析所有传入请求的请求体数据，适用于大多数情况。
2. **特定路由使用** ：可以在需要的路由中添加解析器，以避免不必要的解析，从而提高性能。
3. **解析类型** ：确保根据实际需求选择解析器的类型（如 JSON 或 URL 编码），并配置** **`extended` 选项来处理复杂对象。

> 从 Express 4.16.0 开始，`express.json` 和** **`express.urlencoded` 内置在 Express 中，因此不再需要单独安装和使用** **`body-parser`。这些内置中间件提供了与** **`body-parser` 相同的功能，可以直接使用。

### 2. cors

 **用途** ：启用跨域资源共享（CORS），允许来自不同域的请求。

 **安装** ：

```bash
npm install cors
```

 **使用** ：

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

// 使用 cors 中间件
app.use(cors());

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

1. **全局启用** ：默认情况下启用所有跨域请求，适用于开放 API。
2. **特定路由启用** ：可以在特定路由上启用 CORS，以控制跨域请求的范围。
3. **自定义配置** ：根据安全需求设置允许的来源、方法、头部等，避免安全漏洞。

### 3. express-session

 **用途** ：提供会话管理功能，支持会话数据的持久化存储。

 **安装** ：

```bash
npm install express-session
```

 **使用** ：

```javascript
const express = require('express');
const session = require('express-session');
const app = express();

// 使用 express-session 中间件
app.use(session({
  secret: 'your secret key',
  resave: false,
  saveUninitialized: true
}));

app.get('/', (req, res) => {
  if (req.session.views) {
    req.session.views++;
    res.send(`浏览次数：${req.session.views}`);
  } else {
    req.session.views = 1;
    res.send('欢迎访问会话演示。刷新页面！');
  }
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

1. **默认存储** ：使用内存存储会话数据，适用于开发环境，但不推荐在生产环境中使用。
2. **持久化存储** ：在生产环境中使用** **`Redis`、MongoDB、PostgreSQL等持久化存储会话数据，以确保数据的持久性和一致性。
3. **配置安全性** ：确保配置会话的过期时间、cookie 设置等，以增强安全性。

### 4. helmet

 **用途** ：帮助增强 Express 应用的安全性，通过设置各种 HTTP 头。

 **安装** ：

```bash
npm install helmet
```

 **使用** ：

```javascript
const express = require('express');
const helmet = require('helmet');
const app = express();

// 使用 helmet 中间件
app.use(helmet());

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

1. **默认配置** ：启用所有默认的安全策略，可以满足大多数安全需求。
2. **自定义配置** ：根据应用需求启用或禁用特定的安全策略，如** **`helmet.noCache()`，以避免缓存敏感信息。
3. **单独使用策略** ：在需要的地方单独使用某些特定的安全策略，以满足特定的安全需求。

### 5. cookie-parser

 **用途** ：解析请求中的 Cookie，方便后续处理。

 **安装** ：

```bash
npm install cookie-parser
```

 **使用** ：

```javascript
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

// 使用 cookie-parser 中间件
app.use(cookieParser());

app.get('/', (req, res) => {
  res.send(req.cookies);
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

1. **全局使用** ：在应用的顶层中间件中添加解析器会解析所有传入请求的 Cookie 数据，适用于大多数情况。
2. **特定路由使用** ：可以在需要的路由中添加解析器，以避免不必要的解析，从而提高性能。

### 6. express-fileupload

 **用途** ：处理文件上传的中间件，基于** **[Busboy](https://www.npmjs.com/package/busboy) 实现。

 **安装** ：

```bash
npm install express-fileupload
```

 **使用** ：

```javascript
const express = require('express');
const fileUpload = require('express-fileupload');
const app = express();

app.use(fileUpload());

app.post('/upload', (req, res) => {
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('没有上传文件。');
  }

  let sampleFile = req.files.sampleFile;

  sampleFile.mv('/somewhere/on/your/server/filename.jpg', (err) => {
    if (err) return res.status(500).send(err);

    res.send('文件上传成功！');
  });
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

1. **文件大小限制** ：设置文件大小限制和文件名规则，以避免潜在的安全风险和服务器负担。

### 7. express-handlebars

 **用途** ：Express 的 Handlebars 视图引擎，支持布局、部分视图等。

 **安装** ：

```bash
npm install express-handlebars
```

 **使用** ：

```javascript
const express = require('express');
const exphbs = require('express-handlebars');
const app = express();

app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');

app.get('/', (req, res) => {
  res.render('home', { title: '首页' });
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

### 8. express-validator

 **用途** ：Express 中的请求数据验证中间件，基于 validator 模块。

 **安装** ：

```bash
npm install express-validator
```

 **使用** ：

```javascript
const express = require('express');
const { body, validationResult } = require('express-validator');
const app = express();

app.use(express.json());

app.post('/user', [
  body('username').isLength({ min: 5 }),
  body('email').isEmail()
], (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  res.send('用户验证通过');
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

1. **字段验证** ：确保在适当的路由中对请求中的特定字段进行验证。
2. **自定义验证** ：使用自定义的验证逻辑来满足复杂的验证需求。
3. **错误处理** ：处理验证错误并返回相应的响应，确保用户得到明确的错误信息。

### 9. express-rate-limit

 **用途** ：用于限制重复请求速率的中间件（默认 IP 地址），防止滥用和攻击。

 **安装** ：

```bash
npm install express-rate-limit
```

 **使用** ：

```javascript
const express = require('express');
const rateLimit = require('express-rate-limit');
const app = express();

// 基于 IP 的限流
const ipLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // Limit each IP to 100 requests per windowMs
});
app.use(ipLimiter);

// 基于 API Key 的限流
const apiKeyLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each key to 100 requests per windowMs
  keyGenerator: (req, res) => req.headers['x-api-key'] || req.ip // Use 'x-api-key' header or fallback to IP
});
app.use('/api/', apiKeyLimiter); // 应用在 /api 路由上

// 假设有个身份验证中间件会设置 req.user
app.use((req, res, next) => {
  // 这里需要实际的身份验证逻辑
  req.user = { id: 'user123' }; // 示例用户
  next();
});

// 基于用户 ID 的限流
const userLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each user to 100 requests per windowMs
  keyGenerator: (req, res) => req.user.id // Use user ID
});
app.use('/user/', userLimiter); // 应用在 /user 路由上

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});

```

 **注意** ：

1. **全局限制** ：设置全局的请求速率限制，以防止滥用和攻击。
2. **特定路由限制** ：在特定路由上设置请求速率限制，以确保关键路由的安全性。
3. **自定义配置** ：可以根据应用需求设置请求速率限制的窗口期、请求上限等。
4. **限流策略的顺序** ：确保限流中间件在所有路由之前应用。
5. **限流策略的应用范围** ：根据不同的路由或条件应用不同的限流策略。

### 10. multer

 **用途** ：处理** **`multipart/form-data` 类型的表单数据，通常用于文件上传。

 **安装** ：

```bash
npm install multer
```

 **使用** ：

```javascript
const express = require('express');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const app = express();

app.post('/upload', upload.single('file'), (req, res) => {
  res.send('文件上传成功！');
});

app.listen(3000, () => {
  console.log('服务器运行在端口 3000');
});
```

 **注意** ：

虽然** **`express-fileupload` 和** **`multer` 不会直接冲突，但在同一个项目中使用它们可能会带来以下问题：

1. **冗余** ：两者都能处理文件上传，使用两个中间件会造成代码冗余。
2. **配置混淆** ：不同中间件的配置和用法不同，可能导致开发过程中出现混淆。
3. **性能影响** ：两个中间件都在处理文件上传，可能会影响性能和资源使用。

**建议**

* **简单需求** ：如果你的项目只需要处理简单的文件上传，可以选择** **`express-fileupload`。
* **复杂需求** ：如果需要处理复杂的文件上传需求，如多文件、文件类型验证、大文件上传等，建议使用** **`multer`。

### 11. express-jwt

 **用途** ：`express-jwt` 是一个 Express 中间件，用于自动验证 JSON Web Token (JWT)。

 **安装** ：

```bash
npm install express-jwt
```

 **使用** ：

```javascript
const express = require('express');
const jwt = require('jsonwebtoken');
const expressJwt = require('express-jwt');
const app = express();

const secretKey = 'your_jwt_secret';

app.use(express.json());

// 登录路由，生成 JWT
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // 验证用户逻辑
  const user = { id: 1, username }; // 示例用户
  const token = jwt.sign({ id: user.id }, secretKey, { expiresIn: '1h' });
  res.json({ token });
});

// 使用 express-jwt 中间件保护路由
app.use(expressJwt({ secret: secretKey, algorithms: ['HS256'] }).unless({ path: ['/login'] }));

app.get('/protected', (req, res) => {
  res.send('This is a protected route');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### 12. Passport.js

 **用途** ：Passport.js 是一个灵活且模块化的身份验证中间件，支持多种身份验证策略，如本地策略、OAuth、JWT 等。

 **安装** ：

```bash
npm install passport passport-local passport-jwt
```

 **使用** ：

```javascript
const express = require('express');
const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const JwtStrategy = require('passport-jwt').Strategy;
const ExtractJwt = require('passport-jwt').ExtractJwt;

const app = express();

// 配置本地策略
passport.use(new LocalStrategy(
  function(username, password, done) {
    // 验证用户逻辑
    User.findOne({ username: username }, function (err, user) {
      if (err) { return done(err); }
      if (!user) { return done(null, false); }
      if (!user.verifyPassword(password)) { return done(null, false); }
      return done(null, user);
    });
  }
));

// 配置 JWT 策略
const opts = {
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: 'your_jwt_secret'
};

passport.use(new JwtStrategy(opts, function(jwt_payload, done) {
  User.findById(jwt_payload.id, function(err, user) {
    if (err) { return done(err, false); }
    if (user) { return done(null, user); } else { return done(null, false); }
  });
}));

app.use(passport.initialize());

// 保护路由示例
app.get('/protected', passport.authenticate('jwt', { session: false }), (req, res) => {
  res.send('This is a protected route');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

**注意**

* **express-jwt** ：适合需要快速实现 JWT 验证的场景，简单易用。
* **Passport.js** ：功能强大，支持多种身份验证策略，适合复杂的身份验证需求。

根据你的具体需求选择合适的中间件，可以更高效地实现身份验证和授权功能。

## 总结

中间件是 Express.js 的核心功能，通过中间件可以实现各种功能，如日志记录、身份验证、错误处理等。在使用中间件时，注意它们的执行顺序和** **`next()` 的调用，以确保请求-响应周期的正确流转。理解中间件的原理和职责链模式，可以帮助我们更好地设计和组织 Express 应用程序。

通过使用 `适合`的中间件，可以显著提升 Express 应用的功能性和安全性。express中常见的中间件基本上涵盖了请求解析、日志记录、安全性增强和会话管理等常见需求，是开发 Express 应用时非常有价值的工具。
