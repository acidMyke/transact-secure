<script lang="ts">
	import type { PageData } from './$types.js';
	import TransferForm from './transfer-form.svelte';

	export let data: PageData;
</script>

<TransferForm data={data.form} />
