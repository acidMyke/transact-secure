<!-- Sign in Form, no Signup. -->

<script lang="ts">
	import { pb } from '$lib/pb';

	let username = '';
	let password = '';

	async function login() {
		const authData = await pb.collection('users').authWithPassword(username, password);
	}
</script>

<form on:submit|preventDefault class="flex flex-col items-center justify-center gap-2">
	<input type="text" bind:value={username} placeholder="Username" class="input input-primary" />
	<input type="password" bind:value={password} placeholder="Password" class="input input-primary" />
	<button type="submit" class="btn btn-primary btn-wide" on:click={login}> Sign In </button>
</form>
