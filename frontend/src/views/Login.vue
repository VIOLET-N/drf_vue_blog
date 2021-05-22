<template>
    <BlogHeader/>

    <div id="grid">
        <div id="signup">
            <h3>注册账号</h3>
            <form>
                <div class="form-elem">
                    <span>账号：</span>
                    <input type="text" v-model="signupName" placeholder="输入用户名">
                </div>
                <div class="form-elem">
                    <span>密码：</span>
                    <input type="text" v-model="signupPwd" placeholder="输入密码">
                </div>
                <div class="form-elem">
                    <button v-on:click.prevent="signup">提交</button>
                </div>
            </form>
        </div>

        <div id="signin">
            <h3>登录账号</h3>
            <form>
                <div class="form-elem">
                    <span>账号：</span>
                    <input type="text" v-model="signinName" placeholder="输入用户名...">
                </div>

                <div class="form-elem">
                    <span>密码：</span>
                    <input type="password" v-model="signinPwd" placeholder="输入密码...">
                </div>

                <div class="form-elem">
                    <button v-on:click.prevent="signin">登录</button>
                </div>
            </form>
        </div>
    </div>

    <BlogFooter/>
</template>

<script>
    import BlogHeader from "../components/BlogHeader";
    import BlogFooter from "../components/BlogFooter";
    import axios from 'axios';

    export default {
        name: "Login",
        components: {BlogFooter, BlogHeader},
        data: function () {
            return {
                signupName: '',
                signupPwd: '',
                signupResponse: null,
                signinName: '',
                signinPwd: '',
            }
        },
        methods: {
            signup() {
                const that = this;
                axios
                    .post('/api/user/', {
                        username: this.signupName,
                        password: this.signupPwd,
                    })
                    .then(function (response) {
                        that.signupResponse = response.data;
                        alert('用户注册成功，窥觑登录吧！');
                    })
                    .catch(function (error) {
                        alert(error.message);
                    })

            },
            signin(){
                const that = this;
                axios
                    .post('/api/token/', {
                        username: that.signinName,
                        password: that.signinPwd,
                    })
                    .then(function (response) {
                        const storage = localStorage;
                        const expiredTime = Date.parse(response.headers.data) + 60000;
                        storage.setItem('access.myblog', response.data.access);
                        storage.setItem('refresh.myblog', response.data.refresh);
                        storage.setItem('expiredTime.myblog', expiredTime);
                        storage.setItem('username.myblog', that.signinName);

                        that.$router.push({name: 'Home'});
                    })
            }
        }
    }
</script>

<style scoped>
    #grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
    }

    #signup {
        text-align: center;
    }

    .form-elem{
        padding: 10px;
    }

    input {
        height: 25px;
        padding-left: 10px;
    }

    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: gray;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }

    #signin{
        text-align: center;
    }
</style>