import asyncio


async def main():
    await asyncio.create_subprocess_shell("python manage.py makemigrations")
    await asyncio.sleep(1)
    await asyncio.create_subprocess_shell("python manage.py migrate")
    await asyncio.sleep(1)
    await asyncio.create_subprocess_shell("python manage.py runserver")    
    await asyncio.sleep(1)
    await asyncio.create_subprocess_shell("mqttasgi -H localhost -p 1883 config.asgi:application")  
    await asyncio.sleep(1)
    await asyncio.create_subprocess_shell("python manage.py subscribe_all")  
    await asyncio.sleep(1)  
    await asyncio.create_subprocess_shell("celery -A config worker -l info")    
    await asyncio.sleep(1)  
    await asyncio.create_subprocess_shell("celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler") 
    await asyncio.sleep(1)
    await asyncio.create_subprocess_shell('celery -A config flower')   

if __name__ == "__main__":
    asyncio.run(main())