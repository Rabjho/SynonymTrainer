import { json } from '@sveltejs/kit';

import { MWThesaurus } from '$env/static/private';


export async function POST({ request }) {
    const word = await request.json();
    
    const url = "https://dictionaryapi.com/api/v3/references/thesaurus/json/"
    const response = await fetch(url+word+"?key="+MWThesaurus)
    .then(response => response.json())
    return json(response)
}