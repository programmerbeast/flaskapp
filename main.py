from to_wav import process_input
from wav_to_whisper import wav_to_whisper, prepare_whisper_for_gpt, whisper_to_gpt

#history=""
#prompt=""
#file_path=""
#output_path="output_directory"
def driver(file_path,output_path):
    
    wav_file=process_input(file_path,output_path)
    print("wav_file", wav_file)
    result_whisper=wav_to_whisper("base",wav_file)
    result_whisper="The format is START_TIME-END_TIME|||TEXT" + ";".join(prepare_whisper_for_gpt(result_whisper))
    #whisper_to_gpt(result_whisper, history, prompt)
    return result_whisper

def talk_to_GPT(result, history, prompt):
    (answer,history)=whisper_to_gpt(result, history, prompt)
    return (answer,history)



def main():
    global history

    result=driver(file_path,output_path)
    while(True):
        prompt=input("What is the prompt?")
        (answer,history)=talk_to_GPT(result,history,prompt)
        print(answer)

#main()

