const express = require("express");
const router = express.Router();
const userController = require("../controllers/user");

// ...

// 获取用户信息
router.get("/get_user", userController.queryUser);
// 新增用户信息
router.post("/add_user", userController.addUser);
// 修改用户信息
router.post("/update_user", userController.updateUser);
// 删除用户信息
router.post("/del_user", userController.delUser);

module.exports = router;

