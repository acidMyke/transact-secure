<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { formSchema, type FormSchema } from './schema';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import pb, { currentUser, type User } from '$lib/pb';
	import { onMount } from 'svelte';
	import * as Select from '$lib/components/ui/select';
	import { page } from '$app/stores';
	import { cn } from '@/utils';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Label } from '$lib/components/ui/label';
	import { Button } from '$lib/components/ui/button';

	export let data: SuperValidated<Infer<FormSchema>>;
	let canSubmit: boolean = false;
	let confirmSubmit = false;

	const form = superForm(data, {
		validators: zodClient(formSchema),
		multipleSubmits: 'prevent',
		invalidateAll: false, // this is key for avoid calling the load function on server side
		resetForm: false // I don't want to lose the data after the form is sent,
	});

	const { form: formData, enhance, submit } = form;

	let users: User[] = [];
	let selectedRecipientCreditRating: number;

	const loadUsers = async () => {
		pb.collection<User>('users')
			.getFullList({ filter: `id!='${$currentUser!.id}'` })
			.then((res) => {
				users = res;
			});
	};

	onMount(async () => {
		loadUsers();
		$formData.sender = $currentUser!.id;
		$formData.bankId = $page.params.slug;
	});

	$: {
		canSubmit =
			(selectedRecipientCreditRating < 750 && confirmSubmit) || selectedRecipientCreditRating > 750;
	}
</script>

<form method="POST" use:enhance>
	<Form.Field {form} name="sender">
		<Form.Control let:attrs>
			<Form.Label>Sender</Form.Label>
			<Input {...attrs} bind:value={$formData.sender} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="recipient">
		<Form.Control let:attrs>
			<Form.Label>Recipient</Form.Label>
			<Select.Root
				onSelectedChange={async (v) => {
					if (v) {
						$formData.recipient = v.value.id;

						selectedRecipientCreditRating = Number(
							(await pb.collection('users').getOne(v.value.id, { fields: 'creditRating' }))
								.creditRating
						);
					}
				}}
			>
				<Select.Trigger class="w-[180px]">
					<Select.Value placeholder="User to transfer to." />
				</Select.Trigger>
				<Select.Content>
					{#each users as user}
						<Select.Item value={user} label={user.name} />
					{/each}
				</Select.Content>
			</Select.Root>
			<input hidden bind:value={$formData.recipient} name={attrs.name} />
		</Form.Control>
		<Form.FieldErrors />
		{#if selectedRecipientCreditRating}
			<div class="my-4">
				<span>Credit Rating:</span>
				<strong
					class="
				{cn(
						selectedRecipientCreditRating > 750 && 'text-green-700',
						selectedRecipientCreditRating < 750 &&
							selectedRecipientCreditRating > 500 &&
							'text-yellow-400',
						selectedRecipientCreditRating < 500 && 'text-red-400'
					)}
			"
				>
					{selectedRecipientCreditRating}
				</strong>
			</div>
		{/if}
	</Form.Field>
	<Form.Field {form} name="amount">
		<Form.Control let:attrs>
			<Form.Label>Amount</Form.Label>
			<Input {...attrs} bind:value={$formData.amount} />
		</Form.Control>
		<Form.Description>Amount to transfer to user.</Form.Description>
		<Form.FieldErrors />
	</Form.Field>
	<input hidden bind:value={$formData.bankId} name={'bankId'} />
	{#if selectedRecipientCreditRating < 750}
		<div class="flex items-center space-x-2">
			<Checkbox id="terms" bind:checked={confirmSubmit} aria-labelledby="terms-label" />
			<Label
				id="terms-label"
				for="terms"
				class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
			>
				Confirm transfer
			</Label>
		</div>
	{/if}
	{#if selectedRecipientCreditRating < 750}
		<div class="my-4">
			<strong
				>{selectedRecipientCreditRating < 500
					? 'Recipient is highly suspicious, you might lose your money from this tranasction.'
					: 'Recipient is suspicious, transfer at your own risk.'}
			</strong>
		</div>
	{/if}

	<div class="flex gap-2">
		<Button href="/bank/{$page.params.slug}/home" variant={'outline'}>Back</Button>
		<Form.Button disabled={!canSubmit}>Transfer</Form.Button>
	</div>
</form>
