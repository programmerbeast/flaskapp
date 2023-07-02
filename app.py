from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from main import driver, talk_to_GPT
import os 

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'your_secret_key'
#file_path="rogan.mp4"
output_path="static/video"
history=""
UPLOAD_FOLDER = output_path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#result=driver(file_path,output_path)


@app.route("/")
def hello_world():
    return render_template("first_page.html")


@app.route('/input_docs', methods=['POST'])
def input_docs():
    global result
    global output_file
    crawl_option = request.form.get('crawlOption')

    if crawl_option == 'audio':
        audio_file = request.files.get('audioFile')
        audio_filename = audio_file.filename
        audio_file.save(os.path.join(app.config['UPLOAD_FOLDER'], audio_filename))
        result = driver(audio_filename, output_path)
        output_file = audio_filename[:-4] + ".wav"
        print(audio_file)
        return redirect("/video")
        # Process audio file
    elif crawl_option == 'video':
        video_file = request.files.get('videoFile')
        video_filename = video_file.filename
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
        result = driver(video_filename,output_path)
        output_file = video_filename[:-4] + ".wav"
        return redirect("/video")
        print(video_file)
        # Process video file
    elif crawl_option == 'youtube':
        youtube_url = request.form.get('youtubeURL')
        result = driver(youtube_url,output_path)
        output_file=youtube_url.rsplit('/', 1)[-1].replace("?", "!") + ".wav"
        print(youtube_url)
        # Process YouTube URL

        return redirect("/video")

    # Process the selected option and corresponding values

    return "there was an error"





@app.route('/video', methods=['GET', 'POST'])
def display_video():
    return render_template("second_page.html", path=output_file)





@app.route("/get_chatbot_response", methods=["POST"])
def chatbot():
    global history
    global result
    user_message = request.form["user_message"]
    print("user_message",user_message)
    #print("result", result)
    (answer,history)=talk_to_GPT(result,history,user_message)
    print("histoire", history)
    print("answer", answer, "answer!!!")
    return jsonify({"response": answer})



if __name__ == '__main__':
    app.run(debug=True)