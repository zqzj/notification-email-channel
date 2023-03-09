<template>
	<div class="full-screen">
		<div v-if="loading" class="content">Content is loading...</div>
		<div v-else>
			<!-- Channel configuration body -->
		</div>
	</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

defineProps({
	msg: {
		type: String,
		default: '',
	},
})

const loading = ref(true)
onMounted(async () => {
	await dl.init()
	dl.on('ready', async () => {
		loading.value = false
	})
})
</script>

<style scoped>
</style>
