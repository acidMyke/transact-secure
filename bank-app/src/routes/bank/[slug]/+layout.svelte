<script lang="ts">
	import { currentUser } from '$lib/pb';
	import SignInForm from './sign-in-form.svelte';
</script>

{#if $currentUser}
	<div class="p-10">
		<slot></slot>
	</div>
{:else}
	<div class="flex h-screen items-center justify-center">
		<div class="p-5 shadow-xl shadow-black/80">
			<SignInForm />
		</div>
	</div>
{/if}
