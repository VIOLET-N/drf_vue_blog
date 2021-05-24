<template>
    <br>
    <br>
    <hr>
    <h3>发表评论</h3>
    <textarea
        v-model="message"
        :placeholder="placeholder"
        name="comment"
        id="comment-area"
        rows="10"
        cols="60"
        ></textarea>
    <div>
        <button @click="submit" class="submitBtn">发布</button>
    </div>

    <br>
<!--    <p>已有 {{ comments.length }}</p>-->
    <hr>

    <div
         v-for="comment in comments"
         :key="comment.id"
        >
        <div class="comments">
            <div>
                <span class="username">
                    {{ comment.author.username }}
                </span>
                于
                <span class="created">
                    {{ formatted_time(comment.created) }}
                </span>
                <span v-if="comment.parent">
                    对
                    <span class="parent">
                        {{ comment.parent.author.username }}
                    </span>
                </span>
                说道
            </div>
            <div class="content">
                {{ comment.content }}
            </div>
            <div>
                <button class="commentBtn" @click="replyTo(comment)">回复</button>
            </div>
        </div>
        <hr>
    </div>
</template>

<script>
    import axios from 'axios';
    import authorization from '../utils/authorization';

    export default {
        name: "Comments",
        props: { article: Object },
        data: function () {
            return {
                comments: [],
                message: '',
                placeholder: '说点什么...',
                parentID: null
            }
        },
        watch: {
            article() {
                this.comments = this.article !== null ? this.article.comments : []
            }
        },
        methods: {
            submit() {
                const that = this;
                authorization()
                    .then(function (response) {
                        if (response[0]) {
                            axios
                                .post('/api/comment/',
                                    {
                                        content: that.message,
                                        article_id: that.article.id,
                                        parent_id: that.parentID,
                                    },
                                    {
                                        headers: {Authorization: 'Bearer ' + localStorage.getItem('access.myblog')}
                                    })
                                .then(function (response) {
                                    that.comments.unshift(response.data);
                                    that.message = '';
                                    alert('留言成功')
                                })
                        }
                        else {
                            alert('请登录后评论。')
                        }
                    })
            },
            replyTo(comment) {
                this.parentID = comment.id;
                this.placeholder = '对' + comment.author.username + '说：'
            },
            formatted_time: function (iso_data_string) {
                const date = new Date(iso_data_string);
                return date.toLocaleDateString() + '  ' + date.toLocaleTimeString()
            },
        }
    }
</script>

<style scoped>
    button {
    cursor: pointer;
    border: none;
    outline: none;
    color: whitesmoke;
    border-radius: 5px;
  }
  .submitBtn {
    height: 35px;
    background: steelblue;
    width: 60px;
  }
  .commentBtn {
    height: 25px;
    background: lightslategray;
    width: 40px;
  }
  .comments {
    padding-top: 10px;
  }
  .username {
    font-weight: bold;
    color: darkorange;
  }
  .created {
    font-weight: bold;
    color: darkblue;
  }
  .parent {
    font-weight: bold;
    color: orangered;
  }
  .content {
    font-size: large;
    padding: 15px;
  }
</style>