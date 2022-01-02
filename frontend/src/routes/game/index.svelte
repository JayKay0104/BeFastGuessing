<script>
	import { selectedCategory, playlists, selectedPlaylist, currentRound } from '../../stores.js';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
    import { page } from '$app/stores'
    import Track from '../../components/Track.svelte';
     

	// Init
    let tracks;
	let playlist = { id : $page.query.get('p')};
    let shuffled_tracks;
    var current_round;
    var correctTrackNumber;
    var correctTrack;

    async function getPlaylists(playlist) {
		const tracksEndpoint = 'http://localhost:8000/playlists/' + playlist.id + '/tracks';
		console.log(tracksEndpoint);
		await fetch(tracksEndpoint)
			.then((r) => r.json())
			.then((data) => {
                startTheGame(tracks = data);

			});
            console.log(tracks);
	}

    getPlaylists(playlist);

    // Helper function
    function shuffle(array) {
        let currentIndex = array.length,  randomIndex;

        while (currentIndex != 0) {

            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;

            [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
        }

        return array;
    }

    function routeToPage(route, replaceState) {
		goto(`/${route}`, { replaceState });
	}

    async function sendStart(correctTrackNumber){
        fetch( 'http://localhost:8000/start/'+correctTrackNumber)
        .then( response => response.json() )
        .then( response => {
            console.log(response);
        } );
    }

    // Game logic

    function startTheGame(tracks){
        shuffled_tracks = shuffle(tracks).slice(0,4);
        correctTrackNumber = Math.floor(Math.random() * 4);
        correctTrack = shuffled_tracks[correctTrackNumber];
        sendStart(correctTrack);
        current_round++;
        currentRound.set(current_round);
    }
 


</script>

<main>
	{#if shuffled_tracks === undefined}
		<p>Error</p>
    {:else if shuffled_tracks}
    {#each shuffled_tracks as track}
        <div>
            <Track {track} />
        </div>
    {/each}
    <audio controls="controls" autoplay style="display:none" on:ended={() => routeToPage('selection', false)}>
        <source src="{correctTrack.preview_url}" type="audio/mpeg"/>
      </audio>
{:else}
    <p>loading...</p>
{/if}
</main>