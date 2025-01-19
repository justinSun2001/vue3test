const configs = require("../config");
const knex = require("knex")({
  // 链接配置
  connection: {
    host: configs.mysql.host,
    port: configs.mysql.port,
    user: configs.mysql.user,
    password: configs.mysql.password,
    database: configs.mysql.database,
  },
  // 客户端版本
  client: "mysql2",
  // 打印错误
  log: {
    error(message) {
      console.log("[knex error]", message);
    },
  },
});

class Base {
  constructor(props) {
    this.table = props.table;
    this.schema = props.schema;
    this.createTable();
  }

  async createTable() {
    const exists = await knex.schema.hasTable(this.table);
    if (!exists) {
      await knex.schema.createTable(this.table, this.schema);
    }
  }

  // 新增
  insert(params) {
    return knex(this.table).insert(params);
  }

  // 更改
  update(id, params) {
    return knex(this.table).where("id", "=", id).update(params);
  }

  // 删除
  delete(id) {
    return knex(this.table).where("id", "=", id).del();
  }

  // 查找
  query() {
    return knex(this.table).select();
  }
}

module.exports = Base;
