from openai import OpenAI

def get_url(base_url, class_number, usage, image_number):
    classes = {
    1 :"Shallow%20Squat/",
    2 :"Knee%20Valgus/",
    3 :"Wrong%20Spinal%20Alignment/",
    4 :"Right%20Form/",
    }
    url = base_url + classes[class_number]+usage+"%20set/"+str(image_number)+".jpg"
    return url

def append_text(content_list, text):
    test_dic = {"type": "text", "text": text}
    content_list.append(test_dic)
    
def append_image(content_list, url):
    image_dic = {"type": "image_url", "image_url": {"url": url}}
    content_list.append(image_dic)
    
client = OpenAI()
    
url_head = "https://raw.githubusercontent.com/ZANDHIFORCE/AITrainer/refs/heads/main/squat_img/"


classes_name={
    1 :"Shallow Squat",
    2 :"Knee Valgus",
    3 :"Wrong Spinal Alignment",
    4 :"Right Form",
}

#Training model
training_content=[]
append_text(training_content,"너한테 4개의 클래스를 학습시킬거야 클래스별 training set은 5장씩 줄거야.")
append_text(training_content,"1. Shallow Squat, 2. Knee Valgus, 3. Wrong Spinal Alignment, 4.Right Form")
for class_number in range(1,5):
    append_text(training_content, classes_name[class_number] + "클래스 training set 5장을 알려줄께")
    for image_number in range(1,6):
        append_image(training_content, get_url(url_head, class_number, "training", image_number))
append_text(training_content, "학습이 완료되었으니, 사진 10장에 하나씩 어느 클래스에 해당하는지 알려줘")
append_text(training_content, "ex) 5. **Right Form**")

response_list=[]

#test model
for class_number in range(1,5):
    test_content=[]
    for image_number in range(1,11):
        append_image(test_content, get_url(url_head, class_number, "test", image_number))
    #call
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", 
            "content": "사용자가 원하는 답변을 제공하도록 하십시오."
        },
        {
            "role": "user",
            "content": training_content
        },
        {
            "role": "user",
            "content": test_content
        },
    ],
    max_tokens=1000,
    )
    response_list.append(response.choices[0].message.content)

for x in response_list:
    print(x)
    print("#######################################")
