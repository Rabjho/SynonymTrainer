<script>
    import { onDestroy, createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    export const id="Infoboard"
    export let score = 0;
    export const timerLength = 1;
    export let running = true; 
    export let scoreScreen = false;
    let counter = timerLength;
    const interval = setInterval(countDown, 1000);

    $: minutes = Math.floor(counter / 60)
    $: seconds = counter % 60

    function countDown() {
        if (running) {
            if (counter <= 0) {
                dispatch('gameEnd', {
                    score: score,
                })
                counter = timerLength
                return
            }
            counter--;
        }
    }

    onDestroy(() => clearInterval(interval));


</script>

<style lang="scss">
    @import '../styles/variables';
    .score {
        color: $primary-color;
        
        display: grid;
        font-size: .75rem;
        gap: 1rem;
        grid-auto-flow: column;
        height: max-content;
        justify-content: space-around;
        transition: .125s;
        width: 100%;
        justify-items: center;
        padding: 0.25rem 1rem;        
        width: auto;
        justify-self: center;
        div {
            background-color: $sub-alt-color;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;        
        }
        
    }

    
</style>

<div class="score">
    <!-- {#if minutes == 0}
        <div>{("00"+seconds).slice(-2)}</div>
    {:else}
        <div>{("00"+minutes).slice(-2)}:{("00"+seconds).slice(-2)}</div>
    {/if} -->
    {#if !scoreScreen}
        <div>{("00"+minutes).slice(-2)}:{("00"+seconds).slice(-2)}</div>
        
    {/if}
    <div>
        Score: { score }
    </div>
</div>