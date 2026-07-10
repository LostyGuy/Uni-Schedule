import pytest


#!----Tests----

#----Schedules----
# def test_create_schedule(db_session):
#     toms_user_id = db_session.query(
#             models.user.id_user,
#         ).filter(
#             models.user.username == "tom",
#         ).limit(1).first()
    
#     new_schedule: dict[str | int] = {
#         'title' : "Test Schedule",
#         'description' : "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source.",
#         'creator' : toms_user_id[0],
#     }

#     result = create_schedule(
#         title = new_schedule.get('title'),
#         description = new_schedule.get('description'),
#         creator = new_schedule.get('creator'),
#         db_session = db_session,
#     )

#     created_schedule = db_session.query(
#         models.schedule.name,
#         models.schedule.created_by,
#         models.schedule.status,
#     ).filter(
#         models.schedule.created_by == new_schedule.get('creator'),
#     ).order_by(
#         desc(models.schedule.scheduleId)
#     ).first()

#     assert result is True
#     assert created_schedule[0] == new_schedule.get('title')
#     assert created_schedule[1] == new_schedule.get('creator')

@pytest.mark.skip
def test_alter_schedule():
    raise NotImplementedError

@pytest.mark.skip
def test_delete_schedule():
    raise NotImplementedError
