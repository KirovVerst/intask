from projects.models import Project
from tasks.models import Task
from subtasks.models import Subtask
import random, json, datetime
from django.contrib.auth.models import User
import os

BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'commands/json/')


def random_date(start, end):
    start_year = int(start[:4])
    start_month = int(start[5:7])
    start_day = int(start[8:10])
    end_year = int(end[:4])
    end_month = int(end[5:7])
    end_day = int(end[8:10])
    d1 = datetime.date(start_year, start_month, start_day)
    d2 = datetime.date(end_year, end_month, end_day)
    delta = abs(d1 - d2)
    delta_days = random.randint(0, delta.days)
    result = d1 + datetime.timedelta(days=delta_days)
    return result.__str__()


def load_test_data(output):
    # Users creation

    iam = {'email': "kirov@gmail.com", 'username': "kirov@gmail.com", 'first_name': "Kirov",
           'last_name': "Verst"}
    user = User.objects.create(**iam)
    user.set_password("password")
    user.save()
    users = []
    path = os.path.join(os.path.join(BASE_DATA_DIR, 'users.json'))
    with open(path) as data_file:
        json_data = json.load(data_file)
        for user_data in json_data:
            user_data['username'] = user_data['email']
            user = User.objects.create(**user_data)
            user.set_password("password")
            user.save()
            users.append(user)

    output.write('Successfully create users')

    # Events creation
    projects = []
    with open(os.path.join(os.path.join(BASE_DATA_DIR, 'projects.json'))) as data_file:
        json_data = json.load(data_file)
        for project_data in json_data:
            project_header_index = random.randint(0, len(users) - 1)
            project_header = users[project_header_index]
            project_data['header'] = project_header
            if 'status' in project_data:
                del project_data['status']
            project = Project.objects.create(**project_data)
            project.users.add(project_header)
            projects.append(project)

            maybe_participants = users[:]
            maybe_participants.pop(project_header_index)
            participant_count = random.randint(0, len(maybe_participants) - 2)
            maybe_participant_count = participant_count
            while maybe_participant_count > 0:
                maybe_participant_count -= 1
                participant = random.choice(maybe_participants)
                maybe_participants.remove(participant)
                project.users.add(participant)

    output.write('Successfully create projects')

    tasks = []

    with open(os.path.join(os.path.join(BASE_DATA_DIR, 'tasks.json'))) as data_file:
        json_data = json.load(data_file)
        for task_data in json_data:
            project = projects[random.randint(0, len(projects) - 1)]
            users = project.users.all()
            task_header_index = random.randint(0, len(users) - 1)
            task_header = users[task_header_index]
            start = str(datetime.date.today())
            end = project.finish_time
            task_data['finish_time'] = random_date(start, end)
            task_data['header'] = task_header
            task_data['project'] = project
            if 'is_public' in task_data:
                del task_data['is_public']
            task = Task.objects.create(**task_data)
            tasks.append(task)
            task.users.add(task_header)

            maybe_participants = users[:]
            maybe_participants.pop(task_header_index)
            if len(maybe_participants) == 0:
                continue

            if len(maybe_participants) == 1:
                task.users.add(maybe_participants[0])
                continue

            participant_count = random.randint(0, len(maybe_participants) - 1)
            maybe_participant_count = participant_count
            while maybe_participant_count > 0:
                maybe_participant_count -= 1
                participant = random.choice(maybe_participants)
                maybe_participants.remove(participant)
                task.users.add(participant)

    output.write('Successfully create tasks')

    with open(os.path.join(os.path.join(BASE_DATA_DIR, 'subtasks.json'))) as data_file:
        json_data = json.load(data_file)
        for sub_data in json_data:
            task = tasks[random.randint(0, len(projects) - 1)]
            sub_data['task'] = task
            sub = Subtask.objects.create(**sub_data)

    output.write('Successfully create subtasks')
