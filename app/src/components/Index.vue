<template>
    <el-row type="flex" justify="center">
        <el-col :span="11">
            <el-input v-model="input" @keyup.native.enter="handSearch" placeholder="请输入内容">
            </el-input>
        </el-col>
    </el-row>
</template>


<script>
export default {
    data() {
        return {
            input: ''
        }
    },
    methods: {
        handSearch(query) {
            console.log(this.input);
            this.$router.push({ name: 'search', params: { query: this.input } })
        }
    }
}
</script>