<template>
    <div>
        <!-- 头部的标签 -->
        <el-tabs type="card">
            <el-tab-pane>
                <template #label>
                    <span class="custom-tabs-label">
                        <el-icon>
                            <EditPen />
                        </el-icon>
                        用户数据
                    </span>
                </template>
            </el-tab-pane>
            <el-tab-pane>
                <template #label>
                    <span class="custom-tabs-label" @click="handleTabClick('添加')">
                        <el-icon>
                            <EditPen />
                        </el-icon>
                        添加
                    </span>
                </template>
            </el-tab-pane>

            <el-tab-pane>
                <template #label>
                    <span class="custom-tabs-label" @click="handleTabClick('编辑')">
                        <el-icon>
                            <Edit />
                        </el-icon>
                        编辑
                    </span>
                </template>
            </el-tab-pane>

            <el-tab-pane>
                <template #label>
                    <span class="custom-tabs-label" @click="handleTabClick('删除')">
                        <el-icon>
                            <Delete />
                        </el-icon>
                        删除
                    </span>
                </template>
            </el-tab-pane>


            <el-tab-pane>
                <template #label>
                    <span class="custom-tabs-label" @click="handleTabClick('刷新')">
                        <el-icon>
                            <Refresh />
                        </el-icon>
                        刷新
                    </span>
                </template>
            </el-tab-pane>

        </el-tabs>

        <!-- 表格显示主体 -->
        <el-table :data="data" style="width: 100%" :selection="selection" @selection-change="handleSelectionChange"
            row-key='id'>
            <el-table-column type="selection" reserve-selection width="50"></el-table-column>
            <el-table-column type="index" :index="getIndex" width="50"></el-table-column>
            <el-table-column label="用户后台数据" header-align="center">
                <el-table-column prop="username" label="用户名"></el-table-column>
                <el-table-column prop="password" label="密码"></el-table-column>
                <el-table-column prop="registration_time" label="注册时间"></el-table-column>
            </el-table-column>
            <el-table-column fixed="right" label="操作" header-align="center" width="100">
                <template #default="scope">
                    <el-link type="primary" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-link>
                    <el-link type="primary" size="small" @click="handleDelete(scope.$index, scope.row)">删除</el-link>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
            :page-sizes="pageSizes" :page-size="pageSize" layout="sizes, prev, pager, next, jumper" :total="total"
            style="margin-top: 20px">
        </el-pagination>
    </div>
    <div>
        <el-dialog title="录入新用户数据" :visible="addDialog" append-to-body="true" @close="closeAddDialog">
            <el-form ref="form_add" :model="formData_add" label-width="100px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="username" prop="username">
                            <el-input v-model="formData_add.username"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="password" prop="password">
                            <el-input v-model="formData_add.password"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item>
                    <el-button type="primary" @click="handleSubmitAddForm">提交</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>

    <div>
        <el-dialog title="编辑数据" :visible="editDialog" append-to-body="true" @close="closeEditDialog">
            <el-form ref="form_edit" :model="formData_edit" label-width="100px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="username" prop="username">
                            <el-input v-model="formData_edit.username"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="password" prop="password">
                            <el-input v-model="formData_edit.password"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item>
                    <el-button type="primary" @click="handleSubmitEditForm">提交修改</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
    <!-- 滚动到顶部的按钮 -->
    <button class="scroll-btn" @click="scrollToTop">回到顶部</button>
</template>

<script>
import { getUserNum, getUserData, deleteUser, uploadUser, updateUser} from '../api/url'
export default {
    data() {
        return {
            formData_add: {
                username: '',
                password: '',
            },
            formData_edit: {
                user_id: '',
                username: '',
                password: '',
            },
            addDialog: false, //默认添加项目对话框状态
            editDialog: false,
            data: [],
            selectedData: [],
            selection: [],
            idsToDelete: [],
            idsToExport: [],
            idsToSubmit: [],
            currentPage: 1, // 当前页码
            pageSizes: [10], //页码数选项
            pageSize: 10, // 每页显示的条数
            total: 0, // 数据总数
        };
    },
    computed: {
        getIndex() {
            // 计算表格显示数据的索引值
            return (index) => {
                return (this.currentPage - 1) * this.pageSize + index + 1;
            };
        },
    },
    methods: {
        // 滚动到页面顶部的函数
        scrollToTop() {
            window.scrollTo(0, 0);
        },
        //详情编辑处理
        handleEdit(index, row) {
            this.editDialog = true;
            console.log(row.user_id);
            this.formData_edit = row;
            console.log(this.formData_edit);
        },
        //删除事件处理
        handleDelete(index, row) {
            console.log([row.user_id]);
            deleteUser([row.user_id]).then(response => {
                console.log('Request succeeded');
                this.getData();
                this.$message.success('删除成功');
            })
                .catch(error => {
                    console.error('Request failed:', error);
                    this.$message.error('删除失败');
                });
        },

        //监听表头点击事件
        handleTabClick(name) {
            switch (name) {
                case '添加':
                    this.addDialog = true;//弹出对话框;
                    break;
                case '编辑':
                    if (this.selection.length == 0) {
                        this.$message.warning('编辑项不能为空');
                    } else if (this.selection.length > 1) {
                        this.$message.warning('不能同时编辑多项');
                    } else {
                        this.editDialog = true;
                        console.log(this.selection[0].user_id);
                        this.formData_edit = this.selection[0];
                        console.log(this.formData_edit);
                    }
                    break;
                case '删除':
                    if (this.selection.length > 0) {
                        let length = this.selection.length;
                        let sel = this.selection;
                        let idsToDelete = [];
                        for (let i = 0; i < length; i++) {
                            console.log(sel[i]);
                            idsToDelete.push(sel[i].user_id);
                            console.log(idsToDelete);
                        }
                        deleteUser(idsToDelete).then(response => {
                            console.log('Request succeeded');
                            this.$message.success('删除成功');
                            // 从this.data数组中删除对应的数据项
                            idsToDelete.forEach(id => {
                                const index = this.data.findIndex(item => item.user_id === id);
                                if (index !== -1) {
                                    this.data.splice(index, 1);
                                }
                            });
                            this.updateDisplayData();
                        })
                            .catch(error => {
                                console.error('Request failed:', error);
                                this.$message.error('删除失败');
                            });
                    } else {
                        this.$message.warning('删除项不能为空');

                    }
                    break;
                case '刷新':
                    location.reload();
                    break;
            }
        },
        updateDisplayData() {
            console.log(this.currentPage);
            console.log(this.pageSize);
            getUserData(this.pageSize, this.currentPage)
                .then(response => {
                    console.log(response.data);
                    this.data = response.data;
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        getData() {
            this.data = [];
            getUserNum()
                .then(response => {
                    console.log(response.data);
                    this.total = response.data.num;
                    if (this.total < 10) {
                        this.pageSize = this.total;
                        this.pageSizes = [this.total, 10, 20]
                    } else {
                        this.pageSize = 10;
                        this.pageSizes = [10, 20, this.total]
                    }
                    this.updateDisplayData();
                    this.selection = [];
                    this.selectedData = [];
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        handleSizeChange(newSize) {
            // 每页显示条数改变时触发
            this.pageSize = newSize;
            this.currentPage = 1; // 重置当前页码
            this.updateDisplayData(); // 更新显示数据
        },
        handleCurrentChange(newPage) {
            // 当前页码改变时触发
            this.currentPage = newPage;
            this.updateDisplayData(); // 更新显示数据
        },
        //监听选择项的变化
        handleSelectionChange(selection) {
            this.selection = selection;
            if (selection && this.selection.length != 0) {
                console.log('Selected Data:', this.selection);
                this.selectedData = this.selection;
            }
        },

        closeAddDialog() {
            //关闭对话框
            this.addDialog = false;
            // 清空表单数据
            this.$refs.form.resetFields();
        },
        closeEditDialog() {
            //关闭对话框
            this.editDialog = false;
            // 清空表单数据
            this.$refs.form_edit.resetFields();
        },
        handleSubmitAddForm() {
            const data = this.formData_add;
            console.log(data);
            uploadUser(data)
                .then(response => {
                    this.getData();
                    console.log('Request succeeded');
                    this.$message.success("提交成功");
                })
                .catch(error => {
                    console.error('Request failed:', error);
                    this.$message.error("提交失败");
                    // 处理错误
                });
            // 在组件中添加新的逻辑
            // 关闭对话框
            this.addDialog = false;
            // 清空表单数据
            this.$refs.form_add.resetFields();
        },
        handleSubmitAddForm_edit() {
            const data = this.formData_edit;
            console.log(data);
            updateUser(data)
                .then(response => {
                    this.getData();
                    console.log('Request succeeded');
                    this.$message.success("提交修改成功");
                })
                .catch(error => {
                    console.error('Request failed:', error);
                    this.$message.error("提交修改失败");
                    // 处理错误
                });
            // 在组件中添加新的逻辑
            // 关闭对话框
            this.editDialog = false;
            // 清空表单数据
            this.$refs.form_edit.resetFields();
        },
    },
    mounted() {
        this.getData();
    },
}
</script>

<style scoped>
/* 为按钮添加基础样式 */
.scroll-btn {
    position: fixed;
    /* 绝对定位 */
    bottom: 20px;
    /* 距离底部20px */
    right: 20px;
    /* 距离右侧20px */
    padding: 10px 20px;
    /* 上下10px，左右20px的内边距 */
    background-color: #333;
    /* 按钮背景颜色 */
    font-size: 10px;
    color: white;
    /* 文字颜色 */
    border: none;
    /* 无边框 */
    border-radius: 5px;
    /* 圆角边框 */
    cursor: pointer;
    /* 鼠标悬停时显示手形 */
    z-index: 1000;
    /* 确保按钮在最上层 */
}
</style>