<script>
	import { selectedCategory, playlists, selectedPlaylist } from '../../stores.js';
	import { onMount, onDestroy } from 'svelte';
	import Category from '../../components/Category.svelte';
	import Playlist from '../../components/Playlist.svelte';

	let categories;

	onMount(async () => {
		await fetch(`http://localhost:8000/categories/`)
			.then((r) => r.json())
			.then((data) => {
				categories = data;
			});
	});

	let playlists_value;

	const unsubscribe_playlist = playlists.subscribe((value) => (playlists_value = value));

	onDestroy(unsubscribe_playlist);

	async function getPlaylists(category) {
		selectedCategory.set(category);
		const playlistEndpoint = 'http://localhost:8000/playlists/' + category.id;
		console.log(playlistEndpoint);
		await fetch(playlistEndpoint)
			.then((r) => r.json())
			.then((data) => {
				playlists.set(data);
			});
	}

	$: console.log($selectedCategory);
	$: console.log($selectedPlaylist);
</script>

{#if categories && playlists_value === undefined}
	<h1>Select the Categories</h1>
{:else}
	<h1>Select the Playlist</h1>
{/if}
<main>
	{#if categories && playlists_value === undefined}
		{#each categories as category}
			<div on:click={() => getPlaylists(category)}>
				<Category {category} />
			</div>
		{/each}
	{:else if playlists_value}
		{#each playlists_value as playlist}
			<div on:click={() => selectedPlaylist.set(playlist)}>
				<Playlist {playlist} />
			</div>
		{/each}
	{:else}
		<p>loading...</p>
	{/if}
</main>
