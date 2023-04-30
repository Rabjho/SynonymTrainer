<script>
    
    export let guess = "";
    export let correct = false;
    $: type = correct ? "correctGuess" : "wrongGuess";
</script>

<style lang="scss">
    @import '../styles/variables';
    .correctGuess {
        color: $right-color;
    }

    .wrongGuess {
        color: $wrong-color;
    }
</style>

<div class={type}>
    { guess }
</div>
