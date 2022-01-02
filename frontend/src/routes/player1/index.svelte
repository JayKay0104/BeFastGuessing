<script>

import { goto } from '$app/navigation';

let param;
let options;

function routeToPage(route, replaceState) {
		goto(`/${route}`, { replaceState });
	}

function sendGuess(songNr){
    param = { song: songNr};
    options = {
    method: 'POST',
    body: JSON.stringify( param )  
    };

    fetch( 'http://localhost:8000/result/', options )
    .then( response => response.json() )
    .then( response => {
        console.log(response);
    } );
    routeToPage('selection', false);
}

</script>
<h1>Player1</h1>
<main>
	<button on:click={sendGuess("1")}>Song 1</button>
    <button on:click={sendGuess("2")}>Song 2</button>
    <button on:click={sendGuess("3")}>Song 3</button>
    <button on:click={sendGuess("4")}>Song 4</button>


</main>