// 引用用户模版数据
const User = require("../models/user.js");

const userController = {
  // 获取用户数据
  queryUser: async (req, res, next) => {
    try {
      let resData = await User.query();
      res.json({
        code: 200,
        message: "操作成功",
        data: resData,
      });
    } catch (e) {
      res.json({ code: 0, message: "操作失败", data: e });
    }
  },
  // 添加用户数据
  addUser: async (req, res, next) => {
    try {
      let resData = await User.insert(req.body);
      res.json({
        code: 200,
        message: "操作成功",
        data: resData,
      });
    } catch (e) {
      res.json({ code: 0, message: "操作失败", data: e });
    }
  },
  // 更新用户数据
  updateUser: async (req, res, next) => {
    const { id, params } = req.body;
    try {
      let resData = await User.update(id, params);
      res.json({
        code: 200,
        message: "操作成功",
        data: resData,
      });
    } catch (e) {
      res.json({ code: 0, message: "操作失败", data: e });
    }
  },
  // 删除用户数据
  delUser: async (req, res, next) => {
    try {
      let resData = await User.delete(req.body.id);
      res.json({
        code: 200,
        message: "操作成功",
        data: resData,
      });
    } catch (e) {
      res.json({ code: 0, message: "操作失败", data: e });
    }
  },
};

module.exports = userController;

