<template>
    <BlogHeader/>

    <div id="article-crete">
        <h3>发表文章</h3>
        <form>
            <div class="form-elem">
                <span>标题：</span>
                <input type="text" v-model="title" placeholder="输入标题">
            </div>

            <div class="form-elem">
                <span>分类：</span>
                <span
                    v-for="category in categories"
                    :key="category.id"
                >
                    <button
                            class="category-btn"
                            :style="categoryStyle(category)"
                            @click.prevent="chooseCategory(category)"
                    >
                        {{ category.title }}
                    </button>
                </span>
            </div>

            <div class="form-elem">
                <span>标签：</span>
                <input type="text" v-model="tags" placeholder="输入标签，用都好分割">
            </div>

            <div class="form-elem">
                <span>正文</span>
                <textarea v-model="body" placeholder="输入正文" cols="80" rows="30"></textarea>
            </div>

            <div class="form-elem">
                <button v-on:click.prevent="submit">提交</button>
            </div>
        </form>
    </div>

    <BlogFooter/>
</template>

<script>
    import BlogHeader from "../components/BlogHeader";
    import BlogFooter from "../components/BlogFooter";
    import axios from 'axios';
    import authorization from "../utils/authorization";

    export default {
        name: "ArticleCreate",
        components: {BlogFooter, BlogHeader},
        data: function () {
            return {
                // 文章标题
                title: '',
                // 文章正文
                body: '',
                // 数据库中的所有分类
                categories: [],
                // 选定的分类
                selectCategory: null,
                // 标签
                tags: '',
            }
        },
        mounted() {
            axios
                .get('/api/category/')
                .then(response => this.categories = response.data);
        },
        methods: {
            categoryStyle(category) {
                if (this.selectCategory !== null && category.id === this.selectCategory.id) {
                    return {
                        backgroundColor: 'black',
                    }
                }
                return {
                    backgroundColor: 'lightgrey',
                    color: 'black',
                }
            },
            // 选取分类方法
            chooseCategory(category) {
                // 如果点击已选取的分类， 则将 selectedCategory 置空
                if (this.selectCategory !== null && this.selectCategory.id === category.id) {
                    this.selectCategory = null;
                }
                // 如果没有选中
                else {
                    this.selectCategory = category;
                }
            },
            // 点击提交按钮
            submit() {
                const that = this;
                authorization()
                    .then(function (response) {
                        if (response[0]) {
                            // 需要传给后端的数据字典
                            let data = {
                                title: that.title,
                                body: that.body,
                            };
                            // 添加分类
                            if (that.selectCategory) {
                                data.category_id = that.selectCategory.id;
                                console.log('分类id:',that.selectCategory.id)
                            }
                            // 标签处理
                            data.tages = that.tags
                                // 用逗号分割标签
                                .split(/[，,]/)
                                // 剔除标签首位空格
                                .map(x => x.trim())
                                // 剔除长度为零的无效标签
                                .filter(x => x.charAt(0) !== '');

                            // 将发表文章发送至接口
                            // 成功后前往详情页面
                            const token = localStorage.getItem('access.myblog');

                            axios
                                .post('/api/article/',
                                    data,
                                    {
                                        headers: {Authorization: 'Bearer ' + token }
                                    })
                                .then(function (response) {
                                    that.$router.push({name: 'ArticleDetail', params: {id: response.data.id }});
                                })
                        }
                        else {
                            alert('令牌过期，请从新登录。')
                        }
                    })
            }
        }
    }
</script>

<style scoped>
    .category-btn {
        margin-right: 10px;
    }

    #article-crete {
        text-align: center;
        font-size: large;
    }

    form {
        text-align: left;
        padding-left: 100px;
        padding-right: 10px;
    }

    .form-elem {
        padding: 10px;
    }

    input {
        height: 25px;
        padding-left: 10px;
        width: 50%;
    }

    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: steelblue;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }
</style>