import uuid

from django.db import migrations, models


def generate_rating_tokens(apps, schema_editor):
    ServiceRequest = apps.get_model(
        "service_requests",
        "ServiceRequest",
    )

    for service_request in ServiceRequest.objects.filter(
        rating_token__isnull=True,
    ):
        service_request.rating_token = uuid.uuid4()
        service_request.save(
            update_fields=["rating_token"],
        )


class Migration(migrations.Migration):

    dependencies = [
        (
            "service_requests",
            "0003_remove_servicerequest_rated_at_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="servicerequest",
            name="rating_token",
            field=models.UUIDField(
                default=None,
                editable=False,
                null=True,
                unique=False,
                verbose_name="Токен оценки",
            ),
        ),
        migrations.RunPython(
            generate_rating_tokens,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="servicerequest",
            name="rating_token",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                null=False,
                verbose_name="Токен оценки",
            ),
        ),
    ]
