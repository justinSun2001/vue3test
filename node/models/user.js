const Base = require("./base");

class User extends Base {
  constructor(props = { table: "users", schema: (table) => {
    table.increments('id').primary();
    table.string('name');
    table.string('email');
  }}) {
    super(props);
  }
}

module.exports = new User();
