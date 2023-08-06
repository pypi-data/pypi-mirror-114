from AsteriskRealtimeData.infrastructure.api.pause_reason_controller import (
    PauseReasonController,
)


def main():
    PauseReasonController().create({"pause_code": "2222", "description": "bbbbbbb"})
    print("OK")

    print(PauseReasonController().list())

    print(PauseReasonController().get_by_id("2222"))

    PauseReasonController().delete_by_id("2222")

    PauseReasonController().delete_by_id("2222")


if __name__ == "__main__":
    main()
