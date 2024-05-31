<script lang="ts">
	import { currentUser, pb, type Transaction } from '$lib/pb';
	import { onMount } from 'svelte';
	import type { Writable } from 'svelte/store';

	interface TransactionResponse extends Transaction {
		extends: {
			sender?: {
				name: string;
			};
			recipient?: {
				name: string;
			};
		};
	}

	let transactions: TransactionResponse[] = [];
	let transactionPage: number = 1; // Whats requested by user
	let curTransactionPage = 0; // Whats displayed on the page
	let totalTransactions: number | null = null;

	function loadTransactions(page: number = 1) {
		pb.collection<Transaction>('transaction')
			.getList(page, 10, {
				sort: '-created',
				expands: 'sender,recipient',
				fields: '*,sender.name,recipient.name'
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

<h1>Welcome, {$currentUser?.name}!</h1>

{#if curTransactionPage !== transactionPage}
	<!-- Loader -->
{/if}

{#if transactions.length > 0}
	<table class="table">
		<thead>
			<tr>
				<th>Date</th>
				<th>Sender</th>
				<th>Recipient</th>
				<th>Amount</th>
			</tr>
		</thead>
		<tbody>
			{#each transactions as transaction}
				<tr>
					<td>{new Date(transaction.created).toLocaleString()}</td>
					<td>{transaction.extends.sender?.name || 'N/A'}</td>
					<td>{transaction.extends.recipient?.name || 'N/A'}</td>
					<td>{transaction.amount}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{:else}
	<p>No transactions yet</p>
{/if}
