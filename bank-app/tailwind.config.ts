import type { Config } from 'tailwindcss';
import daisyui from 'daisyui';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {}
	},

	plugins: [daisyui],
	daisyui: {
		
		themes: [{
			'default': {
				'primary': '#89b4fa', // blue
				'secondary': '#f5c2e7', // pink
				'accent': '#94e2d5', // teal
				'neutral': '#11111b', // crust
				'base-100': '#1e1e2e', // base
				'info': '#74c7ec', // sapphire
				'success': '#a6e3a1', // green
				'warning': '#f9e2af', // yellow
				'error': '#f38ba8' // red
			}
		}]
	}
} as Config;
