import whisper
import openai
import tiktoken
openai.api_key = "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"



def wav_to_whisper(model, url):
    model = whisper.load_model(model)
    audio = whisper.load_audio(url)
    result = model.transcribe(audio)
    return result

def prepare_whisper_for_gpt(whisper_obj):
    return [str(segment["start"]) + "-" + str(segment["end"]) + "|" + str(segment["text"]) for segment in whisper_obj["segments"]]


def whisper_to_gpt(whisper_obj, history,prompt):
        # Make an API call
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=truncate_prompt("Question:" + prompt + " This is the text where the question is asked for;" + whisper_obj +";This is the history of your answers in the conversation;"+history+"End of history;", 3900),
    max_tokens=90
    )

    # Access the generated text
    generated_text = response.choices[0].text
    history+="." + generated_text
    return (generated_text,history)


def truncate_prompt(prompt, max_tokens):
    # Tokenize the prompt
    print("gerndsugbzuibg")
    encoding = tiktoken.encoding_for_model("text-davinci-003")
    #tokenized_prompt = tiktoken.tokenize([prompt])
    tokenized_prompt=encoding.encode(prompt)


    # Check if the token count exceeds the limit
    if len(tokenized_prompt) > max_tokens:
        # Calculate the excess tokens
        excess_tokens = len(tokenized_prompt) - max_tokens-100

        # Remove the excess tokens from the prompt
        truncated_prompt = encoding.decode(tokenized_prompt[:-excess_tokens])
        return truncated_prompt

    return prompt
