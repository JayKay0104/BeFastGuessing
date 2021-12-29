<script>
	// create a prop
	export let category;
</script>

<article>
	<h1>{category.name}</h1>
	<img
		src={category.icons[0].url}
		alt={category.name}
		width={category.icons[0].width}
		height={category.icons[0].height}
	/>
</article>
