<script lang="ts">
	import { currentUser, pb, type Transaction } from '$lib/pb';
	import * as Table from '$lib/components/ui/table';
	import { onMount } from 'svelte';
	import type { Writable } from 'svelte/store';
	import { buttonVariants } from '$lib/components/ui/button';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	import { Skeleton } from '$lib/components/ui/skeleton';

	interface TransactionResponse extends Transaction {
		expand: {
			sender: {
				name: string;
			};
			recipient: {
				name: string;
			};
		};
	}

	let transactions: TransactionResponse[] = [];
	let transactionPage: number = 1; // Whats requested by user
	let curTransactionPage = 0; // Whats displayed on the page
	let totalTransactions: number | null = null;

	function loadTransactions(page: number = 1) {
		pb.collection<Transaction>('transactions')
			.getList(page, 10, {
				sort: '-created',
				filter: `bankId='${$page.params.slug}' && (sender.id='${$currentUser.id}' || recipient.id='${$currentUser.id}')`,
				expand: 'sender, recipient',
				fields: '*, expand.sender.name, expand.recipient.name'
			})
			.then((res) => {
				transactions = res.items as TransactionResponse[];
				transactionPage = res.page;
			});
	}

	onMount(async () => {
		loadTransactions();
	});
</script>

<div class="mb-4 flex items-center justify-between">
	<strong>Welcome, {$currentUser?.name}!</strong>
	<div>
		<a href={`/bank/${$page.params.slug}/transfer`} class={buttonVariants({ variant: 'outline' })}>
			Transfer
		</a>
		<Button
			variant="destructive"
			on:click={() => {
				pb.authStore.clear();
			}}>Log out</Button
		>
	</div>
</div>

<!-- {#if curTransactionPage !== transactionPage}
	<Skeleton class="h-4 w-[200px]" />
	<Skeleton class="h-4 w-[200px]" />
	<Skeleton class="h-4 w-[200px]" />
{/if} -->

{#if transactions.length > 0}
	<Table.Root
		><Table.Header>
			<Table.Row>
				<Table.Head>Sender</Table.Head>
				<Table.Head>Recipient</Table.Head>
				<Table.Head>Timestamp</Table.Head>
				<Table.Head class="text-right">Amount</Table.Head>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each transactions as transaction}
				<Table.Row>
					<Table.Cell>{transaction.expand.sender.name}</Table.Cell>
					<Table.Cell>{transaction.expand.recipient.name}</Table.Cell>
					<Table.Cell class="font-medium"
						>{new Date(transaction.created).toLocaleDateString('en-SG')}, {new Date(
							transaction.created
						).toLocaleTimeString('en-SG')}</Table.Cell
					>
					<Table.Cell class="text-right">${transaction.amount.toFixed(2)}</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
{:else}
	<p>No transactions.</p>
{/if}
