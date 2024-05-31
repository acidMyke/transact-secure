import PocketBase from 'pocketbase'
import { writable } from 'svelte/store'

if (import.meta.env.VITE_POCKETBASE_URL === undefined) {
  throw new Error('VITE_POCKETBASE_URL must be defined in .env')
}




interface BaseRecord {
  id: string
  created: string
  updated: string
}

export interface User extends BaseRecord{
  email: string
  username: string
  emailVisibility: string
  verified: boolean
  
  name: string
  avatar: string
  flag: "" | "normal" | "suspicious" | "banned"
}

export interface Transaction extends BaseRecord {
  amount: number
  sender: string
  recipient: string
  chanceIsFraud: number
}

export const pb = new PocketBase(import.meta.env.VITE_POCKETBASE_URL);

export const currentUser = writable(pb.authStore.model)

// Listen for changes to the current user
pb.authStore.onChange(auth => {
  console.log('auth changed', auth);
  currentUser.set(pb.authStore.model)
})

export default pb