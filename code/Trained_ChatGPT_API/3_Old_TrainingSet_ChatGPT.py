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

url_head = "https://raw.githubusercontent.com/ZANDHIFORCE/AITrainer/refs/heads/main/old_squat_img/"


classes_name={
    1 :"Shallow Squat",
    2 :"Knee Valgus",
    3 :"Wrong Spinal Alignment",
    4 :"Right Form",
}

#Training model
training_content=[]
append_text(training_content,"I will train you on four classes, and for each class, I will provide a training set of 5 images.")
append_text(training_content,"1. Shallow Squat, 2. Knee Valgus, 3. Wrong Spinal Alignment, 4.Right Form")
for class_number in range(1,5):
    append_text(training_content, "I'll provide you with 5 images for the " + classes_name[class_number] + " class training set.")
    for image_number in range(1,6):
        append_image(training_content, get_url(url_head, class_number, "training", image_number))
append_text(training_content, "Provide 10 photos and identify which class each photo belongs to one by one.")
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
            "content": "make sure to provide the answer the user wants."
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
