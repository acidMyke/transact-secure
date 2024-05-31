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

	export let data: SuperValidated<Infer<FormSchema>>;

	const form = superForm(data, {
		validators: zodClient(formSchema)
	});

	const { form: formData, enhance, submit } = form;

	$formData.sender = $currentUser!.id;

	let users: User[] = [];

	const loadUsers = async () => {
		pb.collection<User>('users')
			.getFullList({ filter: `id!='${$currentUser!.id}'` })
			.then((res) => {
				users = res;
			});
	};

	const handleSubmit = (e: Event) => {
		e.preventDefault();

		pb.collection<User>('users')
			.getOne($formData.recipient)
			.then((user) => {
				//TODO: How to stop form from submitting
				if (user.creditRating < 750 && user.creditRating > 500) {
					console.log('Warning');
					return;
				} else if (user.creditRating < 500) {
					console.log('cannot transfer');
					return;
				} else {
					submit();
				}
			});
	};

	onMount(async () => {
		loadUsers();
	});

	$: {
		$formData.bankId = $page.params.slug;
	}

	$: selectedRecipient = $formData.recipient
		? {
				label: $formData.recipient,
				value: $formData.recipient
			}
		: undefined;
</script>

<form method="POST" use:enhance on:submit={handleSubmit}>
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
				selected={selectedRecipient}
				onSelectedChange={(v) => {
					v && ($formData.recipient = v.value);
				}}
			>
				<Select.Trigger class="w-[180px]">
					<Select.Value placeholder="User to transfer to." />
				</Select.Trigger>
				<Select.Content>
					{#each users as user}
						<Select.Item value={user.id} label={user.name} />
					{/each}
				</Select.Content>
			</Select.Root>
			<input hidden bind:value={$formData.recipient} name={attrs.name} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="amount">
		<Form.Control let:attrs>
			<Form.Label>Amount</Form.Label>
			<Input {...attrs} bind:value={$formData.amount} />
		</Form.Control>
		<Form.Description>Amount to transfer to user.</Form.Description>
		<Form.FieldErrors />
	</Form.Field> <input hidden bind:value={$formData.bankId} name={'bankId'} />
	<Form.Button>Transfer</Form.Button>
</form>
