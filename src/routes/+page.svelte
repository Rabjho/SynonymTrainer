<svelte:head>
    <style lang="scss">@import "../styles/app.scss";</style>
    <title>SynonymTrainer</title>
</svelte:head>
<svelte:window on:keydown={handleKeyDown}/>

<script>
    import { onMount } from "svelte";
    import randomWords from "random-words"
    import { guesses } from "./stores.js"
    import Guess from "./Guess.svelte"
	import Infoboard from "./Infoboard.svelte";


    let word = "";
    let synonyms = [];
    let score = 0;

    // $: gameActive = +$guesses != 0;
    let gameActive = false;
    let scoreScreen = false;
    let facit = false;

    async function setWord(newWord="error") {
        word = newWord;
        let newWordInput = document.getElementById("newWordInput");
        if (newWordInput.value != "") {
            word = newWordInput.value;
            newWordInput.value = "";
        }
        synonyms = await getSynonyms(word)
        score = 0;
        scoreScreen = false;
        $guesses = [] 
    }
    
    async function getSynonyms(word){
        let words = [];
        const response = await fetch('/getSynonyms', {
            method:"POST",
            body: JSON.stringify(word),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        if (typeof(response[0]) == typeof("")){
            return setWord(response[Math.floor(Math.random() * response.length)])
        }

        for (let i = 0; i < response.length; i++) {
            words.push(response[i]["meta"]["syns"].flat());
        }
        words = words.flat()
        for (let i = words.length-1; i > 0; i--) {
            if (words[i].includes(" ")) {
                words.splice(i, 1);
            }
        }
        return [...new Set(words)];
    }
    
    function guessSynonym(event) {
        let guess = event.target.value;
        if (guess != "") {
            let correct = synonyms.includes(guess.toLowerCase());
            $guesses = [{"guess":guess, "correct":correct}, ...$guesses];
            score += +correct
            synonyms = synonyms.filter( e => e != guess )
            event.target.value = "";
        }
    }

    function handleKeyDown(event) {
        let key = event.key;
        if (key == "Enter") {
            if (event.target.id == "wordsInput"){
                if (+$guesses == 0) {
                    gameActive = true;
                }
                if (gameActive) {
                    guessSynonym(event)
                }
            }
            else if (event.target.id == "newWordInput") {
                setWord()
            }
        }
    }
    onMount( () => setWord(randomWords(1)[0]))
    
    function handleStart(){

    }


    function handleEnd(event) {
        gameActive = false;
        scoreScreen = true;
    }

</script>


<div class="centerContent">

    {#if word != undefined}
    <div class="synonym">{ word.toLowerCase() }</div>
    {/if}
    
    <Infoboard running={gameActive} on:gameEnd={handleEnd} bind:score={score} scoreScreen={scoreScreen}></Infoboard>
    {#if !scoreScreen}
        <input id="wordsInput" class="primaryInput" placeholder="synonym" tabindex="0" autocomplete="off" autocapitalize="off" autocorrect="off" data-gramm="false" data-gramm_editor="false" data-enable-grammarly="false" list="autocompleteOff">
    {/if}
    {#if gameActive || scoreScreen}
        <div class="wordList">
            {#each $guesses as guesses}
                <Guess {...guesses}></Guess>
            {/each}
        </div>
    {/if}
    {#if !gameActive}
        <input placeholder="change word" id="newWordInput">
        <button on:click={() => setWord(randomWords(1)[0])}>random new word</button>
    {/if}
    {#if scoreScreen}
        <button on:click={() => facit = !facit}>correct words</button>
        {#if facit}
            <div class="wordList">
                {#each synonyms as synonym}
                    <div class="word small">
                        { synonym }
                    </div>
                {/each} 
            </div>
        {/if} 
    {/if}
</div>    

