import requests
import json
from bs4 import BeautifulSoup
import numpy as np
DATA_SET={}
# ---------------------------------------------------------------------------------------------
# SCRAPING OBJECT OF QUESTIONS FROM GIT REPO
# ---------------------------------------------------------------------------------------------
# req=requests.get("https://github.com/haoel/leetcode")
# # soup=BeautifulSoup(req.content,"html.parser")
# # with open('output.html', 'w', encoding='utf-8') as file:
# #     file.write(soup.prettify())
# # ----------------------------------------------------------fetching html doc from git repo
# with open('output.html', 'r', encoding='utf-8') as file:
#     html_content = file.read()
# soup = BeautifulSoup(html_content, 'html.parser')
# table_rows = soup.find_all("tr")
# result_list = []
# # ----------------------------------------------------------finding all relevent rows
# # Iterate over each <tr> element
# for row in table_rows:
#     # Extract data from <td> elements
#     columns = row.find_all("td")
#     # Check if the row has the expected number of columns
#     if len(columns) == 4:
#         # Extract data from each <td> and create a dictionary
#         entry = {
#             "id": int(columns[0].get_text(strip=True)),
#             "desc": columns[1].find("a").get_text(strip=True),
#             "url": columns[1].find("a")["href"]
#         }
#         # Append the dictionary to the result list
#         result_list.append(entry)
# # Print the resulting list of dictionaries
# with open('output_result.txt', 'w', encoding='utf-8') as result_file:
#     json.dump(result_list, result_file, indent=2)
# ----------------------------------------------------------writing all result in txt file
# ---------------------------------------------------------------------------------------------
# ITERATING THROUGH EACH OBJECT IN OUTPUT_RESULT FILE AND EXTRATING DATA OBJECT FROM EACH QUESTION
# ---------------------------------------------------------------------------------------------
with open('output_result.txt', 'r', encoding='utf-8') as file:
    data = np.array(json.load(file))
    # print(type(data[0]))
for index,my_dict in enumerate(data):
    try:
        id_value = my_dict["id"]
        desc_value = my_dict["desc"]
        url_value = my_dict["url"]
        req=requests.get(url_value)
        soup=BeautifulSoup(req.content,"html.parser")
        with open('question_html_page.html', 'w', encoding='utf-8') as file1:
            file1.write(soup.prettify())
            # ---------------------------------------------------------------------------------------------
            # EXTRACTING DATA FROM EACH SOURCE
            # ---------------------------------------------------------------------------------------------
        with open('question_html_page.html', 'r', encoding='utf-8') as file2:
            html_content = file2.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'type': 'application/json'})
        script_content = script_tag.string
        with open('dataset_modified.json', 'w', encoding='utf-8') as file3:
            file3.write(script_tag.string)

            # ---------------------------------------------------------------------------------------------
            # EXTRACTING Testcases and description
            # ---------------------------------------------------------------------------------------------
        with open('dataset_modified.json', 'r', encoding='utf-8') as file4:
            json_data = json.load(file4)
        question_id = json_data["props"]["pageProps"]["dehydratedState"]["queries"][3]["state"]["data"]["question"]["questionId"]
        exampleTestcaseList = json_data["props"]["pageProps"]["dehydratedState"]["queries"][3]["state"]["data"]["question"]["exampleTestcaseList"]
        content = json_data["props"]["pageProps"]["dehydratedState"]["queries"][7]["state"]["data"]["question"]["content"]
            # print(question_id,exampleTestcaseList,content)
        question_info={'desc':content,'test_case':exampleTestcaseList}
        DATA_SET[question_id]=question_info
        # with open('question_html_page.html', 'w', encoding='utf-8'):
        #     pass
        # with open('dataset_modified.json', 'w', encoding='utf-8'):
        #     pass
        with open('output_dataset.txt', 'w', encoding='utf-8') as output_file:
            json.dump(DATA_SET, output_file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error on id {index}: {e}")