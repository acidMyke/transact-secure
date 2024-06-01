<!-- Sign in Form, no Signup. -->

<script lang="ts">
	import { pb } from '$lib/pb';
	import Button from '@/components/ui/button/button.svelte';
	import Input from '@/components/ui/input/input.svelte';

	let username = '';
	let password = '';

	async function login() {
		const authData = await pb.collection('users').authWithPassword(username, password);
	}
</script>

<form on:submit|preventDefault class="flex flex-col items-center justify-center gap-2">
	<Input type="text" bind:value={username} placeholder="Username" class="input input-primary" />
	<Input type="password" bind:value={password} placeholder="Password" class="input input-primary" />
	<Button type="submit" class="btn btn-primary btn-wide" on:click={login}>Sign In</Button>
</form>
