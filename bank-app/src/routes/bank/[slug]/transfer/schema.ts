import { z } from 'zod';

export const formSchema = z.object({
	amount: z.string().refine((val) => !isNaN(Number(val)) && Number(val) >= 0, {
		message: 'Amount must be a non-negative number'
	}),
	sender: z.string().min(1, { message: 'Sender cannot be empty' }),
	recipient: z.string().min(1, { message: 'Recipient cannot be empty' }),
	bankId: z.string()
});

export type FormSchema = typeof formSchema;
