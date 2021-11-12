# importing the random module
import random
from .models import CreateUserCode, JoinTable
from datetime import date, timedelta


def gen_user_code():
    """
    Generates a number between 6-10 as the number of digits in the code
    Then a loop generates a random number for very digit in the code
    The generated number is then saved in database
    :return:
    """
    digits = random.randint(6, 10)
    cu = ""
    for x in range(0, digits):
        cu = cu + str(random.randint(0, 9))
    print(cu)
    try:
        cu_id = CreateUserCode.objects.get(id=1)
    except:
        cu_id = CreateUserCode.objects.create(id=1)
    cu_id.code = cu
    cu_id.save()
    pass


def clean_access():
    """
    Cleans facility access
    Removes all JoinTable that have expired
    :return:
    """
    today = date.today() - timedelta(days=1)
    yesterday = today.strftime("%Y-%m-%d")
    JoinTable.objects.all().filter(timer=yesterday).delete()
    pass
