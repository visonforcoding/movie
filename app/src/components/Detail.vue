<template>
  <div>
    <el-row id="movie-title">
      <el-col :offset="2">
        <h3>{{movie.title}}</h3>
      </el-col>
    </el-row>
    <div v-loading="loading" element-loading-text="拼命加载中.." v-if="movie.db_match">
      <el-row>
        <el-col :span="2" :offset="2" v-if="movie.images.large">
          <img style="width:200px;" v-bind:src="movie.images.large"></img>
        </el-col>
        <el-col :span="7" :offset="1">
          <ul class="movie-prop-list">
            <li>
              导演:
              <a v-for="director in movie.directors" :key="director">{{director.name}}</a>
            </li>
            <li>
              剧情:
              <a v-for="genre in movie.genres" :key="genre">{{genre}} </a>
            </li>
            <li>
              主演:
              <a :href="cast.alt" v-for="cast in movie.casts" :key="cast">{{cast.name}} </a>
            </li>
            <li>
              豆瓣评分:{{movie.rating.average}}
              <el-rate v-model="movie_rate" disabled text-color="#ff9900" text-template="{value}">
              </el-rate>
            </li>
            <li>
              年份: {{movie.year}}
            </li>
            <li>
              下载地址:
              <el-tag style="margin-top:5px" v-for="download_url in movie.download_url" :key="download_url">{{download_url}}</el-tag>
            </li>
          </ul>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<style>
#movie-title {
  text-align: left;
}

.movie-prop-list {
  list-style-type: none;
  text-align: left;
}
</style>

<script>
export default {
  data() {
    return {
      loading: false,
      movie: {
        images: { large: null },
        year: null,
        directors: null, rating: { average: 0 }
      },
      movie_cover: false,
      value4: 3.7
    }
  },
  computed: {
    movie_rate: function () {
      return this.movie.rating.average / 10 * 5;
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
        self.$http.get(self.prd_config.API_URL + '/detail/' + self.$route.params.query).then(function (res) {
          if (res) {
            var res_obj = null;
            res_obj = res.body.data;
            if (res_obj.hasOwnProperty('db_match')) {
              res_obj['db_subject']['download_url'] = res_obj['download_url'];
              self.movie = res_obj['db_subject'];
              self.movie['db_match'] = true;
              self.movie_cover = self.movie['images']['large'];
            } else {
              self.movie = res_obj;
            }
          }
        });
        self.loading = false;
      }, 1000);

    }
  }
}
</script>