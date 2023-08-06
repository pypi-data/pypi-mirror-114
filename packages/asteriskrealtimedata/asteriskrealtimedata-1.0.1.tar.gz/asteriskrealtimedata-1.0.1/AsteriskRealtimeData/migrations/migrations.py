import os
import importlib

import runpy


class ProcessMigrations:
    def filter_migration_file(self, file_name: str):
        forbidden = ["__init__.py", "migrations.py"]
        return file_name not in forbidden

    def process_migrations_file(self):
        migration_path = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(migration_path):
            if self.filter_migration_file(filename):
                # print(filename.replace(".py", ""))
                runpy.run_module(
                    f"AsteriskRealtimeData.migrations.{filename.replace('.py', '')}"
                )

                # print(f"{migration_path}/{filename}")
                # runpy.run_path(path_name=f"{migration_path}/{filename}")

                # importlib.import_module(
                #     f"AsteriskRealtimeData.migrations.{filename.replace('.py', '')}"
                # )

                # InitializePauseReasons().initialize_pause_reasons()


if __name__ == "__main__":
    ProcessMigrations().process_migrations_file()
