<script lang="ts">
	import { currentUser, pb, type Transaction } from '$lib/pb';
	import * as Table from '$lib/components/ui/table';
	import { onMount } from 'svelte';
	import type { Writable } from 'svelte/store';
	import { buttonVariants } from '$lib/components/ui/button';
	import { page } from '$app/stores';

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
				filter: `bankId='${$page.params.slug}'`,
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

<div class="flex items-center justify-between">
	<h1>Welcome, {$currentUser?.name}!</h1>
	<a href={`/bank/${$page.params.slug}/transfer`} class={buttonVariants({ variant: 'outline' })}>
		Transfer
	</a>
</div>

{#if curTransactionPage !== transactionPage}
	<!-- Loader -->
{/if}

{#if transactions.length > 0}
	<Table.Root
		><Table.Header>
			<Table.Row>
				<Table.Head class="w-[100px]">Date</Table.Head>
				<Table.Head>Sender</Table.Head>
				<Table.Head>Recipient</Table.Head>
				<Table.Head class="text-right">Amount</Table.Head>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each transactions as transaction}
				<Table.Row>
					<Table.Cell class="font-medium">{transaction.created}</Table.Cell>
					<Table.Cell>{transaction.expand.sender.name}</Table.Cell>
					<Table.Cell>{transaction.expand.recipient.name}</Table.Cell>
					<Table.Cell class="text-right">${transaction.amount.toFixed(2)}</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
{:else}
	<p>No transactions yet</p>
{/if}
