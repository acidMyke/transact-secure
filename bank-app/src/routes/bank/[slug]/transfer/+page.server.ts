import type { PageServerLoad, Actions } from './$types.js';
import { fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { formSchema } from './schema.js';
import { zod } from 'sveltekit-superforms/adapters';
import { User, pb, type Transaction } from '$lib/pb';

export const load: PageServerLoad = async () => {
	return {
		form: await superValidate(zod(formSchema))
	};
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			console.log(form);
			return fail(400, {
				form
			});
		}

		const { amount, sender, recipient, bankId } = form.data;

		//TODO: Use ml to get chanceIsFraud
		const collection = await pb.collection<Transaction>('transactions').create({
			amount: Number(amount),
			sender,
			recipient,
			chanceIsFraud: 0,
			bankId
		});

		return redirect(300, `/bank/${form.data.bankId}/home`);
	}
};
