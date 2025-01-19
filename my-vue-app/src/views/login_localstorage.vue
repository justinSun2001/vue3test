<template>
    <div class="loaded">
        <div class="container">
            <div class="box">
                <div v-if="showLoginForm" class="inner_box">
                    <div class="box_title">
                        欢迎来到登录界面
                    </div>
                    <div class="box_main_container">
                        <div class="box_main">
                            <el-form ref="form_login" :model="form_login" :rules="rules_login" label-position="top">
                                <!-- 登录表单内容 -->
                                <el-form-item label="用户名:" prop="username_login">
                                    <el-input v-model="form_login.username_login"></el-input>
                                </el-form-item>
                                <el-form-item label="密码:" prop="password_login">
                                    <el-input type="password" v-model="form_login.password_login"></el-input>
                                </el-form-item>
                                <el-form-item label="验证码:" prop="captcha">
                                    <el-input v-model="form_login.captcha"></el-input>
                                    <canvas id="captchaCanvas" @click="drawCaptcha" width="120" height="30"
                                        style="margin-top: 10px; width: 50%;"></canvas>
                                </el-form-item>
                            </el-form>
                        </div>
                    </div>
                </div>
                <div v-else class="inner_box">
                    <div class="box_title">
                        欢迎来到注册界面
                    </div>
                    <div class="box_main_container">
                        <div class="box_main">
                            <el-form ref="form_reg" :model="form_reg" :rules="rules_reg" label-position="top">
                                <!-- 注册表单内容 -->
                                <el-form-item label="用户名:" prop="username_reg">
                                    <el-input v-model="form_reg.username_reg"></el-input>
                                </el-form-item>
                                <el-form-item label="密码:" prop="password_reg">
                                    <el-input type="password" v-model="form_reg.password_reg"></el-input>
                                </el-form-item>
                                <el-form-item label="确认密码:" prop="confirmPassword">
                                    <el-input type="password" v-model="form_reg.confirmPassword"></el-input>
                                </el-form-item>
                                <el-form-item label="邮箱:" prop="email">
                                    <el-input v-model="form_reg.email"></el-input>
                                </el-form-item>
                            </el-form>
                        </div>
                    </div>
                </div>
                <div style="padding-bottom: 20px;">
                    <el-button @click="toggleForm">{{ showLoginForm ? '没有账号？切换到注册' : '已有账号？切换到登录' }}</el-button>
                    <el-button type="primary" @click="submitForm">{{ btnName }}</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            form_reg: {
                username_reg: '',
                password_reg: '',
                confirmPassword: '',
                email: '',
            },
            form_login: {
                username_login: '',
                password_login: '',
                captcha: '', // 用户输入的验证码
            },
            showLoginForm: false, // 控制显示登录表单还是注册表单
            captcha: '',
            btnName: '注册',
            rules_reg: {
                username_reg: [{ required: true, message: '请输入用户名(注册)', trigger: 'blur' }],
                password_reg: [{ required: true, message: '请输入密码(注册)', trigger: 'blur' }],
                confirmPassword: [{ required: true, message: '请确认密码', trigger: 'blur' },
                { validator: this.validateConfirmPassword, trigger: 'blur' }],
                email: [{ required: true, message: '请输入邮箱', trigger: 'blur' },
                { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }],
            },
            rules_login: {
                username_login: [{ required: true, message: '请输入用户名(登录)', trigger: 'blur' }],
                password_login: [{ required: true, message: '请输入密码(登录)', trigger: 'blur' }],
                captcha: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
            }
        }
    },
    mounted() {
    },
    methods: {
        generateRandomCode(length) {
            const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            let result = '';
            for (let i = 0; i < length; i++) {
                const randomIndex = Math.floor(Math.random() * characters.length);
                result += characters.charAt(randomIndex);
            }
            return result;
        },
        drawCaptcha() {
            const canvas = document.getElementById('captchaCanvas');
            const ctx = canvas.getContext('2d');

            // 生成随机背景色
            const randomColor = () => {
                const r = Math.floor(Math.random() * 256);
                const g = Math.floor(Math.random() * 256);
                const b = Math.floor(Math.random() * 256);
                return `rgb(${r},${g},${b})`;
            };

            ctx.fillStyle = randomColor();
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            const code = this.generateRandomCode(6);
            ctx.font = '20px Arial';
            ctx.fillStyle = 'black';
            ctx.fillText(code, 25, 25);
            this.captcha = code;

            // 可以将 code 保存到 localStorage 或者其他地方
        },
        toggleForm() {
            // Reset the form validation state
            if (this.showLoginForm) {
                this.$refs.form_login.resetFields();
            } else {
                this.$refs.form_reg.resetFields();
            }
            // Toggle the form display
            this.showLoginForm = !this.showLoginForm;
            if (this.showLoginForm === true) {
                this.btnName = '登录';
                this.$nextTick(() => {
                    this.drawCaptcha();
                });
            } else {
                this.btnName = '注册';
            }
        },
        validateConfirmPassword(rule, value) {
            if (value !== this.form_reg.password_reg) {
                return Promise.reject('两次输入的密码不一致');
            } else {
                return Promise.resolve();
            }
        },
        // 提交表单的方法
        submitForm() {
            if (this.showLoginForm) {
                console.log("登录");
                // 提交登录表单
                this.$refs.form_login.validate((valid) => {
                    if (valid) {
                        // 登录表单验证通过，执行登录逻辑
                        // 从localStorage中获取用户列表
                        const users = JSON.parse(localStorage.getItem('users')) || [];
                        // 查找匹配的用户
                        const user = users.find(user => user.username === this.form_login.username_login && user.password === this.form_login.password_login);


                        if (user && this.captcha === this.form_login.captcha) {
                            this.$message.success('Login successful!');
                            window.location.href = 'main.html?username=' + this.form_login.username_login + '&password=' + this.form_login.password_login;
                            // 可以跳转到登录成功后的页面
                        } else {
                            this.$message.error('Invalid username or password');
                        }
                    }
                });
            } else {
                // 提交注册表单
                console.log("注册");
                this.$refs.form_reg.validate((valid) => {
                    if (valid) {
                        // 注册表单验证通过，执行注册逻辑
                        // 从localStorage中获取之前存储的用户列表
                        let users = localStorage.getItem('users');
                        if (!users) {
                            // 如果用户列表不存在，则初始化为一个空数组
                            users = [];
                        } else {
                            // 如果用户列表存在，则解析成数组
                            users = JSON.parse(users);
                        }
                        // 检查是否存在相同用户名的用户
                        const existingUser = users.find(user => user.username === this.form_reg.username_reg);
                        if (existingUser) {
                            this.$message.error('Username already exists!');
                            return;
                        }
                        let username = this.form_reg.username_reg;
                        let password = this.form_reg.password_reg;
                        // 添加新用户到用户列表中
                        users.push({ username, password });
                        // 将用户列表重新存储到localStorage中
                        localStorage.setItem('users', JSON.stringify(users));
                        this.$message.success('Register successful!');
                        this.showLoginForm = true;
                        this.btnName = '登录';
                        this.$nextTick(() => {
                            this.drawCaptcha();
                        });
                    }
                });
            }
        }
    }
}
</script>

<style scoped>
.loaded {
    margin: 0;
    padding: 0;
    background-image: url('../assets/background.jpeg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: white;
}

/* 使用 CSS 来更改所有标签的字体颜色 */
.el-form--label-top .el-form-item .el-form-item__label {
    color: white;
}

/* 整体容器布局 */
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
    /* 隐藏子容器溢出部分 */
}

.box {
    text-align: center;
    max-width: 80%;
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 5px;
    max-height: 80%;
    padding: 0 5%;
    /* 子容器的最大高度等于父容器的高度 */
    overflow-y: auto;
    overflow-x: auto;
    /* 允许子容器在超过父容器高度时出现滚动条 */
}

.inner_box {
    width: 100%;
}

.box_title {
    border-bottom: 1px solid #d6d6d6;
    width: 100%;
    text-align: center;
    display: block;
    font-size: 18px;
    padding-top: 20px;
    padding-bottom: 20px;

}

.box_main_container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.box_main {
    width: 100%;
    text-align: center;
}

/* label标签布局 */
.el-form-item__label {
    width: 100%;
    white-space: nowrap;
}

.label-wrapper {
    display: flex;
    justify-content: space-between;
    width: 100%;
    white-space: nowrap;
    padding-top: 10%;
    padding-bottom: 10px;
}

.left-label {
    flex: 1;
    text-align: left;
}

.right-label {
    flex: 1;
    text-align: right;
}
</style>