<script lang="ts">
	import { currentUser } from '$lib/pb';
	import SignInForm from './SignInForm.svelte';
</script>

{#if $currentUser}
	<slot></slot>
{:else}
	<div class="flex h-screen items-center justify-center">
		<div class="p-5 shadow-xl shadow-black/80">
			<SignInForm />
		</div>
	</div>
{/if}
