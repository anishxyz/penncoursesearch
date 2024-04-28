import pandas as pd
import requests

# Read the parquet file
# df = pd.read_parquet('data/courses_embed.parquet')
df = pd.read_csv('backend/data/courses_embed.csv')

# Define a function to get the professor information
def get_professors_info(course_id):
    url = f"https://penncoursereview.com/api/base/current/courses/{course_id.replace(' ', '-')}/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed for {course_id}")
        return None

    course_data = response.json()

    professors_info = []
    added_professors = set()

    for section in course_data['sections']:
        for instructor in section['instructors']:
            instructor_id = instructor['id']
            if instructor_id not in added_professors:
                added_professors.add(instructor_id)
                instructor['name'] = instructor['name'].replace("'"," ")
                professors_info.append({
                    'name': instructor['name'],
                    'course_quality': section['course_quality'],
                    'instructor_quality': section['instructor_quality'],
                    'difficulty': section['difficulty'],
                    'work_required': section['work_required']
                })

    print(f"Success for {course_id}")
    print(professors_info)
    return professors_info


# Add a new column 'professors' to the DataFrame
df['professor_stats'] = df.apply(lambda x: get_professors_info(x["Department Code"]+"-"+str(x["Course Code"])), axis = 1)

# Save the updated DataFrame to a new parquet file
df.to_csv('backend/data/courses_embed_profs.csv')
# df.to_parquet('data/courses_embed.parquet')
