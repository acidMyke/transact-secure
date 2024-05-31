<!-- Generate a svelte compoenent that has a table displaying transaction  -->
<!-- With Date, Sender, Recipient and Amount -->

<script lang="ts">
	let transactions = [
		{
			date: '2021-10-10',
			sender: 'Alice',
			recipient: 'Clara',
			amount: 1000
		},
		{
			date: '2021-10-11',
			sender: 'Clara',
			recipient: 'Bobby',
			amount: 500
		}
	];
</script>

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
				<td>{transaction.date}</td>
				<td>{transaction.sender}</td>
				<td>{transaction.recipient}</td>
				<td>{transaction.amount}</td>
			</tr>
		{/each}
	</tbody>
</table>
