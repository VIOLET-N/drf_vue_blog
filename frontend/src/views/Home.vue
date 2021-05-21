<template>

    <BlogHeader/>

    <ArticleList/>

    <BlogFooter/>
</template>

<script>
    import BlogHeader from '../components/BlogHeader'
    import BlogFooter from '../components/BlogFooter'
    import ArticleList from '../components/ArticleList'

    export default {
        name: "Home",
        components: {BlogHeader, ArticleList, BlogFooter}
    }

</script>

<style scoped>

</style>