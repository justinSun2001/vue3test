const configs = {
    mysql: {
      host: "localhost",
      port: "3306",
      user: "root", // 数据库用户
      password: "bieber1994", // 数据库密码
      database: "test", // 数据库的名字
    },
    // 打印错误
    log: {
      error(message) {
        console.log("[knex error]", message);
      },
    },
  };
  
  module.exports = configs;
  