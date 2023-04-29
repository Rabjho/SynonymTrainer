<svelte:head>
    <style lang="scss">@import "../styles/app.scss";</style>
    <title>SynonymTrainer</title>
</svelte:head>
<svelte:window on:keydown={handleKeyDown}/>

<script>
    import { onMount } from "svelte";
    import randomWords from "random-words"
    import { guesses } from "./stores.js"
    
    let word = "";
    let synonyms = [];
    let score = 0;

    async function setWord(newWord="error") {
        word = newWord;
        let newWordInput = document.getElementById("newWordInput");
        if (newWordInput.value != "") {
            word = newWordInput.value;
            newWordInput.value = "";
        }
        synonyms = await getSynonyms(word)
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
        console.log(response);
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
        return words
    }
    
    function guessSynonym(event) {
        let guess = event.target.value;
        let correct = synonyms.includes(guess.toLowerCase());
        $guesses = [{"guess":guess, "correct":correct}, ...$guesses];
        score += +correct
        event.target.value = "";
        console.log($guesses);
    }
// {"guess":guess, "correct":synonyms.includes(guess.toLowerCase())}
    function handleKeyDown(event) {
        let key = event.key;
        if (key == "Enter") {
            if (event.target.id == "wordsInput"){
                guessSynonym(event)
            }
        }
    }
    onMount( () => setWord(randomWords(1)[0]))
    
</script>

{#if word != undefined}
<div class="synonym">{ word.toLowerCase() }</div>
{/if}

<div>Score: { score }</div>

<input id="wordsInput" class="" placeholder="Synonym" tabindex="0" autocomplete="off" autocapitalize="off" autocorrect="off" data-gramm="false" data-gramm_editor="false" data-enable-grammarly="false" list="autocompleteOff">

{#each $guesses as guesses, i}
    {#if guesses.correct}
        <div style="color:lime">
            { guesses.guess }
        </div>
    {:else}
        <div style="color:red">
            { guesses.guess }
        </div>  
    {/if}
{/each}

<div class="newWordGroup">
    <input placeholder="New word?" id="newWordInput">
    <button on:click={ () => setWord()}></button>
</div>

