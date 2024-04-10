from django.db import migrations, models
import uuid

def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('loans', 'Loan')
    for row in MyModel.objects.all():
        row.code = uuid.uuid4()
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0013_loan_code'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
