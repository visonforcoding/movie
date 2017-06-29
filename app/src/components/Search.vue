<template>
    <el-row id="movie-list" type="flex" justify="center" v-loading="loading" element-loading-text="拼命加载中">
        <el-col :span="20">
            <a v-link="{path:'detail',params:{query:'test'}}">
            <div v-for="movie in movies" :key="movie" class="text item">
                <div class="title">
                    <el-col :span="5">{{movie.title }}</el-col>
                    <span class="tags">
                        <el-tag v-for="tag in movie.tag" :key="tag">{{tag}}</el-tag>
                    </span>
                </div>
            </div>
            </a>
        </el-col>
    </el-row>
</template>
<style>
#movie-list {
    min-height: 100px;
}

.text {
    font-size: 14px;
}

.item {
    margin: 10px;
    padding: 18px 0;
    border: 1px solid silver;
}

.box-card {
    width: 480px;
}
</style>

<script>
export default {
    data() {
        return {
            loading: false,
            movies: [
            ]
        }
    },
    created() {
        // 组件创建完后获取数据，
        // 此时 data 已经被 observed 了
        this.fetchData()
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'routeChange'
    },
    methods: {
        routeChange(r) {
            console.log('t');
        },
        fetchData() {
            this.error = this.post = null
            this.loading = true
            var self = this;
            setTimeout(function () {
                self.$http.get('http://127.0.0.1:5000/movie/' + self.$route.params.query).then(function (res) {
                    if (res) {
                        self.movies = res.body.data.movies;
                    }
                });
                self.loading = false;
            }, 1000);

        }
    }
}
</script>