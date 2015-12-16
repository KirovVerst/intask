from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from events.models import *
from invitations.models import *
from users.models import CustomUser
import random, json, datetime


def random_date(start, end):
    start_year = int(start[:4])
    start_month = int(start[5:7])
    start_day = int(start[8:10])
    end_year = int(end[:4])
    end_month = int(end[5:7])
    end_day = int(end[8:10])
    d1 = datetime.date(start_year, start_month, start_day)
    d2 = datetime.date(end_year, end_month, end_day)
    delta = d2 - d1
    delta_days = random.randint(0, delta.days - 1)
    result = d1 + datetime.timedelta(days=delta_days)
    return result.__str__()


def load_test_data(output):
    # Users creation

    iam = {'email': "kirov.verst@gmail.com", 'username': "kirov.verst@gmail.com", 'first_name': "Азат",
           'last_name': "Абубакиров"}
    user = User.objects.create(**iam)
    user.set_password("password")
    user.save()
    Token.objects.create(user=user)
    CustomUser.objects.create(user=user)
    users = [user, ]

    with open('/Users/Kirov/Projects/intask/events/management/commands/users.json') as data_file:
        json_data = json.load(data_file)
        for user_data in json_data:
            user_data['username'] = user_data['email']
            user = User.objects.create(**user_data)
            user.set_password("password")
            user.save()
            Token.objects.create(user=user)
            CustomUser.objects.create(user=user)
            users.append(user)

    output.write('Successfully create users')

    # Events creation
    events = []
    with open('/Users/Kirov/Projects/intask/events/management/commands/events.json') as data_file:
        json_data = json.load(data_file)
        for event_data in json_data:
            event_header_index = random.randint(0, len(users) - 1)
            event_header = users[event_header_index]
            event_data['event_header'] = event_header
            event = Event.objects.create(**event_data)
            event.users.add(event_header)
            events.append(event)

            maybe_participants = users[:]
            maybe_participants.pop(event_header_index)
            participant_count = random.randint(0, len(maybe_participants) - 2)
            maybe_participant_count = participant_count
            while maybe_participant_count > 0:
                maybe_participant_count -= 1
                participant = random.choice(maybe_participants)
                maybe_participants.remove(participant)
                event.users.add(participant)

    output.write('Successfully create events')

    tasks = []

    with open('/Users/Kirov/Projects/intask/events/management/commands/tasks.json') as data_file:
        json_data = json.load(data_file)
        for task_data in json_data:
            event = events[random.randint(0, len(events) - 1)]
            users = event.users.all()
            task_header_index = random.randint(0, len(users) - 1)
            task_header = users[task_header_index]
            start = str(datetime.date.today())
            end = event.finish_time
            task_data['finish_time'] = random_date(start, end)
            task_data['task_header'] = task_header
            task_data['event'] = event
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

    with open('/Users/Kirov/Projects/intask/events/management/commands/subtasks.json') as data_file:
        json_data = json.load(data_file)
        for sub_data in json_data:
            task = tasks[random.randint(0, len(events) - 1)]
            sub_data['task'] = task
            sub = Subtask.objects.create(**sub_data)

    output.write('Successfully create subtasks')

    for event in events:
        diff = []
        all_users = User.objects.all()
        event_users = event.users.all()
        for user in all_users:
            found = False
            for event_user in event_users:
                if user == event_user:
                    found = True
                    break
            if not found:
                diff.append(user)

        count = random.randint(0, len(diff) - 1)
        start = random.randint(0, len(diff) - count)
        participants = diff[start:count]
        for participant in participants:
            event.add_email_to_list(participant.email)
            data = {
                'event': event,
                'sender': event.event_header,
                'recipient': participant.email
            }
            Invitation.objects.create(**data)

    output.write('Successfully create invitations')
