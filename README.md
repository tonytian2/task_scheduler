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
#### request format (task name need to be unique)
```cmd
{
    "task_name":"new task",
    "task_description": "need to finish math homework "
}
```

## view all task, highest priority task will be shown first
#### endpoint: "/texttask/all", 
#### method: "GET"

## post task
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
