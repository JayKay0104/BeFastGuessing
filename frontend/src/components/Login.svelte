<script>
	import { spotifyUser } from '../stores.js';
	import { onMount } from 'svelte';

	onMount(async () => {
		await fetch(`http://localhost:8000/login/`)
			.then((r) => r.json())
			.then((data) => {
				spotifyUser.set(data);
			});
	});

	let user;

	spotifyUser.subscribe((value) => {
		user = value;
	});
</script>

{#if user}
	<p>Logged in as {user.display_name}</p>
{/if}
