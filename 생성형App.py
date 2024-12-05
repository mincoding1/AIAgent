######################
#40, 57번 라인에서 test.py 를 현재 파일명으로 바꿔서 사용하세요
#전역변수로 쓰시면 됩니다.
#####################

from openai import OpenAI
import os
import sys

def get_response(content, sentense):
    #########################################
    #api_key 입력해줘야 함 (made by inho.choi)#
    #########################################
    api_key = "sk-proj-BlwtVjdLzhG649uK3MpIUpB8lTG0OCUXWgp2ipcDygfwYLMVDvlFl2E8osRckxX0H2QFxIIkLT3BlbkFJIxAAmNw-KMZdiSzyKp8J8k0ofzQYjA1MDj2m9-G74h4PJR1FCF7RsSSa2FLceTl3bCNfEInMcA"

    bot = OpenAI(api_key=api_key)
    response = bot.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": content},
            {"role":"user", "content" : sentense}
        ],
        #max_tokens 1~16383
        max_tokens=16383,
        #temperature 0 ~ 2
        temperature=1,
        #top_p 0 ~ 1
        top_p=1.0,
        #frequency_penalty 0 ~ 2
        frequency_penalty=0,
        #presence_penalty 0 ~ 2
        presence_penalty=0
    )

    return response.choices[0].message.content

def say(sentense) :
    content = "기존 소스코드는 다음과 같다.\n"
    content += "=============================================================\n"

    with open("test.py", "r", encoding="utf-8") as file:
        content += file.read()

    content += "=============================================================\n"
    content += "이 소스코드에서 다음과 같은 기능을 추가해줘"
    content += sentense

    content += "아무런 설명이 없이 소스코드만으로 답변해줘,"
    content += "제공되는 소스코드 기능들을 모두 유지한채로 기능을 추가하고, 추가된 기능을 사용해 볼 수 있도록 해줘"

    ret = get_response(content, sentense)

    removeTarget1 = '`' + '`' + '`' + 'python'
    removeTarget2 = '`' + '`' + '`'
    ret = ret.replace(removeTarget1, "");
    ret = ret.replace(removeTarget2, "");

    with open("test.py", "w", encoding="utf-8") as file:
        file.write(ret)

    python = sys.executable
    os.execl(python, python, * sys.argv)

def command():
    sentense = input("프롬프트 입력 : >> ")
    say(sentense)

if __name__ == "__main__":
    sentense = input("명령 입력 : >> ")
    if sentense == "cmd":
        command()
    #else...
