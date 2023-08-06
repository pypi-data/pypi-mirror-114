CREATE_TABLE_QUERY = '''
create table if not exists tasks 
(
id bigserial not null
    constraint task_pkey
        primary key,
queue_name text not null,
data json,
finished boolean default false,
started_at timestamp default CURRENT_TIMESTAMP
);'''

PUT_TASK_QUERY = '''
insert into tasks (queue_name, data) values ($1, $2)
'''

QUERY_TAKE_TASK = '''
with next_task as (
select id, data from tasks
where queue_name = $1 and 
(started_at IS NULL or started_at < current_timestamp - interval '5 seconds' and finished = false)
limit 1
for update skip locked
)
update tasks
set
    started_at = current_timestamp
from next_task
where tasks.id = next_task.id
returning tasks.id, tasks.data;'''

UPDATE_FINISHED_TASK_QUERY = '''
update tasks set finished = true where id = $1
'''
