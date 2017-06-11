<<template>
<el-row class="demo-autocomplete">
  <el-col :span="24">
    <el-autocomplete
      class="inline-input"
      v-model="state1"
      :fetch-suggestions="querySearch"
      placeholder="请输入内容"
      @select="handleSelect"
      id="search-input"
    ></el-autocomplete>
  </el-col>
</el-row>
</template>
<style>
#search-input {
    width: 520px;
}
</style>
<script>
export default {
    data() {
        return {
            restaurants: [],
            state1: '',
            state2: ''
        };
    },
    methods: {
        querySearch(queryString, cb) {
            var restaurants = this.restaurants;
            var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
            // 调用 callback 返回建议列表的数据
            cb(results);
        },
        createFilter(queryString) {
            return (restaurant) => {
                return (restaurant.value.indexOf(queryString.toLowerCase()) === 0);
            };
        },
        loadAll() {
            var data = [
                { "value": "三全鲜食（北新泾店）", "address": "长宁区新渔路144号" },
                { "value": "Hot honey 首尔炸鸡（仙霞路）", "address": "上海市长宁区淞虹路661号" },
            ];
            var query = '无间道';
            this.$http.get('http://api.movie.com/movie/'+query).then(function(res){
                if(res){
                    data = res.data;
                }
            });
            return data;
        },
        handleSelect(item) {
            console.log(item);
        }
    },
    mounted() {
        this.restaurants = this.loadAll();
    }
}
</script>