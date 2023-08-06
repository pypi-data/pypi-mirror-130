from dagster.core.storage.io_manager import IOManager
from dagster.core.storage.io_manager import io_manager as dagster_io_manager
from qdk.materialization import Materializer


class QDKIOManager(IOManager):
    def __init__(self):
        self.values = {}

    def handle_output(self, context, obj):
        keys = tuple(context.get_output_identifier())
        self.values[keys] = obj

        print("After storing:", self.values)

        # Create a materializer for the object
        asset_materialization = Materializer(
            asset_key=[
                context.pipeline_name,
                context.solid_def.name,
                keys[-1],
            ],
            object=obj,
        ).materialize()

        # If the asset was materialized, yield the asset
        if asset_materialization:
            yield asset_materialization

        print(keys, type(obj))

    def load_input(self, context):
        keys = tuple(context.upstream_output.get_output_identifier())
        print("After loading:", self.values, keys)
        obj = self.values[keys]
        return obj


@dagster_io_manager
def qdk_io_manager(_):
    return QDKIOManager()
