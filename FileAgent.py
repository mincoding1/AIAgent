#########################
# 완성된 코드가 아닙니다. DEMO 용으로 만들었고
# 폴더 생성만 테스트 해보시면 됩니다. made by inho.choi
###########################

import os
import stat
from openai import OpenAI
import shutil  # 폴더와 내부 파일 삭제를 위해 필요

# OpenAI API 키 설정
api_key = "soj-nrZXhElnq9dHQWfidCWzd-rU4RpRhew_uwv81TSND7YRUenbOcZvGihBpNeYlVXvlkFXB8PjMxT3BlbkFJMoO_xfy2itBWJR6gcFjlcZvVmbpswN5NOic3Bk0pwLAzOAqBht-xwHUYLNbrhBqOTDM2RzCxQA"
client = OpenAI(api_key=api_key)


# 작업 함수들
def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    return f"폴더 '{folder_name}'이(가) 생성되었습니다."

#폴더와 파일 열기
def open_file(param):
    folder_path = param
    if not os.path.exists(folder_path):
        return f"폴더 '{folder_path}'이(가) 존재하지 않습니다."
    os.startfile(folder_path)
    return f"폴더 '{folder_path} 폴더를 열었습니다."

def delete_folder(folder_name):
    if os.path.exists(folder_name):
        # 폴더가 비어 있는지 확인
        if os.listdir(folder_name):  # 폴더에 내용물이 있다면
            shutil.rmtree(folder_name)  # 폴더와 내부 파일까지 모두 삭제
            return f"폴더 '{folder_name}'이(가) 포함된 모든 내용과 함께 삭제되었습니다."
        else:
            os.rmdir(folder_name)  # 폴더가 비어 있다면 삭제
            return f"폴더 '{folder_name}'이(가) 삭제되었습니다."
    return f"폴더 '{folder_name}'이(가) 존재하지 않습니다."


def create_txt_file(file_path, content=""):
    folder_name = os.path.dirname(file_path)
    if folder_name:
        os.makedirs(folder_name, exist_ok=True)  # 필요한 경우 폴더 생성

    # 사용자로부터 파일 내용 입력 받기
    content = ""

    # 파일 생성
    with open(file_path, "w", encoding="utf-8") as file:  # UTF-8 인코딩 추가
        file.write(content)

    # 파일 권한 설정 (읽기 및 쓰기 권한 추가)
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    return f"파일 '{file_path}'이(가) 생성되었습니다. 내용: {content}"


def open_txt_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:  # UTF-8 인코딩 추가
            return f"파일 내용:\n{file.read()}"
    return f"파일 '{file_name}'이(가) 존재하지 않습니다."


def delete_txt_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        return f"파일 '{file_name}'이(가) 삭제되었습니다."
    return f"파일 '{file_name}'이(가) 존재하지 않습니다."


# OpenAI API 기반 작업 처리
def process_command(command):
    system_message_base = f"""
        만약 대화에서 폴더를 생성 해 달라는 의도라고 생각한다면 다른 아무 말 없이 "CREATE_FOLDER:폴더이름" 형태로 말을 해
        예를들면 test 폴더를 생성한다는 의도로 파악된다면 "CREATE_FOLDER:test" 라고 말을 하면 돼
        
        그렇지 않고 만약 폴더를 삭제해달라는 의도라고 생각한다면 "DELETE_FOLDER:폴더이름" 이라고 말해
        예를들면 test 폴더를 삭제한다는 의도로 파악된다면 "DELETE_FOLDER:test" 라고 말을 하면 돼

        그렇지 않고 만약 폴더를 열어달라는 의도라고 생각한다면 "OPEN_FOLDER:폴더이름" 이라고 말해
        예를들면 test 폴더를 삭제한다는 의도로 파악된다면 "OPEN:test" 라고 말을 하면 돼

        그렇지 않고 만약 Text 파일을 어떤 내용으로 생성해달라는 의도라고 생각한다면 "CREATE_FILE:파일이름#파일내용" 이라고 말해
        예를들면 abc 파일을 생성하는데 'SHOW ME ME'라는 내용을 적어달라는 의도로 파악된다면 "CREATE_FILE:abc#SHOW ME ME" 라고 말을 하면 돼

        그렇지 않고 만약 Text 파일을 생성해달라는 의도라고 생각한다면 "CREATE_FILE:파일이름" 이라고 말해
        예를들면 abc 파일을 생성한다는 의도로 파악된다면 "CREATE_FILE:abc" 라고 말을 하면 돼
                
        그렇지 않고 만약 Text 파일을 삭제한다는 의도라고 생각한다면 "DELETE_FILE:파일이름" 이라고 말해
        예를들면 abc 파일을 삭제한다는 의도로 파악된다면 "DELETE_FILE:abc" 라고 말을 하면 돼

        그렇지 않고 만약 Text 파일을 열어달라는 의도라고 생각한다면 "OPEN_FILE:파일이름" 이라고 말해
        예를들면 abc 파일을 열어달라는 의도로 파악된다면 "OPEN_FILE:abc" 라고 말을 하면 돼

        그렇지 않고만약 어떤 폴더 안에 파일 생성하고 어떤 내용을 적어달라는 의도라고 생각한다면 "CREATE_FILE:폴더경로/파일이름#파일내용" 이라고 말해
        예를들면 test 폴더 안에 abc 파일을 생성하는데 'SHOW ME ME'라는 내용을 적어달라는 의도로 파악된다면 "CREATE_FILE:test/abc#SHOW ME ME" 라고 말을 하면 돼

        그렇지 않고 만약 어떤 폴더 안에 파일 생성해달라는 의도라고 생각한다면 "CREATE_FILE:폴더경로/파일이름" 이라고 말해
        예를들면 test 폴더 안에 abc 파일을 생성해달라는 의도로 파악된다면 "CREATE_FILE:test/abc" 라고 말을 하면 돼

        그렇지 않고 만약 어떤 폴더 안에 파일 열어달라는 의도라고 생각한다면 "OPEN_FILE:폴더경로/파일이름" 이라고 말해
        예를들면 test 폴더 안에 abc 파일을 열어달라는 의도로 파악된다면 "OPEN_FILE:test/abc" 라고 말을 하면 돼

        그렇지 않다면 평상시 처럼 친절하게 말해줘
        
        ========
        {command}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_message_base
            },
        ],
        max_tokens=150
    )
    return response.choices[0].message.content


# 메인 로직
def main():
    print("=== 파일 제어가 가능한 AI Agent ===")

    while True:
        user_input = input("SHELL : ")
        if user_input.lower() in ["종료", "quit"]:
            break

        # 명령 처리
        parsed_command = process_command(user_input)

        # 작업 실행
        if parsed_command.startswith(("CREATE_FOLDER", "DELETE_FOLDER", "OPEN_FOLDER", "CREATE_FILE", "OPEN_FILE", "DELETE_FILE")):
            try:
                # 분석된 명령에서 액션과 매개변수 추출
                parts = parsed_command.split(":")
                if len(parts) != 2:
                    print(f'ERROR!! : parsed_command = {parsed_command}')
                    raise ValueError("잘못된 포맷의 답변")

                action = parts[0]
                args = parts[1]

                if action == "CREATE_FOLDER":
                    result = create_folder(args)
                elif action == "DELETE_FOLDER":
                    result = delete_folder(args)
                elif action == "OPEN_FOLDER":
                    result = open_file(args)
                elif action == "CREATE_FILE":
                    result = create_txt_file(args)
                elif action == "OPEN_FILE":
                    result = open_file(args)
                elif action == "DELETE_FILE":
                    result = delete_txt_file(args)
                else:
                    print(f"{parsed_command}")

                print(result)
            except Exception as e:
                print(f"오류 발생: {e}")
        else:
            # 명령어가 아닌 일반 대화 처리
            print(f"{parsed_command}")


if __name__ == "__main__":
    main()
