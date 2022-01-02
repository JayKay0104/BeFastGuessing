<script>
	import { goto } from '$app/navigation';

	function routeToPage(route, replaceState) {
		goto(`/${route}`, { replaceState });
	}

</script>

<h1>Welcome to BeFastGuessing</h1>
<main>
	<button on:click={() => routeToPage('login', false)}>Login</button>

	<button on:click={() => routeToPage('selection', false)}>Select categories</button>

</main>
