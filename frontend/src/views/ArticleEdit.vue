<template>
    <BlogHeader/>

    <div id="article-create">
        <h3>更新文章</h3>
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
                <input type="text" v-model="tags" placeholder="输入标签，用逗号分割">
            </div>

            <div class="form-elem">
                <span>正文：</span>
                <textarea cols="80" rows="20" v-model="body" placeholder="输入正文"></textarea>
            </div>

            <div class="form-elem">
                <button v-on:click.prevent="submit">提交</button>
            </div>

            <div class="form-elem">
                <button v-on:click.prevent="deleteArticle" style="background-color: darkred">删除</button>
            </div>
        </form>
    </div>

    <BlogFooter/>
</template>

<script>
    import BlogHeader from "../components/BlogHeader";
    import BlogFooter from "../components/BlogFooter";
    import axios from 'axios'
    import authorization from "../utils/authorization"

    export default {
        name: "ArticleEdit",
        components: {BlogFooter, BlogHeader},
        data: function () {
            return {
                title: '',
                body: '',
                // 所有分类
                category: [],
                // 选定分类
                selectCategory: null,
                // 标签
                tags: '',
                // article id
                articleID: null
            }
        },
        mounted() {
            // 页面初始化时获取所有分类
            axios
                .get('/api/category/')
                .then(response => this.categories = response.data);

            const that = this;
            axios
                .get('/api/article/' + that.$route.params.id + '/')
                .then(function (response) {
                    const data = response.data;
                    that.title = data.title;
                    that.body = data.body;
                    that.selectCategory = data.category;
                    that.tags = data.tags.join(',');
                    that.articleID = data.id;
                })
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
            chooseCategory(category) {
                if (this.selectCategory !== null && this.selectCategory.id === category.id) {
                    this.selectCategory = null
                }
                else {
                    this.selectCategory = category;
                }
            },
            submit() {
                const that = this;
                authorization()
                    .then(function (response) {
                        if (response[0]) {
                            let data = {
                                title: that.title,
                                body: that.body,
                            };

                            data.category_id = that.selectCategory ? that.selectCategory.id : null;

                            data.tags = that.tags
                                .split('/[,，]/')
                                .map(x => x.trim())
                                .filter(x => x.charAt(0) !== '');

                            const token = localStorage.getItem('access.myblog');
                            axios
                                .put('/api/article/' + that.articleID + '/',
                                    data,
                                    {
                                        headers: {Authorization: 'Bearer ' + token}
                                    })
                                .then(function (response) {
                                    that.$router.push({name: 'ArticleDetail', params: {id: response.data.id}});
                                })
                        }
                        else {
                            alert('令牌过期，请重新登录。')
                        }
                    })
            },
            deleteArticle(){
                const that = this;
                const token = localStorage.getItem('access.myblog');
                authorization()
                    .then(function (response) {
                        if (response[0]) {
                            axios
                                .delete('/api/article/' + that.articleID + '/',
                                    {
                                        headers: {Authorization: 'Bearer ' + token}
                                    })
                                .then(() => that.$router.push({name: 'Home'}))
                        }
                        else {
                            alert('令牌过期，从新登录。')
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

    #article-create {
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
        color: whitesmoke;;
        border-radius: 5px;
        width: 60px;
    }
</style>