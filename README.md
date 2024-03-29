# Task Scheduler - Backend

Can put in personal tasks and view\n
and automatically send your progress to others by email!

## Set up

### Set up virtual environment
Navigate to project root directory, then open docker

#### In .env file

##### set up your email and app_password
##### FDM wifi disables email sending funcationality, please use other wifi to try email


#### In terminal
```cmd
docker compose build
```
then

```cmd
docker compose up
```


Use port 5000 to access the backend



# End points

## post task
#### endpoint: "/texttask", 
#### method: "POST"
#### request format (task name need to be unique, priority can be 1,2 or 3, 3 is highest, 2 is default)
```cmd
{
    "task_name":"new task",
    "priority":3,
    "task_description": "need to finish math homework "
}
```

## view all task, highest priority task will be shown first
#### endpoint: "/texttask/all", 
#### method: "GET"

## update task by task id
#### endpoint: "/texttask/update", 
#### method: "POST"
#### request format (only task_id is required, other fields are optional)
```cmd
{
    "task_id":1,
    "task_descrition": "updated description",
    "priority":1,
    "finished":1
}
```

## delete task by id
#### endpoint: "/texttask", 
#### method: "DELETE"
#### request format
```cmd
{
    "task_id":1
}
```


## send others your unfinished tasks by email periodically, data updates in real time
#### endpoint: "/emailReporter", 
#### method: "POST"
#### request format (task_name is unique, cron_exp see cron expression "* * * * *" means every minute, email receiver is defined by "receiver")
```cmd
{
   {
    "content": {"email_body": "The report is in the attachment", "title": "Unfinished Tasks Report",
    "receiver": "imtonytian@gmail.com",
    "sql_file": "select_unfinished_text_tasks",
    "csv_file": "report1"},
    "cron_exp" :"* * * * *",
    "task_name" : "task1"
}
```
