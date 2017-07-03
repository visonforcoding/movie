<template>
    <div>
        <el-row>
            <img style="width:400px;" src="../assets/logo.jpg">
        </el-row>
        <el-row type="flex" justify="center">
            <el-col :span="11">
                <el-input v-model="input" @keyup.native.enter="handSearch" placeholder="请输入想搜索的电影">
                </el-input>
            </el-col>
        </el-row>
        <el-row id="rating-list" type="flex">
            <el-col :span="6" :offset="6">
                <ul>
                    <li>最新收录</li>
                    <li v-for="newMovie in new_movies" :key="newMovie">
                        <router-link v-bind:to="{name:'detail',params:{ query:newMovie.hash}}">
                            {{newMovie.title}}
                        </router-link>
                    </li>
                </ul>
            </el-col>
            <el-col :span="10">
                <ul style="margin-left:120px;">
                    <li>豆瓣好评</li>
                    <li v-for="ratingMovie in rating_movies" :key="ratingMovie">
                        <router-link v-bind:to="{name:'detail',params:{ query:ratingMovie.hash}}">
                            <img style="width:40px;" v-bind:src="ratingMovie.db_subject.images.small"> 
                            <span v-for="genre in ratingMovie.db_subject.genres" :key="genre">[{{genre}}] </span>
                            {{ratingMovie.db_subject.title}}
                        </router-link>
                    </li>
                </ul>
            </el-col>
        </el-row>
    </div>
</template>
<style>
#rating-list ul li {
    list-style: none;
    list-style-type: none;
    text-align: left;
}
</style>


<script>
export default {
    data() {
        return {
            input: '',
            new_movies: [],
            rating_movies: []
        }
    },
    created() {
        this.initData()
    },
    methods: {
        handSearch(query) {
            console.log(this.input);
            this.$router.push({ name: 'search', params: { query: this.input } })
        },
        initData() {
            console.log('init data...');
            this.$http.get(this.prd_config.API_URL + '/index').then(function (res) {
                if (res) {
                    this.new_movies = res.body.data.new_movies;
                    this.rating_movies = res.body.data.rating_movies;
                }
            });
        }
    }
}
</script>